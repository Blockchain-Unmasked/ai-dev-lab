/**
 * Main JavaScript file for AI/DEV Lab Customer Support Demo
 * Enhanced with professional design system and advanced features
 */

// Global app state
window.appState = {
    version: '2.0.0',
    environment: 'demo',
    debug: true, // Set to true for verbose logging
    features: {
        chat: true,
        aiMode: true,
        qaMode: false,
        stealthMode: true,
        dualMode: true,
        metrics: true,
        export: true
    },
    theme: 'light',
    performance: {
        lastInteraction: Date.now(),
        interactions: 0,
        errors: 0
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 AI/DEV Lab Customer Support Demo v2.0 initialized');
    
    // Check if chat agent is available
    if (window.chatAgent) {
        console.log('✅ Chat agent loaded successfully');
        window.appState.features.chat = true;
    } else {
        console.warn('⚠️ Chat agent not found');
        window.appState.features.chat = false;
    }
    
    // Add global event listeners
    setupGlobalEventListeners();
    
    // Initialize enhanced features
    initializeEnhancedFeatures();
    
    // Initialize model options
    initializeModelOptions();
    
    // Initialize scroll functionality
    initializeScrollFeatures();
    
    // Initialize API key functionality
    initializeAPIKeyFeatures();
    
    // Setup performance monitoring
    setupPerformanceMonitoring();
    
    // Initialize accessibility features
    setupAccessibility();
    
    console.log('🎯 All systems operational');
});

function setupGlobalEventListeners() {
    // Handle keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to send message
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeChatForm = getActiveChatForm();
            if (activeChatForm) {
                activeChatForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            const activeChatInput = getActiveChatInput();
            if (activeChatInput) {
                activeChatInput.value = '';
                activeChatInput.blur();
            }
        }
        
        // Tab to switch modes (when in QA mode)
        if (e.key === 'Tab' && e.shiftKey) {
            e.preventDefault();
            toggleMode();
        }
    });
    
    // Handle window focus/blur for better UX
    window.addEventListener('focus', () => {
        document.body.classList.remove('window-blurred');
        window.appState.performance.lastInteraction = Date.now();
    });
    
    window.addEventListener('blur', () => {
        document.body.classList.add('window-blurred');
    });
    
    // Handle visibility change for performance
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            console.log('📱 App backgrounded');
        } else {
            console.log('📱 App foregrounded');
            window.appState.performance.lastInteraction = Date.now();
        }
    });
    
    // Handle online/offline status
    window.addEventListener('online', () => {
        console.log('🌐 Connection restored');
        showNotification('Connection restored', 'success');
    });
    
    window.addEventListener('offline', () => {
        console.log('🌐 Connection lost');
        showNotification('Connection lost', 'warning');
    });
}

function initializeEnhancedFeatures() {
    // Initialize performance monitoring
    initializePerformanceMonitoring();
    
    // Initialize error handling
    initializeErrorHandling();
    
    // Initialize analytics (if available)
    initializeAnalytics();
    
    console.log('🔧 Enhanced features initialized');
}

function setupPerformanceMonitoring() {
    // Monitor interaction performance
    let lastFrameTime = performance.now();
    
    let frameCount = 0;
    let lastCheckTime = performance.now();
    
    function monitorPerformance(currentTime) {
        frameCount++;
        
        // Only check FPS every 2 seconds to reduce console spam
        if (currentTime - lastCheckTime >= 2000) {
            const fps = Math.round((frameCount * 1000) / (currentTime - lastCheckTime));
            
            // Only warn for very low FPS (< 20) to reduce noise
            if (fps < 20) {
                console.warn('⚠️ Low FPS detected:', fps);
            }
            
            frameCount = 0;
            lastCheckTime = currentTime;
        }
        
        requestAnimationFrame(monitorPerformance);
    }
    
    requestAnimationFrame(monitorPerformance);
    
    // Monitor memory usage (if available)
    if ('memory' in performance) {
        setInterval(() => {
            const memory = performance.memory;
            if (memory.usedJSHeapSize > memory.jsHeapSizeLimit * 0.8) {
                console.warn('⚠️ High memory usage detected');
            }
        }, 10000);
    }
}

function setupAccessibility() {
    // Setup focus management
    setupFocusManagement();
    
    // Add ARIA live regions
    addAriaLiveRegions();
    
    console.log('♿ Accessibility features initialized');
}



