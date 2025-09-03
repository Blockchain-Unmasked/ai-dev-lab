/**
 * Session Manager for AI Intake/Support Agent Demo
 * Handles individual customer sessions, context, and session-specific operations
 */

class SessionManager {
    constructor(queueSystem) {
        this.queueSystem = queueSystem;
        this.currentSession = null;
        this.sessionHistory = new Map(); // sessionId -> session data
        this.customerProfiles = new Map(); // customerId -> profile data
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadCustomerProfiles();
    }

    setupEventListeners() {
        // Listen for session creation
        document.addEventListener('sessionCreated', (e) => {
            this.initializeSession(e.detail.session);
        });

        // Listen for session assignment
        document.addEventListener('sessionAssigned', (e) => {
            this.handleSessionAssignment(e.detail.sessionId, e.detail.agentId);
        });

        // Listen for session updates
        document.addEventListener('sessionUpdated', (e) => {
            this.handleSessionUpdate(e.detail.sessionId, e.detail.updates);
        });

        // Listen for chat messages
        document.addEventListener('chatMessageSent', (e) => {
            this.addMessageToSession(e.detail.message, e.detail.sessionId);
        });

        // Listen for agent responses
        document.addEventListener('chatResponseReceived', (e) => {
            this.addAgentResponse(e.detail.response, e.detail.sessionId);
        });
    }

    /**
     * Initialize a new session
     */
    initializeSession(session) {
        // Create customer profile if doesn't exist
        if (!this.customerProfiles.has(session.customerId)) {
            this.createCustomerProfile(session);
        }

        // Initialize session context
        session.context = {
            conversationHistory: [],
            customerIntent: null,
            issueCategory: null,
            escalationTriggers: [],
            agentNotes: [],
            customerSatisfaction: null,
            resolutionPath: [],
            lastAgentInteraction: null,
            sessionStartTime: Date.now()
        };

        // Add to session history
        this.sessionHistory.set(session.sessionId, session);
        
        // Dispatch event
        this.dispatchEvent('sessionInitialized', { session });
    }

    /**
     * Create customer profile
     */
    createCustomerProfile(session) {
        const profile = {
            customerId: session.customerId,
            name: session.customerName,
            email: session.customerEmail,
            phone: session.customerPhone,
            firstContact: Date.now(),
            lastContact: Date.now(),
            totalSessions: 0,
            resolvedIssues: 0,
            escalatedIssues: 0,
            averageResolutionTime: 0,
            customerTier: this.calculateCustomerTier(session),
            preferences: {
                communicationChannel: 'chat',
                language: 'en',
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
            },
            tags: [],
            notes: []
        };

        this.customerProfiles.set(session.customerId, profile);
        this.persistCustomerProfile(profile);
    }

    /**
     * Calculate customer tier based on session data
     */
    calculateCustomerTier(session) {
        let tier = 'standard';
        
        if (session.metadata?.source === 'vip') tier = 'vip';
        if (session.category === 'crypto_theft') tier = 'urgent';
        if (session.category === 'onboarding') tier = 'new_client';
        
        return tier;
    }

    /**
     * Handle session assignment to agent
     */
    handleSessionAssignment(sessionId, agentId) {
        const session = this.queueSystem.getSession(sessionId);
        if (!session) return;

        session.assignedAgent = agentId;
        session.assignmentTime = Date.now();
        
        // Update session context
        session.context.agentAssignment = {
            agentId: agentId,
            timestamp: Date.now(),
            assignmentReason: 'queue_processing'
        };

        // Dispatch event
        this.dispatchEvent('sessionAssignedToAgent', { sessionId, agentId, session });
    }

    /**
     * Handle session updates
     */
    handleSessionUpdate(sessionId, updates) {
        const session = this.queueSystem.getSession(sessionId);
        if (!session) return;

        // Update session context based on changes
        if (updates.status) {
            this.updateSessionStatus(session, updates.status);
        }

        if (updates.tier) {
            this.handleTierChange(session, updates.tier);
        }

        // Update customer profile
        this.updateCustomerProfile(session);
    }

    /**
     * Update session status
     */
    updateSessionStatus(session, newStatus) {
        const oldStatus = session.status;
        session.status = newStatus;
        
        // Add to context
        session.context.statusChanges.push({
            from: oldStatus,
            to: newStatus,
            timestamp: Date.now(),
            reason: 'status_update'
        });

        // Handle specific status changes
        if (newStatus === 'completed') {
            this.handleSessionCompletion(session);
        } else if (newStatus === 'escalated') {
            this.handleSessionEscalation(session);
        }
    }

