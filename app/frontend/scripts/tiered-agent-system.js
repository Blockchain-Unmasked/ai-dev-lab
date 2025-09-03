/**
 * Enhanced Tiered Agent System for AI Intake/Support Agent Demo
 * Based on Enterprise Contact Center Research Findings
 * Implements proper 4-tier structure with knowledge boundaries and enterprise best practices
 */

class TieredAgentSystem {
    constructor() {
        this.agents = new Map(); // agentId -> agent data
        this.agentTiers = new Map(); // tier -> tier configuration
        this.knowledgeBase = new Map(); // knowledgeId -> knowledge data
        this.escalationRules = new Map(); // ruleId -> escalation rule
        this.qaSystem = null; // Quality Assurance system reference
        
        this.init();
    }

    init() {
        this.initializeAgentTiers();
        this.initializeKnowledgeBase();
        this.initializeEscalationRules();
        this.setupEventListeners();
        this.initializeQASystem();
    }

    /**
     * Initialize Quality Assurance System
     */
    initializeQASystem() {
        this.qaSystem = {
            scorecards: new Map(),
            evaluations: new Map(),
            qualityMetrics: new Map(),
            calibrationSessions: [],
            qualityIndex: 0
        };
    }

    /**
     * Initialize agent tiers with enterprise-grade configurations
     * Based on research findings for modern contact centers
     */
    initializeAgentTiers() {
        // Tier 0: Self-Service (Customer Self-Help)
        this.agentTiers.set(0, {
            tier: 0,
            name: 'Self-Service',
            description: 'Customer self-help through FAQs, chatbots, and IVR systems',
            capabilities: [
                'faq_resolution',
                'basic_troubleshooting',
                'account_information',
                'order_status',
                'payment_processing'
            ],
            knowledgeAccess: [
                'public_faqs',
                'self_service_guides',
                'interactive_troubleshooters'
            ],
            restrictions: [
                'no_sensitive_data_access',
                'no_account_changes',
                'no_complex_issue_resolution'
            ],
            escalationTriggers: [
                'customer_request_human',
                'complex_issue_detected',
                'frustration_detected',
                'multiple_attempts_failed'
            ],
            maxSessionDuration: 5 * 60 * 1000, // 5 minutes
            deflectionRate: 0.65, // Target 65% deflection
            requiredTraining: ['self_service_guidelines', 'escalation_procedures'],
            performanceMetrics: ['deflection_rate', 'escalation_rate', 'customer_satisfaction']
        });

        // Tier 1: Entry Level Support (General Inquiries)
        this.agentTiers.set(1, {
            tier: 1,
            name: 'Entry Level Support',
            description: 'Frontline customer support with broad but basic knowledge',
            capabilities: [
                'basic_customer_greeting',
                'simple_issue_resolution',
                'basic_product_information',
                'escalation_triggering',
                'scripted_troubleshooting',
                'account_verification'
            ],
            knowledgeAccess: [
                'basic_faq',
                'product_overview',
                'contact_information',
                'escalation_procedures',
                'standard_scripts',
                'basic_troubleshooting_guides'
            ],
            restrictions: [
                'no_financial_transactions',
                'no_legal_advice',
                'no_system_configuration',
                'limited_case_access',
                'no_policy_exceptions'
            ],
            escalationTriggers: [
                'complex_technical_issues',
                'financial_concerns',
                'legal_questions',
                'customer_complaints',
                'escalation_requests',
                'billing_disputes',
                'policy_exceptions'
            ],
            maxSessionDuration: 15 * 60 * 1000, // 15 minutes
            requiredTraining: ['basic_support', 'escalation_procedures', 'customer_service_fundamentals'],
            performanceMetrics: ['first_contact_resolution', 'average_handle_time', 'escalation_accuracy', 'customer_satisfaction'],
            targetFCR: 0.75, // 75% first contact resolution
            targetAHT: 8 * 60 * 1000 // 8 minutes average handle time
        });

        // Tier 2: Intermediate Support (Specialized or Technical Support)
        this.agentTiers.set(2, {
            tier: 2,
            name: 'Intermediate Support',
            description: 'Specialized support and complex issue resolution',
            capabilities: [
                'advanced_issue_resolution',
                'technical_support',
                'billing_support',
                'case_management',
                'supervisor_support',
                'remote_diagnostics',
                'account_changes',
                'policy_exception_handling'
            ],
            knowledgeAccess: [
                'technical_documentation',
                'billing_procedures',
                'case_management_tools',
                'escalation_guidelines',
                'quality_assurance_procedures',
                'internal_troubleshooting_guides',
                'admin_dashboards'
            ],
            restrictions: [
                'no_legal_advice',
                'no_system_administration',
                'limited_financial_authority',
                'no_code_changes'
            ],
            escalationTriggers: [
                'legal_issues',
                'system_administration',
                'financial_disputes',
                'complex_technical_issues',
                'management_escalation',
                'vendor_escalation'
            ],
            maxSessionDuration: 30 * 60 * 1000, // 30 minutes
            requiredTraining: ['technical_support', 'billing_procedures', 'case_management', 'advanced_troubleshooting'],
            performanceMetrics: ['resolution_rate', 'escalation_accuracy', 'customer_satisfaction', 'case_completion', 'technical_competency'],
            targetResolutionRate: 0.85, // 85% resolution rate
            targetAHT: 20 * 60 * 1000 // 20 minutes average handle time
        });

        // Tier 3: Senior/Expert Support (Advanced Resolution)
        this.agentTiers.set(3, {
            tier: 3,
            name: 'Senior/Expert Support',
            description: 'Complex case resolution and quality oversight',
            capabilities: [
                'complex_case_resolution',
                'quality_assurance',
                'agent_training',
                'process_improvement',
                'management_support',
                'bug_investigation',
                'integration_troubleshooting',
                'design_change_approval'
            ],
            knowledgeAccess: [
                'full_system_access',
                'quality_assurance_tools',
                'training_materials',
                'process_documentation',
                'management_reports',
                'engineering_notes',
                'error_logs',
                'development_team_access'
            ],
            restrictions: [
                'no_legal_advice',
                'compliance_with_company_policies',
                'approval_required_for_major_changes'
            ],
            escalationTriggers: [
                'legal_issues',
                'compliance_violations',
                'management_approval_required',
                'vendor_escalation',
                'executive_escalation'
            ],
            maxSessionDuration: 60 * 60 * 1000, // 60 minutes
            requiredTraining: ['advanced_support', 'quality_assurance', 'training_methodologies', 'process_optimization'],
            performanceMetrics: ['complex_resolution_rate', 'quality_scores', 'training_effectiveness', 'process_improvement', 'knowledge_contribution'],
            targetComplexResolutionRate: 0.90, // 90% complex issue resolution
            targetAHT: 45 * 60 * 1000 // 45 minutes average handle time
        });

        // Tier 4: Supervisors/Managers
        this.agentTiers.set(4, {
            tier: 4,
            name: 'Supervisor/Manager',
            description: 'Team management and strategic oversight',
            capabilities: [
                'team_management',
                'performance_monitoring',
                'strategic_decision_making',
                'process_optimization',
                'stakeholder_communication',
                'resource_allocation',
                'crisis_management',
                'policy_approval'
            ],
            knowledgeAccess: [
                'management_dashboard',
                'performance_analytics',
                'strategic_plans',
                'budget_information',
                'stakeholder_contacts',
                'executive_reports',
                'compliance_dashboards'
            ],
            restrictions: [
                'compliance_with_company_policies',
                'approval_required_for_major_changes',
                'board_approval_for_budget_changes'
            ],
            escalationTriggers: [
                'legal_issues',
                'compliance_violations',
                'budget_exceeded',
                'stakeholder_concerns',
                'executive_escalation'
            ],
            maxSessionDuration: null, // No limit for managers
            requiredTraining: ['management_skills', 'leadership_development', 'strategic_planning', 'financial_management'],
            performanceMetrics: ['team_performance', 'customer_satisfaction', 'operational_efficiency', 'strategic_goals', 'cost_management'],
            targetTeamPerformance: 0.90, // 90% team performance
            targetCustomerSatisfaction: 4.5 // 4.5/5 customer satisfaction
        });
    }

