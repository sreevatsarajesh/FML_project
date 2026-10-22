const form = document.getElementById("url-form");
const urlInput = document.getElementById("url-input");
const result = document.getElementById("result");

function addLine(parent, label, value) {
    const p = document.createElement("p");
    const strong = document.createElement("strong");
    strong.textContent = label + " ";
    p.appendChild(strong);
    p.appendChild(document.createTextNode(value));
    parent.appendChild(p);
}

function percent(value) {
    return (Number(value) * 100).toFixed(1) + "%";
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();
    result.textContent = "Checking...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: urlInput.value }),
        });
        const data = await response.json();

        if (!response.ok) {
            result.textContent = data.detail || "Request failed.";
            return;
        }

        result.textContent = "";
        const title = document.createElement("h2");
        title.textContent = data.Prediction === "phishing"
            ? "Likely phishing"
            : "Looks safe";
        result.appendChild(title);

        if (data.Trusted_Domain) {
            addLine(result, "Trusted domain:", data.Trusted_Domain);
        }
        addLine(result, "Risk Level:", data["Risk Level"]);
        addLine(result, "Risk Score:", Number(data["Risk Score"]).toFixed(1) + " / 100");
        addLine(result, "NLP model:", percent(data.NLP_Probability));
        addLine(result, "Numeric model:", percent(data.Numeric_Probability));
    } catch (error) {
        result.textContent = "An error occurred.";
        console.error(error);
    }
});
