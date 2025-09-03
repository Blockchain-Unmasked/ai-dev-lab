/**
 * Professional Chat Agent for AI/DEV Lab Customer Support Demo
 * Enhanced with dual-mode interface, toggle switches, and professional features
 */

class ChatAgent {
    constructor() {
        this.messages = [];
        this.qaMessages = [];
        this.isConnected = false;
        this.modes = {
            qa: false,
            ai: true,
            stealth: true
        };
        
        this.metrics = {
            responseTime: 0,
            qualityScore: 0,
            escalations: 0,
            queueLength: 0,
            agentAvailable: 2,
            agentBusy: 0,
            agentOffline: 0
        };
        
        this.initialize();
    }

    initialize() {
        this.bindEvents();
        this.setupToggleSwitches();
        this.addWelcomeMessage();
        this.updateMetrics();
        this.startMetricsUpdate();
        
        // Initialize API key display after a short delay to ensure geminiAPI is loaded
        setTimeout(() => {
            this.updateApiKeyDisplay();
        }, 100);
    }

    setupToggleSwitches() {
        // Initialize toggle switches with proper event handling
        this.qaToggle = document.getElementById('qa-mode-toggle');
        this.aiToggle = document.getElementById('ai-mode-toggle');
        this.stealthToggle = document.getElementById('stealth-mode-toggle');
        
        if (this.qaToggle) {
            this.qaToggle.addEventListener('toggleChange', (e) => {
                this.modes.qa = e.detail.checked;
                this.switchMode();
            });
        }
        
        if (this.aiToggle) {
            this.aiToggle.addEventListener('toggleChange', (e) => {
                this.modes.ai = e.detail.checked;
                this.updateModeDisplay();
            });
        }
        
        if (this.stealthToggle) {
            this.stealthToggle.addEventListener('toggleChange', (e) => {
                this.modes.stealth = e.detail.checked;
                this.updateModeDisplay();
            });
        }
    }

    bindEvents() {
        // Chat form
        const chatForm = document.getElementById('chat-form');
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }

        // QA Chat form
        const qaChatForm = document.getElementById('qa-chat-form');
        if (qaChatForm) {
            qaChatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendQAMessage();
            });
        }

        // Clear chat button removed for MVP - will implement proper session management later

        const qaClearChatBtn = document.getElementById('qa-clear-chat');
        if (qaClearChatBtn) {
            qaClearChatBtn.addEventListener('click', () => {
                this.clearQAChat();
            });
        }

        // Test connection button removed from chat interface

        // API Key management
        const saveApiKeyBtn = document.getElementById('save-api-key');
        const clearApiKeyBtn = document.getElementById('clear-api-key');
        const apiKeyInput = document.getElementById('api-key-input');
        
        if (saveApiKeyBtn) {
            saveApiKeyBtn.addEventListener('click', () => {
                this.saveApiKey();
            });
        }
        
        if (clearApiKeyBtn) {
            clearApiKeyBtn.addEventListener('click', () => {
                this.clearApiKey();
            });
        }
        
        if (apiKeyInput) {
            apiKeyInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.saveApiKey();
                }
            });
        }

        const qaTestAIBtn = document.getElementById('qa-test-ai');
        if (qaTestAIBtn) {
            qaTestAIBtn.addEventListener('click', () => {
                this.testAI();
            });
        }



        // New session button
        const newSessionBtn = document.getElementById('new-session');
        if (newSessionBtn) {
            newSessionBtn.addEventListener('click', () => {
                this.startNewSession();
            });
        }

        // Export and reset buttons
        const exportDataBtn = document.getElementById('export-data');
        if (exportDataBtn) {
            exportDataBtn.addEventListener('click', () => {
                this.exportData();
            });
        }

        const resetMetricsBtn = document.getElementById('reset-metrics');
        if (resetMetricsBtn) {
            resetMetricsBtn.addEventListener('click', () => {
                this.resetMetrics();
            });
        }
    }

    switchMode() {
        const customerMode = document.getElementById('customer-mode');
        const qaMode = document.getElementById('qa-mode');
        
        if (this.modes.qa) {
            // Switch to QA mode
            customerMode.classList.remove('active');
            qaMode.classList.add('active');
            
            // Update header title
            const headerTitle = document.querySelector('.header h1');
            if (headerTitle) {
                headerTitle.textContent = 'AI/DEV Lab - QA Dashboard';
            }
            
            // Update subtitle
            const subtitle = document.querySelector('.header .subtitle');
            if (subtitle) {
                subtitle.textContent = 'Quality Assurance Dashboard';
            }
            
            // Update metrics display
            this.updateMetrics();
            
            console.log('🔧 Switched to QA Mode');
        } else {
            // Switch to Customer mode
            qaMode.classList.remove('active');
            customerMode.classList.add('active');
            
            // Update header title
            const headerTitle = document.querySelector('.header h1');
            if (headerTitle) {
                headerTitle.textContent = 'AI/DEV Lab';
            }
            
            // Update subtitle
            const subtitle = document.querySelector('.header .subtitle');
            if (subtitle) {
                subtitle.textContent = 'Customer Support Demo';
            }
            
            console.log('👤 Switched to Customer Mode');
        }
    }

    addWelcomeMessage() {
        const welcomeMessage = {
            type: 'system',
            content: 'Welcome to AI/DEV Lab Customer Support! How can I help you today?',
            timestamp: new Date()
        };
        this.messages.push(welcomeMessage);
        this.displayMessage(welcomeMessage, 'customer');
        
        // Add QA welcome message
        const qaWelcomeMessage = {
            type: 'system',
            content: '🔧 QA Mode Active - Enhanced monitoring and controls available',
            timestamp: new Date()
        };
        this.qaMessages.push(qaWelcomeMessage);
        this.displayMessage(qaWelcomeMessage, 'qa');
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        // Add user message
        const userMessage = {
            type: 'customer',
            content: message,
            timestamp: new Date()
        };
        
        this.messages.push(userMessage);
        this.displayMessage(userMessage, 'customer');
        input.value = '';

        // Log user message
        console.log('👤 User message sent:', {
            message: message,
            length: message.length,
            timestamp: new Date().toISOString()
        });

        // Track the interaction
        if (window.trackEvent) {
            window.trackEvent('chat_message', {
                type: 'user_message',
                length: message.length,
                mode: 'customer'
            });
        }

        // Show typing indicator
        this.showTypingIndicator('chat-messages');

        try {
            // Get support mode from dropdown
            const supportModeSelect = document.getElementById('support-mode');
            const supportMode = supportModeSelect ? supportModeSelect.value : 'general-support';
            
            // Use enhanced AI response via backend
            const response = await fetch('http://localhost:8000/api/v1/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message,
                    support_mode: supportMode
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Log AI response details
            console.log('🤖 AI Response received:', {
                model: data.model,
                client_type: data.client_type,
                mcp_integration: data.mcp_integration,
                confidence: data.confidence,
                quality: data.quality,
                response_length: data.ai_response?.length || 0,
                isRealAI: data.mcp_integration === 'active' && data.model !== 'fallback-model'
            });
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add AI response to chat
            const aiMessage = {
                type: 'agent',
                content: data.ai_response,
                timestamp: new Date(),
                metadata: {
                    model: data.model,
                    mcp_tools_used: data.mcp_tools_used,
                    confidence: data.confidence,
                    quality: data.quality,
                    mcp_integration: data.mcp_integration,
                    client_type: data.client_type || 'legacy',
                    isRealAI: data.mcp_integration === 'active' && data.model !== 'fallback-model',
                    isEnhanced: data.client_type === 'enhanced'
                }
            };
            
            this.messages.push(aiMessage);
            this.displayMessage(aiMessage, 'customer');
            
            // Update AI status indicator
            this.updateAIStatus(data);

            // Track the AI response
            if (window.trackEvent) {
                window.trackEvent('ai_response', {
                    model: data.model,
                    client_type: data.client_type,
                    mcp_integration: data.mcp_integration,
                    confidence: data.confidence,
                    quality: data.quality,
                    response_length: data.ai_response?.length || 0,
                    isRealAI: data.mcp_integration === 'active' && data.model !== 'fallback-model'
                });
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            
            // Fallback to simulated response
            this.simulateAIResponse(message, 'customer');
        }
    }

    sendQAMessage() {
        const input = document.getElementById('qa-chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        // Add user message
        const userMessage = {
            type: 'user',
            content: message,
            timestamp: new Date()
        };
        
        this.qaMessages.push(userMessage);
        this.displayMessage(userMessage, 'qa');
        input.value = '';

        // Simulate AI response with enhanced QA features
        this.simulateAIResponse(message, 'qa');
    }

    simulateAIResponse(userMessage, mode) {
        const isQAMode = mode === 'qa';
        const chatMessagesId = isQAMode ? 'qa-chat-messages' : 'chat-messages';
        const messages = isQAMode ? this.qaMessages : this.messages;
        
        // Show typing indicator
        const typingIndicator = this.showTypingIndicator(chatMessagesId);
        
        // Simulate response delay (stealth mode)
        const delay = this.modes.stealth ? Math.random() * 2000 + 1000 : 500;
        
        setTimeout(() => {
            this.hideTypingIndicator(typingIndicator);
            
            // Generate response based on user message
            const response = this.generateResponse(userMessage, isQAMode);
            
            const aiMessage = {
                type: 'agent',
                content: response.content,
                timestamp: new Date(),
                confidence: response.confidence,
                metadata: response.metadata
            };
            
            messages.push(aiMessage);
            this.displayMessage(aiMessage, mode);
            
            // Update metrics
            this.updateResponseMetrics(response);
        }, delay);
    }

    generateResponse(userMessage, isQAMode) {
        const lowerMessage = userMessage.toLowerCase();
        
        // Enhanced response logic with confidence scores
        let response = {
            content: "I understand your question. Let me help you with that.",
            confidence: 0.7,
            metadata: {
                responseType: 'general',
                keywords: [],
                suggestedActions: []
            }
        };
        
        if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
            response = {
                content: "Hello! I'm here to help you with any questions or support you might need. What can I assist you with today?",
                confidence: 0.95,
                metadata: {
                    responseType: 'greeting',
                    keywords: ['hello', 'hi'],
                    suggestedActions: ['ask_question', 'request_support']
                }
            };
        } else if (lowerMessage.includes('help') || lowerMessage.includes('support')) {
            response = {
                content: "I'm here to help! I can assist with general inquiries, technical questions, or connect you with the right resources. What specific help do you need?",
                confidence: 0.9,
                metadata: {
                    responseType: 'support_offer',
                    keywords: ['help', 'support'],
                    suggestedActions: ['describe_issue', 'request_technical_support']
                }
            };
        } else if (lowerMessage.includes('ai') || lowerMessage.includes('artificial intelligence')) {
            response = {
                content: "Yes, I'm an AI-powered support agent! I'm designed to help answer questions and provide assistance. I'm constantly learning and improving to better serve our customers.",
                confidence: 0.85,
                metadata: {
                    responseType: 'ai_explanation',
                    keywords: ['ai', 'artificial intelligence'],
                    suggestedActions: ['ask_ai_capabilities', 'request_human_agent']
                }
            };
        } else if (lowerMessage.includes('thank')) {
            response = {
                content: "You're very welcome! I'm glad I could help. Is there anything else you'd like to know or discuss?",
                confidence: 0.9,
                metadata: {
                    responseType: 'gratitude_response',
                    keywords: ['thank', 'thanks'],
                    suggestedActions: ['continue_conversation', 'end_session']
                }
            };
        } else if (lowerMessage.includes('bye') || lowerMessage.includes('goodbye')) {
            response = {
                content: "Goodbye! Thank you for chatting with me. Have a great day, and feel free to return if you need any more assistance!",
                confidence: 0.95,
                metadata: {
                    responseType: 'farewell',
                    keywords: ['bye', 'goodbye'],
                    suggestedActions: ['end_session', 'provide_feedback']
                }
            };
        } else {
            // Default responses with varying confidence
            const responses = [
                {
                    content: "That's an interesting question! Let me help you with that.",
                    confidence: 0.75
                },
                {
                    content: "I understand what you're asking about. Here's what I can tell you...",
                    confidence: 0.8
                },
                {
                    content: "Great question! I'd be happy to help you with that.",
                    confidence: 0.85
                },
                {
                    content: "I see what you're looking for. Let me provide some information on that topic.",
                    confidence: 0.8
                },
                {
                    content: "That's a good point! Here's what I know about that...",
                    confidence: 0.75
                }
            ];
            
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            response = {
                content: randomResponse.content,
                confidence: randomResponse.confidence,
                metadata: {
                    responseType: 'general_assistance',
                    keywords: [],
                    suggestedActions: ['ask_follow_up', 'request_more_details']
                }
            };
        }
        
        // Add QA-specific metadata if in QA mode
        if (isQAMode) {
            response.metadata.qaMode = true;
            response.metadata.responseQuality = this.calculateResponseQuality(response);
        }
        
        return response;
    }

    calculateResponseQuality(response) {
        // Simple quality calculation based on confidence and content length
        let quality = response.confidence * 100;
        
        if (response.content.length > 100) quality += 10;
        if (response.metadata.keywords.length > 0) quality += 5;
        if (response.metadata.suggestedActions.length > 0) quality += 5;
        
        return Math.min(100, Math.round(quality));
    }

    displayMessage(message, mode) {
        const chatMessagesId = mode === 'qa' ? 'qa-chat-messages' : 'chat-messages';
        const chatMessages = document.getElementById(chatMessagesId);
        
        if (!chatMessages) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${message.type}`;
        
        // Determine message type and avatar
        let messageType = message.type;
        let avatarText = '';
        let avatarClass = '';
        
        if (message.type === 'customer' || message.type === 'user') {
            messageType = 'user';
            avatarText = 'U';
            avatarClass = 'user';
        } else if (message.type === 'agent' || message.type === 'ai') {
            messageType = 'agent';
            avatarText = 'AI';
            avatarClass = 'agent';
        } else if (message.type === 'system') {
            messageType = 'system';
            avatarText = 'S';
            avatarClass = 'system';
        }
        
        let content = `
            <div class="message-avatar ${avatarClass}">${avatarText}</div>
            <div class="message-bubble ${messageType}">
                <div class="message-content">${message.content}</div>
        `;
        
        // Add metadata information if available
        if (message.metadata) {
            if (message.confidence) {
                content += `<div class="message-meta"><small>Confidence: ${(message.confidence * 100).toFixed(1)}%</small></div>`;
            }
            if (message.metadata.quality) {
                content += `<div class="message-meta"><small>Quality: ${(message.metadata.quality * 100).toFixed(1)}%</small></div>`;
            }
            if (message.metadata.model) {
                content += `<div class="message-meta"><small>Model: ${message.metadata.model}</small></div>`;
            }
            if (message.metadata.isRealAI !== undefined) {
                const aiStatus = message.metadata.isRealAI ? '🤖 Real AI' : '⚠️ Fallback';
                content += `<div class="message-meta"><small>${aiStatus}</small></div>`;
            }
        }
        
        content += '</div>';
        messageElement.innerHTML = content;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        // Wait for DOM to be ready if needed
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.showTypingIndicator());
            return;
        }
        
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) {
            console.error('Chat messages container not found. Available elements:', 
                Array.from(document.querySelectorAll('[id*="chat"]')).map(el => el.id));
            return;
        }
        
        // Remove existing typing indicator
        this.hideTypingIndicator();
        
        const typingElement = document.createElement('div');
        typingElement.id = 'typing-indicator';
        typingElement.className = 'message agent typing-indicator';
        
        const content = `
            <div class="message-avatar agent">AI</div>
            <div class="message-bubble agent">
                <div class="message-content">AI is thinking...</div>
            </div>
        `;
        
        typingElement.innerHTML = content;
        chatMessages.appendChild(typingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    updateAIStatus(data) {
        // Update the model status indicator in the config panel
        const modelStatus = document.querySelector('.model-status');
        if (modelStatus && data) {
            if (data.mcp_integration === 'active' && data.model !== 'fallback-model') {
                modelStatus.textContent = '🤖 AI Active';
                modelStatus.className = 'model-status ready';
            } else {
                modelStatus.textContent = '⚠️ Fallback';
                modelStatus.className = 'model-status warning';
            }
        }
    }

    showTypingIndicator(chatMessagesId) {
        const chatMessages = document.getElementById(chatMessagesId);
        if (!chatMessages) {
            console.error('Chat messages container not found for ID:', chatMessagesId);
            return null;
        }
        
        const typingElement = document.createElement('div');
        typingElement.className = 'message agent-message typing-indicator';
        typingElement.innerHTML = `
            <div class="message-content">
                <p>AI is typing<span class="dots">...</span></p>
            </div>
        `;
        
        chatMessages.appendChild(typingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return typingElement;
    }

    hideTypingIndicator(typingElement) {
        if (typingElement && typingElement.parentNode) {
            typingElement.parentNode.removeChild(typingElement);
        }
    }

    clearChat() {
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.innerHTML = '';
        }
        this.messages = [];
        this.addWelcomeMessage();
    }

    clearQAChat() {
        const qaChatMessages = document.getElementById('qa-chat-messages');
        if (qaChatMessages) {
            qaChatMessages.innerHTML = '';
        }
        this.qaMessages = [];
        this.addWelcomeMessage();
    }

    async testConnection() {
        try {
            // Check if Gemini API is available
            if (!window.geminiAPI) {
                throw new Error('Gemini API not loaded');
            }
            
            // Test the actual Gemini API connection
            const result = await window.geminiAPI.testConnection();
            
            if (result.success) {
                // Show success message
                this.showNotification('API connection successful!', 'success');
            } else {
                throw new Error(result.error || 'Connection test failed');
            }
            
        } catch (error) {
            console.error('Connection test failed:', error);
            
            // Show error message
            this.showNotification(`Connection failed: ${error.message}`, 'error');
        }
    }

    testAI() {
        const button = document.getElementById('qa-test-ai');
        const originalText = button.textContent;
        
        button.textContent = 'Testing AI...';
        button.disabled = true;
        
        // Simulate AI test
        setTimeout(() => {
            button.textContent = 'AI Active!';
            button.style.background = 'var(--success-500)';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
                button.style.background = '';
            }, 2000);
        }, 1500);
    }

    updateModeDisplay() {
        console.log('Modes updated:', this.modes);
        
        // Update visual indicators based on modes
        if (this.aiToggle) {
            if (this.modes.ai) {
                this.aiToggle.classList.add('success');
            } else {
                this.aiToggle.classList.remove('success');
            }
        }
        
        if (this.stealthToggle) {
            if (this.modes.stealth) {
                this.stealthToggle.classList.add('info');
            } else {
                this.stealthToggle.classList.remove('info');
            }
        }
    }

    updateResponseMetrics(response) {
        // Update response time
        this.metrics.responseTime = Math.round(Math.random() * 3 + 1);
        
        // Update quality score
        if (response.metadata.responseQuality) {
            this.metrics.qualityScore = response.metadata.responseQuality;
        }
        
        // Random escalation (for demo purposes)
        if (Math.random() < 0.1) {
            this.metrics.escalations++;
        }
        
        this.updateMetrics();
    }

    updateMetrics() {
        // Update queue metrics
        const queueWaiting = document.getElementById('queue-waiting');
        if (queueWaiting) {
            queueWaiting.textContent = this.metrics.queueLength;
        }
        
        const queueActive = document.getElementById('queue-active');
        if (queueActive) {
            queueActive.textContent = this.metrics.queueLength > 0 ? 1 : 0;
        }
        
        const queueAvgWait = document.getElementById('queue-avg-wait');
        if (queueAvgWait) {
            queueAvgWait.textContent = `${this.metrics.responseTime}s`;
        }
        
        // Update agent metrics
        const agentAvailable = document.getElementById('agent-available');
        if (agentAvailable) {
            agentAvailable.textContent = this.metrics.agentAvailable;
        }
        
        const agentBusy = document.getElementById('agent-busy');
        if (agentBusy) {
            agentBusy.textContent = this.metrics.agentBusy;
        }
        
        const agentOffline = document.getElementById('agent-offline');
        if (agentOffline) {
            agentOffline.textContent = this.metrics.agentOffline;
        }
        
        // Update performance metrics
        const perfResponseTime = document.getElementById('perf-response-time');
        if (perfResponseTime) {
            perfResponseTime.textContent = `${this.metrics.responseTime}s`;
        }
        
        const perfQualityScore = document.getElementById('perf-quality-score');
        if (perfQualityScore) {
            perfQualityScore.textContent = this.metrics.qualityScore > 0 ? `${this.metrics.qualityScore}/100` : '-';
        }
        
        const perfEscalations = document.getElementById('perf-escalations');
        if (perfEscalations) {
            perfEscalations.textContent = this.metrics.escalations;
        }
    }

    startMetricsUpdate() {
        // Simulate real-time metrics updates
        setInterval(() => {
            // Random queue changes
            if (Math.random() < 0.3) {
                this.metrics.queueLength = Math.max(0, this.metrics.queueLength + (Math.random() < 0.5 ? 1 : -1));
            }
            
            // Random agent status changes
            if (Math.random() < 0.2) {
                const totalAgents = this.metrics.agentAvailable + this.metrics.agentBusy + this.metrics.agentOffline;
                this.metrics.agentAvailable = Math.floor(Math.random() * totalAgents);
                this.metrics.agentBusy = Math.floor(Math.random() * (totalAgents - this.metrics.agentAvailable));
                this.metrics.agentOffline = totalAgents - this.metrics.agentAvailable - this.metrics.agentBusy;
            }
            
            this.updateMetrics();
        }, 5000);
    }



    startNewSession() {
        this.clearChat();
        this.clearQAChat();
        
        // Show session started message
        const sessionMessage = {
            type: 'system',
            content: '🆕 New session started. How can I help you today?',
            timestamp: new Date()
        };
        
        this.messages.push(sessionMessage);
        this.displayMessage(sessionMessage, 'customer');
        
        const qaSessionMessage = {
            type: 'system',
            content: '🆕 New QA session started. Enhanced monitoring active.',
            timestamp: new Date()
        };
        
        this.qaMessages.push(qaSessionMessage);
        this.displayMessage(qaSessionMessage, 'qa');
        
        // Reset metrics
        this.resetMetrics();
    }

    exportData() {
        const data = {
            timestamp: new Date().toISOString(),
            modes: this.modes,
            metrics: this.metrics,
            customerMessages: this.messages.length,
            qaMessages: this.qaMessages.length
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ai-dev-lab-data-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        console.log('📊 Data exported successfully');
    }

    resetMetrics() {
        this.metrics = {
            responseTime: 0,
            qualityScore: 0,
            escalations: 0,
            queueLength: 0,
            agentAvailable: 2,
            agentBusy: 0,
            agentOffline: 0
        };
        
        this.updateMetrics();
        console.log('🔄 Metrics reset successfully');
    }

    /**
     * Save API key
     */
    saveApiKey() {
        const apiKeyInput = document.getElementById('api-key-input');
        const apiKeyStatus = document.getElementById('api-key-status');
        
        if (!apiKeyInput) return;
        
        const apiKey = apiKeyInput.value.trim();
        
        if (!apiKey) {
            this.showNotification('Please enter an API key', 'error');
            return;
        }
        
        // Validate API key format
        if (!window.geminiAPI || !window.geminiAPI.validateApiKey(apiKey)) {
            this.showNotification('Invalid API key format', 'error');
            return;
        }
        
        // Set the API key
        if (window.geminiAPI.setApiKey(apiKey)) {
            // Save to localStorage
            const config = {
                apiKey: apiKey,
                model: window.geminiAPI.model || 'gemini-1.5-pro',
                temperature: window.geminiAPI.temperature || 0.7
            };
            localStorage.setItem('ai-dev-lab-config', JSON.stringify(config));
            
            // Update UI
            apiKeyInput.value = '';
            apiKeyStatus.textContent = 'API key saved successfully';
            apiKeyStatus.style.color = '#10b981';
            
            this.showNotification('API key saved successfully!', 'success');
            
            // Update the API key display
            this.updateApiKeyDisplay();
        } else {
            this.showNotification('Failed to save API key', 'error');
        }
    }
    
    /**
     * Clear API key
     */
    clearApiKey() {
        const apiKeyInput = document.getElementById('api-key-input');
        const apiKeyStatus = document.getElementById('api-key-status');
        
        if (window.geminiAPI) {
            window.geminiAPI.clearApiKey();
        }
        
        // Clear from localStorage
        localStorage.removeItem('ai-dev-lab-config');
        
        // Update UI
        if (apiKeyInput) apiKeyInput.value = '';
        if (apiKeyStatus) {
            apiKeyStatus.textContent = 'No API key configured';
            apiKeyStatus.style.color = '#6b7280';
        }
        
        this.showNotification('API key cleared', 'info');
        this.updateApiKeyDisplay();
    }
    
    /**
     * Update API key display
     */
    updateApiKeyDisplay() {
        const apiKeyStatus = document.getElementById('api-key-status');
        
        if (window.geminiAPI && window.geminiAPI.isConfigured()) {
            if (apiKeyStatus) {
                apiKeyStatus.textContent = 'API key configured';
                apiKeyStatus.style.color = '#10b981';
            }
        } else {
            if (apiKeyStatus) {
                apiKeyStatus.textContent = 'No API key configured';
                apiKeyStatus.style.color = '#6b7280';
            }
        }
    }

    /**
     * Show notification message
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        // Set background color based on type
        switch (type) {
            case 'success':
                notification.style.background = '#10b981';
                break;
            case 'error':
                notification.style.background = '#ef4444';
                break;
            case 'warning':
                notification.style.background = '#f59e0b';
                break;
            default:
                notification.style.background = '#3b82f6';
        }
        
        // Add to page
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto-remove after 4 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }
}

// Initialize chat agent when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatAgent = new ChatAgent();
});