    /**
     * Initialize knowledge base with enterprise-grade role-based access control
     * Based on research findings for knowledge management best practices
     */
    initializeKnowledgeBase() {
        // Public Knowledge (Tier 0+)
        this.knowledgeBase.set('public_faqs', {
            id: 'public_faqs',
            title: 'Public Frequently Asked Questions',
            content: {
                'company_info': 'OCINT (Onchain Intelligence) provides blockchain security and intelligence services.',
                'contact_methods': 'Support available via chat, email, and phone during business hours.',
                'service_hours': 'Monday-Friday 9 AM - 6 PM EST, emergency support available 24/7.',
                'basic_troubleshooting': 'Common solutions for frequently encountered issues.'
            },
            accessTier: 0,
            lastUpdated: Date.now(),
            tags: ['public', 'faq', 'company_info'],
            contentOwner: 'marketing_team',
            reviewCycle: 'monthly',
            version: '1.0'
        });

        // Basic FAQ (Tier 1+)
        this.knowledgeBase.set('basic_faq', {
            id: 'basic_faq',
            title: 'Basic Frequently Asked Questions',
            content: {
                'company_info': 'OCINT (Onchain Intelligence) provides blockchain security and intelligence services.',
                'contact_methods': 'Support available via chat, email, and phone during business hours.',
                'service_hours': 'Monday-Friday 9 AM - 6 PM EST, emergency support available 24/7.',
                'escalation_process': 'Complex issues are automatically escalated to higher-tier agents.',
                'account_setup': 'Step-by-step guide for new client account setup.',
                'password_reset': 'Standard password reset procedures for client accounts.'
            },
            accessTier: 1,
            lastUpdated: Date.now(),
            tags: ['basic', 'faq', 'company_info'],
            contentOwner: 'support_team',
            reviewCycle: 'monthly',
            version: '1.0'
        });

        // Product Overview (Tier 1+)
        this.knowledgeBase.set('product_overview', {
            id: 'product_overview',
            title: 'Product and Service Overview',
            content: {
                'blockchain_security': 'Comprehensive blockchain security analysis and threat detection.',
                'crypto_theft_recovery': 'Specialized services for investigating and recovering stolen cryptocurrency.',
                'client_onboarding': 'Streamlined process for new client registration and service activation.',
                'consulting_services': 'Expert consultation on blockchain security and intelligence.',
                'service_tiers': 'Different service levels and what they include.',
                'pricing_information': 'Service pricing and billing information.'
            },
            accessTier: 1,
            lastUpdated: Date.now(),
            tags: ['products', 'services', 'overview'],
            contentOwner: 'product_team',
            reviewCycle: 'quarterly',
            version: '1.0'
        });

        // Technical Documentation (Tier 2+)
        this.knowledgeBase.set('technical_documentation', {
            id: 'technical_documentation',
            title: 'Technical Support Documentation',
            content: {
                'system_requirements': 'Minimum system requirements for our security tools and platforms.',
                'troubleshooting': 'Common technical issues and their solutions.',
                'integration_guides': 'Step-by-step guides for integrating our services.',
                'api_documentation': 'Technical API documentation for developers.',
                'error_codes': 'Common error codes and their meanings.',
                'performance_optimization': 'Tips for optimizing system performance.'
            },
            accessTier: 2,
            lastUpdated: Date.now(),
            tags: ['technical', 'documentation', 'support'],
            contentOwner: 'engineering_team',
            reviewCycle: 'monthly',
            version: '1.0'
        });

        // Billing Procedures (Tier 2+)
        this.knowledgeBase.set('billing_procedures', {
            id: 'billing_procedures',
            title: 'Billing and Payment Procedures',
            content: {
                'payment_methods': 'Accepted payment methods and processing times.',
                'billing_cycles': 'Billing frequency and invoice generation.',
                'refund_policy': 'Refund eligibility and processing procedures.',
                'dispute_resolution': 'How to resolve billing disputes and discrepancies.',
                'payment_processing': 'Step-by-step payment processing procedures.',
                'invoice_explanation': 'How to read and understand invoices.'
            },
            accessTier: 2,
            lastUpdated: Date.now(),
            tags: ['billing', 'payment', 'procedures'],
            contentOwner: 'finance_team',
            reviewCycle: 'quarterly',
            version: '1.0'
        });

        // Quality Assurance (Tier 3+)
        this.knowledgeBase.set('quality_assurance', {
            id: 'quality_assurance',
            title: 'Quality Assurance Procedures',
            content: {
                'qa_standards': 'Quality standards and evaluation criteria for agent performance.',
                'monitoring_procedures': 'Live and recorded call monitoring procedures.',
                'feedback_processes': 'How customer feedback is collected and used.',
                'improvement_methods': 'Methods for continuous improvement and training.',
                'scorecard_guidelines': 'How to use QA scorecards effectively.',
                'calibration_procedures': 'QA calibration and consistency procedures.'
            },
            accessTier: 3,
            lastUpdated: Date.now(),
            tags: ['quality', 'assurance', 'procedures'],
            contentOwner: 'qa_team',
            reviewCycle: 'monthly',
            version: '1.0'
        });

        // Management Information (Tier 4+)
        this.knowledgeBase.set('management_dashboard', {
            id: 'management_dashboard',
            title: 'Management Dashboard and Analytics',
            content: {
                'performance_metrics': 'Key performance indicators and team metrics.',
                'resource_allocation': 'Agent allocation and workload distribution.',
                'budget_tracking': 'Budget utilization and cost analysis.',
                'strategic_planning': 'Strategic initiatives and long-term planning.',
                'executive_reporting': 'How to create and present executive reports.',
                'team_development': 'Strategies for team growth and development.'
            },
            accessTier: 4,
            lastUpdated: Date.now(),
            tags: ['management', 'analytics', 'strategic'],
            contentOwner: 'management_team',
            reviewCycle: 'quarterly',
            version: '1.0'
        });

        // Internal Procedures (Tier 2+)
        this.knowledgeBase.set('internal_procedures', {
            id: 'internal_procedures',
            title: 'Internal Support Procedures',
            content: {
                'escalation_workflow': 'Step-by-step escalation procedures for each tier.',
                'case_management': 'How to properly manage and track support cases.',
                'knowledge_creation': 'Guidelines for creating and updating knowledge articles.',
                'team_collaboration': 'Best practices for working with other teams.',
                'incident_response': 'Procedures for handling critical incidents.',
                'change_management': 'Process for implementing system changes.'
            },
            accessTier: 2,
            lastUpdated: Date.now(),
            tags: ['internal', 'procedures', 'workflow'],
            contentOwner: 'operations_team',
            reviewCycle: 'monthly',
            version: '1.0'
        });
    }

