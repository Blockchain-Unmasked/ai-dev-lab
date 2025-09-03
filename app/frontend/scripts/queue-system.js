/**
 * Queue System for AI Intake/Support Agent Demo
 * Handles multiple customer sessions, unique identifiers, and queue management
 */

class QueueSystem {
    constructor() {
        this.sessions = new Map(); // sessionId -> session data
        this.queue = []; // ordered list of waiting sessions
        this.activeSessions = new Map(); // sessionId -> active session data
        this.agentPool = new Map(); // agentId -> agent data
        this.sessionCounter = 0;
        this.agentCounter = 0;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadPersistedData();
        this.startQueueProcessor();
    }

    setupEventListeners() {
        // Listen for new customer sessions
        document.addEventListener('customerSessionStarted', (e) => {
            this.createSession(e.detail.customerData);
        });

        // Listen for session updates
        document.addEventListener('sessionUpdated', (e) => {
            this.updateSession(e.detail.sessionId, e.detail.updates);
        });

        // Listen for agent availability
        document.addEventListener('agentAvailable', (e) => {
            this.assignNextSession(e.detail.agentId);
        });
    }

    /**
     * Create a new customer session
     */
    createSession(customerData) {
        const sessionId = this.generateSessionId();
        const timestamp = Date.now();
        
        const session = {
            sessionId,
            customerId: customerData.customerId || this.generateCustomerId(),
            customerName: customerData.name || 'Anonymous Customer',
            customerEmail: customerData.email || '',
            customerPhone: customerData.phone || '',
            status: 'waiting', // waiting, active, completed, escalated
            priority: this.calculatePriority(customerData),
            category: customerData.category || 'general',
            createdAt: timestamp,
            lastActivity: timestamp,
            messages: [],
            agentId: null,
            tier: 1, // Starting tier
            escalationHistory: [],
            metadata: {
                source: customerData.source || 'web',
                userAgent: customerData.userAgent || '',
                ipAddress: customerData.ipAddress || '',
                referrer: customerData.referrer || ''
            }
        };

        this.sessions.set(sessionId, session);
        this.addToQueue(sessionId);
        this.persistSession(session);
        
        // Dispatch event
        this.dispatchEvent('sessionCreated', { session });
        
        return sessionId;
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        this.sessionCounter++;
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `session_${timestamp}_${random}_${this.sessionCounter}`;
    }

