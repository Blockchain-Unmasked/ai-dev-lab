/**
 * Modular Prompt System for AI/DEV Lab
 * Generic prompt management system that can work with any chat interface
 */

class PromptSystem {
    constructor() {
        this.activePrompt = null;
        this.promptConfigs = new Map();
        this.conversationState = {
            currentStep: 1,
            messageCount: 0,
            extractedData: {},
            status: 'incomplete'
        };
        this.initialize();
    }

    initialize() {
        this.loadPromptConfigurations();
        this.setupEventListeners();
    }

    /**
     * Load prompt configurations from JSON files or API
     */
    async loadPromptConfigurations() {
        try {
            // Load OCINT prompt configuration
            const ocintConfig = await this.loadPromptConfig('ocint-victim-report');
            this.promptConfigs.set('ocint-victim-report', ocintConfig);

            // Load general support prompt configuration
            const generalConfig = await this.loadPromptConfig('general-support');
            this.promptConfigs.set('general-support', generalConfig);

            console.log('✅ Prompt configurations loaded:', Array.from(this.promptConfigs.keys()));
        } catch (error) {
            console.error('❌ Failed to load prompt configurations:', error);
        }
    }

    /**
     * Load a specific prompt configuration
     */
    async loadPromptConfig(configName) {
        try {
            const response = await fetch(`/api/v1/prompts/${configName}`);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.log(`Using fallback config for ${configName}`);
        }

        // Fallback configurations
        return this.getFallbackConfig(configName);
    }