    /**
     * Handle session completion
     */
    handleSessionCompletion(session) {
        session.context.resolutionTime = Date.now() - session.context.sessionStartTime;
        session.context.resolutionStatus = 'resolved';
        
        // Update customer profile
        const profile = this.customerProfiles.get(session.customerId);
        if (profile) {
            profile.resolvedIssues++;
            profile.lastContact = Date.now();
            profile.totalSessions++;
            
            // Update average resolution time
            const totalTime = profile.averageResolutionTime * (profile.resolvedIssues - 1) + session.context.resolutionTime;
            profile.averageResolutionTime = totalTime / profile.resolvedIssues;
            
            this.persistCustomerProfile(profile);
        }
    }

    /**
     * Handle session escalation
     */
    handleSessionEscalation(session) {
        session.context.escalationCount = (session.context.escalationCount || 0) + 1;
        session.context.lastEscalation = Date.now();
        
        // Update customer profile
        const profile = this.customerProfiles.get(session.customerId);
        if (profile) {
            profile.escalatedIssues++;
            this.persistCustomerProfile(profile);
        }
    }

    /**
     * Handle tier change
     */
    handleTierChange(session, newTier) {
        const oldTier = session.tier;
        session.tier = newTier;
        
        session.context.tierChanges.push({
            from: oldTier,
            to: newTier,
            timestamp: Date.now(),
            reason: 'escalation'
        });
    }

    /**
     * Add message to session
     */
    addMessageToSession(message, sessionId) {
        const session = this.queueSystem.getSession(sessionId);
        if (!session) return;

        const messageData = {
            id: this.generateMessageId(),
            timestamp: Date.now(),
            type: 'customer',
            content: message,
            metadata: {
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            }
        };

        session.messages.push(messageData);
        session.context.conversationHistory.push(messageData);
        
        // Analyze customer intent
        this.analyzeCustomerIntent(session, message);
        
        // Check for escalation triggers
        this.checkEscalationTriggers(session, message);
        
        // Update session
        this.queueSystem.updateSession(sessionId, {
            messages: session.messages,
            lastActivity: Date.now()
        });
    }

    /**
     * Add agent response to session
     */
    addAgentResponse(response, sessionId) {
        const session = this.queueSystem.getSession(sessionId);
        if (!session) return;

        const responseData = {
            id: this.generateMessageId(),
            timestamp: Date.now(),
            type: 'agent',
            content: response.content,
            agentId: response.agentId,
            responseType: response.type, // ai, canned, human
            confidence: response.confidence,
            metadata: {
                responseTime: response.responseTime,
                model: response.model,
                tier: response.tier
            }
        };

        session.messages.push(responseData);
        session.context.conversationHistory.push(responseData);
        session.context.lastAgentInteraction = Date.now();
        
        // Update session
        this.queueSystem.updateSession(sessionId, {
            messages: session.messages,
            lastActivity: Date.now()
        });
    }

    /**
     * Analyze customer intent from message
     */
    analyzeCustomerIntent(session, message) {
        const lowerMessage = message.toLowerCase();
        
        // Simple intent detection (could be enhanced with AI)
        if (lowerMessage.includes('crypto') && lowerMessage.includes('stolen')) {
            session.context.customerIntent = 'report_crypto_theft';
            session.context.issueCategory = 'crypto_theft';
        } else if (lowerMessage.includes('onboard') || lowerMessage.includes('new client')) {
            session.context.customerIntent = 'client_onboarding';
            session.context.issueCategory = 'onboarding';
        } else if (lowerMessage.includes('urgent') || lowerMessage.includes('emergency')) {
            session.context.customerIntent = 'urgent_support';
            session.context.issueCategory = 'urgent';
        } else if (lowerMessage.includes('billing') || lowerMessage.includes('payment')) {
            session.context.customerIntent = 'billing_support';
            session.context.issueCategory = 'billing';
        } else {
            session.context.customerIntent = 'general_support';
            session.context.issueCategory = 'general';
        }
    }

    /**
     * Check for escalation triggers
     */
    checkEscalationTriggers(session, message) {
        const lowerMessage = message.toLowerCase();
        const triggers = [];
        
        // Check for escalation keywords
        if (lowerMessage.includes('manager') || lowerMessage.includes('supervisor')) {
            triggers.push('customer_requested_escalation');
        }
        
        if (lowerMessage.includes('frustrated') || lowerMessage.includes('angry')) {
            triggers.push('customer_emotion_escalation');
        }
        
        if (lowerMessage.includes('legal') || lowerMessage.includes('lawyer')) {
            triggers.push('legal_escalation');
        }
        
        if (lowerMessage.includes('complaint') || lowerMessage.includes('formal')) {
            triggers.push('formal_complaint');
        }
        
        // Add triggers to context
        if (triggers.length > 0) {
            session.context.escalationTriggers.push(...triggers);
            
            // Auto-escalate for certain triggers
            if (triggers.includes('legal_escalation') || triggers.includes('formal_complaint')) {
                this.queueSystem.updateSession(session.sessionId, {
                    status: 'escalated',
                    escalationReason: triggers.join(', ')
                });
            }
        }
    }