    /**
     * Initialize escalation rules based on enterprise best practices
     */
    initializeEscalationRules() {
        // Automatic escalation rules
        this.escalationRules.set('urgent_issue', {
            id: 'urgent_issue',
            name: 'Urgent Issue Escalation',
            description: 'Automatically escalate urgent issues to higher tiers',
            triggers: ['crypto_theft', 'urgent_support', 'emergency', 'system_outage'],
            fromTier: 1,
            toTier: 2,
            priority: 'high',
            autoEscalate: true,
            notificationRequired: true,
            sla: 15 * 60 * 1000 // 15 minutes
        });

        this.escalationRules.set('complex_technical', {
            id: 'complex_technical',
            name: 'Complex Technical Issue',
            description: 'Escalate complex technical issues to specialized agents',
            triggers: ['technical_complexity', 'system_error', 'integration_issue', 'bug_report'],
            fromTier: 1,
            toTier: 2,
            priority: 'medium',
            autoEscalate: false,
            notificationRequired: true,
            sla: 60 * 60 * 1000 // 1 hour
        });

        this.escalationRules.set('customer_complaint', {
            id: 'customer_complaint',
            name: 'Customer Complaint',
            description: 'Escalate customer complaints to supervisors',
            triggers: ['customer_frustration', 'formal_complaint', 'escalation_request', 'negative_sentiment'],
            fromTier: 1,
            toTier: 3,
            priority: 'high',
            autoEscalate: true,
            notificationRequired: true,
            sla: 30 * 60 * 1000 // 30 minutes
        });

        this.escalationRules.set('legal_issue', {
            id: 'legal_issue',
            name: 'Legal Issue',
            description: 'Escalate legal issues to management',
            triggers: ['legal_question', 'legal_threat', 'compliance_concern', 'regulatory_issue'],
            fromTier: 1,
            toTier: 4,
            priority: 'critical',
            autoEscalate: true,
            notificationRequired: true,
            sla: 5 * 60 * 1000 // 5 minutes
        });

        this.escalationRules.set('billing_dispute', {
            id: 'billing_dispute',
            name: 'Billing Dispute',
            description: 'Escalate billing disputes to specialized team',
            triggers: ['billing_dispute', 'payment_issue', 'refund_request', 'pricing_concern'],
            fromTier: 1,
            toTier: 2,
            priority: 'medium',
            autoEscalate: false,
            notificationRequired: true,
            sla: 120 * 60 * 1000 // 2 hours
        });
    }

