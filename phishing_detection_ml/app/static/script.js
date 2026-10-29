
const API_URL = "http://127.0.0.1:8000";

const urlInput = document.getElementById("target-url");
const scanButton = [...document.querySelectorAll("button")].find(button =>
    button.textContent.trim() === "RUN DIAGNOSTIC SCAN"
);
const alertBox = document.querySelector(".alert-brutal");
const tableBody = document.querySelector("table tbody");

function setMetric(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value ?? "--");
}

function percent(value) {
    const number = Number(value);
    return value != null && Number.isFinite(number)
        ? `${(number * 100).toFixed(1)}%`
        : "--";
}

function addLine(parent, label, value) {
    const line = document.createElement("div");
    line.style.marginTop = "8px";

    const strong = document.createElement("strong");
    strong.textContent = `${label} `;
    line.append(strong, document.createTextNode(String(value ?? "N/A")));
    parent.appendChild(line);
}

function showMessage(message, isPhishing = false, details = []) {
    alertBox.className =
        `alert-brutal ${isPhishing ? "alert-danger" : "alert-success"}`;
    alertBox.replaceChildren();

    const icon = document.createElement("div");
    icon.className = "alert-icon";
    icon.textContent = isPhishing ? "⚠️" : "✓";

    const content = document.createElement("div");
    const heading = document.createElement("div");
    heading.style.fontWeight = "900";
    heading.textContent = message;
    content.appendChild(heading);

    details.forEach(([label, value]) => addLine(content, label, value));
    alertBox.append(icon, content);
}

function updateMetrics(data) {
    const prediction = String(data.Prediction ?? "").toLowerCase();
    const risk = Number(data["Risk Score"]);
    const confidence = data.Model_Probability ?? data.Probability;
    const trusted = data.Trusted_Domain || "NONE";

    setMetric(
        "metric-threshold",
        data.Threshold != null ? Number(data.Threshold).toFixed(2) : "--"
    );

    setMetric(
        "metric-risk",
        data["Risk Score"] != null && Number.isFinite(risk)
            ? `${risk.toFixed(1)}/100`
            : "--"
    );

    setMetric(
        "metric-result",
        prediction === "phishing"
            ? "PHISHING"
            : prediction === "safe" || prediction === "legitimate"
                ? "SAFE"
                : prediction.toUpperCase() || "--"
    );

    setMetric("metric-confidence", percent(confidence));
    setMetric("metric-trusted", trusted);

    const note = document.getElementById("metric-trusted-note");
    if (note) {
        note.textContent = data.Trusted_Domain
            ? "Trusted domain match returned by API"
            : "No trusted domain match reported";
    }
}

function addEvaluation(url, data) {
    const empty = tableBody.querySelector('td[colspan="4"]');
    if (empty) empty.parentElement.remove();

    const prediction = String(data.Prediction ?? "").toLowerCase();
    const suspicious =
        String(data["Risk Level"] ?? "").toLowerCase() === "suspicious";

    const row = document.createElement("tr");
    const values = [
        new Date().toLocaleTimeString(),
        url,
        prediction === "phishing"
            ? "PHISHING"
            : suspicious
                ? "SUSPICIOUS"
                : prediction.toUpperCase(),
        data["Risk Score"] != null
            ? `${Number(data["Risk Score"]).toFixed(1)}/100`
            : percent(data.Probability)
    ];

    values.forEach((value, index) => {
        const cell = document.createElement("td");

        if (index === 2) {
            const badge = document.createElement("span");
            badge.className = `badge ${
                prediction === "phishing"
                    ? "badge-threat"
                    : suspicious
                        ? "badge-warn"
                        : "badge-safe"
            }`;
            badge.textContent = value;
            cell.appendChild(badge);
        } else {
            cell.textContent = value;
        }

        row.appendChild(cell);
    });

    tableBody.prepend(row);

    while (tableBody.rows.length > 10) {
        tableBody.deleteRow(tableBody.rows.length - 1);
    }
}

async function scanUrl() {
    const url = urlInput.value.trim();

    if (!url) {
        showMessage("ENTER A URL TO BEGIN ANALYSIS");
        urlInput.focus();
        return;
    }

    scanButton.disabled = true;
    scanButton.textContent = "SCANNING...";
    showMessage("ANALYZING TARGET URL...");

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const raw = await response.text();
        let data;

        try {
            data = JSON.parse(raw);
        } catch {
            throw new Error(`Invalid API response: HTTP ${response.status}`);
        }

        if (!response.ok) {
            throw new Error(data.detail || `HTTP ${response.status}`);
        }

        updateMetrics(data);
        addEvaluation(url, data);

        const phishing =
            String(data.Prediction ?? "").toLowerCase() === "phishing";

        showMessage(
            phishing ? "PHISHING DETECTED" : "NO PHISHING DETECTED",
            phishing,
            [
                ["Risk level:", data["Risk Level"]],
                ["Risk score:", data["Risk Score"]],
                ["Fusion probability:", percent(data.Model_Probability ?? data.Probability)],
                ["NLP probability:", percent(data.NLP_Probability)],
                ["Numeric probability:", percent(data.Numeric_Probability)],
                ["Trusted domain:", data.Trusted_Domain || "No match"]
            ]
        );
    } catch (error) {
        console.error("Scan failed:", error);
        showMessage(error.message || "Unable to reach the API.");
    } finally {
        scanButton.disabled = false;
        scanButton.textContent = "RUN DIAGNOSTIC SCAN";
    }
}

if (scanButton && urlInput && alertBox && tableBody) {
    scanButton.addEventListener("click", scanUrl);

    urlInput.addEventListener("keydown", event => {
        if (event.key === "Enter") scanUrl();
    });
} else {
    console.error("Phish Guard: Required HTML elements were not found.");
}
