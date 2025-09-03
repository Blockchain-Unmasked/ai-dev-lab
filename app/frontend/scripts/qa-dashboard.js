/**
 * QA Dashboard JavaScript - AI/DEV Lab
 * Handles API configuration, canned responses, and system metrics
 */

// Global state for QA dashboard
window.qaState = {
    apiKey: null,
    apiStatus: 'disconnected',
    cannedResponses: [],
    metrics: {
        totalRequests: 0,
        successRate: 100,
        avgResponseTime: 0,
        requestsToday: 0,
        cannedUsed: 0,
        customUsed: 0
    },
    spending: {
        monthlyBudget: 50.00,
        spentThisMonth: 0.00,
        inputTokens: 0,
        outputTokens: 0,
        inputCost: 0.00,
        outputCost: 0.00,
        costPerRequest: 0.00,
        dailyAverage: 0.00,
        budgetResetDay: 1,
        alertEmail: null,
        lastReset: null
    },
    startTime: Date.now()
};

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔧 QA Dashboard initialized');
    
    // Initialize all components
    initializeAPIKeyManagement();
    initializeCannedResponseSystem();
    initializeMetricsDashboard();
    initializeSpendingTracking();
    initializeEventListeners();
    
    // Load saved data
    loadSavedData();
    
    // Start metrics updates
    startMetricsUpdates();
    
    console.log('✅ QA Dashboard ready');
});

// ===== API KEY MANAGEMENT =====

function initializeAPIKeyManagement() {
    console.log('🔑 Initializing API key management...');
    
    // Load saved API key
    const savedKey = localStorage.getItem('ai-dev-lab-gemini-api-key');
    if (savedKey) {
        document.getElementById('gemini-api-key').value = savedKey;
        window.qaState.apiKey = savedKey;
        updateAPIStatus('saved');
    }
    
    // Test API connection if key exists
    if (window.qaState.apiKey) {
        testAPIConnection();
    }
}

function saveAPIKey() {
    const apiKeyInput = document.getElementById('gemini-api-key');
    const apiKey = apiKeyInput.value.trim();
    
    if (!apiKey) {
        showNotification('Please enter an API key', 'error');
        return;
    }
    
    // Save to localStorage
    localStorage.setItem('ai-dev-lab-gemini-api-key', apiKey);
    window.qaState.apiKey = apiKey;
    
    // Update status
    updateAPIStatus('saved');
    
    // Test connection
    testAPIConnection();
    
    showNotification('API key saved successfully', 'success');
}

function clearAPIKey() {
    document.getElementById('gemini-api-key').value = '';
    localStorage.removeItem('ai-dev-lab-gemini-api-key');
    window.qaState.apiKey = null;
    updateAPIStatus('disconnected');
    showNotification('API key cleared', 'info');
}

function toggleAPIKeyVisibility() {
    const input = document.getElementById('gemini-api-key');
    const toggleBtn = document.getElementById('toggle-api-key-visibility');
    
    if (input.type === 'password') {
        input.type = 'text';
        toggleBtn.textContent = '🙈';
    } else {
        input.type = 'password';
        toggleBtn.textContent = '👁️';
    }
}

async function testAPIConnection() {
    if (!window.qaState.apiKey) {
        updateAPIStatus('no-key');
        return;
    }
    
    updateAPIStatus('testing');
    
    try {
        // Simple test request to Gemini API - use API key as query parameter
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=${window.qaState.apiKey}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: "Hello, this is a test message."
                    }]
                }]
            })
        });
        
        if (response.ok) {
            updateAPIStatus('connected');
            showNotification('API connection successful', 'success');
        } else {
            updateAPIStatus('error');
            showNotification('API connection failed', 'error');
        }
    } catch (error) {
        console.error('API test error:', error);
        updateAPIStatus('error');
        showNotification('API connection failed', 'error');
    }
}