    /**
     * Generate unique customer ID
     */
    generateCustomerId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `customer_${timestamp}_${random}`;
    }

    /**
     * Calculate session priority based on customer data
     */
    calculatePriority(customerData) {
        let priority = 1; // Default priority
        
        // VIP customers get higher priority
        if (customerData.isVip) priority += 3;
        
        // Premium customers get higher priority
        if (customerData.isPremium) priority += 2;
        
        // Urgent issues get higher priority
        if (customerData.urgency === 'high') priority += 2;
        if (customerData.urgency === 'critical') priority += 3;
        
        // Crypto theft reports get highest priority
        if (customerData.category === 'crypto_theft') priority += 4;
        
        // New client onboarding gets higher priority
        if (customerData.category === 'onboarding') priority += 1;
        
        return Math.min(priority, 10); // Cap at 10
    }

    /**
     * Add session to queue
     */
    addToQueue(sessionId) {
        const session = this.sessions.get(sessionId);
        if (!session) return;

        // Remove from queue if already there
        this.queue = this.queue.filter(id => id !== sessionId);
        
        // Insert based on priority (higher priority first)
        let inserted = false;
        for (let i = 0; i < this.queue.length; i++) {
            const queuedSession = this.sessions.get(this.queue[i]);
            if (queuedSession && session.priority > queuedSession.priority) {
                this.queue.splice(i, 0, sessionId);
                inserted = true;
                break;
            }
        }
        
        if (!inserted) {
            this.queue.push(sessionId);
        }

        this.updateQueueDisplay();
    }

    /**
     * Assign next available session to agent
     */
    assignNextSession(agentId) {
        if (this.queue.length === 0) return null;
        
        const sessionId = this.queue.shift();
        const session = this.sessions.get(sessionId);
        
        if (!session) return null;
        
        // Update session
        session.status = 'active';
        session.agentId = agentId;
        session.lastActivity = Date.now();
        session.assignedAt = Date.now();
        
        // Move to active sessions
        this.activeSessions.set(sessionId, session);
        
        // Update agent pool
        const agent = this.agentPool.get(agentId);
        if (agent) {
            agent.currentSessionId = sessionId;
            agent.status = 'busy';
            agent.lastAssigned = Date.now();
        }
        
        this.persistSession(session);
        this.updateQueueDisplay();
        
        // Dispatch event
        this.dispatchEvent('sessionAssigned', { sessionId, agentId, session });
        
        return sessionId;
    }

    /**
     * Update session information
     */
    updateSession(sessionId, updates) {
        const session = this.sessions.get(sessionId);
        if (!session) return false;
        
        // Update session data
        Object.assign(session, updates);
        session.lastActivity = Date.now();
        
        // Handle status changes
        if (updates.status === 'completed') {
            this.completeSession(sessionId);
        } else if (updates.status === 'escalated') {
            this.escalateSession(sessionId, updates.escalationReason);
        }
        
        this.persistSession(session);
        this.updateQueueDisplay();
        
        // Dispatch event
        this.dispatchEvent('sessionUpdated', { sessionId, updates, session });
        
        return true;
    }

    /**
     * Complete a session
     */
    completeSession(sessionId) {
        const session = this.sessions.get(sessionId);
        if (!session) return;
        
        session.completedAt = Date.now();
        session.duration = session.completedAt - session.createdAt;
        
        // Free up agent
        if (session.agentId) {
            const agent = this.agentPool.get(session.agentId);
            if (agent) {
                agent.currentSessionId = null;
                agent.status = 'available';
                agent.lastAvailable = Date.now();
            }
        }
        
        // Remove from active sessions
        this.activeSessions.delete(sessionId);
        
        // Dispatch event
        this.dispatchEvent('sessionCompleted', { sessionId, session });
    }

    /**
     * Escalate a session to higher tier
     */
    escalateSession(sessionId, reason) {
        const session = this.sessions.get(sessionId);
        if (!session) return;
        
        session.tier++;
        session.escalationHistory.push({
            timestamp: Date.now(),
            reason: reason,
            fromTier: session.tier - 1,
            toTier: session.tier
        });
        
        // Re-queue with higher priority
        this.addToQueue(sessionId);
        
        // Dispatch event
        this.dispatchEvent('sessionEscalated', { sessionId, reason, newTier: session.tier });
    }

    /**
     * Get session by ID
     */
    getSession(sessionId) {
        return this.sessions.get(sessionId);
    }

    /**
     * Get all sessions
     */
    getAllSessions() {
        return Array.from(this.sessions.values());
    }

    /**
     * Get active sessions
     */
    getActiveSessions() {
        return Array.from(this.activeSessions.values());
    }

    /**
     * Get queue status
     */
    getQueueStatus() {
        return {
            totalSessions: this.sessions.size,
            waitingSessions: this.queue.length,
            activeSessions: this.activeSessions.size,
            availableAgents: this.getAvailableAgents().length,
            averageWaitTime: this.calculateAverageWaitTime(),
            priorityDistribution: this.getPriorityDistribution()
        };
    }

    /**
     * Get available agents
     */
    getAvailableAgents() {
        return Array.from(this.agentPool.values()).filter(agent => agent.status === 'available');
    }

    /**
     * Calculate average wait time
     */
    calculateAverageWaitTime() {
        const waitingSessions = this.queue.map(id => this.sessions.get(id)).filter(Boolean);
        if (waitingSessions.length === 0) return 0;
        
        const totalWaitTime = waitingSessions.reduce((total, session) => {
            return total + (Date.now() - session.createdAt);
        }, 0);
        
        return Math.round(totalWaitTime / waitingSessions.length / 1000); // in seconds
    }

    /**
     * Get priority distribution
     */
    getPriorityDistribution() {
        const distribution = {};
        this.sessions.forEach(session => {
            distribution[session.priority] = (distribution[session.priority] || 0) + 1;
        });
        return distribution;
    }

    /**
     * Update queue display
     */
    updateQueueDisplay() {
        // Dispatch event for UI updates
        this.dispatchEvent('queueUpdated', {
            queueStatus: this.getQueueStatus(),
            queue: this.queue.map(id => this.sessions.get(id)).filter(Boolean)
        });
    }

    /**
     * Start queue processor
     */
    startQueueProcessor() {
        setInterval(() => {
            this.processQueue();
        }, 5000); // Check every 5 seconds
    }

    /**
     * Process queue and assign sessions
     */
    processQueue() {
        const availableAgents = this.getAvailableAgents();
        
        while (this.queue.length > 0 && availableAgents.length > 0) {
            const agent = availableAgents.shift();
            const sessionId = this.assignNextSession(agent.agentId);
            
            if (sessionId) {
                // Remove agent from available list since they're now busy
                const index = availableAgents.findIndex(a => a.agentId === agent.agentId);
                if (index > -1) {
                    availableAgents.splice(index, 1);
                }
            }
        }
    }

    /**
     * Persist session data
     */
    persistSession(session) {
        try {
            const key = `session_${session.sessionId}`;
            localStorage.setItem(key, JSON.stringify(session));
        } catch (error) {
            console.error('Failed to persist session:', error);
        }
    }

    /**
     * Load persisted data
     */
    loadPersistedData() {
        try {
            // Load sessions
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith('session_')) {
                    const sessionData = JSON.parse(localStorage.getItem(key));
                    if (sessionData && sessionData.sessionId) {
                        this.sessions.set(sessionData.sessionId, sessionData);
                        
                        // Re-add to queue if waiting
                        if (sessionData.status === 'waiting') {
                            this.addToQueue(sessionData.sessionId);
                        }
                        
                        // Re-add to active if active
                        if (sessionData.status === 'active') {
                            this.activeSessions.set(sessionData.sessionId, sessionData);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Failed to load persisted data:', error);
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
     * Export queue data
     */
    exportQueueData() {
        return {
            sessions: Array.from(this.sessions.values()),
            queue: this.queue,
            activeSessions: Array.from(this.activeSessions.values()),
            agentPool: Array.from(this.agentPool.values()),
            queueStatus: this.getQueueStatus(),
            exportTimestamp: Date.now()
        };
    }

    /**
     * Clear all data (for testing)
     */
    clearAllData() {
        this.sessions.clear();
        this.queue = [];
        this.activeSessions.clear();
        this.agentPool.clear();
        this.sessionCounter = 0;
        this.agentCounter = 0;
        
        // Clear localStorage
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith('session_')) {
                localStorage.removeItem(key);
            }
        });
        
        this.updateQueueDisplay();
    }
}

// Export for use in other modules
window.QueueSystem = QueueSystem;
