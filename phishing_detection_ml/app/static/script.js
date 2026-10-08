const form = document.getElementById("url-form");
const urlInput = document.getElementById("url-input");
const result = document.getElementById("result");

form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const url = urlInput.value;
    result.innerHTML = "Checking...";
    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });
        const data = await response.json();
        result.innerHTML = `
            <h2>Result</h2>
            <p>
                <strong>Probability:</strong>
                ${data.Probability}
            </p>
            <p>
                <strong>Risk Score:</strong>
                ${data["Risk Score"]}
            </p>
            <p>
                <strong>Risk Level:</strong>
                ${data["Risk Level"]}
            </p>
        `;
    } catch (error) {
        result.innerHTML = "An error occurred.";
        console.error(error);
    }

});