    /**
     * Generate unique message ID
     */
    generateMessageId() {
        return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Get session context
     */
    getSessionContext(sessionId) {
        const session = this.queueSystem.getSession(sessionId);
        if (!session) return null;
        
        return {
            session: session,
            context: session.context,
            customerProfile: this.customerProfiles.get(session.customerId),
            queuePosition: this.getQueuePosition(sessionId),
            estimatedWaitTime: this.calculateEstimatedWaitTime(sessionId)
        };
    }

    /**
     * Get queue position for session
     */
    getQueuePosition(sessionId) {
        const queue = this.queueSystem.queue;
        const position = queue.indexOf(sessionId);
        return position >= 0 ? position + 1 : null;
    }

    /**
     * Calculate estimated wait time
     */
    calculateEstimatedWaitTime(sessionId) {
        const position = this.getQueuePosition(sessionId);
        if (!position) return 0;
        
        const averageWaitTime = this.queueSystem.getQueueStatus().averageWaitTime;
        const availableAgents = this.queueSystem.getAvailableAgents().length;
        
        if (availableAgents === 0) return position * averageWaitTime;
        return Math.ceil(position / availableAgents) * averageWaitTime;
    }

    /**
     * Update customer profile
     */
    updateCustomerProfile(session) {
        const profile = this.customerProfiles.get(session.customerId);
        if (!profile) return;
        
        profile.lastContact = Date.now();
        profile.totalSessions = Math.max(profile.totalSessions, 1);
        
        // Update tags based on session data
        if (session.category && !profile.tags.includes(session.category)) {
            profile.tags.push(session.category);
        }
        
        this.persistCustomerProfile(profile);
    }

    /**
     * Persist customer profile
     */
    persistCustomerProfile(profile) {
        try {
            const key = `customer_${profile.customerId}`;
            localStorage.setItem(key, JSON.stringify(profile));
        } catch (error) {
            console.error('Failed to persist customer profile:', error);
        }
    }

    /**
     * Load customer profiles
     */
    loadCustomerProfiles() {
        try {
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith('customer_')) {
                    const profileData = JSON.parse(localStorage.getItem(key));
                    if (profileData && profileData.customerId) {
                        this.customerProfiles.set(profileData.customerId, profileData);
                    }
                }
            }
        } catch (error) {
            console.error('Failed to load customer profiles:', error);
        }
    }

    /**
     * Dispatch custom events
     */
    dispatchEvent(eventName, detail) {
        const event = new CustomEvent(eventName, { detail });
        document.dispatchEvent(event);
    }

    /**
     * Export session data
     */
    exportSessionData(sessionId) {
        const session = this.queueSystem.getSession(sessionId);
        if (!session) return null;
        
        return {
            session: session,
            context: session.context,
            customerProfile: this.customerProfiles.get(session.customerId),
            messages: session.messages,
            exportTimestamp: Date.now()
        };
    }

    /**
     * Get all customer profiles
     */
    getAllCustomerProfiles() {
        return Array.from(this.customerProfiles.values());
    }

    /**
     * Search sessions by criteria
     */
    searchSessions(criteria) {
        const allSessions = this.queueSystem.getAllSessions();
        return allSessions.filter(session => {
            // Search by customer name/email
            if (criteria.customer && (
                session.customerName.toLowerCase().includes(criteria.customer.toLowerCase()) ||
                session.customerEmail.toLowerCase().includes(criteria.customer.toLowerCase())
            )) {
                return true;
            }
            
            // Search by category
            if (criteria.category && session.category === criteria.category) {
                return true;
            }
            
            // Search by status
            if (criteria.status && session.status === criteria.status) {
                return true;
            }
            
            // Search by date range
            if (criteria.startDate && criteria.endDate) {
                const sessionDate = new Date(session.createdAt);
                const startDate = new Date(criteria.startDate);
                const endDate = new Date(criteria.endDate);
                return sessionDate >= startDate && sessionDate <= endDate;
            }
            
            return false;
        });
    }
}

// Export for use in other modules
window.SessionManager = SessionManager;