    /**
     * Get fallback prompt configurations
     */
    getFallbackConfig(configName) {
        const configs = {
            'ocint-victim-report': {
                id: 'ocint-victim-report',
                name: 'OCINT Victim Report',
                description: 'Crypto theft victim report creation',
                agent: {
                    name: 'Alex',
                    personality: 'empathetic, professional, casual',
                    age_range: '25-35',
                    tone: 'relaxed, supportive, clear'
                },
                scope: {
                    primary_function: 'Crypto theft victim report creation and validation',
                    boundaries: [
                        'DO NOT attempt to trace transactions',
                        'DO NOT provide legal advice',
                        'DO NOT investigate the crime',
                        'ONLY focus on report creation'
                    ],
                    max_messages: 8,
                    escalation_triggers: [
                        'Report is complete and validated',
                        'Victim requests human assistance',
                        'Maximum message limit reached'
                    ]
                },
                conversation_flow: [
                    {
                        step: 1,
                        purpose: 'Initial greeting and report initiation',
                        messages: [
                            "Hey there! 👋 I'm Alex, and I'm here to help you report what happened with your crypto. I know this is probably really stressful, but we're going to get through this together, okay?",
                            "My job is to help you create a detailed report and guide you through the process. Here's the reality: most law enforcement agencies don't have specialized crypto teams, so victims usually need to do the investigative work themselves first.",
                            "We'll help you gather all the evidence and documentation you need. Once you have everything organized, THEN you can approach law enforcement with a complete case file. That's when they're most likely to be able to help.",
                            "Sound good? Let's start with getting your contact info so we can stay in touch throughout this process. What's your name and email address? And what's the best phone number to reach you at?"
                        ],
                        collects: ['victim_name', 'victim_email', 'victim_phone'],
                        extraction_patterns: {
                            victim_name: /my name is ([A-Z][a-z]+ [A-Z][a-z]+)/i,
                            victim_email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/,
                            victim_phone: /(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})/
                        }
                    },
                    {
                        step: 2,
                        purpose: 'Incident details collection',
                        messages: [
                            "Thanks for that info! Now let's talk about what happened. When did you first notice the theft? Do you remember the date and roughly what time it was?",
                            "Can you walk me through what happened? Like, how did you discover that your crypto was gone? Did you get any notifications or did you just notice it when you checked your wallet?"
                        ],
                        collects: ['incident_date', 'incident_time', 'incident_description', 'how_discovered'],
                        extraction_patterns: {
                            incident_date: /\d{1,2}\/\d{1,2}\/\d{4}|\d{4}-\d{1,2}-\d{1,2}/,
                            incident_time: /\d{1,2}:\d{2}\s*(AM|PM|am|pm)?/,
                            incident_description: /.*/
                        }
                    },
                    {
                        step: 3,
                        purpose: 'Transaction information',
                        messages: [
                            "Okay, so what kind of crypto are we talking about here? Bitcoin, Ethereum, something else? And do you have a rough idea of how much was taken?",
                            "If you have any wallet addresses that were involved, that would be super helpful. And if you've got any transaction hash IDs or transaction IDs, those are like gold for our investigators.",
                            "Were you using any exchanges or was this all in a personal wallet? If it was an exchange, which one?"
                        ],
                        collects: ['crypto_type', 'amount_stolen', 'wallet_addresses', 'transaction_hashes'],
                        extraction_patterns: {
                            crypto_type: /(bitcoin|btc|ethereum|eth|litecoin|ltc|dogecoin|doge)/i,
                            amount_stolen: /\$?(\d+(?:,\d{3})*(?:\.\d{2})?)/,
                            wallet_addresses: /[13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40}/,
                            transaction_hashes: /[a-fA-F0-9]{64}/
                        }
                    },
                    {
                        step: 4,
                        purpose: 'Evidence and validation',
                        messages: [
                            "Do you have any screenshots or evidence you can share? Like screenshots of your wallet, transaction records, or any emails or messages related to this?",
                            "Is there anything else about this situation that you think might be important? Sometimes the smallest details can make a big difference in an investigation."
                        ],
                        collects: ['evidence_files', 'additional_details'],
                        extraction_patterns: {
                            evidence_files: /(screenshot|image|photo|picture|record|receipt)/i
                        }
                    },
                    {
                        step: 5,
                        purpose: 'Report completion and escalation',
                        messages: [
                            "Perfect! I think I've got everything I need to put together a solid report for you. Our investigation team will review this within 24 hours and someone will reach out to you directly.",
                            "Is there anything else you want to add before I submit this? Sometimes people remember things after we go through everything."
                        ],
                        collects: ['final_confirmation'],
                        escalation: true
                    }
                ],
                escalation: {
                    threshold: 0.8,
                    message: "🎉 Great job! Your report is ready. I've got everything we need to create a comprehensive case file. Here's what happens next: you'll need to take this evidence to law enforcement yourself, but now you have everything organized and documented properly.",
                    next_steps: "With this complete case file, you can approach local law enforcement. They'll be much more likely to help when you have all the evidence already gathered and organized. You've done the hard work - now they can take action."
                }
            },
            'general-support': {
                id: 'general-support',
                name: 'General Customer Support',
                description: 'General customer support and assistance',
                agent: {
                    name: 'Sam',
                    personality: 'helpful, professional, friendly',
                    age_range: '25-35',
                    tone: 'professional, supportive, clear'
                },
                scope: {
                    primary_function: 'General customer support and assistance',
                    boundaries: [
                        'Provide helpful information and support',
                        'Escalate complex issues to specialists',
                        'Maintain professional communication'
                    ],
                    max_messages: 20,
                    escalation_triggers: [
                        'Complex technical issues',
                        'Customer requests human assistance',
                        'Issues beyond general support scope'
                    ]
                },
                conversation_flow: [
                    {
                        step: 1,
                        purpose: 'Initial greeting and assistance',
                        messages: [
                            "Hello! I'm Sam, your AI support assistant. How can I help you today?",
                            "I'm here to assist with general questions, provide information, and help resolve any issues you might be experiencing."
                        ],
                        collects: ['user_inquiry', 'issue_type'],
                        extraction_patterns: {
                            user_inquiry: /.*/,
                            issue_type: /(help|problem|issue|question|support)/i
                        }
                    }
                ],
                escalation: {
                    threshold: 0.5,
                    message: "I'd like to connect you with one of our human specialists who can provide more detailed assistance.",
                    next_steps: "A human agent will be with you shortly to help resolve your issue."
                }
            }
        };