function setupFocusManagement() {
    // Handle focus trapping in modals (if any)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            const activeElement = document.activeElement;
            const focusableElements = document.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            
            if (focusableElements.length > 0) {
                const firstElement = focusableElements[0];
                const lastElement = focusableElements[focusableElements.length - 1];
                
                if (e.shiftKey && activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                } else if (!e.shiftKey && activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        }
    });
}

function addAriaLiveRegions() {
    // Add live region for notifications
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    document.body.appendChild(liveRegion);
    
    window.liveRegion = liveRegion;
}



function initializePerformanceMonitoring() {
    // Monitor long tasks (only for very long tasks to reduce noise)
    if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                // Only warn for tasks longer than 100ms to reduce false positives
                if (entry.duration > 100) {
                    console.warn('⚠️ Long task detected:', entry.duration + 'ms');
                }
            }
        });
        
        observer.observe({ entryTypes: ['longtask'] });
    }
    
    // Monitor layout shifts
    if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.value > 0.1) {
                    console.warn('⚠️ Layout shift detected:', entry.value);
                }
            }
        });
        
        observer.observe({ entryTypes: ['layout-shift'] });
    }
}

function initializeErrorHandling() {
    // Global error handler
    window.addEventListener('error', (e) => {
        console.error('🚨 Global error:', e.error);
        window.appState.performance.errors++;
        
        // Show user-friendly error message
        showNotification('An error occurred. Please try again.', 'error');
    });
    
    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', (e) => {
        console.error('🚨 Unhandled promise rejection:', e.reason);
        window.appState.performance.errors++;
        
        // Show user-friendly error message
        showNotification('A network error occurred. Please check your connection.', 'error');
    });
}

function initializeAnalytics() {
    // Simple analytics tracking
    window.trackEvent = (eventName, data = {}) => {
        const event = {
            name: eventName,
            data: data,
            timestamp: Date.now(),
            sessionId: getSessionId()
        };
        
        // Log events based on debug mode and importance
        if (window.appState.debug || ['error', 'api_key_saved', 'api_key_cleared', 'model_selection_changed', 'interaction', 'ai_response', 'chat_message'].includes(eventName)) {
            console.log('📊 Event tracked:', event);
        }
        
        // Uncomment the line below to completely disable event logging
        // console.log('📊 Event tracked:', event);
        
        // Store in localStorage for demo purposes
        const analytics = JSON.parse(localStorage.getItem('ai-dev-lab-analytics') || '[]');
        analytics.push(event);
        localStorage.setItem('ai-dev-lab-analytics', JSON.stringify(analytics));
        
        // Limit stored events
        if (analytics.length > 100) {
            analytics.splice(0, analytics.length - 100);
            localStorage.setItem('ai-dev-lab-analytics', JSON.stringify(analytics));
        }
    };
    
    // Track page views
    trackEvent('page_view', { path: window.location.pathname });
    
    // Track interactions
    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') {
            trackEvent('interaction', {
                type: 'click',
                element: e.target.textContent || e.target.className
            });
        }
    });
}

// Utility functions
window.utils = {
    // Format timestamp
    formatTime: (date) => {
        return new Date(date).toLocaleTimeString();
    },
    
    // Generate random ID
    generateId: () => {
        return Math.random().toString(36).substr(2, 9);
    },
    
    // Debounce function
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Show notification
    showNotification: (message, type = 'info') => {
        showNotification(message, type);
    },
    
    // Copy to clipboard
    copyToClipboard: async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            showNotification('Copied to clipboard', 'success');
            return true;
        } catch (err) {
            console.error('Failed to copy:', err);
            showNotification('Failed to copy', 'error');
            return false;
        }
    },
    
    // Download data
    downloadData: (data, filename) => {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    }
};

// Helper functions
function getActiveChatForm() {
    const customerForm = document.getElementById('chat-form');
    const qaForm = document.getElementById('qa-chat-form');
    
    if (document.getElementById('qa-mode').classList.contains('active')) {
        return qaForm;
    }
    return customerForm;
}

function getActiveChatInput() {
    const customerInput = document.getElementById('chat-input');
    const qaInput = document.getElementById('qa-chat-input');
    
    if (document.getElementById('qa-mode').classList.contains('active')) {
        return qaInput;
    }
    return customerInput;
}

function toggleMode() {
    const qaToggle = document.getElementById('qa-mode-toggle');
    if (qaToggle) {
        qaToggle.click();
    }
}

