/**
 * App Prompt Engine for AI Intake/Support Agent Demo
 * Handles agent identity, persona management, context handling, and guardrails
 */

class AppPromptEngine {
    constructor() {
        this.templates = new Map();
        this.personas = new Map();
        this.contextManager = null;
        this.guardrailSystem = null;
        this.performanceMetrics = new Map();
        
        this.init();
    }

    init() {
        this.initializeTemplates();
        this.initializePersonas();
        this.setupEventListeners();
        this.loadConfiguration();
    }

    /**
     * Initialize prompt templates
     */
    initializeTemplates() {
        // Customer Greeting Template
        this.templates.set('customer_greeting', {
            id: 'customer_greeting',
            name: 'Customer Greeting',
            type: 'system',
            content: 'Hello {{customer_name}}! Welcome to {{company_name}} support. I\'m {{agent_name}}, your {{agent_role}}. How can I assist you today?',
            variables: [
                { name: 'customer_name', type: 'string', required: true },
                { name: 'company_name', type: 'string', required: true },
                { name: 'agent_name', type: 'string', required: true },
                { name: 'agent_role', type: 'string', required: true }
            ],
            persona_requirements: ['tier1_customer_service', 'tier2_technical_support'],
            guardrail_level: 'low',
            performance_metrics: { expected_response_time: 2.0, quality_threshold: 0.8 }
        });

        // Technical Issue Response Template
        this.templates.set('technical_issue_response', {
            id: 'technical_issue_response',
            name: 'Technical Issue Response',
            type: 'assistant',
            content: 'I understand you\'re experiencing a technical issue with {{issue_description}}. Let me help you troubleshoot this step by step. First, let\'s verify {{first_step}}. Can you confirm if {{verification_question}}?',
            variables: [
                { name: 'issue_description', type: 'string', required: true },
                { name: 'first_step', type: 'string', required: true },
                { name: 'verification_question', type: 'string', required: true }
            ],
            persona_requirements: ['tier2_technical_support', 'tier3_senior_specialist'],
            guardrail_level: 'medium',
            performance_metrics: { expected_response_time: 5.0, quality_threshold: 0.9 }
        });

        // Escalation Notice Template
        this.templates.set('escalation_notice', {
            id: 'escalation_notice',
            name: 'Escalation Notice',
            type: 'system',
            content: 'I understand this issue requires specialized attention. I\'m escalating your case to our {{escalation_team}} team. {{escalation_reason}}. You\'ll be contacted by {{escalation_timeframe}} with a resolution or next steps.',
            variables: [
                { name: 'escalation_team', type: 'string', required: true },
                { name: 'escalation_reason', type: 'string', required: true },
                { name: 'escalation_timeframe', type: 'string', required: true }
            ],
            persona_requirements: ['tier1_customer_service', 'tier2_technical_support'],
            guardrail_level: 'high',
            performance_metrics: { expected_response_time: 3.0, quality_threshold: 0.95 }
        });

        // Crypto Theft Response Template
        this.templates.set('crypto_theft_response', {
            id: 'crypto_theft_response',
            name: 'Crypto Theft Response',
            type: 'assistant',
            content: 'I understand this is a critical situation regarding cryptocurrency theft. This requires immediate attention from our specialized recovery team. I\'m escalating your case to our {{escalation_team}} immediately. {{escalation_reason}}. You\'ll receive a call from our specialist within {{escalation_timeframe}}.',
            variables: [
                { name: 'escalation_team', type: 'string', required: true },
                { name: 'escalation_reason', type: 'string', required: true },
                { name: 'escalation_timeframe', type: 'string', required: true }
            ],
            persona_requirements: ['tier1_customer_service'],
            guardrail_level: 'critical',
            performance_metrics: { expected_response_time: 1.0, quality_threshold: 0.98 }
        });

        // Client Onboarding Template
        this.templates.set('client_onboarding', {
            id: 'client_onboarding',
            name: 'Client Onboarding',
            type: 'assistant',
            content: 'Welcome to {{company_name}}! I\'m excited to help you get started with our services. Let me gather some information to create your account. First, I\'ll need {{first_requirement}}. Then we can proceed with {{next_step}}.',
            variables: [
                { name: 'company_name', type: 'string', required: true },
                { name: 'first_requirement', type: 'string', required: true },
                { name: 'next_step', type: 'string', required: true }
            ],
            persona_requirements: ['tier1_customer_service', 'tier2_technical_support'],
            guardrail_level: 'low',
            performance_metrics: { expected_response_time: 3.0, quality_threshold: 0.85 }
        });
    }