    /**
     * Create a new agent with enterprise-grade configuration
     */
    createAgent(agentData) {
        const agentId = this.generateAgentId();
        const timestamp = Date.now();
        
        // Validate agent tier
        if (!this.agentTiers.has(agentData.tier)) {
            console.error(`Invalid agent tier: ${agentData.tier}`);
            return null;
        }

        const tierConfig = this.agentTiers.get(agentData.tier);
        
        const agent = {
            agentId,
            name: agentData.name || 'Agent',
            email: agentData.email || '',
            tier: agentData.tier || 1,
            status: 'available', // available, busy, offline, training, break
            currentSessionId: null,
            skills: agentData.skills || [],
            training: agentData.training || [],
            certifications: agentData.certifications || [],
            performance: {
                totalSessions: 0,
                resolvedSessions: 0,
                escalatedSessions: 0,
                averageResolutionTime: 0,
                customerSatisfaction: 0,
                qualityScore: 0,
                firstContactResolution: 0,
                averageHandleTime: 0
            },
            availability: {
                startTime: agentData.startTime || '09:00',
                endTime: agentData.endTime || '17:00',
                timezone: agentData.timezone || 'EST',
                workingDays: agentData.workingDays || ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
                maxConcurrentSessions: tierConfig.maxSessionDuration ? 1 : 3
            },
            knowledgeAccess: this.getKnowledgeAccessForTier(agentData.tier),
            escalationAuthority: this.getEscalationAuthorityForTier(agentData.tier),
            createdAt: timestamp,
            lastActive: timestamp,
            metadata: agentData.metadata || {},
            qaHistory: [],
            trainingHistory: [],
            supervisorId: agentData.supervisorId || null
        };

        this.agents.set(agentId, agent);
        
        // Dispatch event
        this.dispatchEvent('agentCreated', { agent });
        
        return agentId;
    }