function updateAPIStatus(status) {
    const statusElement = document.getElementById('api-status');
    const testBtn = document.getElementById('test-api-connection');
    
    window.qaState.apiStatus = status;
    
    switch (status) {
        case 'connected':
            statusElement.textContent = 'Status: Connected ✅';
            statusElement.className = 'api-status status-connected';
            testBtn.textContent = 'Test Connection ✅';
            testBtn.className = 'btn btn-secondary status-connected';
            break;
        case 'saved':
            statusElement.textContent = 'Status: Saved (Not Tested)';
            statusElement.className = 'api-status status-saved';
            testBtn.textContent = 'Test Connection';
            testBtn.className = 'btn btn-secondary';
            break;
        case 'testing':
            statusElement.textContent = 'Status: Testing...';
            statusElement.className = 'api-status status-testing';
            testBtn.textContent = 'Testing...';
            testBtn.className = 'btn btn-secondary';
            testBtn.disabled = true;
            break;
        case 'error':
            statusElement.textContent = 'Status: Connection Failed ❌';
            statusElement.className = 'api-status status-error';
            testBtn.textContent = 'Retry Connection';
            testBtn.className = 'btn btn-secondary';
            break;
        case 'disconnected':
        default:
            statusElement.textContent = 'Status: No API Key';
            statusElement.className = 'api-status status-disconnected';
            testBtn.textContent = 'Test Connection';
            testBtn.className = 'btn btn-secondary';
            break;
    }
}

// ===== CANNED RESPONSE SYSTEM =====

function initializeCannedResponseSystem() {
    console.log('💬 Initializing canned response system...');
    
    // Load saved responses
    loadCannedResponses();
    
    // Add default responses if none exist
    if (window.qaState.cannedResponses.length === 0) {
        addDefaultResponses();
    }
    
    // Update display
    updateCannedResponseDisplay();
}

function loadCannedResponses() {
    const saved = localStorage.getItem('ai-dev-lab-canned-responses');
    if (saved) {
        try {
            window.qaState.cannedResponses = JSON.parse(saved);
        } catch (error) {
            console.warn('Failed to load canned responses:', error);
            window.qaState.cannedResponses = [];
        }
    }
}

function saveCannedResponses() {
    localStorage.setItem('ai-dev-lab-canned-responses', JSON.stringify(window.qaState.cannedResponses));
}

function addDefaultResponses() {
    const defaultResponses = [
        {
            id: 'welcome',
            title: 'Welcome Message',
            category: 'greetings',
            content: '👋 Welcome to AI/DEV Lab Customer Support! How can I help you today?',
            triggers: ['hello', 'hi', 'welcome', 'start'],
            usageCount: 0,
            lastUsed: null
        },
        {
            id: 'technical-support',
            title: 'Technical Support',
            category: 'technical',
            content: '🔧 I understand you\'re experiencing a technical issue. Let me help you troubleshoot this step by step.',
            triggers: ['problem', 'issue', 'error', 'broken', 'not working'],
            usageCount: 0,
            lastUsed: null
        },
        {
            id: 'billing-inquiry',
            title: 'Billing Inquiry',
            category: 'billing',
            content: '💳 I\'d be happy to help with your billing question. Let me look up your account information.',
            triggers: ['bill', 'payment', 'charge', 'cost', 'pricing'],
            usageCount: 0,
            lastUsed: null
        },
        {
            id: 'general-help',
            title: 'General Help',
            category: 'general',
            content: '🤝 I\'m here to help! Could you please provide more details about what you need assistance with?',
            triggers: ['help', 'assist', 'support', 'question'],
            usageCount: 0,
            lastUsed: null
        }
    ];
    
    window.qaState.cannedResponses = defaultResponses;
    saveCannedResponses();
}

function addCannedResponse() {
    const modal = document.getElementById('add-response-modal');
    modal.classList.remove('hidden');
    
    // Clear form
    document.getElementById('response-title').value = '';
    document.getElementById('response-content').value = '';
    document.getElementById('response-triggers').value = '';
    document.getElementById('response-category').value = 'general';
}