    /**
     * Initialize persona profiles
     */
    initializePersonas() {
        // Tier 1 Customer Service Agent
        this.personas.set('tier1_customer_service', {
            id: 'tier1_customer_service',
            name: 'Tier 1 Customer Service Agent',
            type: 'customer_service',
            description: 'Entry-level customer service agent with basic support capabilities',
            personality_traits: ['helpful', 'patient', 'professional', 'empathetic'],
            expertise_areas: ['basic_support', 'escalation_procedures', 'company_policies'],
            response_style: 'friendly_professional',
            formality_level: 'professional',
            emoji_usage: 'minimal',
            response_length: 'concise',
            tone: 'helpful_and_supportive',
            limitations: ['no_technical_details', 'no_financial_advice', 'escalation_required_for_complex_issues'],
            escalation_triggers: ['technical_issues', 'financial_concerns', 'complaints', 'escalation_requests'],
            knowledge_access: ['basic_faq', 'company_info', 'escalation_procedures']
        });

        // Tier 2 Technical Support Specialist
        this.personas.set('tier2_technical_support', {
            id: 'tier2_technical_support',
            name: 'Tier 2 Technical Support Specialist',
            type: 'technical_support',
            description: 'Intermediate technical support specialist with advanced troubleshooting capabilities',
            personality_traits: ['technical', 'analytical', 'helpful', 'thorough'],
            expertise_areas: ['technical_support', 'troubleshooting', 'system_configuration', 'advanced_issues'],
            response_style: 'technical_friendly',
            formality_level: 'friendly_professional',
            emoji_usage: 'moderate',
            response_length: 'detailed',
            tone: 'technical_and_helpful',
            limitations: ['no_system_administration', 'limited_financial_authority'],
            escalation_triggers: ['system_administration', 'complex_technical_issues', 'management_approval'],
            knowledge_access: ['technical_documentation', 'troubleshooting_guides', 'system_requirements']
        });

        // Tier 3 Senior Specialist
        this.personas.set('tier3_senior_specialist', {
            id: 'tier3_senior_specialist',
            name: 'Tier 3 Senior Specialist',
            type: 'specialist',
            description: 'Senior specialist with expert-level knowledge and complex issue resolution capabilities',
            personality_traits: ['expert', 'confident', 'helpful', 'efficient'],
            expertise_areas: ['complex_issue_resolution', 'quality_assurance', 'agent_training', 'process_improvement'],
            response_style: 'expert_friendly',
            formality_level: 'expert_friendly',
            emoji_usage: 'appropriate',
            response_length: 'comprehensive',
            tone: 'expert_and_helpful',
            limitations: ['no_legal_advice', 'compliance_with_company_policies'],
            escalation_triggers: ['legal_issues', 'compliance_violations', 'management_approval'],
            knowledge_access: ['full_system_access', 'quality_assurance_tools', 'training_materials']
        });
    }

    setupEventListeners() {
        // Listen for prompt generation requests
        document.addEventListener('promptGenerationRequested', (e) => {
            this.handlePromptGeneration(e.detail);
        });

        // Listen for persona changes
        document.addEventListener('personaChanged', (e) => {
            this.handlePersonaChange(e.detail);
        });

        // Listen for context updates
        document.addEventListener('contextUpdated', (e) => {
            this.handleContextUpdate(e.detail);
        });
    }

