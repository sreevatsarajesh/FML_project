"""Shared URL helpers.

IMPORTANT: training and prediction BOTH import from this file, so the model
always sees URLs in exactly the same shape at train time and at predict time.
(The old code normalised URLs while training but fed raw URLs at predict time.)
"""

import math
import re

_SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.\-]*://")
_WWW_RE = re.compile(r"^www\d*\.")
_IPV4_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

# Second-level labels that act like a TLD (co.uk, com.au, co.in, gov.in ...)
_SECOND_LEVEL = {"co", "com", "org", "net", "gov", "edu", "ac", "or", "ne", "go"}

SUSPICIOUS_WORDS = (
    "login", "signin", "verify", "secure", "account", "update", "bank",
    "paypal", "confirm", "password", "webscr", "wallet", "billing", "support",
)

MAX_NLP_CHARS = 150

FEATURE_NAMES = [
    "url_length", "n_slash", "n_hyphens", "n_dots", "n_questionmark", "n_at",
    "n_equal", "n_and", "n_percent", "n_plus", "n_space", "n_dollar",
    "n_asterisk", "host_length", "subdomain_count", "has_ip", "path_length",
    "query_length", "domain_length", "tld_length", "host_digit_count",
    "host_hyphen_count", "host_entropy", "digit_ratio", "suspicious_words",
]


def canonicalize_url(url: str) -> str:
    """Lower-case, drop scheme / www. / default port / fragment / trailing '/'.

    Why: in the training data the scheme (https) and 'has a path' were almost
    perfect label shortcuts (94.5% of bare-domain rows are phishing), so the
    model learned "https://google.com => phishing". Removing the scheme and
    www makes those shortcuts unavailable to the model.
    """
    u = str(url).strip().lower()
    u = _SCHEME_RE.sub("", u)
    u = u.split("#", 1)[0]

    cut = len(u)
    for ch in "/?":
        pos = u.find(ch)
        if pos != -1:
            cut = min(cut, pos)
    authority, rest = u[:cut], u[cut:]

    userinfo = ""
    if "@" in authority:
        userinfo, authority = authority.rsplit("@", 1)
        userinfo += "@"

    authority = _WWW_RE.sub("", authority)
    for port in (":80", ":443"):
        if authority.endswith(port):
            authority = authority[: -len(port)]

    return (userinfo + authority + rest).rstrip("/")


def get_host(canonical_url: str) -> str:
    u = canonical_url
    cut = len(u)
    for ch in "/?":
        pos = u.find(ch)
        if pos != -1:
            cut = min(cut, pos)
    authority = u[:cut].split("@")[-1]
    return authority.split(":")[0].strip("[]")


def registered_domain(host: str) -> str:
    labels = [p for p in host.split(".") if p]
    if len(labels) <= 2 or _IPV4_RE.match(host):
        return host
    if len(labels[-1]) == 2 and labels[-2] in _SECOND_LEVEL:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def prepare_nlp_text(url: str) -> str:
    return canonicalize_url(url)[:MAX_NLP_CHARS]


def _entropy(text: str) -> float:
    if not text:
        return 0.0
    total = len(text)
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def extract_features(url: str) -> dict:
    canon = canonicalize_url(url)
    host = get_host(canon)
    rest = canon[len(canon.split("/")[0].split("?")[0]):]

    path, _, query = rest.partition("?")
    labels = [p for p in host.split(".") if p]
    tld = labels[-1] if labels else ""
    domain = registered_domain(host).split(".")[0] if host else ""
    has_ip = int(bool(_IPV4_RE.match(host)) and all(
        int(p) <= 255 for p in host.split(".")
    ))
    digits = sum(ch.isdigit() for ch in canon)

    return {
        "url_length": len(canon),
        "n_slash": canon.count("/"),
        "n_hyphens": canon.count("-"),
        "n_dots": canon.count("."),
        "n_questionmark": canon.count("?"),
        "n_at": canon.count("@"),
        "n_equal": canon.count("="),
        "n_and": canon.count("&"),
        "n_percent": canon.count("%"),
        "n_plus": canon.count("+"),
        "n_space": canon.count(" "),
        "n_dollar": canon.count("$"),
        "n_asterisk": canon.count("*"),
        "host_length": len(host),
        "subdomain_count": max(
            0, len(labels) - len(registered_domain(host).split("."))
        ),
        "has_ip": has_ip,
        "path_length": len(path),
        "query_length": len(query),
        "domain_length": len(domain),
        "tld_length": len(tld),
        "host_digit_count": sum(ch.isdigit() for ch in host),
        "host_hyphen_count": host.count("-"),
        "host_entropy": _entropy(host),
        "digit_ratio": digits / max(1, len(canon)),
        "suspicious_words": sum(canon.count(w) for w in SUSPICIOUS_WORDS),
    }