    /**
     * Get knowledge access permissions for a specific tier
     */
    getKnowledgeAccessForTier(tier) {
        const access = [];
        for (const [knowledgeId, knowledge] of this.knowledgeBase) {
            if (knowledge.accessTier <= tier) {
                access.push({
                    knowledgeId,
                    accessLevel: 'read',
                    canEdit: tier >= 3, // Only Tier 3+ can edit
                    canApprove: tier >= 4 // Only Tier 4+ can approve
                });
            }
        }
        return access;
    }

    /**
     * Get escalation authority for a specific tier
     */
    getEscalationAuthorityForTier(tier) {
        const authority = {
            canEscalateTo: [],
            canApproveEscalations: false,
            canOverridePolicies: false,
            maxCompensation: 0
        };

        switch (tier) {
            case 1:
                authority.canEscalateTo = [2, 3, 4];
                authority.canApproveEscalations = false;
                authority.canOverridePolicies = false;
                authority.maxCompensation = 0;
                break;
            case 2:
                authority.canEscalateTo = [3, 4];
                authority.canApproveEscalations = false;
                authority.canOverridePolicies = false;
                authority.maxCompensation = 50;
                break;
            case 3:
                authority.canEscalateTo = [4];
                authority.canApproveEscalations = true;
                authority.canOverridePolicies = true;
                authority.maxCompensation = 200;
                break;
            case 4:
                authority.canEscalateTo = [];
                authority.canApproveEscalations = true;
                authority.canOverridePolicies = true;
                authority.maxCompensation = 1000;
                break;
        }

        return authority;
    }

    /**
     * Handle session escalation based on enterprise best practices
     */
    handleEscalation(sessionId, reason) {
        const session = this.getSession(sessionId);
        if (!session) return false;

        // Find appropriate escalation rule
        const escalationRule = this.findEscalationRule(reason);
        if (!escalationRule) {
            console.warn(`No escalation rule found for reason: ${reason}`);
            return false;
        }

        // Check if current agent can escalate
        const currentAgent = this.agents.get(session.agentId);
        if (!currentAgent) return false;

        const authority = this.getEscalationAuthorityForTier(currentAgent.tier);
        if (!authority.canEscalateTo.includes(escalationRule.toTier)) {
            console.warn(`Agent tier ${currentAgent.tier} cannot escalate to tier ${escalationRule.toTier}`);
            return false;
        }

        // Perform escalation
        const oldTier = session.tier;
        session.tier = escalationRule.toTier;
        session.escalationHistory.push({
            timestamp: Date.now(),
            reason: reason,
            fromTier: oldTier,
            toTier: escalationRule.toTier,
            escalatedBy: currentAgent.agentId,
            escalationRule: escalationRule.id,
            priority: escalationRule.priority,
            sla: escalationRule.sla
        });

        // Update session status
        session.status = 'escalated';
        session.escalationReason = reason;
        session.escalationTimestamp = Date.now();
        session.escalationSLA = escalationRule.sla;

        // Find available agent at higher tier
        const availableAgent = this.findAvailableAgentByTier(escalationRule.toTier);
        if (availableAgent) {
            session.agentId = availableAgent.agentId;
            session.status = 'active';
            session.assignedAt = Date.now();
        }

        // Dispatch event
        this.dispatchEvent('sessionEscalated', { 
            sessionId, 
            reason, 
            newTier: session.tier,
            escalationRule: escalationRule,
            assignedAgent: session.agentId
        });

        return true;
    }