function saveCannedResponse() {
    const title = document.getElementById('response-title').value.trim();
    const category = document.getElementById('response-category').value;
    const content = document.getElementById('response-content').value.trim();
    const triggers = document.getElementById('response-triggers').value.trim();
    
    if (!title || !content) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    const newResponse = {
        id: 'response_' + Date.now(),
        title,
        category,
        content,
        triggers: triggers ? triggers.split(',').map(t => t.trim()) : [],
        usageCount: 0,
        lastUsed: null,
        createdAt: new Date().toISOString()
    };
    
    window.qaState.cannedResponses.push(newResponse);
    saveCannedResponses();
    updateCannedResponseDisplay();
    
    // Close modal
    closeModal();
    showNotification('Canned response added successfully', 'success');
}

function closeModal() {
    document.getElementById('add-response-modal').classList.add('hidden');
}

function updateCannedResponseDisplay() {
    const responseList = document.getElementById('response-list');
    const responseCount = document.getElementById('response-count');
    const totalResponses = document.getElementById('total-responses');
    
    // Update counts
    responseCount.textContent = `${window.qaState.cannedResponses.length} Responses`;
    totalResponses.textContent = window.qaState.cannedResponses.length;
    
    // Clear existing list
    responseList.innerHTML = '';
    
    // Add responses to list
    window.qaState.cannedResponses.forEach(response => {
        const responseElement = createResponseElement(response);
        responseList.appendChild(responseElement);
    });
}

function createResponseElement(response) {
    const div = document.createElement('div');
    div.className = 'response-item';
    div.innerHTML = `
        <div class="response-header">
            <h5>${response.title}</h5>
            <span class="response-category">${response.category}</span>
        </div>
        <div class="response-content">
            <p>${response.content}</p>
        </div>
        <div class="response-footer">
            <span class="response-triggers">Triggers: ${response.triggers.join(', ') || 'None'}</span>
            <span class="response-usage">Used: ${response.usageCount} times</span>
            <button class="btn btn-sm btn-secondary" onclick="editResponse('${response.id}')">Edit</button>
            <button class="btn btn-sm btn-secondary" onclick="deleteResponse('${response.id}')">Delete</button>
        </div>
    `;
    return div;
}

// ===== METRICS DASHBOARD =====

function initializeMetricsDashboard() {
    console.log('📊 Initializing metrics dashboard...');
    
    // Load saved metrics
    loadMetrics();
    
    // Update display
    updateMetricsDisplay();
}

function loadMetrics() {
    const saved = localStorage.getItem('ai-dev-lab-qa-metrics');
    if (saved) {
        try {
            const savedMetrics = JSON.parse(saved);
            window.qaState.metrics = { ...window.qaState.metrics, ...savedMetrics };
        } catch (error) {
            console.warn('Failed to load metrics:', error);
        }
    }
}

function saveMetrics() {
    localStorage.setItem('ai-dev-lab-qa-metrics', JSON.stringify(window.qaState.metrics));
}

function updateMetricsDisplay() {
    // Update all metric displays
    document.getElementById('avg-response-time').textContent = `${window.qaState.metrics.avgResponseTime}ms`;
    document.getElementById('success-rate').textContent = `${window.qaState.metrics.successRate}%`;
    document.getElementById('total-requests').textContent = window.qaState.metrics.totalRequests;
    document.getElementById('requests-today').textContent = window.qaState.metrics.requestsToday;
    document.getElementById('canned-used').textContent = window.qaState.metrics.cannedUsed;
    document.getElementById('custom-used').textContent = window.qaState.metrics.customUsed;
    document.getElementById('efficiency').textContent = `${calculateEfficiency()}%`;
    
    // Update system status
    updateSystemStatus();
    
    // Update last updated time
    document.getElementById('last-updated').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
}

function calculateEfficiency() {
    const total = window.qaState.metrics.cannedUsed + window.qaState.metrics.customUsed;
    if (total === 0) return 0;
    return Math.round((window.qaState.metrics.cannedUsed / total) * 100);
}

