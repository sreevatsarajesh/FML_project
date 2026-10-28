import { useMemo, useState } from "react";
import {
  Activity, ArrowUpRight, BadgeCheck, BarChart3, BrainCircuit, Check,
  ChevronRight, CircleAlert, Clock3, ExternalLink, Fingerprint, Globe2,
  Link2, LoaderCircle, LockKeyhole, Radar, ScanSearch, Shield,
  ShieldAlert, ShieldCheck, Sparkles, Terminal, TriangleAlert, Zap
} from "lucide-react";

const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const examples = [
  { label: "Google", url: "https://www.google.com/" },
  { label: "GitHub repository", url: "https://github.com/openai/openai-python" },
  { label: "Suspicious pattern", url: "http://paypal-login-verify.example.xyz/account" },
];

function percent(value) {
  const n = Number(value);
  return Number.isFinite(n) ? `${(n * 100).toFixed(1)}%` : "—";
}
function score(value) {
  const n = Number(value);
  return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : 0;
}
function riskTone(result) {
  const prediction = String(result?.Prediction || "").toLowerCase();
  return prediction === "phishing" ? "danger" : prediction === "benign" ? "safe" : "neutral";
}
function cleanHost(value) {
  try { return new URL(value.includes("://") ? value : `https://${value}`).hostname; }
  catch { return value; }
}

function Meter({ value, tone = "violet" }) {
  return <div className="meter"><span className={`meter-fill ${tone}`} style={{ width: `${score(Number(value) * 100)}%` }} /></div>;
}
function ModelCard({ icon: Icon, title, tag, probability, description, tone, weight }) {
  return <article className="model-card glass-card">
    <div className="model-card-top"><div className={`model-icon ${tone}`}><Icon size={19} /></div><span className="model-tag">{tag}</span></div>
    <div className="model-title-row"><h3>{title}</h3><span className={`model-dot ${tone}`} /></div>
    <div className="model-value">{percent(probability)}</div>
    <Meter value={probability} tone={tone} />
    <p className="model-description">{description}</p>
    <div className="model-foot"><span>Phishing probability</span><span>{weight}</span></div>
  </article>;
}
function Stat({ label, value, icon: Icon }) {
  return <div className="mini-stat"><span className="mini-stat-icon"><Icon size={15} /></span><div><span className="mini-label">{label}</span><strong>{value}</strong></div></div>;
}