function getSessionId() {
    let sessionId = localStorage.getItem('ai-dev-lab-session-id');
    if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('ai-dev-lab-session-id', sessionId);
    }
    return sessionId;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fade-in`;
    notification.textContent = message;
    
    // Add to live region for screen readers
    if (window.liveRegion) {
        window.liveRegion.textContent = message;
    }
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
    
    // Track notification
    trackEvent('notification_shown', { type, message });
}

// Export for use in other modules
window.MainApp = {
    utils: window.utils,
    state: window.appState,
    trackEvent: window.trackEvent || (() => {}),
    showNotification: showNotification
};

// Performance monitoring
window.addEventListener('load', () => {
    // Track page load performance
    if ('performance' in window) {
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
            trackEvent('page_load_performance', {
                loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime || 0,
                firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
            });
        }
    }
    
    console.log('📊 Performance monitoring active');
});

// ===== MODEL OPTIONS FUNCTIONALITY =====

function initializeModelOptions() {
    console.log('🔧 Initializing model options...');
    
    // Initialize sliders
    initializeSliders();
    
    // Initialize preset buttons
    initializePresetButtons();
    
    // Load saved settings
    loadModelSettings();
    
    console.log('✅ Model options initialized');
}

function initializeScrollFeatures() {
    console.log('🔧 Initializing scroll features...');
    
    // Scroll to settings button
    const scrollToSettingsBtn = document.getElementById('scroll-to-settings');
    if (scrollToSettingsBtn) {
        scrollToSettingsBtn.addEventListener('click', () => {
            const modelOptions = document.querySelector('.model-options');
            if (modelOptions) {
                modelOptions.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
                
                // Add highlight effect
                modelOptions.style.animation = 'none';
                setTimeout(() => {
                    modelOptions.style.animation = 'highlightPulse 1s ease-out';
                }, 10);
                
                // Track scroll action
                trackEvent('scroll_to_settings_clicked');
            }
        });
    }
    
    // Add scroll highlight animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes highlightPulse {
            0% { transform: scale(1); box-shadow: var(--shadow-sm); }
            50% { transform: scale(1.02); box-shadow: var(--shadow-lg); }
            100% { transform: scale(1); box-shadow: var(--shadow-sm); }
        }
    `;
    document.head.appendChild(style);
    
    console.log('✅ Scroll features initialized');
}

function initializeAPIKeyFeatures() {
    console.log('🔑 Initializing API key features...');
    
    // Initialize model selection
    initializeModelSelection();
    
    // Check backend API status first
    checkBackendAPIStatus();
    
    // Add event listeners for API key management
    const saveBtn = document.getElementById('save-api-key');
    const clearBtn = document.getElementById('clear-api-key');
    
    if (saveBtn) {
        saveBtn.addEventListener('click', saveAPIKey);
    }
    if (clearBtn) {
        clearBtn.addEventListener('click', clearAPIKey);
    }
    
    console.log('✅ API key features initialized');
}

function initializeModelSelection() {
    const modelSelect = document.getElementById('model-select');
    const modelInfo = document.getElementById('model-info');
    const apiKeyLabel = document.getElementById('api-key-label');
    
    if (!modelSelect) return;
    
    // Load saved model selection
    const savedModel = localStorage.getItem('ai-dev-lab-selected-model') || 'gemini-pro';
    modelSelect.value = savedModel;
    updateModelSelection(savedModel);
    
    // Add event listener for model changes
    modelSelect.addEventListener('change', (e) => {
        const selectedModel = e.target.value;
        updateModelSelection(selectedModel);
        localStorage.setItem('ai-dev-lab-selected-model', selectedModel);
        trackEvent('model_selection_changed', { model: selectedModel });
    });
}