    /**
     * Generate prompt using template and context
     */
    generatePrompt(templateId, context, personaId, variables = {}) {
        const startTime = Date.now();
        
        try {
            // Validate inputs
            if (!this.templates.has(templateId)) {
                throw new Error(`Template ${templateId} not found`);
            }
            
            if (!this.personas.has(personaId)) {
                throw new Error(`Persona ${personaId} not found`);
            }
            
            const template = this.templates.get(templateId);
            const persona = this.personas.get(personaId);
            
            // Validate persona requirements
            if (!this.validatePersonaRequirements(template, persona)) {
                throw new Error(`Persona ${personaId} does not meet requirements for template ${templateId}`);
            }
            
            // Merge variables with context
            const mergedVariables = this.mergeVariablesWithContext(template, context, variables);
            
            // Generate prompt content
            let promptContent = this.replaceVariables(template.content, mergedVariables);
            
            // Apply persona characteristics
            promptContent = this.applyPersonaCharacteristics(promptContent, persona);
            
            // Apply guardrails
            const guardrailResult = this.applyGuardrails(promptContent, template.guardrail_level, context);
            
            // Generate metadata
            const metadata = {
                template_id: templateId,
                persona_id: personaId,
                variables_used: mergedVariables,
                guardrail_result: guardrailResult,
                generation_time: Date.now() - startTime,
                timestamp: new Date().toISOString(),
                version: '1.0'
            };
            
            // Update performance metrics
            this.updatePerformanceMetrics(templateId, metadata);
            
            return { prompt: promptContent, metadata };
            
        } catch (error) {
            console.error('Failed to generate prompt:', error);
            
            // Return fallback prompt
            const fallbackPrompt = this.generateFallbackPrompt(context, personaId);
            const metadata = {
                error: error.message,
                fallback_used: true,
                generation_time: Date.now() - startTime,
                timestamp: new Date().toISOString()
            };
            
            return { prompt: fallbackPrompt, metadata };
        }
    }

    /**
     * Validate persona requirements
     */
    validatePersonaRequirements(template, persona) {
        if (!template.persona_requirements || template.persona_requirements.length === 0) {
            return true;
        }
        
        return template.persona_requirements.includes(persona.id);
    }

    /**
     * Merge variables with context
     */
    mergeVariablesWithContext(template, context, variables) {
        const merged = {};
        
        // Add context data
        if (context.customer_profile) {
            Object.assign(merged, context.customer_profile);
        }
        
        // Add session context
        Object.assign(merged, {
            session_id: context.session_id,
            current_topic: context.current_topic,
            customer_intent: context.customer_intent,
            escalation_level: context.escalation_level,
            agent_tier: context.agent_tier
        });
        
        // Add provided variables
        Object.assign(merged, variables);
        
        // Add default values for missing required variables
        for (const var_def of template.variables) {
            if (var_def.required && !(var_def.name in merged)) {
                merged[var_def.name] = this.getDefaultValue(var_def);
            }
        }
        
        return merged;
    }

    /**
     * Get default value for a variable
     */
    getDefaultValue(varDef) {
        const varType = varDef.type || 'string';
        
        switch (varType) {
            case 'string':
                return varDef.default || '';
            case 'number':
                return varDef.default || 0;
            case 'boolean':
                return varDef.default || false;
            case 'list':
                return varDef.default || [];
            default:
                return varDef.default || '';
        }
    }

    /**
     * Replace variables in template content
     */
    replaceVariables(content, variables) {
        for (const [varName, varValue] of Object.entries(variables)) {
            const placeholder = `{{${varName}}}`;
            if (content.includes(placeholder)) {
                content = content.replace(new RegExp(placeholder, 'g'), String(varValue));
            }
        }
        
        return content;
    }

    /**
     * Apply persona characteristics to content
     */
    applyPersonaCharacteristics(content, persona) {
        // Apply formality level
        switch (persona.formality_level) {
            case 'professional':
                content = this.makeProfessional(content);
                break;
            case 'friendly_professional':
                content = this.makeFriendlyProfessional(content);
                break;
            case 'expert_friendly':
                content = this.makeExpertFriendly(content);
                break;
        }
        
        // Apply response length preferences
        switch (persona.response_length) {
            case 'concise':
                content = this.makeConcise(content);
                break;
            case 'comprehensive':
                content = this.makeComprehensive(content);
                break;
        }
        
        // Apply tone adjustments
        switch (persona.tone) {
            case 'helpful_and_supportive':
                content = this.addHelpfulTone(content);
                break;
            case 'technical_and_helpful':
                content = this.addTechnicalTone(content);
                break;
        }
        
        return content;
    }

    /**
     * Make content more professional
     */
    makeProfessional(content) {
        content = content.trim();
        if (content && !content.match(/[.!?]$/)) {
            content += '.';
        }
        return content;
    }

