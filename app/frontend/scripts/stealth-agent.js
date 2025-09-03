/**
 * Stealth Agent Module for AI Intake/Support Agent Demo
 * Simulates human response timing and behavior patterns
 */

class StealthAgent {
    constructor() {
        this.typingIndicators = new Map(); // sessionId -> typing state
        this.responseDelays = new Map(); // sessionId -> delay configuration
        this.humanBehaviorProfiles = new Map(); // agentId -> behavior profile
        this.typingSpeed = 150; // ms per character (adjustable)
        this.minResponseDelay = 1000; // minimum delay before response (1 second)
        this.maxResponseDelay = 8000; // maximum delay before response (8 seconds)
        
        this.init();
    }

    init() {
        this.initializeHumanBehaviorProfiles();
        this.setupEventListeners();
    }

    /**
     * Initialize human behavior profiles for different agent types
     */
    initializeHumanBehaviorProfiles() {
        // Tier 1 Agent Profile (Entry Level)
        this.humanBehaviorProfiles.set('tier1', {
            typingSpeed: 120, // Slightly slower typing
            minResponseDelay: 1500, // 1.5 seconds minimum
            maxResponseDelay: 6000, // 6 seconds maximum
            typingVariability: 0.3, // 30% variability in typing speed
            responsePatterns: {
                greeting: { delay: 2000, typingDuration: 3000 },
                simple_answer: { delay: 1500, typingDuration: 2000 },
                complex_answer: { delay: 3000, typingDuration: 5000 },
                escalation: { delay: 4000, typingDuration: 4000 }
            },
            personality: {
                formality: 'professional',
                emojiUsage: 'minimal',
                responseLength: 'concise'
            }
        });

        // Tier 2 Agent Profile (Intermediate)
        this.humanBehaviorProfiles.set('tier2', {
            typingSpeed: 140, // Moderate typing speed
            minResponseDelay: 1200, // 1.2 seconds minimum
            maxResponseDelay: 7000, // 7 seconds maximum
            typingVariability: 0.25, // 25% variability
            responsePatterns: {
                greeting: { delay: 1800, typingDuration: 2800 },
                simple_answer: { delay: 1200, typingDuration: 1800 },
                complex_answer: { delay: 2500, typingDuration: 4500 },
                escalation: { delay: 3500, typingDuration: 3800 }
            },
            personality: {
                formality: 'friendly_professional',
                emojiUsage: 'moderate',
                responseLength: 'detailed'
            }
        });

        // Tier 3 Agent Profile (Senior/Expert)
        this.humanBehaviorProfiles.set('tier3', {
            typingSpeed: 160, // Faster typing (experienced)
            minResponseDelay: 1000, // 1 second minimum
            maxResponseDelay: 5000, // 5 seconds maximum
            typingVariability: 0.2, // 20% variability
            responsePatterns: {
                greeting: { delay: 1500, typingDuration: 2500 },
                simple_answer: { delay: 1000, typingDuration: 1500 },
                complex_answer: { delay: 2000, typingDuration: 4000 },
                escalation: { delay: 3000, typingDuration: 3500 }
            },
            personality: {
                formality: 'expert_friendly',
                emojiUsage: 'appropriate',
                responseLength: 'comprehensive'
            }
        });

        // Manager Profile
        this.humanBehaviorProfiles.set('manager', {
            typingSpeed: 180, // Very fast typing
            minResponseDelay: 800, // 0.8 seconds minimum
            maxResponseDelay: 4000, // 4 seconds maximum
            typingVariability: 0.15, // 15% variability
            responsePatterns: {
                greeting: { delay: 1200, typingDuration: 2000 },
                simple_answer: { delay: 800, typingDuration: 1200 },
                complex_answer: { delay: 1500, typingDuration: 3000 },
                escalation: { delay: 2000, typingDuration: 2500 }
            },
            personality: {
                formality: 'executive_professional',
                emojiUsage: 'minimal',
                responseLength: 'precise'
            }
        });
    }

    setupEventListeners() {
        // Listen for stealth mode activation
        document.addEventListener('stealthModeActivated', (e) => {
            this.activateStealthMode(e.detail.sessionId, e.detail.agentId);
        });

        // Listen for response generation requests
        document.addEventListener('stealthResponseRequested', (e) => {
            this.generateStealthResponse(e.detail);
        });

        // Listen for typing indicator requests
        document.addEventListener('typingIndicatorRequested', (e) => {
            this.showTypingIndicator(e.detail.sessionId, e.detail.agentId);
        });
    }