function updateModelSelection(model) {
    const modelInfo = document.getElementById('model-info');
    const apiKeyLabel = document.getElementById('api-key-label');
    const modelBadge = document.querySelector('.model-badge');
    
    // Update model descriptions and labels
    const modelConfigs = {
        'gemini-pro': {
            name: 'Gemini Pro',
            provider: 'Google',
            description: 'Google\'s advanced AI model with strong reasoning capabilities',
            apiKeyLabel: 'Gemini API Key:',
            placeholder: 'Enter your Gemini API key...',
            helpText: 'Get your API key from Google AI Studio (makersuite.google.com)'
        },
        'gpt-4': {
            name: 'GPT-4',
            provider: 'OpenAI',
            description: 'OpenAI\'s most capable model with excellent conversation skills',
            apiKeyLabel: 'OpenAI API Key:',
            placeholder: 'Enter your OpenAI API key...',
            helpText: 'Get your API key from OpenAI Platform (platform.openai.com)'
        },
        'claude-3': {
            name: 'Claude 3',
            provider: 'Anthropic',
            description: 'Anthropic\'s helpful, harmless, and honest AI assistant',
            apiKeyLabel: 'Anthropic API Key:',
            placeholder: 'Enter your Anthropic API key...',
            helpText: 'Get your API key from Anthropic Console (console.anthropic.com)'
        }
    };
    
    const config = modelConfigs[model];
    if (!config) return;
    
    // Update model badge
    if (modelBadge) {
        modelBadge.textContent = config.name;
    }
    
    // Update API key label
    if (apiKeyLabel) {
        apiKeyLabel.textContent = config.apiKeyLabel;
    }
    
    // Update API key input placeholder
    const apiKeyInput = document.getElementById('api-key-input');
    if (apiKeyInput) {
        apiKeyInput.placeholder = config.placeholder;
    }
    
    // Update help tooltip
    const helpTooltip = document.querySelector('.help-tooltip');
    if (helpTooltip) {
        helpTooltip.setAttribute('data-tooltip', config.helpText);
    }
    
    // Update model info
    if (modelInfo) {
        modelInfo.innerHTML = `
            <span class="model-description">${config.description}</span>
            <div class="model-provider">Provider: ${config.provider}</div>
        `;
    }
}

async function checkBackendAPIStatus() {
    try {
        // Use the correct backend URL (port 8000)
        const backendURL = window.location.origin.replace('3000', '8000') || 'http://localhost:8000';
        const response = await fetch(`${backendURL}/api/v1/ai/config`);
        
        if (response.ok) {
            const config = await response.json();
            const geminiStatus = config.gemini;
            
            if (geminiStatus && geminiStatus.api_key_configured) {
                // Backend has API key configured
                updateModelStatus('ready');
                const statusElement = document.getElementById('api-key-status');
                if (statusElement) {
                    statusElement.textContent = 'API key configured (backend)';
                    statusElement.style.color = '#10b981';
                }
                console.log('✅ Backend API key detected');
            } else {
                // Check localStorage for frontend API key
                const savedKey = localStorage.getItem('ai-dev-lab-gemini-api-key');
                if (savedKey) {
                    document.getElementById('api-key-input').value = savedKey;
                    updateModelStatus('ready');
                    const statusElement = document.getElementById('api-key-status');
                    if (statusElement) {
                        statusElement.textContent = 'API key configured (frontend)';
                        statusElement.style.color = '#10b981';
                    }
                    console.log('✅ Frontend API key detected');
                } else {
                    updateModelStatus('not-configured');
                    console.log('⚠️ No API key found');
                }
            }
        } else {
            console.warn('Backend API status check failed:', response.status);
            // Fallback to localStorage check
            const savedKey = localStorage.getItem('ai-dev-lab-gemini-api-key');
            if (savedKey) {
                document.getElementById('api-key-input').value = savedKey;
                updateModelStatus('ready');
            } else {
                updateModelStatus('not-configured');
            }
        }
    } catch (error) {
        console.warn('Could not check backend API status:', error);
        // Fallback to localStorage check
        const savedKey = localStorage.getItem('ai-dev-lab-gemini-api-key');
        if (savedKey) {
            document.getElementById('api-key-input').value = savedKey;
            updateModelStatus('ready');
        } else {
            updateModelStatus('not-configured');
        }
    }
}

// Model status and API connection functions
function updateModelStatus(status) {
    const statusElement = document.getElementById('model-status');
    if (!statusElement) return;
    
    // Remove existing status classes
    statusElement.classList.remove('testing', 'error');
    
    switch (status) {
        case 'ready':
            statusElement.textContent = 'Ready';
            statusElement.className = 'model-status';
            break;
        case 'testing':
            statusElement.textContent = 'Testing...';
            statusElement.className = 'model-status testing';
            break;
        case 'error':
            statusElement.textContent = 'Error';
            statusElement.className = 'model-status error';
            break;
        case 'not-configured':
            statusElement.textContent = 'Not Configured';
            statusElement.className = 'model-status error';
            break;
        default:
            statusElement.textContent = 'Unknown';
            statusElement.className = 'model-status error';
    }
}

// testAPIConnection function moved to Model Configuration panel only

function saveAPIKey() {
    const apiKeyInput = document.getElementById('api-key-input');
    const apiKey = apiKeyInput.value.trim();
    
    if (!apiKey) {
        showNotification('Please enter an API key', 'warning');
        return;
    }
    
    // Save to localStorage
    localStorage.setItem('ai-dev-lab-gemini-api-key', apiKey);
    
    // Update model status
    updateModelStatus('ready');
    
    // Update API key status display
    const statusElement = document.getElementById('api-key-status');
    if (statusElement) {
        statusElement.textContent = 'API key configured';
        statusElement.style.color = '#10b981';
    }
    
    // Track the event
    trackEvent('api_key_saved', { hasKey: true });
    
    showNotification('✅ API key saved successfully', 'success');
}