    /**
     * Make content friendly but professional
     */
    makeFriendlyProfessional(content) {
        content = this.makeProfessional(content);
        
        const friendlyPrefixes = [
            'I understand your concern',
            'Let me help you with that',
            'I appreciate you bringing this to our attention'
        ];
        
        if (!friendlyPrefixes.some(prefix => content.toLowerCase().includes(prefix.toLowerCase()))) {
            content = `${friendlyPrefixes[0]}. ${content}`;
        }
        
        return content;
    }

    /**
     * Make content expert-friendly
     */
    makeExpertFriendly(content) {
        content = this.makeFriendlyProfessional(content);
        
        const expertPrefixes = [
            'Based on my experience',
            'From what I can see',
            'Let me analyze this for you'
        ];
        
        if (!expertPrefixes.some(prefix => content.toLowerCase().includes(prefix.toLowerCase()))) {
            content = `${expertPrefixes[0]}, ${content}`;
        }
        
        return content;
    }

    /**
     * Make content more concise
     */
    makeConcise(content) {
        const unnecessaryPhrases = [
            'I would like to inform you that',
            'Please be advised that',
            'It is important to note that'
        ];
        
        for (const phrase of unnecessaryPhrases) {
            content = content.replace(phrase, '');
        }
        
        return content.trim();
    }

    /**
     * Make content more comprehensive
     */
    makeComprehensive(content) {
        if (content.toLowerCase().includes('troubleshoot')) {
            content += ' I\'ll guide you through each step to ensure we resolve this completely.';
        }
        
        return content;
    }

    /**
     * Add helpful tone to content
     */
    addHelpfulTone(content) {
        const helpfulWords = ['help', 'assist', 'support'];
        if (!helpfulWords.some(word => content.toLowerCase().includes(word))) {
            content += ' I\'m here to help you resolve this issue.';
        }
        
        return content;
    }

    /**
     * Add technical tone to content
     */
    addTechnicalTone(content) {
        if (content.toLowerCase().includes('issue') && !content.toLowerCase().includes('technical')) {
            content = content.replace(/issue/gi, 'technical issue');
        }
        
        return content;
    }

    /**
     * Apply guardrails to content
     */
    applyGuardrails(content, guardrailLevel, context) {
        const violations = [];
        let riskLevel = 'low';
        let requiresEscalation = false;
        let escalationReason = '';
        
        // Content safety checks
        if (this.containsInappropriateContent(content)) {
            violations.push('inappropriate_content');
            riskLevel = 'high';
            requiresEscalation = true;
            escalationReason = 'Inappropriate content detected';
        }
        
        // Compliance checks
        if (this.violatesCompliance(content, context)) {
            violations.push('compliance_violation');
            riskLevel = 'critical';
            requiresEscalation = true;
            escalationReason = 'Compliance violation detected';
        }
        
        // Escalation level checks
        if (context.escalation_level >= 3) {
            violations.push('high_escalation_level');
            riskLevel = 'high';
            requiresEscalation = true;
            escalationReason = 'High escalation level reached';
        }
        
        // Agent tier capability checks
        if (!this.validateAgentCapabilities(content, context)) {
            violations.push('capability_exceeded');
            riskLevel = 'medium';
            requiresEscalation = true;
            escalationReason = 'Agent capability exceeded';
        }
        
        const passed = violations.length === 0;
        const recommendations = this.generateGuardrailRecommendations(violations, content, context);
        
        return {
            passed,
            violations,
            risk_level: riskLevel,
            recommendations,
            requires_escalation: requiresEscalation,
            escalation_reason: escalationReason
        };
    }

    /**
     * Check if content contains inappropriate material
     */
    containsInappropriateContent(content) {
        const inappropriatePatterns = [
            /\b(hate|racist|discriminatory)\b/i,
            /\b(violence|threat|harm)\b/i,
            /\b(inappropriate|offensive)\b/i
        ];
        
        return inappropriatePatterns.some(pattern => pattern.test(content));
    }

    /**
     * Check if content violates compliance requirements
     */
    violatesCompliance(content, context) {
        // Check for financial advice if agent tier is too low
        if (context.agent_tier < 2 && /(investment|financial|money|profit)/i.test(content)) {
            return true;
        }
        
        // Check for legal advice if agent tier is too low
        if (context.agent_tier < 3 && /(legal|law|attorney|court)/i.test(content)) {
            return true;
        }
        
        return false;
    }

