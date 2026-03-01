/**
 * LogIQ Frontend - Vanilla JS
 * Handles log classification via FastAPI backend
 * Theme: Lavender Periwinkle with Light/Dark mode
 */

// ============================================
// STATE MANAGEMENT
// ============================================

let currentMode = 'paste';
let selectedFile = null;

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

    // Setup file upload handlers
    setupFileUploadHandlers();
});

function updateToggleIcon(theme) {
    const icon = document.querySelector('.toggle-icon');
    if (icon) {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// ============================================
// MODE SWITCHING
// ============================================

function switchMode(mode) {
    currentMode = mode;

    // Update button states
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('mode-btn-active');
    });
    document.querySelector(`[data-mode="${mode}"]`).classList.add('mode-btn-active');

    // Hide all mode contents
    document.querySelectorAll('.mode-content').forEach(content => {
        content.classList.remove('mode-content-active');
    });

    // Show selected mode content
    if (mode === 'paste') {
        document.getElementById('pasteMode').classList.add('mode-content-active');
        document.getElementById('logs').focus();
    } else {
        document.getElementById('fileMode').classList.add('mode-content-active');
    }

    // Clear errors
    clearErrorMessage();
}

// ============================================
// FILE UPLOAD HANDLERS
// ============================================

function setupFileUploadHandlers() {
    const dragDropArea = document.getElementById('dragDropArea');
    const fileInput = document.getElementById('fileInput');

    // Click to browse
    dragDropArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File selection
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // Drag and drop
    dragDropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dragDropArea.classList.add('drag-over');
    });

    dragDropArea.addEventListener('dragleave', () => {
        dragDropArea.classList.remove('drag-over');
    });

    dragDropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dragDropArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
}

function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const validExtensions = ['.csv', '.xlsx'];

    const hasValidType = validTypes.includes(file.type);
    const hasValidExtension = validExtensions.some(ext => file.name.endsWith(ext));

    if (!hasValidType && !hasValidExtension) {
        showError('Please upload a CSV or Excel (.xlsx) file');
        return;
    }

    selectedFile = file;

    // Show file preview
    const dragDropArea = document.getElementById('dragDropArea');
    const filePreview = document.getElementById('filePreview');

    dragDropArea.style.display = 'none';
    filePreview.style.display = 'block';

    // Update preview
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);

    // Enable scan button
    document.getElementById('scanFileBtn').disabled = false;

    // Clear errors
    clearErrorMessage();
}

function removeFile() {
    selectedFile = null;

    const dragDropArea = document.getElementById('dragDropArea');
    const filePreview = document.getElementById('filePreview');
    const fileInput = document.getElementById('fileInput');

    dragDropArea.style.display = 'block';
    filePreview.style.display = 'none';
    fileInput.value = '';

    document.getElementById('scanFileBtn').disabled = true;
    clearErrorMessage();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ============================================
// CLASSIFY FILE FUNCTION
// ============================================

async function classifyFile() {
    if (!selectedFile) {
        showError('Please select a file first');
        return;
    }

    const button = document.getElementById('scanFileBtn');
    const fileResults = document.getElementById('fileResults');

    // Clear previous results
    fileResults.innerHTML = '';
    clearErrorMessage();

    try {
        // Set loading state
        button.disabled = true;
        const originalText = button.innerText;
        button.innerHTML = '<span class="spinner"></span>Processing...';

        // Build FormData
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Call API
        const response = await fetch('/api/classify-file', {
            method: 'POST',
            body: formData
        });

        // Check if response is successful
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Failed to process file');
        }

        // Get blob and trigger download
        const blob = await response.blob();
        triggerDownload(blob, selectedFile.name);

        // Show success message
        showSuccessMessage('File classified successfully');

        // Reset file mode
        setTimeout(() => {
            removeFile();
            clearFileMode();
        }, 1500);

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        button.disabled = false;
        button.innerHTML = 'Scan File';
    }
}

function triggerDownload(blob, originalFileName) {
    // Create a temporary URL for the blob
    const url = window.URL.createObjectURL(blob);

    // Create download link
    const link = document.createElement('a');
    link.href = url;

    // Generate output filename
    const timestamp = new Date().toISOString().slice(0, 10);
    const extension = originalFileName.endsWith('.xlsx') ? '.xlsx' : '.csv';
    const outputName = `classified_logs_${timestamp}${extension}`;

    link.download = outputName;

    // Trigger download
    document.body.appendChild(link);
    link.click();

    // Cleanup
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

function clearFileMode() {
    document.getElementById('fileResults').innerHTML = '';
}

// ============================================
// MAIN CLASSIFY FUNCTION (PASTE MODE)
// ============================================

async function classifyLogs() {
    const textarea = document.getElementById("logs");
    const resultsContainer = document.getElementById("results");
    const button = document.getElementById("classifyBtn");

    // Clear previous results and errors
    resultsContainer.innerHTML = "";
    clearErrorMessage();

    // Validate input
    const logs = textarea.value.trim();
    if (!logs) {
        showError("Please enter logs to classify.");
        return;
    }

    try {
        // Set loading state
        button.disabled = true;
        button.innerHTML = '<span class="spinner"></span>Processing...';

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
        button.innerHTML = "Classify Logs";
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
    clearErrorMessage();
}

// ============================================
// ERROR & SUCCESS HANDLING
// ============================================

function showError(message) {
    const errorContainer = document.getElementById("error-message");
    errorContainer.innerText = message;
    errorContainer.classList.add("show");
    clearSuccessMessage();
}

function clearErrorMessage() {
    const errorContainer = document.getElementById("error-message");
    errorContainer.classList.remove("show");
    errorContainer.innerText = "";
}

function showSuccessMessage(message) {
    let successContainer = document.getElementById("success-message");
    
    if (!successContainer) {
        // Create success message element if it doesn't exist
        successContainer = document.createElement("div");
        successContainer.id = "success-message";
        successContainer.className = "success-message";
        document.querySelector(".app-card").appendChild(successContainer);
    }

    successContainer.innerHTML = `<span class="success-icon">✓</span>${escapeHtml(message)}`;
    successContainer.classList.add("show");

    // Auto-hide after 3 seconds
    setTimeout(() => {
        successContainer.classList.remove("show");
    }, 3000);

    clearErrorMessage();
}

function clearSuccessMessage() {
    const successContainer = document.getElementById("success-message");
    if (successContainer) {
        successContainer.classList.remove("show");
    }
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