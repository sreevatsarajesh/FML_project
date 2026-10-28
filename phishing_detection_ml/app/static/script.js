
const urlInput = document.getElementById("target-url");
const scanButton = [...document.querySelectorAll("button")].find(button =>
    button.textContent.trim() === "RUN DIAGNOSTIC SCAN"
);
const alertBox = document.querySelector(".alert-brutal");
const tableBody = document.querySelector("table tbody");

function addLine(parent, label, value) {
    const line = document.createElement("div");
    line.style.marginTop = "8px";
    const strong = document.createElement("strong");
    strong.textContent = `${label} `;
    line.append(strong, document.createTextNode(String(value ?? "N/A")));
    parent.appendChild(line);
}

function percent(value) {
    return `${(Number(value) * 100).toFixed(1)}%`;
}

function showMessage(message, type = "alert-danger") {
    alertBox.className = `alert-brutal ${type}`;
    alertBox.replaceChildren();
    const content = document.createElement("div");
    content.textContent = message;
    alertBox.appendChild(content);
}

async function scanUrl() {
    const url = urlInput.value.trim();

    if (!url) {
        showMessage("Enter a URL before running the diagnostic scan.");
        urlInput.focus();
        return;
    }

    scanButton.disabled = true;
    scanButton.textContent = "SCANNING...";
    showMessage("Analyzing URL against the phishing detection models...", "alert-success");

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "The scan request failed.");
        }

        const phishing = String(data.Prediction).toLowerCase() === "phishing";
        alertBox.className = `alert-brutal ${phishing ? "alert-danger" : "alert-success"}`;
        alertBox.replaceChildren();

        const icon = document.createElement("div");
        icon.className = "alert-icon";
        icon.textContent = phishing ? "⚠️" : "✓";

        const details = document.createElement("div");
        const heading = document.createElement("div");
        heading.style.fontWeight = "900";
        heading.style.fontSize = "1.1rem";
        heading.textContent = phishing ? "PHISHING DETECTED" : "NO PHISHING DETECTED";

        details.appendChild(heading);
        addLine(details, "Risk level:", data["Risk Level"]);
        addLine(details, "Risk score:", `${Number(data["Risk Score"]).toFixed(1)} / 100`);
        addLine(details, "Fusion probability:", percent(data.Model_Probability ?? data.Probability));
        addLine(details, "NLP probability:", percent(data.NLP_Probability));
        addLine(details, "Numeric probability:", percent(data.Numeric_Probability));

        if (data.Trusted_Domain) {
            addLine(details, "Trusted domain match:", data.Trusted_Domain);
        }

        alertBox.append(icon, details);

        const row = document.createElement("tr");
        const timestamp = new Date().toLocaleTimeString();
        const values = [
            timestamp,
            url,
            phishing ? "PHISHING" : "LEGITIMATE",
            percent(data.Probability)
        ];

        values.forEach((value, index) => {
            const cell = document.createElement("td");
            if (index === 2) {
                const badge = document.createElement("span");
                badge.className = `badge ${phishing ? "badge-threat" : "badge-safe"}`;
                badge.textContent = value;
                cell.appendChild(badge);
            } else {
                cell.textContent = value;
            }
            row.appendChild(cell);
        });

        tableBody.prepend(row);
        urlInput.value = url;
    } catch (error) {
        showMessage(error.message || "Unable to connect to the detection API.");
        console.error("Scan failed:", error);
    } finally {
        scanButton.disabled = false;
        scanButton.textContent = "RUN DIAGNOSTIC SCAN";
    }
}

scanButton.addEventListener("click", scanUrl);

urlInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        scanUrl();
    }
});