    /**
     * Validate if agent has capabilities for the content
     */
    validateAgentCapabilities(content, context) {
        // Check if agent can handle technical issues
        if (context.agent_tier < 2 && /(technical|system|configuration|admin)/i.test(content)) {
            return false;
        }
        
        // Check if agent can handle complex issues
        if (context.agent_tier < 3 && /(complex|advanced|expert|specialized)/i.test(content)) {
            return false;
        }
        
        return true;
    }

    /**
     * Generate recommendations for guardrail violations
     */
    generateGuardrailRecommendations(violations, content, context) {
        const recommendations = [];
        
        for (const violation of violations) {
            switch (violation) {
                case 'inappropriate_content':
                    recommendations.push('Review and revise content to remove inappropriate language');
                    break;
                case 'compliance_violation':
                    recommendations.push('Escalate to appropriate tier agent for compliance-sensitive content');
                    break;
                case 'high_escalation_level':
                    recommendations.push('Immediate escalation to senior agent or supervisor required');
                    break;
                case 'capability_exceeded':
                    recommendations.push('Transfer to agent with appropriate capabilities and training');
                    break;
            }
        }
        
        return recommendations;
    }

    /**
     * Generate fallback prompt if template generation fails
     */
    generateFallbackPrompt(context, personaId) {
        return 'I apologize for the technical difficulty. I\'m here to help you with your inquiry. How can I assist you today?';
    }

    /**
     * Update performance metrics
     */
    updatePerformanceMetrics(templateId, metadata) {
        if (!this.performanceMetrics.has(templateId)) {
            this.performanceMetrics.set(templateId, {
                total_generations: 0,
                successful_generations: 0,
                failed_generations: 0,
                average_generation_time: 0.0,
                total_generation_time: 0.0
            });
        }
        
        const metrics = this.performanceMetrics.get(templateId);
        metrics.total_generations += 1;
        
        if (!metadata.error) {
            metrics.successful_generations += 1;
        } else {
            metrics.failed_generations += 1;
        }
        
        const generationTime = metadata.generation_time || 0;
        metrics.total_generation_time += generationTime;
        metrics.average_generation_time = metrics.total_generation_time / metrics.total_generations;
    }

    /**
     * Handle prompt generation requests
     */
    handlePromptGeneration(detail) {
        const { templateId, context, personaId, variables } = detail;
        const result = this.generatePrompt(templateId, context, personaId, variables);
        
        // Dispatch result event
        this.dispatchEvent('promptGenerated', result);
    }

    /**
     * Handle persona changes
     */
    handlePersonaChange(detail) {
        const { sessionId, newPersonaId } = detail;
        
        // Update context with new persona
        if (this.contextManager) {
            this.contextManager.updatePersona(sessionId, newPersonaId);
        }
        
        // Dispatch event
        this.dispatchEvent('personaUpdated', detail);
    }

    /**
     * Handle context updates
     */
    handleContextUpdate(detail) {
        const { sessionId, context } = detail;
        
        // Update local context cache
        this.contextCache.set(sessionId, context);
        
        // Dispatch event
        this.dispatchEvent('contextUpdated', detail);
    }

    /**
     * Dispatch custom events
     */
    dispatchEvent(eventName, detail) {
        const event = new CustomEvent(eventName, { detail });
        document.dispatchEvent(event);
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return Object.fromEntries(this.performanceMetrics);
    }

    /**
     * Get available templates
     */
    getAvailableTemplates() {
        return Array.from(this.templates.keys());
    }

    /**
     * Get available personas
     */
    getAvailablePersonas() {
        return Array.from(this.personas.keys());
    }

    /**
     * Add new template
     */
    addTemplate(template) {
        this.templates.set(template.id, template);
        console.log(`Added template: ${template.id}`);
    }

    /**
     * Add new persona
     */
    addPersona(persona) {
        this.personas.set(persona.id, persona);
        console.log(`Added persona: ${persona.id}`);
    }

    /**
     * Export configuration
     */
    exportConfiguration() {
        return {
            templates: Object.fromEntries(this.templates),
            personas: Object.fromEntries(this.personas),
            performance_metrics: this.getPerformanceMetrics(),
            export_timestamp: new Date().toISOString(),
            version: '1.0'
        };
    }
}

// Export for use in other modules
window.AppPromptEngine = AppPromptEngine;