export default function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [analysedUrl, setAnalysedUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const disagreement = useMemo(() => {
    if (!result) return false;
    return Math.abs(Number(result.NLP_Probability) - Number(result.Numeric_Probability)) >= 0.3;
  }, [result]);

  async function analyse(event) {
    event?.preventDefault();
    const candidate = url.trim();
    if (!candidate) { setError("Enter a URL to start the analysis."); return; }
    if (candidate.length > 2048) { setError("This URL exceeds the 2,048-character limit."); return; }
    setLoading(true); setError(""); setResult(null); setAnalysedUrl(candidate);
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: candidate }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail || `API request failed (${response.status}).`);
      if (data.NLP_Probability == null || data.Numeric_Probability == null || data.Probability == null || !data.Prediction) {
        throw new Error("The API response is missing one or more model outputs. Check that the backend is running the fusion endpoint.");
      }
      setResult(data);
    } catch (err) {
      setError(`${err.message || "Could not connect to the API."} Make sure FastAPI is running at ${API_URL}.`);
    } finally { setLoading(false); }
  }

  async function copyReport() {
    if (!result) return;
    const text = [
      "PhishLens URL analysis", `URL: ${analysedUrl}`,
      `Prediction: ${result.Prediction}`, `Final probability: ${percent(result.Probability)}`,
      `NLP probability: ${percent(result.NLP_Probability)}`,
      `Numerical probability: ${percent(result.Numeric_Probability)}`,
      `Pre-adjustment fusion: ${percent(result.Model_Probability)}`,
      `Risk: ${result["Risk Level"] ?? "Unavailable"} (${result["Risk Score"] ?? "—"}/100)`,
      `Trusted domain: ${result.Trusted_Domain || "None"}`,
    ].join("\n");
    try { await navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 1600); }
    catch { setError("Clipboard access was blocked by the browser."); }
  }

  const tone = result ? riskTone(result) : "neutral";
  const threshold = Number(result?.Threshold);
  const hasThreshold = Number.isFinite(threshold);

  return <div className="app-shell">
    <div className="ambient ambient-one" /><div className="ambient ambient-two" />
    <header className="topbar">
      <a className="brand" href="#top" aria-label="PhishLens home"><span className="brand-mark"><Shield size={21} strokeWidth={2.4} /></span><span>phish<span>lens</span><small>URL INTELLIGENCE</small></span></a>
      <div className="topbar-right"><span className="system-status"><i /> DUAL-MODEL ENGINE</span><a className="docs-link" href={`${API_URL}/docs`} target="_blank" rel="noreferrer">API docs <ExternalLink size={13} /></a></div>
    </header>

    <main id="top">
      <section className="hero">
        <div className="hero-copy"><div className="eyebrow"><Sparkles size={13} /> INTELLIGENCE, NOT GUESSWORK</div>
          <h1>Look closer.<br /><span>Click safer.</span></h1>
          <p className="hero-description">Two machine-learning perspectives. One clear report. Inspect URL language signals, structural features, and the combined prediction in one place.</p>
          <div className="hero-points"><span><Check size={14} /> NLP pattern analysis</span><span><Check size={14} /> Numerical URL features</span><span><Check size={14} /> Fused risk estimate</span></div>
        </div>
        <div className="hero-visual" aria-hidden="true"><div className="orbit orbit-a"/><div className="orbit orbit-b"/><div className="orbit orbit-c"/><div className="visual-core"><ShieldCheck size={46}/></div><span className="orbit-chip chip-a"><BrainCircuit size={15}/> NLP</span><span className="orbit-chip chip-b"><BarChart3 size={15}/> FEATURES</span><span className="orbit-chip chip-c"><Zap size={15}/> FUSION</span><span className="visual-cross cross-a">+</span><span className="visual-cross cross-b">+</span></div>
      </section>

      <section className="scanner-section" aria-labelledby="scan-title">
        <div className="section-heading"><div><span className="section-kicker">01 / URL SCANNER</span><h2 id="scan-title">Inspect a destination</h2></div><span className="input-limit"><LockKeyhole size={13}/> Max 2,048 characters</span></div>
        <form className="scanner-form" onSubmit={analyse}>
          <div className="url-input-wrap"><Link2 size={18}/><input aria-label="URL to analyse" value={url} onChange={e => setUrl(e.target.value)} placeholder="Paste a URL to analyse…" autoComplete="url" spellCheck="false"/><button type="button" className="clear-input" onClick={() => {setUrl("");setError("");}} disabled={!url}>Clear</button></div>
          <button className="analyse-button" type="submit" disabled={loading}>{loading ? <><LoaderCircle size={17} className="spin"/> Analysing</> : <><ScanSearch size={17}/> Analyse URL <ArrowUpRight size={16}/></>}</button>
        </form>
        <div className="scanner-bottom"><span className="examples-label">TRY AN EXAMPLE</span>{examples.map(item => <button key={item.label} className="example-chip" onClick={() => setUrl(item.url)} type="button">{item.label}<ChevronRight size={13}/></button>)}</div>
        {error && <div className="error-banner" role="alert"><CircleAlert size={17}/><span>{error}</span></div>}
      </section>

      {loading && <section className="loading-panel glass-card"><div className="loading-orb"><Radar size={25}/></div><div><strong>Running model analysis</strong><p>Sending URL to the NLP and numerical models…</p></div><LoaderCircle className="spin loading-spinner" size={20}/></section>}

      {result && !loading && <section className="results-section" aria-live="polite">
        <div className="results-heading"><div><span className="section-kicker">02 / ANALYSIS REPORT</span><h2>Signals, side by side.</h2><p>Live outputs returned by your fusion API.</p></div><button className="secondary-button" onClick={copyReport}>{copied ? <Check size={15}/> : <Terminal size={15}/>} {copied ? "Copied" : "Copy report"}</button></div>
        <div className={`verdict-card verdict-${tone}`}>
          <div className="verdict-symbol">{tone === "danger" ? <ShieldAlert size={27}/> : <ShieldCheck size={27}/>}</div>
          <div className="verdict-main"><span className="verdict-label">FINAL CLASSIFICATION</span><h3>{String(result.Prediction).toLowerCase() === "phishing" ? "Potential phishing detected" : "Classified as benign"}</h3><p>{cleanHost(analysedUrl)} <span className="verdict-separator">/</span> {result.Trusted_Domain ? `Trusted domain match: ${result.Trusted_Domain}` : "No trusted-domain match reported"}</p></div>
          <div className="verdict-score"><span>FINAL PROBABILITY</span><strong>{percent(result.Probability)}</strong><small>{result["Risk Level"] ?? "Risk level unavailable"} risk</small></div>
        </div>

        <div className="model-grid">
          <ModelCard icon={BrainCircuit} title="NLP model" tag="TEXT SIGNALS" probability={result.NLP_Probability} description="Evaluates character sequences and URL text patterns for learned indicators." tone="violet" weight="Independent output"/>
          <ModelCard icon={Fingerprint} title="Numerical model" tag="URL STRUCTURE" probability={result.Numeric_Probability} description="Evaluates engineered numerical characteristics extracted from the URL." tone="amber" weight="Independent output"/>
        </div>

        <article className="fusion-panel glass-card">
          <div className="fusion-heading"><div className="fusion-icon"><Activity size={18}/></div><div><span className="section-kicker">MODEL COMBINATION</span><h3>Fusion confidence</h3></div><span className="fusion-weight">Numeric weight <b>{Number.isFinite(Number(result.Numeric_Weight)) ? `${(Number(result.Numeric_Weight)*100).toFixed(0)}%` : "—"}</b></span></div>
          <div className="fusion-comparison"><div className="fusion-number"><span>Pre-adjustment fusion</span><strong>{percent(result.Model_Probability)}</strong></div><div className="fusion-divider"><ChevronRight size={17}/></div><div className="fusion-number"><span>Final probability</span><strong>{percent(result.Probability)}</strong></div><div className="fusion-number risk-number"><span>Risk score</span><strong>{Number.isFinite(Number(result["Risk Score"])) ? `${Number(result["Risk Score"]).toFixed(1)}<small>/100</small>` : "—"}</strong></div></div>
          <div className="fusion-bar-labels"><span>0% phishing probability</span><span>100%</span></div><Meter value={result.Probability} tone={tone === "danger" ? "red" : "green"}/>
          {Number.isFinite(Number(result.Model_Probability)) && Math.abs(Number(result.Model_Probability)-Number(result.Probability)) > 0.000001 && <div className="adjustment-note"><BadgeCheck size={16}/><span><b>Post-processing adjustment applied.</b> The final probability differs from the weighted model output. Your backend may have applied its trusted-root safeguard.</span></div>}
          {disagreement && <div className="disagreement-note"><TriangleAlert size={17}/><span><b>The models disagree.</b> Their phishing probabilities differ by at least 30 percentage points. Treat this as a signal to inspect the URL carefully.</span></div>}
          <div className="fusion-footer"><span><Activity size={14}/> Threshold decision: <b>{hasThreshold ? percent(threshold) : "not returned by API"}</b></span><span><Clock3 size={14}/> Analysis complete</span></div>
        </article>

        <div className="detail-grid">
          <article className="detail-card glass-card"><div className="detail-title"><Globe2 size={17}/><h3>Destination details</h3></div><div className="detail-row"><span>Submitted URL</span><strong className="url-break">{analysedUrl}</strong></div><div className="detail-row"><span>Hostname</span><strong>{cleanHost(analysedUrl)}</strong></div><div className="detail-row"><span>Trusted-domain signal</span><strong>{result.Trusted_Domain || "No match"}</strong></div></article>
          <article className="detail-card glass-card"><div className="detail-title"><ShieldCheck size={17}/><h3>Interpretation</h3></div><div className="interpretation-line"><span className={`interpretation-icon ${tone}`}>{tone === "danger" ? <TriangleAlert size={16}/> : <BadgeCheck size={16}/>}</span><div><strong>{tone === "danger" ? "Elevated suspicion" : "Lower model-estimated risk"}</strong><p>{tone === "danger" ? "The final model decision is phishing. Avoid entering credentials until the destination is independently verified." : "The final model decision is benign. This is not a guarantee that the destination is safe."}</p></div></div><div className="fine-print">Machine-learning outputs are estimates, not proof of legitimacy or maliciousness. A trusted-domain match is not a guarantee of safety.</div></article>
        </div>
        <div className="report-footnote"><Shield size={14}/> Results are generated by your current backend models. No external website is visited by this interface.</div>
      </section>}

      {!result && !loading && <section className="empty-state"><div className="empty-icon"><ScanSearch size={25}/></div><span className="section-kicker">READY WHEN YOU ARE</span><h2>Your analysis starts here.</h2><p>Submit a URL to see both model probabilities, their combined output, and the final classification.</p><div className="empty-features"><span><BrainCircuit size={15}/> NLP signals</span><span><BarChart3 size={15}/> Numeric features</span><span><Activity size={15}/> Fusion output</span></div></section>}

      <section className="method-strip"><div className="method-item"><span className="method-icon"><BrainCircuit size={17}/></span><div><strong>Language patterns</strong><p>Character n-grams and URL text</p></div></div><div className="method-item"><span className="method-icon"><BarChart3 size={17}/></span><div><strong>Structural signals</strong><p>Engineered numerical features</p></div></div><div className="method-item"><span className="method-icon"><Zap size={17}/></span><div><strong>Weighted fusion</strong><p>One combined probability</p></div></div></section>
    </main>
    <footer className="footer"><a className="footer-brand" href="#top"><Shield size={15}/> phishlens</a><span>Machine-learning assisted URL analysis</span><span className="footer-status"><i/> Local API integration</span></footer>
  </div>;
}