    /**
     * Find appropriate escalation rule for a given reason
     */
    findEscalationRule(reason) {
        for (const [ruleId, rule] of this.escalationRules) {
            if (rule.triggers.some(trigger => 
                reason.toLowerCase().includes(trigger.toLowerCase())
            )) {
                return rule;
            }
        }
        return null;
    }

    /**
     * Find available agent by tier
     */
    findAvailableAgentByTier(tier) {
        for (const [agentId, agent] of this.agents) {
            if (agent.tier === tier && agent.status === 'available') {
                return agent;
            }
        }
        return null;
    }

    /**
     * Get agent performance metrics
     */
    getAgentPerformance(agentId) {
        const agent = this.agents.get(agentId);
        if (!agent) return null;

        const tierConfig = this.agentTiers.get(agent.tier);
        const performance = { ...agent.performance };

        // Calculate performance against targets
        if (tierConfig.targetFCR) {
            performance.fcrTarget = tierConfig.targetFCR;
            performance.fcrGap = tierConfig.targetFCR - performance.firstContactResolution;
        }

        if (tierConfig.targetAHT) {
            performance.ahtTarget = tierConfig.targetAHT;
            performance.ahtGap = performance.averageHandleTime - tierConfig.targetAHT;
        }

        // Calculate quality score
        performance.qualityScore = this.calculateQualityScore(agent);

        return performance;
    }

    /**
     * Calculate agent quality score based on multiple factors
     */
    calculateQualityScore(agent) {
        let score = 0;
        let totalWeight = 0;

        // Customer satisfaction (30% weight)
        score += (agent.performance.customerSatisfaction / 5) * 30;
        totalWeight += 30;

        // First contact resolution (25% weight)
        score += agent.performance.firstContactResolution * 25;
        totalWeight += 25;

        // Quality from QA evaluations (25% weight)
        score += (agent.performance.qualityScore / 100) * 25;
        totalWeight += 25;

        // Efficiency (20% weight) - inverse of escalation rate
        const escalationRate = agent.performance.escalatedSessions / Math.max(agent.performance.totalSessions, 1);
        score += (1 - escalationRate) * 20;
        totalWeight += 20;

        return totalWeight > 0 ? Math.round(score) : 0;
    }

    /**
     * Get all agents with performance data
     */
    getAllAgentsWithPerformance() {
        const agentsWithPerformance = [];
        
        for (const [agentId, agent] of this.agents) {
            const performance = this.getAgentPerformance(agentId);
            agentsWithPerformance.push({
                ...agent,
                performance: performance
            });
        }

        return agentsWithPerformance.sort((a, b) => b.performance.qualityScore - a.performance.qualityScore);
    }

    /**
     * Get agents by tier with performance data
     */
    getAgentsByTierWithPerformance(tier) {
        return this.getAllAgentsWithPerformance().filter(agent => agent.tier === tier);
    }

    /**
     * Update agent status
     */
    updateAgentStatus(agentId, status) {
        const agent = this.agents.get(agentId);
        if (!agent) return false;
        
        agent.status = status;
        agent.lastActive = Date.now();
        
        // Dispatch event
        this.dispatchEvent('agentStatusUpdated', { agentId, status, agent });
        
        return true;
    }