        return configs[configName] || configs['general-support'];
    }

    /**
     * Set the active prompt configuration
     */
    setActivePrompt(promptId) {
        if (this.promptConfigs.has(promptId)) {
            this.activePrompt = this.promptConfigs.get(promptId);
            this.resetConversationState();
            console.log(`✅ Active prompt set to: ${this.activePrompt.name}`);
            return true;
        }
        console.error(`❌ Prompt configuration not found: ${promptId}`);
        return false;
    }

    /**
     * Get the current prompt configuration
     */
    getActivePrompt() {
        return this.activePrompt;
    }

    /**
     * Reset conversation state
     */
    resetConversationState() {
        this.conversationState = {
            currentStep: 1,
            messageCount: 0,
            extractedData: {},
            status: 'incomplete'
        };
    }

    /**
     * Get the next message(s) for the current step
     */
    getNextMessages() {
        if (!this.activePrompt) {
            return ["I'm not sure how to help you. Please select a support mode."];
        }

        const currentStep = this.activePrompt.conversation_flow[this.conversationState.currentStep - 1];
        if (!currentStep) {
            return ["I'm not sure what to do next. Let me connect you with a human agent."];
        }

        return currentStep.messages || [];
    }

    /**
     * Process user message and extract information
     */
    processUserMessage(message) {
        if (!this.activePrompt) {
            return { success: false, error: 'No active prompt configuration' };
        }

        const currentStep = this.activePrompt.conversation_flow[this.conversationState.currentStep - 1];
        if (!currentStep) {
            return { success: false, error: 'Invalid conversation step' };
        }

        // Extract information based on patterns
        const extracted = this.extractInformation(message, currentStep.extraction_patterns);
        
        // Update conversation state
        this.conversationState.messageCount++;
        this.conversationState.extractedData = { ...this.conversationState.extractedData, ...extracted };

        // Check if step is complete
        const stepComplete = this.isStepComplete(currentStep, extracted);
        
        // Move to next step if complete
        if (stepComplete) {
            this.conversationState.currentStep++;
        }

        // Check for escalation
        const shouldEscalate = this.shouldEscalate();

        return {
            success: true,
            extracted,
            stepComplete,
            shouldEscalate,
            nextStep: this.conversationState.currentStep,
            conversationState: { ...this.conversationState }
        };
    }

    /**
     * Extract information from message using patterns
     */
    extractInformation(message, patterns) {
        const extracted = {};
        
        for (const [field, pattern] of Object.entries(patterns)) {
            const match = message.match(pattern);
            if (match) {
                extracted[field] = match[1] || match[0];
            }
        }
        
        return extracted;
    }

    /**
     * Check if current step is complete
     */
    isStepComplete(step, extracted) {
        if (!step.collects) return true;
        
        const requiredFields = step.collects;
        const extractedFields = Object.keys(extracted);
        
        // Check if we have at least 80% of required fields
        const completionRatio = extractedFields.length / requiredFields.length;
        return completionRatio >= 0.8;
    }

    /**
     * Check if conversation should escalate
     */
    shouldEscalate() {
        if (!this.activePrompt) return false;

        const { escalation } = this.activePrompt;
        if (!escalation) return false;

        // Check message limit
        if (this.conversationState.messageCount >= this.activePrompt.scope.max_messages) {
            return true;
        }

        // Check completion threshold
        const totalFields = this.activePrompt.conversation_flow.reduce((acc, step) => 
            acc + (step.collects ? step.collects.length : 0), 0);
        const extractedFields = Object.keys(this.conversationState.extractedData).length;
        const completionRatio = extractedFields / totalFields;

        return completionRatio >= escalation.threshold;
    }

    /**
     * Get escalation message
     */
    getEscalationMessage() {
        if (!this.activePrompt || !this.activePrompt.escalation) {
            return "I'm connecting you with a human agent who can provide more assistance.";
        }

        return this.activePrompt.escalation.message;
    }

    /**
     * Get conversation status
     */
    getConversationStatus() {
        return {
            activePrompt: this.activePrompt?.name || 'None',
            currentStep: this.conversationState.currentStep,
            messageCount: this.conversationState.messageCount,
            extractedData: this.conversationState.extractedData,
            status: this.conversationState.status,
            shouldEscalate: this.shouldEscalate()
        };
    }

    /**
     * Setup event listeners for prompt system
     */
    setupEventListeners() {
        // Listen for prompt mode changes
        document.addEventListener('promptModeChanged', (event) => {
            const { promptId } = event.detail;
            this.setActivePrompt(promptId);
        });

        // Listen for conversation resets
        document.addEventListener('conversationReset', () => {
            this.resetConversationState();
        });
    }

    /**
     * Get available prompt configurations
     */
    getAvailablePrompts() {
        return Array.from(this.promptConfigs.values()).map(config => ({
            id: config.id,
            name: config.name,
            description: config.description
        }));
    }
}

// Export for use in other modules
window.PromptSystem = PromptSystem;