function clearAPIKey() {
    const apiKeyInput = document.getElementById('api-key-input');
    
    // Clear the input
    apiKeyInput.value = '';
    
    // Remove from localStorage
    localStorage.removeItem('ai-dev-lab-gemini-api-key');
    
    // Update model status
    updateModelStatus('not-configured');
    
    // Update API key status display
    const statusElement = document.getElementById('api-key-status');
    if (statusElement) {
        statusElement.textContent = 'No API key configured';
        statusElement.style.color = '#6b7280';
    }
    
    // Track the event
    trackEvent('api_key_cleared', { hasKey: false });
    
    showNotification('🗑️ API key cleared', 'info');
}

function initializeSliders() {
    const sliders = document.querySelectorAll('.slider');
    
    sliders.forEach(slider => {
        const valueDisplay = document.getElementById(slider.id.replace('-slider', '-value'));
        
        if (valueDisplay) {
            // Update display on input
            slider.addEventListener('input', (e) => {
                valueDisplay.textContent = e.target.value;
                saveModelSettings();
            });
            
            // Update display on change
            slider.addEventListener('change', (e) => {
                valueDisplay.textContent = e.target.value;
                saveModelSettings();
                updateModelConfiguration();
            });
        }
    });
}

function initializePresetButtons() {
    const presetButtons = document.querySelectorAll('.preset-btn');
    
    presetButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const preset = e.target.dataset.preset;
            applyPreset(preset);
            
            // Update active state
            presetButtons.forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');
        });
    });
}

function applyPreset(preset) {
    const presets = {
        conservative: {
            temperature: 0.3,
            maxTokens: 500,
            topP: 0.8
        },
        balanced: {
            temperature: 0.7,
            maxTokens: 1000,
            topP: 0.9
        },
        creative: {
            temperature: 1.2,
            maxTokens: 2000,
            topP: 0.95
        }
    };
    
    const settings = presets[preset];
    
    // Update sliders
    Object.keys(settings).forEach(key => {
        const slider = document.getElementById(`${key}-slider`);
        const valueDisplay = document.getElementById(`${key}-value`);
        
        if (slider && valueDisplay) {
            slider.value = settings[key];
            valueDisplay.textContent = settings[key];
        }
    });
    
    // Save and update
    saveModelSettings();
    updateModelConfiguration();
    
    // Show notification
    showNotification(`Applied ${preset} preset`, 'success');
}

function updateModelConfiguration() {
    const temperature = document.getElementById('temperature-slider')?.value || 0.7;
    const maxTokens = document.getElementById('max-tokens-slider')?.value || 1000;
    const topP = document.getElementById('top-p-slider')?.value || 0.9;
    
    // Update global state
    window.appState.modelConfig = {
        temperature: parseFloat(temperature),
        maxTokens: parseInt(maxTokens),
        topP: parseFloat(topP),
        model: 'gemini'
    };
    
    console.log('🔧 Model configuration updated:', window.appState.modelConfig);
    
    // Track configuration change
    trackEvent('model_configuration_changed', window.appState.modelConfig);
}

function saveModelSettings() {
    const settings = {
        temperature: document.getElementById('temperature-slider')?.value || 0.7,
        maxTokens: document.getElementById('max-tokens-slider')?.value || 1000,
        topP: document.getElementById('top-p-slider')?.value || 0.9
    };
    
    localStorage.setItem('ai-dev-lab-model-settings', JSON.stringify(settings));
}

function loadModelSettings() {
    const saved = localStorage.getItem('ai-dev-lab-model-settings');
    
    if (saved) {
        try {
            const settings = JSON.parse(saved);
            
            // Apply saved settings
            Object.keys(settings).forEach(key => {
                const slider = document.getElementById(`${key}-slider`);
                const valueDisplay = document.getElementById(`${key}-value`);
                
                if (slider && valueDisplay) {
                    slider.value = settings[key];
                    valueDisplay.textContent = settings[key];
                }
            });
            
            // Update configuration
            updateModelConfiguration();
            
            console.log('📁 Loaded saved model settings');
        } catch (error) {
            console.warn('⚠️ Failed to load saved model settings:', error);
        }
    }
}