    /**
     * Assign session to agent
     */
    assignSessionToAgent(sessionId, agentId) {
        const agent = this.agents.get(agentId);
        const session = this.getSession(sessionId);
        
        if (!agent || !session) return false;

        // Check if agent can handle this tier
        if (agent.tier < session.tier) {
            console.warn(`Agent tier ${agent.tier} cannot handle session tier ${session.tier}`);
            return false;
        }

        // Check agent availability
        if (agent.status !== 'available') {
            console.warn(`Agent ${agentId} is not available (status: ${agent.status})`);
            return false;
        }

        // Check concurrent session limits
        if (agent.currentSessionId && agent.availability.maxConcurrentSessions <= 1) {
            console.warn(`Agent ${agentId} is already handling a session`);
            return false;
        }

        // Assign session
        session.agentId = agentId;
        session.status = 'active';
        session.assignedAt = Date.now();
        
        agent.currentSessionId = sessionId;
        agent.status = 'busy';
        agent.lastAssigned = Date.now();

        // Dispatch event
        this.dispatchEvent('sessionAssignedToAgent', { sessionId, agentId, session, agent });
        
        return true;
    }

    /**
     * Get session by ID
     */
    getSession(sessionId) {
        // This would typically come from the queue system
        // For now, return a mock session
        return {
            sessionId,
            tier: 1,
            status: 'waiting',
            agentId: null,
            escalationHistory: []
        };
    }

    /**
     * Generate unique agent ID
     */
    generateAgentId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `agent_${timestamp}_${random}`;
    }

    /**
     * Get agent by ID
     */
    getAgent(agentId) {
        return this.agents.get(agentId);
    }

    /**
     * Get all agents
     */
    getAllAgents() {
        return Array.from(this.agents.values());
    }

    /**
     * Get agents by tier
     */
    getAgentsByTier(tier) {
        return Array.from(this.agents.values()).filter(agent => agent.tier === tier);
    }

    /**
     * Get available agents by tier
     */
    getAvailableAgentsByTier(tier) {
        return this.getAgentsByTier(tier).filter(agent => agent.status === 'available');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Listen for agent creation
        document.addEventListener('agentCreated', (e) => {
            this.createAgent(e.detail.agentData);
        });

        // Listen for session escalations
        document.addEventListener('sessionEscalated', (e) => {
            this.handleEscalation(e.detail.sessionId, e.detail.reason);
        });

        // Listen for knowledge requests
        document.addEventListener('knowledgeRequested', (e) => {
            this.provideKnowledge(e.detail.agentId, e.detail.topic, e.detail.tier);
        });
    }

    /**
     * Provide knowledge to agent based on tier and topic
     */
    provideKnowledge(agentId, topic, tier) {
        const agent = this.agents.get(agentId);
        if (!agent) return null;

        // Filter knowledge based on agent's tier access
        const accessibleKnowledge = Array.from(this.knowledgeBase.values())
            .filter(knowledge => knowledge.accessTier <= agent.tier)
            .filter(knowledge => 
                knowledge.title.toLowerCase().includes(topic.toLowerCase()) ||
                knowledge.tags.some(tag => tag.toLowerCase().includes(topic.toLowerCase()))
            );

        return accessibleKnowledge;
    }

    /**
     * Dispatch custom events
     */
    dispatchEvent(eventName, detail) {
        const event = new CustomEvent(eventName, { detail });
        document.dispatchEvent(event);
    }

    /**
     * Export agent system data
     */
    exportAgentSystemData() {
        return {
            agents: Array.from(this.agents.values()),
            agentTiers: Array.from(this.agentTiers.values()),
            knowledgeBase: Array.from(this.knowledgeBase.values()),
            escalationRules: Array.from(this.escalationRules.values()),
            qaSystem: this.qaSystem,
            exportTimestamp: Date.now()
        };
    }

    /**
     * Get system status and health
     */
    getSystemStatus() {
        const totalAgents = this.agents.size;
        const availableAgents = Array.from(this.agents.values()).filter(a => a.status === 'available').length;
        const busyAgents = Array.from(this.agents.values()).filter(a => a.status === 'busy').length;
        
        const tierDistribution = {};
        for (let i = 0; i <= 4; i++) {
            tierDistribution[i] = this.getAgentsByTier(i).length;
        }

        return {
            totalAgents,
            availableAgents,
            busyAgents,
            tierDistribution,
            systemHealth: availableAgents > 0 ? 'healthy' : 'degraded',
            lastUpdated: Date.now()
        };
    }
}

// Export for use in other modules
window.TieredAgentSystem = TieredAgentSystem;
