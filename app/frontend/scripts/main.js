/**
 * Main JavaScript file for AI/DEV Lab Customer Support Demo
 * Enhanced with professional design system and advanced features
 */

// Global app state
window.appState = {
    version: '2.0.0',
    environment: 'demo',
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
    
    // Initialize QA dashboard
    initializeQADashboard();
    
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
    // Initialize theme system
    initializeThemeSystem();
    
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
    
    function monitorPerformance(currentTime) {
        const deltaTime = currentTime - lastFrameTime;
        const fps = 1000 / deltaTime;
        
        if (fps < 30) {
            console.warn('⚠️ Low FPS detected:', Math.round(fps));
        }
        
        lastFrameTime = currentTime;
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

function initializeThemeSystem() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('ai-dev-lab-theme') || 'light';
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme
    const theme = savedTheme === 'auto' ? (prefersDark ? 'dark' : 'light') : savedTheme;
    setTheme(theme);
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (localStorage.getItem('ai-dev-lab-theme') === 'auto') {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    window.appState.theme = theme;
    
    // Update theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '🌙' : '☀️';
    }
    
    // Save theme preference
    localStorage.setItem('ai-dev-lab-theme', theme);
    
    console.log(`🎨 Theme set to: ${theme}`);
}

function initializePerformanceMonitoring() {
    // Monitor long tasks
    if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.duration > 50) {
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
        
        console.log('📊 Event tracked:', event);
        
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
    
    // Load saved API key
    const savedKey = localStorage.getItem('ai-dev-lab-gemini-api-key');
    if (savedKey) {
        updateAPIKeyDisplay(savedKey, true);
    }
    
    // Add event listeners for API key toggle
    const toggleBtn = document.getElementById('toggle-api-key');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleAPIKeyVisibility);
    }
    
    console.log('✅ API key features initialized');
}

function updateAPIKeyDisplay(apiKey, isVisible = false) {
    const displayElement = document.getElementById('api-key-display');
    if (displayElement) {
        if (isVisible) {
            displayElement.textContent = apiKey.substring(0, 8) + '...' + apiKey.substring(apiKey.length - 4);
            displayElement.classList.add('visible');
        } else {
            displayElement.textContent = '••••••••••••••••';
            displayElement.classList.remove('visible');
        }
    }
}

function toggleAPIKeyVisibility() {
    const displayElement = document.getElementById('api-key-display');
    const toggleBtn = document.getElementById('toggle-api-key');
    
    if (displayElement && toggleBtn) {
        const savedKey = localStorage.getItem('ai-dev-lab-gemini-api-key');
        if (savedKey) {
            const isCurrentlyVisible = displayElement.classList.contains('visible');
            updateAPIKeyDisplay(savedKey, !isCurrentlyVisible);
            
            // Update button text
            toggleBtn.textContent = isCurrentlyVisible ? '👁️' : '🙈';
        }
    }
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