    /**
     * Activate stealth mode for a session
     */
    activateStealthMode(sessionId, agentId) {
        const agentTier = this.getAgentTier(agentId);
        const behaviorProfile = this.humanBehaviorProfiles.get(agentTier) || this.humanBehaviorProfiles.get('tier1');
        
        this.responseDelays.set(sessionId, {
            agentId: agentId,
            agentTier: agentTier,
            behaviorProfile: behaviorProfile,
            lastResponseTime: Date.now(),
            responseCount: 0
        });

        // Dispatch event
        this.dispatchEvent('stealthModeActivated', { sessionId, agentId, agentTier });
    }

    /**
     * Get agent tier from agent ID
     */
    getAgentTier(agentId) {
        // Extract tier from agent ID or get from tiered agent system
        if (window.tieredAgentSystem) {
            const agent = window.tieredAgentSystem.getAgent(agentId);
            if (agent) {
                return `tier${agent.tier}`;
            }
        }
        
        // Default to tier 1 if can't determine
        return 'tier1';
    }

    /**
     * Generate stealth response with human-like timing
     */
    async generateStealthResponse(detail) {
        const { sessionId, message, responseType, content } = detail;
        const delayConfig = this.responseDelays.get(sessionId);
        
        if (!delayConfig) {
            console.warn('No stealth mode configuration found for session:', sessionId);
            return;
        }

        const behaviorProfile = delayConfig.behaviorProfile;
        const responsePattern = behaviorProfile.responsePatterns[responseType] || behaviorProfile.responsePatterns.simple_answer;

        // Calculate realistic delays
        const responseDelay = this.calculateResponseDelay(behaviorProfile, responsePattern, delayConfig);
        const typingDuration = this.calculateTypingDuration(content, behaviorProfile, responsePattern);

        // Show typing indicator
        this.showTypingIndicator(sessionId, delayConfig.agentId, typingDuration);

        // Wait for response delay
        await this.delay(responseDelay);

        // Simulate typing
        await this.simulateTyping(content, typingDuration, sessionId);

        // Hide typing indicator
        this.hideTypingIndicator(sessionId);

        // Generate final response with human-like characteristics
        const stealthResponse = this.applyHumanCharacteristics(content, behaviorProfile);

        // Update response tracking
        delayConfig.lastResponseTime = Date.now();
        delayConfig.responseCount++;

        // Dispatch response ready event
        this.dispatchEvent('stealthResponseReady', {
            sessionId,
            agentId: delayConfig.agentId,
            content: stealthResponse,
            responseType,
            timing: {
                responseDelay,
                typingDuration,
                totalTime: responseDelay + typingDuration
            }
        });

        return stealthResponse;
    }

    /**
     * Calculate realistic response delay
     */
    calculateResponseDelay(behaviorProfile, responsePattern, delayConfig) {
        const baseDelay = responsePattern.delay;
        const variability = behaviorProfile.typingVariability;
        
        // Add some randomness based on response count (agents get faster with experience)
        const experienceFactor = Math.max(0.7, 1 - (delayConfig.responseCount * 0.05));
        
        // Add variability
        const randomFactor = 1 + (Math.random() - 0.5) * variability;
        
        // Apply experience factor
        const finalDelay = baseDelay * randomFactor * experienceFactor;
        
        // Ensure within bounds
        return Math.max(behaviorProfile.minResponseDelay, 
                       Math.min(behaviorProfile.maxResponseDelay, finalDelay));
    }

