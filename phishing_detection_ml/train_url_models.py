import argparse
import json
import sys
import time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.url_utils import (FEATURE_NAMES, canonicalize_url,  # noqa: E402
                           extract_features, get_host, prepare_nlp_text,
                           registered_domain)

DATA_PATH = ROOT.parent / "NLP_classifier" / "data" / "malicious_phish.csv"
TOP_DOMAINS = ROOT / "data" / "top_domains.txt"
MODEL_DIR = ROOT / "models"
RESULT_DIR = ROOT / "results" / "fusion"
NLP_MODEL_PATH = MODEL_DIR / "url_nlp_model.pkl"
NUMERIC_MODEL_PATH = MODEL_DIR / "url_numeric_model.pkl"
CONFIG_PATH = MODEL_DIR / "fusion_config.json"
SEED = 42
EPOCHS = 4
CHUNK = 50_000
SANITY_URLS = [
    ("benign", "google.com"), ("benign", "https://www.google.com/"),
    ("benign", "https://github.com"), ("benign", "https://www.wikipedia.org/"),
    ("benign", "https://www.amazon.com/"), ("benign", "https://www.youtube.com/watch?v=abc123"),
    ("benign", "https://stackoverflow.com/questions/12345/how-to-x"),
    ("phishing", "http://paypal-login-verify.xyz/account"),
    ("phishing", "http://192.168.10.5/secure/login.php?user=1&pass=2"),
    ("phishing", "https://secure-update-apple-id.verify-account.top/signin"),
    ("phishing", "http://amazon.com.account-verify.tk/login"),
]
def load_data(sample):
    df = pd.read_csv(DATA_PATH).dropna(subset=["url", "type"]).copy()
    df["type"] = df["type"].astype(str).str.strip().str.lower()
    df["canon"] = df["url"].astype(str).map(canonicalize_url)
    df = df[df["canon"] != ""]
    df["label"] = (df["type"] == "phishing").astype(int)

    # same canonical URL with conflicting labels -> ambiguous, drop it
    conflict = df.groupby("canon")["label"].nunique()
    df = df[~df["canon"].isin(conflict[conflict > 1].index)]
    df = df.drop_duplicates("canon").reset_index(drop=True)

    df["host"] = df["canon"].map(get_host)
    df["group"] = df["host"].map(registered_domain)
    df = df[df["group"] != ""].reset_index(drop=True)

    if sample:
        df = df.sample(n=min(sample, len(df)), random_state=SEED).reset_index(drop=True)
    return df
def split_by_domain(df):
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
    train_idx, rest_idx = next(gss.split(df, df["label"], df["group"]))
    train, rest = df.iloc[train_idx], df.iloc[rest_idx]

    gss2 = GroupShuffleSplit(n_splits=1, test_size=0.5, random_state=SEED)
    val_idx, test_idx = next(gss2.split(rest, rest["label"], rest["group"]))
    return train, rest.iloc[val_idx], rest.iloc[test_idx]
def add_host_only_rows(train):
    """One extra 'bare host' example per (host, label) in the TRAIN split."""
    hosts = (train[["host", "label"]].drop_duplicates()
             .rename(columns={"host": "canon"}))
    hosts = hosts[hosts["canon"] != ""]

    extra = [hosts]
    if TOP_DOMAINS.exists():
        top = [line.strip().lower() for line in
               TOP_DOMAINS.read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.startswith("#")]
        extra.append(pd.DataFrame({"canon": top, "label": 0}))
        print(f"Added {len(top):,} trusted domains from {TOP_DOMAINS.name}")

    out = pd.concat([train[["canon", "label"]], *extra], ignore_index=True)
    out = out.drop_duplicates(["canon", "label"])
    return out.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
def metrics(y, prob, threshold=0.5):
    pred = (prob >= threshold).astype(int)
    return {
        "accuracy": accuracy_score(y, pred),
        "precision": precision_score(y, pred, zero_division=0),
        "recall": recall_score(y, pred, zero_division=0),
        "f1": f1_score(y, pred, zero_division=0),
    }
def numeric_matrix(canon_series):
    rows = [extract_features(u) for u in canon_series]
    return pd.DataFrame(rows, columns=FEATURE_NAMES).astype(np.float32)
def train_nlp(train_aug):
    vec = HashingVectorizer(
        analyzer="char", ngram_range=(3, 5), n_features=2 ** 20,
        alternate_sign=False, binary=True, norm="l2",
        lowercase=False, dtype=np.float32,
    )
    pos_weight = float(np.sqrt((train_aug["label"] == 0).sum() /
                               max(1, (train_aug["label"] == 1).sum())))
    clf = SGDClassifier(
        loss="log_loss", alpha=2e-7, random_state=SEED,
        class_weight={0: 1.0, 1: pos_weight},
    )
    texts = train_aug["canon"].map(lambda u: u[:150]).tolist()
    labels = train_aug["label"].to_numpy()
    print("NLP: vectorising training data ...")
    chunks = []
    for start in range(0, len(texts), CHUNK):
        chunks.append((vec.transform(texts[start:start + CHUNK]),
                       labels[start:start + CHUNK]))
    rng = np.random.default_rng(SEED)
    for epoch in range(EPOCHS):
        for i in rng.permutation(len(chunks)):
            X, y = chunks[i]
            clf.partial_fit(X, y, classes=[0, 1])
        print(f"NLP: epoch {epoch + 1}/{EPOCHS} done")

    return Pipeline([("vec", vec), ("clf", clf)])
