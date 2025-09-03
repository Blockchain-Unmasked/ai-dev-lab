/**
 * Generic Chat Interface for AI/DEV Lab
 * Works with any prompt system configuration
 */

class GenericChat {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            showProgress: true,
            showStatus: true,
            showModeSelector: true,
            ...options
        };
        
        this.promptSystem = new PromptSystem();
        this.messages = [];
        this.isTyping = false;
        
        this.initialize();
    }

    initialize() {
        this.createChatInterface();
        this.bindEvents();
        this.setDefaultPrompt();
    }

    /**
     * Create the chat interface HTML
     */
    createChatInterface() {
        this.container.innerHTML = `
            <div class="generic-chat-container">
                ${this.options.showModeSelector ? this.createModeSelector() : ''}
                ${this.options.showProgress ? this.createProgressBar() : ''}
                <div class="chat-messages" id="chat-messages"></div>
                ${this.options.showStatus ? this.createStatusPanel() : ''}
                <div class="chat-input-container">
                    <form class="chat-form" id="chat-form">
                        <input type="text" class="chat-input" id="chat-input" placeholder="Type your message..." required>
                        <button type="submit" class="btn btn-primary" id="send-btn">Send</button>
                    </form>
                </div>
            </div>
        `;

        // Add CSS styles
        this.addStyles();
    }

    /**
     * Create mode selector
     */
    createModeSelector() {
        return `
            <div class="mode-selector">
                <label for="prompt-mode">Support Mode:</label>
                <select id="prompt-mode" class="prompt-mode-select">
                    <option value="">Select a mode...</option>
                </select>
            </div>
        `;
    }

    /**
     * Create progress bar
     */
    createProgressBar() {
        return `
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
                <div class="progress-text" id="progress-text">Step 1 of 5</div>
            </div>
        `;
    }

    /**
     * Create status panel
     */
    createStatusPanel() {
        return `
            <div class="status-panel">
                <div class="status-item">
                    <span>Mode:</span>
                    <span class="status-value" id="active-mode">None</span>
                </div>
                <div class="status-item">
                    <span>Messages:</span>
                    <span class="status-value" id="message-count">0</span>
                </div>
                <div class="status-item">
                    <span>Status:</span>
                    <span class="status-value" id="conversation-status">incomplete</span>
                </div>
            </div>
        `;
    }

    /**
     * Add CSS styles
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .generic-chat-container {
                display: flex;
                flex-direction: column;
                height: 100%;
                background: white;
                border-radius: 8px;
                overflow: hidden;
            }
            
            .mode-selector {
                padding: 1rem;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }
            
            .mode-selector label {
                font-weight: 600;
                margin-right: 0.5rem;
            }
            
            .prompt-mode-select {
                padding: 0.5rem;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background: white;
            }
            
            .progress-container {
                padding: 1rem;
                background: #e9ecef;
                border-bottom: 1px solid #dee2e6;
            }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background: #dee2e6;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 0.5rem;
            }
            
            .progress-fill {
                height: 100%;
                background: #007bff;
                transition: width 0.3s ease;
                width: 20%;
            }
            
            .progress-text {
                font-size: 0.875rem;
                color: #6c757d;
                text-align: center;
            }
            
            .chat-messages {
                flex: 1;
                padding: 1rem;
                overflow-y: auto;
                background: #f8f9fa;
            }
            
            .message {
                margin-bottom: 1rem;
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
            }
            
            .message.user {
                flex-direction: row-reverse;
            }
            
            .message-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                font-size: 0.875rem;
                flex-shrink: 0;
            }
            
            .message.ai .message-avatar {
                background: #007bff;
                color: white;
            }
            
            .message.user .message-avatar {
                background: #6c757d;
                color: white;
            }
            
            .message-content {
                max-width: 70%;
                padding: 0.75rem 1rem;
                border-radius: 1rem;
                font-size: 0.9rem;
                line-height: 1.5;
            }
            
            .message.ai .message-content {
                background: white;
                border: 1px solid #dee2e6;
                color: #495057;
            }
            
            .message.user .message-content {
                background: #007bff;
                color: white;
            }
            
            .message-time {
                font-size: 0.75rem;
                opacity: 0.6;
                margin-top: 0.25rem;
            }
            
            .status-panel {
                padding: 1rem;
                background: #f8f9fa;
                border-top: 1px solid #dee2e6;
                display: flex;
                justify-content: space-between;
                font-size: 0.875rem;
            }
            
            .status-item {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .status-value {
                font-weight: 600;
                color: #007bff;
            }
            
            .chat-input-container {
                padding: 1rem;
                background: white;
                border-top: 1px solid #dee2e6;
            }
            
            .chat-form {
                display: flex;
                gap: 0.75rem;
            }
            
            .chat-input {
                flex: 1;
                padding: 0.75rem 1rem;
                border: 1px solid #ced4da;
                border-radius: 0.5rem;
                font-size: 0.9rem;
                outline: none;
            }
            
            .chat-input:focus {
                border-color: #007bff;
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
            }
            
            .btn {
                padding: 0.75rem 1.5rem;
                border: none;
                border-radius: 0.5rem;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.2s;
            }
            
            .btn-primary {
                background: #007bff;
                color: white;
            }
            
            .btn-primary:hover {
                background: #0056b3;
            }
            
            .btn-primary:disabled {
                background: #6c757d;
                cursor: not-allowed;
            }
            
            .typing-indicator {
                display: none;
                align-items: center;
                gap: 0.5rem;
                color: #6c757d;
                font-size: 0.875rem;
                margin: 0.5rem 0;
            }
            
            .typing-dots {
                display: flex;
                gap: 0.25rem;
            }
            
            .typing-dot {
                width: 6px;
                height: 6px;
                background: #6c757d;
                border-radius: 50%;
                animation: typing 1.4s infinite ease-in-out;
            }
            
            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes typing {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
            }
            
            .escalation-message {
                background: #d1fae5;
                border: 1px solid #10b981;
                color: #065f46;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
                text-align: center;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Chat form submission
        const form = document.getElementById('chat-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Mode selector change
        const modeSelect = document.getElementById('prompt-mode');
        if (modeSelect) {
            modeSelect.addEventListener('change', (e) => {
                this.setPromptMode(e.target.value);
            });
        }

        // Enter key handling
        const input = document.getElementById('chat-input');
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    /**
     * Set default prompt mode
     */
    setDefaultPrompt() {
        // Load available prompts
        const availablePrompts = this.promptSystem.getAvailablePrompts();
        const modeSelect = document.getElementById('prompt-mode');
        
        if (modeSelect) {
            availablePrompts.forEach(prompt => {
                const option = document.createElement('option');
                option.value = prompt.id;
                option.textContent = prompt.name;
                modeSelect.appendChild(option);
            });
        }
    }

    /**
     * Set prompt mode
     */
    setPromptMode(promptId) {
        if (this.promptSystem.setActivePrompt(promptId)) {
            this.clearMessages();
            this.showInitialMessages();
            this.updateStatus();
        }
    }

    /**
     * Show initial messages for the active prompt
     */
    showInitialMessages() {
        const messages = this.promptSystem.getNextMessages();
        messages.forEach((message, index) => {
            setTimeout(() => {
                this.addMessage(message, 'ai');
            }, index * 1000);
        });
    }

    /**
     * Send message
     */
    sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        
        // Process message
        const result = this.promptSystem.processUserMessage(message);
        
        if (result.success) {
            // Show extracted information if any
            if (Object.keys(result.extracted).length > 0) {
                this.addMessage(`✅ Information recorded: ${JSON.stringify(result.extracted, null, 2)}`, 'ai');
            }
            
            // Check if should escalate
            if (result.shouldEscalate) {
                this.escalateConversation();
            } else {
                // Show next messages
                this.showNextMessages();
            }
        } else {
            this.addMessage(`❌ Error: ${result.error}`, 'ai');
        }
        
        // Clear input
        input.value = '';
        this.updateStatus();
    }

    /**
     * Show next messages
     */
    showNextMessages() {
        const messages = this.promptSystem.getNextMessages();
        if (messages.length > 0) {
            this.showTyping();
            setTimeout(() => {
                this.hideTyping();
                messages.forEach((message, index) => {
                    setTimeout(() => {
                        this.addMessage(message, 'ai');
                    }, index * 1000);
                });
            }, 1000 + Math.random() * 2000);
        }
    }

    /**
     * Escalate conversation
     */
    escalateConversation() {
        const escalationMessage = this.promptSystem.getEscalationMessage();
        this.addMessage(`
            <div class="escalation-message">
                <h3>🎉 ${escalationMessage}</h3>
                <p>Your case has been submitted and will be reviewed by our team.</p>
            </div>
        `, 'ai', false);
    }

    /**
     * Add message to chat
     */
    addMessage(content, type = 'ai', showTime = true) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = type === 'ai' ? 'AI' : 'You';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = content;
        
        if (showTime) {
            const timeDiv = document.createElement('div');
            timeDiv.className = 'message-time';
            timeDiv.textContent = 'Just now';
            messageContent.appendChild(timeDiv);
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        this.messages.push({ content, type, timestamp: new Date() });
    }

    /**
     * Show typing indicator
     */
    showTyping() {
        const messagesContainer = document.getElementById('chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <span>AI is typing</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        this.isTyping = true;
    }

    /**
     * Hide typing indicator
     */
    hideTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        this.isTyping = false;
    }

    /**
     * Update status panel
     */
    updateStatus() {
        const status = this.promptSystem.getConversationStatus();
        
        // Update status elements
        const activeMode = document.getElementById('active-mode');
        const messageCount = document.getElementById('message-count');
        const conversationStatus = document.getElementById('conversation-status');
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');
        
        if (activeMode) activeMode.textContent = status.activePrompt;
        if (messageCount) messageCount.textContent = status.messageCount;
        if (conversationStatus) conversationStatus.textContent = status.status;
        
        if (progressFill && progressText) {
            const activePrompt = this.promptSystem.getActivePrompt();
            if (activePrompt) {
                const totalSteps = activePrompt.conversation_flow.length;
                const progress = (status.currentStep / totalSteps) * 100;
                progressFill.style.width = `${progress}%`;
                progressText.textContent = `Step ${status.currentStep} of ${totalSteps}`;
            }
        }
    }

    /**
     * Clear messages
     */
    clearMessages() {
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = '';
        this.messages = [];
    }

    /**
     * Reset conversation
     */
    resetConversation() {
        this.promptSystem.resetConversationState();
        this.clearMessages();
        this.showInitialMessages();
        this.updateStatus();
    }
}

// Export for use in other modules
window.GenericChat = GenericChat;