    /**
     * Calculate typing duration based on content length and agent profile
     */
    calculateTypingDuration(content, behaviorProfile, responsePattern) {
        const baseTypingDuration = responsePattern.typingDuration;
        const contentLength = content.length;
        
        // Adjust based on content length
        const lengthFactor = Math.max(0.5, Math.min(2.0, contentLength / 100));
        
        // Add some randomness
        const randomFactor = 0.8 + Math.random() * 0.4; // 0.8 to 1.2
        
        // Apply agent typing speed
        const speedFactor = 200 / behaviorProfile.typingSpeed; // Normalize to 200ms base
        
        return Math.round(baseTypingDuration * lengthFactor * randomFactor * speedFactor);
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator(sessionId, agentId, duration) {
        const typingState = {
            sessionId,
            agentId,
            startTime: Date.now(),
            duration,
            isTyping: true
        };
        
        this.typingIndicators.set(sessionId, typingState);
        
        // Create typing indicator element
        this.createTypingIndicator(sessionId, agentId);
        
        // Dispatch event
        this.dispatchEvent('typingIndicatorShown', { sessionId, agentId, duration });
    }

    /**
     * Create typing indicator UI element
     */
    createTypingIndicator(sessionId, agentId) {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;

        // Remove existing typing indicator for this session
        const existingIndicator = chatMessages.querySelector(`[data-typing-session="${sessionId}"]`);
        if (existingIndicator) {
            existingIndicator.remove();
        }

        // Create new typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message agent-message typing-indicator';
        typingDiv.setAttribute('data-typing-session', sessionId);
        typingDiv.innerHTML = `
            <div class="message-header">
                <span class="message-type">Agent (Typing...)</span>
                <span class="message-time">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="message-content">
                <div class="typing-dots">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                </div>
            </div>
        `;

        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator(sessionId) {
        const typingState = this.typingIndicators.get(sessionId);
        if (typingState) {
            typingState.isTyping = false;
        }

        // Remove typing indicator from UI
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            const typingIndicator = chatMessages.querySelector(`[data-typing-session="${sessionId}"]`);
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }

        // Dispatch event
        this.dispatchEvent('typingIndicatorHidden', { sessionId });
    }

    /**
     * Simulate realistic typing behavior
     */
    async simulateTyping(content, duration, sessionId) {
        const typingState = this.typingIndicators.get(sessionId);
        if (!typingState) return;

        const startTime = Date.now();
        const endTime = startTime + duration;
        
        // Update typing indicator with partial content
        while (Date.now() < endTime && typingState.isTyping) {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(1, elapsed / duration);
            
            // Show partial content based on progress
            this.updateTypingProgress(sessionId, content, progress);
            
            // Wait a bit before next update
            await this.delay(100);
        }
    }

    /**
     * Update typing progress with partial content
     */
    updateTypingProgress(sessionId, content, progress) {
        const typingIndicator = document.querySelector(`[data-typing-session="${sessionId}"]`);
        if (!typingIndicator) return;

        const charsToShow = Math.floor(content.length * progress);
        const partialContent = content.substring(0, charsToShow);
        
        const messageContent = typingIndicator.querySelector('.message-content');
        if (messageContent) {
            if (progress < 1) {
                messageContent.innerHTML = `
                    <div class="typing-dots">
                        <span class="dot"></span>
                        <span class="dot"></span>
                        <span class="dot"></span>
                    </div>
                    <div class="partial-content">${partialContent}</div>
                `;
            } else {
                messageContent.innerHTML = partialContent;
            }
        }
    }

    /**
     * Apply human characteristics to response
     */
    applyHumanCharacteristics(content, behaviorProfile) {
        let enhancedContent = content;

        // Apply personality-based modifications
        switch (behaviorProfile.personality.formality) {
            case 'professional':
                enhancedContent = this.makeProfessional(enhancedContent);
                break;
            case 'friendly_professional':
                enhancedContent = this.makeFriendlyProfessional(enhancedContent);
                break;
            case 'expert_friendly':
                enhancedContent = this.makeExpertFriendly(enhancedContent);
                break;
            case 'executive_professional':
                enhancedContent = this.makeExecutiveProfessional(enhancedContent);
                break;
        }

        // Add appropriate emojis based on personality
        if (behaviorProfile.personality.emojiUsage !== 'minimal') {
            enhancedContent = this.addAppropriateEmojis(enhancedContent, behaviorProfile.personality.emojiUsage);
        }

        // Add human-like variations
        enhancedContent = this.addHumanVariations(enhancedContent);

        return enhancedContent;
    }

    /**
     * Make content more professional
     */
    makeProfessional(content) {
        // Ensure proper capitalization and punctuation
        content = content.charAt(0).toUpperCase() + content.slice(1);
        if (!content.endsWith('.') && !content.endsWith('!') && !content.endsWith('?')) {
            content += '.';
        }
        return content;
    }

    /**
     * Make content friendly but professional
     */
    makeFriendlyProfessional(content) {
        content = this.makeProfessional(content);
        
        // Add friendly touches
        const friendlyPhrases = [
            'I understand your concern',
            'Let me help you with that',
            'I appreciate you bringing this to our attention',
            'I want to make sure we get this resolved for you'
        ];
        
        if (Math.random() < 0.3) { // 30% chance
            const phrase = friendlyPhrases[Math.floor(Math.random() * friendlyPhrases.length)];
            content = `${phrase}. ${content}`;
        }
        
        return content;
    }

    /**
     * Make content expert-friendly
     */
    makeExpertFriendly(content) {
        content = this.makeFriendlyProfessional(content);
        
        // Add expertise indicators
        const expertPhrases = [
            'Based on my experience',
            'From what I can see',
            'Let me analyze this for you',
            'I can help you resolve this'
        ];
        
        if (Math.random() < 0.4) { // 40% chance
            const phrase = expertPhrases[Math.floor(Math.random() * expertPhrases.length)];
            content = `${phrase}, ${content}`;
        }
        
        return content;
    }

    /**
     * Make content executive professional
     */
    makeExecutiveProfessional(content) {
        content = this.makeProfessional(content);
        
        // Add executive-level language
        const executivePhrases = [
            'I understand the urgency of this matter',
            'Let me ensure we address this promptly',
            'I will personally oversee the resolution',
            'This is a priority for our team'
        ];
        
        if (Math.random() < 0.5) { // 50% chance
            const phrase = executivePhrases[Math.floor(Math.random() * executivePhrases.length)];
            content = `${phrase}. ${content}`;
        }
        
        return content;
    }

    /**
     * Add appropriate emojis
     */
    addAppropriateEmojis(content, emojiLevel) {
        const emojis = {
            minimal: [],
            moderate: ['👍', '🙂', '✅'],
            appropriate: ['👍', '🙂', '✅', '💡', '🔍']
        };
        
        const availableEmojis = emojis[emojiLevel] || [];
        if (availableEmojis.length === 0) return content;
        
        // Add emoji at the end occasionally
        if (Math.random() < 0.2) { // 20% chance
            const emoji = availableEmojis[Math.floor(Math.random() * availableEmojis.length)];
            content += ` ${emoji}`;
        }
        
        return content;
    }

    /**
     * Add human-like variations
     */
    addHumanVariations(content) {
        // Occasionally add filler words or corrections
        if (Math.random() < 0.1) { // 10% chance
            const variations = [
                'Actually, ',
                'Let me clarify, ',
                'To be clear, ',
                'I should mention that '
            ];
            const variation = variations[Math.floor(Math.random() * variations.length)];
            content = variation + content;
        }
        
        return content;
    }

    /**
     * Utility function for delays
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Dispatch custom events
     */
    dispatchEvent(eventName, detail) {
        const event = new CustomEvent(eventName, { detail });
        document.dispatchEvent(event);
    }

    /**
     * Get stealth mode status for a session
     */
    isStealthModeActive(sessionId) {
        return this.responseDelays.has(sessionId);
    }

    /**
     * Deactivate stealth mode for a session
     */
    deactivateStealthMode(sessionId) {
        this.responseDelays.delete(sessionId);
        this.hideTypingIndicator(sessionId);
        
        // Dispatch event
        this.dispatchEvent('stealthModeDeactivated', { sessionId });
    }

    /**
     * Update agent behavior profile
     */
    updateAgentBehavior(agentId, newProfile) {
        this.humanBehaviorProfiles.set(agentId, newProfile);
        
        // Dispatch event
        this.dispatchEvent('agentBehaviorUpdated', { agentId, newProfile });
    }

    /**
     * Get current behavior profile for an agent
     */
    getAgentBehavior(agentId) {
        return this.humanBehaviorProfiles.get(agentId);
    }

    /**
     * Export stealth agent configuration
     */
    exportConfiguration() {
        return {
            humanBehaviorProfiles: Object.fromEntries(this.humanBehaviorProfiles),
            responseDelays: Object.fromEntries(this.responseDelays),
            typingIndicators: Object.fromEntries(this.typingIndicators),
            configuration: {
                typingSpeed: this.typingSpeed,
                minResponseDelay: this.minResponseDelay,
                maxResponseDelay: this.maxResponseDelay
            }
        };
    }
}

// Export for use in other modules
window.StealthAgent = StealthAgent;
