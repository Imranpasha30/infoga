document.addEventListener('DOMContentLoaded', () => {
    // This script runs after the HTML document has been fully loaded.
    const resultDataElement = document.getElementById('result-data');
    if (!resultDataElement) {
        console.error('Result data not found!');
        return;
    }

    const result = JSON.parse(resultDataElement.textContent);
    const emailData = result.emails || [];

    // --- Attach event listeners to buttons ---
    const copyAllBtn = document.getElementById('copy-all-btn');
    if (copyAllBtn) copyAllBtn.addEventListener('click', () => copyAllEmails(emailData));

    const downloadCsvBtn = document.getElementById('download-csv-btn');
    if (downloadCsvBtn) downloadCsvBtn.addEventListener('click', () => downloadCSV(emailData, result.domain));

    const downloadTxtBtn = document.getElementById('download-txt-btn');
    if (downloadTxtBtn) downloadTxtBtn.addEventListener('click', () => downloadTXT(emailData, result.domain));

    const downloadJsonBtn = document.getElementById('download-json-btn');
    if (downloadJsonBtn) downloadJsonBtn.addEventListener('click', () => downloadJSON(result));

    // Attach listeners for individual copy/verify buttons
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const email = e.currentTarget.dataset.email;
            copyEmail(email);
        });
    });

    document.querySelectorAll('.verify-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const email = e.currentTarget.dataset.email;
            verifyEmail(email, result.discovery_timestamp);
        });
    });
});

// --- Core Functions ---

function copyEmail(email) {
    navigator.clipboard.writeText(email).then(() => {
        showNotification('Email copied: ' + email, 'success');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        fallbackCopyText(email);
        showNotification('Email copied: ' + email, 'success');
    });
}

function copyAllEmails(emailData) {
    if (emailData.length === 0) return;
    const emailsText = emailData.map(item => item.email).join('\n');
    navigator.clipboard.writeText(emailsText).then(() => {
        showNotification('All ' + emailData.length + ' emails copied!', 'success');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        fallbackCopyText(emailsText);
        showNotification('All ' + emailData.length + ' emails copied!', 'success');
    });
}

function downloadCSV(emailData, domain) {
    if (emailData.length === 0) return;
    const csvContent = "Email,Source,Context\n" +
        emailData.map(item => `"${item.email}","${item.source}","${item.context || 'N/A'}"`).join('\n');
    createDownloadLink(csvContent, `${domain}_emails.csv`, 'text/csv;charset=utf-8;');
    showNotification('CSV file downloaded!', 'success');
}

function downloadTXT(emailData, domain) {
    if (emailData.length === 0) return;
    const txtContent = emailData.map(item => item.email).join('\n');
    createDownloadLink(txtContent, `${domain}_emails.txt`, 'text/plain;charset=utf-8;');
    showNotification('TXT file downloaded!', 'success');
}

function downloadJSON(resultData) {
    const jsonContent = JSON.stringify(resultData, null, 2);
    createDownloadLink(jsonContent, `${resultData.domain}_emails.json`, 'application/json;charset=utf-8;');
    showNotification('JSON file downloaded!', 'success');
}

function verifyEmail(email, timestamp) {
    const sampleEmail = `From: ${email}
To: recipient@example.com
Subject: Email to verify
Date: ${new Date(timestamp).toUTCString()}
Message-ID: <sample@${email.split('@')[1]}>

[Paste the complete email content here including all headers for proper verification]

This is a sample email format. Replace this with the actual email content you want to verify.`;
    localStorage.setItem('emailToVerify', sampleEmail);
    window.location.href = '/?tab=verify';
}

// --- Helper Functions ---

function createDownloadLink(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

function fallbackCopyText(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed"; // Avoid scrolling to bottom
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
    } catch (err) {
        console.error('Fallback copy failed', err);
    }
    document.body.removeChild(textArea);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-5 right-5 p-4 rounded-lg shadow-xl text-white z-50 transition-transform duration-300 transform translate-x-full ${type === 'success' ? 'bg-green-500' : 'bg-blue-500'
        }`;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);

    // Animate out
    setTimeout(() => {
        notification.style.transform = 'translateX(120%)';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}