def nlp_probability(model, canon_urls):
    texts = [u[:150] for u in canon_urls]
    return model.predict_proba(texts)[:, list(model.classes_).index(1)]
def train_numeric(train_aug):
    print("Numeric: extracting features ...")
    X = numeric_matrix(train_aug["canon"])
    y = train_aug["label"].to_numpy()

    model = HistGradientBoostingClassifier(
        max_iter=200, learning_rate=0.08, max_leaf_nodes=48,
        min_samples_leaf=40, l2_regularization=1.0,
        class_weight="balanced", early_stopping=False, random_state=SEED,
    )
    print("Numeric: fitting ...")
    model.fit(X, y)
    return model
def numeric_probability(model, canon_urls):
    X = numeric_matrix(canon_urls)
    return model.predict_proba(X)[:, list(model.classes_).index(1)]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=0,
                        help="use only N random rows (smoke test)")
    parser.add_argument("--no-refit", action="store_true",
                        help="save the train-split models instead of "
                             "refitting on all data")
    args = parser.parse_args()
    t0 = time.time()
    df = load_data(args.sample)
    train, val, test = split_by_domain(df)
    print(f"Rows  train={len(train):,}  val={len(val):,}  test={len(test):,}")
    print(f"Phishing share  train={train.label.mean():.3f}  "
          f"val={val.label.mean():.3f}  test={test.label.mean():.3f}")
    overlap = set(train.group) & set(test.group)
    print(f"Registered-domain overlap train/test: {len(overlap)} (must be 0)")

    train_aug = add_host_only_rows(train)
    print(f"Training rows after host-only augmentation: {len(train_aug):,}")
    nlp = train_nlp(train_aug)
    numeric = train_numeric(train_aug)
    y_val = val["label"].to_numpy()
    nlp_val = nlp_probability(nlp, val["canon"])
    num_val = numeric_probability(numeric, val["canon"])
    grid = []
    for w in np.round(np.arange(0.0, 1.0001, 0.05), 3):
        grid.append({"numeric_weight": w,
                     **metrics(y_val, w * num_val + (1 - w) * nlp_val)})
    grid = pd.DataFrame(grid)
    best = grid.sort_values(["f1", "recall"], ascending=False).iloc[0]
    weight = float(best["numeric_weight"])
    print(f"\nSelected numeric weight on validation: {weight:.2f} "
          f"(val F1 {best['f1']:.4f})")
    y_test = test["label"].to_numpy()
    nlp_test = nlp_probability(nlp, test["canon"])
    num_test = numeric_probability(numeric, test["canon"])
    fused_test = weight * num_test + (1 - weight) * nlp_test
    results = pd.DataFrame([
        {"model": "Numeric", **metrics(y_test, num_test)},
        {"model": "NLP", **metrics(y_test, nlp_test)},
        {"model": f"Fusion (w={weight:.2f})", **metrics(y_test, fused_test)},
    ])
    print("\nHeld-out test (unseen domains)")
    print(results.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    bare = test[~test["canon"].str.contains(r"[/?]", regex=True)]
    if len(bare) and bare["label"].nunique() == 2:
        print(f"\nBare-domain test rows: {len(bare):,}")
        print("Fusion on bare domains:", {
            k: round(v, 4) for k, v in
            metrics(bare["label"].to_numpy(),
                    weight * numeric_probability(numeric, bare["canon"])
                    + (1 - weight) * nlp_probability(nlp, bare["canon"])
                    ).items()})
    if not args.no_refit:
        print("\nRefitting both models on train+val+test for deployment ...")
        full_aug = add_host_only_rows(df)
        nlp = train_nlp(full_aug)
        numeric = train_numeric(full_aug)
    sanity = []
    for expected, url in SANITY_URLS:
        canon = canonicalize_url(url)
        p_nlp = float(nlp_probability(nlp, [canon])[0])
        p_num = float(numeric_probability(numeric, [canon])[0])
        sanity.append({"expected": expected, "url": url,
                       "nlp": round(p_nlp, 3), "numeric": round(p_num, 3),
                       "fused": round(weight * p_num + (1 - weight) * p_nlp, 3)})
    sanity = pd.DataFrame(sanity)
    print("\nSanity URLs (model only, before the trusted-domain list)")
    print(sanity.to_string(index=False))
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(nlp, NLP_MODEL_PATH, compress=3)
    joblib.dump(numeric, NUMERIC_MODEL_PATH, compress=3)
    CONFIG_PATH.write_text(json.dumps(
        {"numeric_weight": weight, "threshold": 0.5,
         "features": FEATURE_NAMES}, indent=2))
    results.to_csv(RESULT_DIR / "final_metrics.csv", index=False)
    grid.to_csv(RESULT_DIR / "final_validation_weights.csv", index=False)
    sanity.to_csv(RESULT_DIR / "sanity_checks.csv", index=False)
    for path in (NLP_MODEL_PATH, NUMERIC_MODEL_PATH):
        print(f"Saved {path.name}: {path.stat().st_size / 1e6:.1f} MB")
    print(f"Done in {(time.time() - t0) / 60:.1f} min")
if __name__ == "__main__":
    main()
