/**
 * LogIQ Frontend - Vanilla JS
 * Handles log classification via FastAPI backend
 * Theme: Lavender Periwinkle with Light/Dark mode
 */

// ============================================
// THEME TOGGLE FUNCTIONALITY
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme on page load
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateToggleIcon(savedTheme);
    
    // Setup theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateToggleIcon(newTheme);
        });
    }
});

function updateToggleIcon(theme) {
    const icon = document.querySelector('.toggle-icon');
    if (icon) {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

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
            throw new Error(data.detail || "Failed to classify logs. Please try again.");
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
        container.innerHTML = `
            <div style="padding: 16px; text-align: center; color: #666666; font-style: italic;">
                No classifications returned.
            </div>
        `;
        return;
    }

    // Render each result card
    results.forEach((result, index) => {
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

        // Stagger animation
        setTimeout(() => {
            container.appendChild(card);
        }, index * 50);
    });
}

// ============================================
// CLEAR ALL
// ============================================

function clearAll() {
    document.getElementById("logs").value = "";
    document.getElementById("logs").focus();
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