function updateSystemStatus() {
    const statusElement = document.getElementById('system-status');
    const uptimeElement = document.getElementById('system-uptime');
    
    // Calculate uptime
    const uptime = Date.now() - window.qaState.startTime;
    const hours = Math.floor(uptime / (1000 * 60 * 60));
    const minutes = Math.floor((uptime % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((uptime % (1000 * 60)) / 1000);
    
    uptimeElement.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Update system status based on API connection
    if (window.qaState.apiStatus === 'connected') {
        statusElement.textContent = 'Healthy';
        statusElement.className = 'metric-value status-healthy';
    } else if (window.qaState.apiStatus === 'saved') {
        statusElement.textContent = 'Warning';
        statusElement.className = 'metric-value status-warning';
    } else {
        statusElement.textContent = 'Critical';
        statusElement.className = 'metric-value status-critical';
    }
}

function startMetricsUpdates() {
    // Update metrics every 5 seconds
    setInterval(() => {
        updateMetricsDisplay();
    }, 5000);
    
    // Update uptime every second
    setInterval(() => {
        updateSystemStatus();
    }, 1000);
}

// ===== EVENT LISTENERS =====

function initializeEventListeners() {
    // API Key Management
    document.getElementById('save-api-key').addEventListener('click', saveAPIKey);
    document.getElementById('clear-api-key').addEventListener('click', clearAPIKey);
    document.getElementById('toggle-api-key-visibility').addEventListener('click', toggleAPIKeyVisibility);
    document.getElementById('test-api-connection').addEventListener('click', testAPIConnection);
    
    // Canned Response System
    document.getElementById('add-canned-response').addEventListener('click', addCannedResponse);
    document.getElementById('save-response').addEventListener('click', saveCannedResponse);
    document.getElementById('close-modal').addEventListener('click', closeModal);
    document.getElementById('cancel-response').addEventListener('click', closeModal);
    
    // Category filtering
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            filterResponsesByCategory(e.target.dataset.category);
        });
    });
    
    // Dashboard controls
    document.getElementById('refresh-dashboard').addEventListener('click', refreshDashboard);
    document.getElementById('export-metrics').addEventListener('click', exportMetrics);
    
    // Modal backdrop click
    document.getElementById('add-response-modal').addEventListener('click', (e) => {
        if (e.target.id === 'add-response-modal') {
            closeModal();
        }
    });
}

function filterResponsesByCategory(category) {
    const responseList = document.getElementById('response-list');
    const responses = window.qaState.cannedResponses;
    
    // Clear list
    responseList.innerHTML = '';
    
    // Filter and display responses
    const filteredResponses = category === 'all' ? responses : responses.filter(r => r.category === category);
    
    filteredResponses.forEach(response => {
        const responseElement = createResponseElement(response);
        responseList.appendChild(responseElement);
    });
}

function refreshDashboard() {
    console.log('🔄 Refreshing dashboard...');
    
    // Reload all data
    loadSavedData();
    
    // Test API connection if key exists
    if (window.qaState.apiKey) {
        testAPIConnection();
    }
    
    // Update displays
    updateCannedResponseDisplay();
    updateMetricsDisplay();
    
    showNotification('Dashboard refreshed', 'success');
}

function loadSavedData() {
    loadCannedResponses();
    loadMetrics();
}

function exportMetrics() {
    const data = {
        timestamp: new Date().toISOString(),
        apiStatus: window.qaState.apiStatus,
        metrics: window.qaState.metrics,
        cannedResponses: window.qaState.cannedResponses
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `qa-dashboard-export-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showNotification('Metrics exported successfully', 'success');
}

// ===== UTILITY FUNCTIONS =====

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Export functions for use in other modules
window.QADashboard = {
    getAPIKey: () => window.qaState.apiKey,
    getAPIStatus: () => window.qaState.apiStatus,
    getCannedResponses: () => window.qaState.cannedResponses,
    getMetrics: () => window.qaState.metrics,
    testConnection: testAPIConnection,
    addResponse: addCannedResponse
};
