async function classifyLogs() {
    const textarea = document.getElementById("logs");
    const container = document.getElementById("results");
    const button = document.getElementById("classifyBtn");

    container.innerHTML = "";

    const logs = textarea.value.trim();

    if (!logs) {
        container.innerHTML = `<div class="error">Please enter logs.</div>`;
        return;
    }

    try {
        button.disabled = true;
        button.innerText = "Processing...";

        const response = await fetch("/api/classify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ raw: logs })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        renderResults(data);

    } catch (error) {
        container.innerHTML = `<div class="error">${error.message}</div>`;
    } finally {
        button.disabled = false;
        button.innerText = "Classify Logs";
    }
}

function renderResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    const results = Array.isArray(data) ? data : [data];

    results.forEach(result => {
        const card = document.createElement("div");
        card.className = "result-card";

        card.innerHTML = `
            <div class="result-label">${result.label}</div>
            <div class="result-source ${result.source}">
                ${result.source.toUpperCase()}
            </div>
        `;

        container.appendChild(card);
    });
}

function clearAll() {
    document.getElementById("logs").value = "";
    document.getElementById("results").innerHTML = "";
}