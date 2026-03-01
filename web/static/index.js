/**
 * LogIQ Frontend - Vanilla JS
 * Handles log classification via FastAPI backend
 */

// ============================================
// MAIN CLASSIFY FUNCTION
// ============================================

async function classifyLogs() {
    const textarea = document.getElementById("logs");
    const resultsContainer = document.getElementById("results");
    const errorContainer = document.getElementById("error-message");
    const button = document.getElementById("classifyBtn");

    // Clear previous results and errors
    resultsContainer.innerHTML = "";
    errorContainer.classList.remove("show");
    errorContainer.innerText = "";

    // Validate input
    const logs = textarea.value.trim();
    if (!logs) {
        showError("Please enter logs to classify.");
        return;
    }

    try {
        // Set loading state
        button.disabled = true;
        button.innerText = "Processing...";

        // Call API
        const response = await fetch("/api/classify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ raw: logs })
        });

        // Handle response
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to classify logs.");
        }

        // Render results
        renderResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        button.disabled = false;
        button.innerText = "Classify Logs";
    }
}

// ============================================
// RENDER RESULTS
// ============================================

function renderResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    // Ensure data is an array
    const results = Array.isArray(data) ? data : [data];

    // Handle empty results
    if (results.length === 0) {
        container.innerHTML = `<div style="padding: 1rem; text-align: center; color: #6b7280;">No results returned.</div>`;
        return;
    }

    // Render each result card
    results.forEach((result) => {
        const card = document.createElement("div");
        card.className = "result-card";

        // Validate result structure
        const label = result.label || "Unknown";
        const source = result.source || "unknown";
        const badgeClass = source === "regex" ? "badge-regex" : "badge-llm";

        card.innerHTML = `
            <div class="result-label">${escapeHtml(label)}</div>
            <div class="result-badge ${badgeClass}">
                ${source.toUpperCase()}
            </div>
        `;

        container.appendChild(card);
    });
}

// ============================================
// CLEAR ALL
// ============================================

function clearAll() {
    document.getElementById("logs").value = "";
    document.getElementById("results").innerHTML = "";
    document.getElementById("error-message").classList.remove("show");
}

// ============================================
// ERROR HANDLING
// ============================================

function showError(message) {
    const errorContainer = document.getElementById("error-message");
    errorContainer.innerText = message;
    errorContainer.classList.add("show");
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Escape HTML special characters to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}