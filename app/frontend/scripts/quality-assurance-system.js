/**
 * Quality Assurance System for AI Intake/Support Agent Demo
 * Based on Enterprise Contact Center Research Findings
 * Implements comprehensive QA processes, scoring systems, and monitoring
 */

class QualityAssuranceSystem {
    constructor() {
        this.scorecards = new Map(); // scorecardId -> scorecard data
        this.evaluations = new Map(); // evaluationId -> evaluation data
        this.qualityMetrics = new Map(); // metricId -> metric data
        this.calibrationSessions = []; // calibration session history
        this.qualityIndex = 0; // overall quality index
        this.qaAgents = new Map(); // qaAgentId -> qa agent data
        
        this.init();
    }

    init() {
        this.initializeScorecards();
        this.initializeQualityMetrics();
        this.setupEventListeners();
        this.createDefaultQAAgents();
    }

    /**
     * Initialize QA scorecards based on enterprise best practices
     */
    initializeScorecards() {
        // General Support Scorecard (Tier 1)
        this.scorecards.set('general_support', {
            id: 'general_support',
            name: 'General Support Quality Scorecard',
            description: 'Quality evaluation criteria for Tier 1 support interactions',
            version: '1.0',
            lastUpdated: Date.now(),
            criteria: [
                {
                    id: 'greeting_and_opening',
                    name: 'Greeting and Call Opening',
                    description: 'Proper greeting, verification, and call opening procedures',
                    weight: 10,
                    maxScore: 10,
                    required: true,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Professional greeting used', points: 3 },
                        { name: 'Company name stated', points: 2 },
                        { name: 'Customer verification completed', points: 3 },
                        { name: 'Purpose of call confirmed', points: 2 }
                    ]
                },
                {
                    id: 'product_knowledge',
                    name: 'Product Knowledge and Accuracy',
                    description: 'Accuracy of information provided about products and services',
                    weight: 20,
                    maxScore: 20,
                    required: true,
                    autoFail: true,
                    subCriteria: [
                        { name: 'Correct product information', points: 8 },
                        { name: 'Accurate policy information', points: 6 },
                        { name: 'Proper procedure explanation', points: 6 }
                    ]
                },
                {
                    id: 'problem_solving',
                    name: 'Problem-Solving Skills',
                    description: 'Ability to diagnose and resolve customer issues',
                    weight: 25,
                    maxScore: 25,
                    required: true,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Proper issue diagnosis', points: 8 },
                        { name: 'Appropriate solution provided', points: 10 },
                        { name: 'Escalation when needed', points: 7 }
                    ]
                },
                {
                    id: 'communication_skills',
                    name: 'Communication Skills',
                    description: 'Clarity, tone, professionalism, and empathy',
                    weight: 20,
                    maxScore: 20,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Clear and concise communication', points: 5 },
                        { name: 'Professional tone maintained', points: 5 },
                        { name: 'Empathy demonstrated', points: 5 },
                        { name: 'Active listening shown', points: 5 }
                    ]
                },
                {
                    id: 'compliance_and_policies',
                    name: 'Compliance and Policy Adherence',
                    description: 'Following required procedures and compliance requirements',
                    weight: 15,
                    maxScore: 15,
                    required: true,
                    autoFail: true,
                    subCriteria: [
                        { name: 'Required disclosures given', points: 8 },
                        { name: 'Policy procedures followed', points: 7 }
                    ]
                },
                {
                    id: 'call_closure',
                    name: 'Call Closure and Follow-up',
                    description: 'Proper call closure and next steps confirmation',
                    weight: 10,
                    maxScore: 10,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Resolution confirmed', points: 4 },
                        { name: 'Next steps explained', points: 3 },
                        { name: 'Professional closing', points: 3 }
                    ]
                }
            ],
            passingScore: 85,
            autoFailCriteria: ['product_knowledge', 'compliance_and_policies']
        });

        // Technical Support Scorecard (Tier 2)
        this.scorecards.set('technical_support', {
            id: 'technical_support',
            name: 'Technical Support Quality Scorecard',
            description: 'Quality evaluation criteria for Tier 2 technical support',
            version: '1.0',
            lastUpdated: Date.now(),
            criteria: [
                {
                    id: 'technical_accuracy',
                    name: 'Technical Accuracy',
                    description: 'Accuracy of technical information and solutions',
                    weight: 25,
                    maxScore: 25,
                    required: true,
                    autoFail: true,
                    subCriteria: [
                        { name: 'Correct technical diagnosis', points: 10 },
                        { name: 'Accurate solution provided', points: 10 },
                        { name: 'Proper escalation criteria', points: 5 }
                    ]
                },
                {
                    id: 'troubleshooting_methodology',
                    name: 'Troubleshooting Methodology',
                    description: 'Systematic approach to problem resolution',
                    weight: 20,
                    maxScore: 20,
                    required: true,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Logical troubleshooting sequence', points: 8 },
                        { name: 'Appropriate tools used', points: 6 },
                        { name: 'Documentation maintained', points: 6 }
                    ]
                },
                {
                    id: 'knowledge_application',
                    name: 'Knowledge Application',
                    description: 'Effective use of knowledge base and resources',
                    weight: 15,
                    maxScore: 15,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Knowledge base utilized', points: 8 },
                        { name: 'Internal resources accessed', points: 7 }
                    ]
                },
                {
                    id: 'customer_education',
                    name: 'Customer Education',
                    description: 'Teaching customers to prevent future issues',
                    weight: 15,
                    maxScore: 15,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Prevention tips provided', points: 8 },
                        { name: 'Self-service options explained', points: 7 }
                    ]
                },
                {
                    id: 'escalation_handling',
                    name: 'Escalation Handling',
                    description: 'Proper escalation procedures and handoff',
                    weight: 15,
                    maxScore: 15,
                    required: true,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Escalation criteria met', points: 8 },
                        { name: 'Proper handoff completed', points: 7 }
                    ]
                },
                {
                    id: 'communication_skills',
                    name: 'Communication Skills',
                    description: 'Technical communication clarity and professionalism',
                    weight: 10,
                    maxScore: 10,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Technical concepts explained clearly', points: 5 },
                        { name: 'Professional communication maintained', points: 5 }
                    ]
                }
            ],
            passingScore: 88,
            autoFailCriteria: ['technical_accuracy']
        });

        // Senior Support Scorecard (Tier 3)
        this.scorecards.set('senior_support', {
            id: 'senior_support',
            name: 'Senior Support Quality Scorecard',
            description: 'Quality evaluation criteria for Tier 3 senior support',
            version: '1.0',
            lastUpdated: Date.now(),
            criteria: [
                {
                    id: 'expert_knowledge',
                    name: 'Expert Knowledge Application',
                    description: 'Demonstration of deep technical expertise',
                    weight: 25,
                    maxScore: 25,
                    required: true,
                    autoFail: true,
                    subCriteria: [
                        { name: 'Advanced technical knowledge', points: 10 },
                        { name: 'Innovative problem solving', points: 8 },
                        { name: 'Industry best practices', points: 7 }
                    ]
                },
                {
                    id: 'complex_resolution',
                    name: 'Complex Issue Resolution',
                    description: 'Ability to resolve complex, multi-faceted issues',
                    weight: 25,
                    maxScore: 25,
                    required: true,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Root cause analysis', points: 10 },
                        { name: 'Comprehensive solution design', points: 10 },
                        { name: 'Implementation oversight', points: 5 }
                    ]
                },
                {
                    id: 'knowledge_contribution',
                    name: 'Knowledge Contribution',
                    description: 'Contributing to knowledge base and team development',
                    weight: 20,
                    maxScore: 20,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Knowledge articles created/updated', points: 10 },
                        { name: 'Team training provided', points: 10 }
                    ]
                },
                {
                    id: 'process_improvement',
                    name: 'Process Improvement',
                    description: 'Identifying and implementing process improvements',
                    weight: 15,
                    maxScore: 15,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Process gaps identified', points: 8 },
                        { name: 'Improvement suggestions', points: 7 }
                    ]
                },
                {
                    id: 'mentoring',
                    name: 'Mentoring and Support',
                    description: 'Supporting and mentoring lower-tier agents',
                    weight: 15,
                    maxScore: 15,
                    required: false,
                    autoFail: false,
                    subCriteria: [
                        { name: 'Agent guidance provided', points: 8 },
                        { name: 'Best practices shared', points: 7 }
                    ]
                }
            ],
            passingScore: 90,
            autoFailCriteria: ['expert_knowledge']
        });
    }

    /**
     * Initialize quality metrics tracking
     */
    initializeQualityMetrics() {
        // Agent Performance Metrics
        this.qualityMetrics.set('agent_performance', {
            id: 'agent_performance',
            name: 'Agent Performance Metrics',
            description: 'Key performance indicators for agent quality',
            metrics: [
                {
                    name: 'QA Score',
                    description: 'Average quality assurance score',
                    target: 90,
                    unit: 'percentage',
                    calculation: 'average_qa_scores'
                },
                {
                    name: 'First Contact Resolution',
                    description: 'Percentage of issues resolved on first contact',
                    target: 75,
                    unit: 'percentage',
                    calculation: 'resolved_first_contact / total_contacts'
                },
                {
                    name: 'Customer Satisfaction',
                    description: 'Average customer satisfaction score',
                    target: 4.5,
                    unit: 'out_of_5',
                    calculation: 'average_csat_scores'
                },
                {
                    name: 'Escalation Rate',
                    description: 'Percentage of contacts escalated to higher tiers',
                    target: 15,
                    unit: 'percentage',
                    calculation: 'escalated_contacts / total_contacts'
                },
                {
                    name: 'Average Handle Time',
                    description: 'Average time to handle customer contacts',
                    target: 600,
                    unit: 'seconds',
                    calculation: 'total_handle_time / total_contacts'
                }
            ]
        });

        // Quality Assurance Metrics
        this.qualityMetrics.set('qa_operations', {
            id: 'qa_operations',
            name: 'Quality Assurance Operations',
            description: 'Metrics for QA operations and effectiveness',
            metrics: [
                {
                    name: 'Evaluation Coverage',
                    description: 'Percentage of interactions evaluated',
                    target: 10,
                    unit: 'percentage',
                    calculation: 'evaluated_interactions / total_interactions'
                },
                {
                    name: 'Calibration Accuracy',
                    description: 'Consistency of QA evaluations across reviewers',
                    target: 95,
                    unit: 'percentage',
                    calculation: 'calibrated_scores / total_evaluations'
                },
                {
                    name: 'QA Turnaround Time',
                    description: 'Average time to complete QA evaluations',
                    target: 24,
                    unit: 'hours',
                    calculation: 'total_evaluation_time / total_evaluations'
                },
                {
                    name: 'Quality Index',
                    description: 'Overall quality index across all interactions',
                    target: 85,
                    unit: 'percentage',
                    calculation: 'weighted_quality_scores'
                }
            ]
        });
    }

    /**
     * Create default QA agents
     */
    createDefaultQAAgents() {
        // QA Specialist
        this.qaAgents.set('qa_specialist_1', {
            id: 'qa_specialist_1',
            name: 'Sarah Johnson',
            email: 'sarah.johnson@ocint.com',
            role: 'QA Specialist',
            expertise: ['general_support', 'technical_support'],
            certifications: ['CCXP', 'Quality Management'],
            status: 'active',
            evaluationsCompleted: 0,
            averageScore: 0,
            lastCalibration: null
        });

        // Senior QA Analyst
        this.qaAgents.set('senior_qa_1', {
            id: 'senior_qa_1',
            name: 'Michael Chen',
            email: 'michael.chen@ocint.com',
            role: 'Senior QA Analyst',
            expertise: ['all_tiers', 'process_improvement'],
            certifications: ['CCXP', 'Six Sigma', 'Quality Management'],
            status: 'active',
            evaluationsCompleted: 0,
            averageScore: 0,
            lastCalibration: null
        });

        // QA Manager
        this.qaAgents.set('qa_manager_1', {
            id: 'qa_manager_1',
            name: 'Jennifer Rodriguez',
            email: 'jennifer.rodriguez@ocint.com',
            role: 'QA Manager',
            expertise: ['all_tiers', 'management', 'strategy'],
            certifications: ['CCXP', 'PMP', 'Quality Management'],
            status: 'active',
            evaluationsCompleted: 0,
            averageScore: 0,
            lastCalibration: null
        });
    }

    /**
     * Create a new QA evaluation
     */
    createEvaluation(interactionData, scorecardId, qaAgentId) {
        const evaluationId = this.generateEvaluationId();
        const timestamp = Date.now();
        
        const scorecard = this.scorecards.get(scorecardId);
        if (!scorecard) {
            console.error(`Scorecard not found: ${scorecardId}`);
            return null;
        }

        const qaAgent = this.qaAgents.get(qaAgentId);
        if (!qaAgent) {
            console.error(`QA Agent not found: ${qaAgentId}`);
            return null;
        }

        const evaluation = {
            id: evaluationId,
            interactionId: interactionData.interactionId,
            agentId: interactionData.agentId,
            customerId: interactionData.customerId,
            channel: interactionData.channel,
            scorecardId: scorecardId,
            qaAgentId: qaAgentId,
            timestamp: timestamp,
            status: 'in_progress',
            criteria: this.initializeEvaluationCriteria(scorecard),
            totalScore: 0,
            weightedScore: 0,
            passed: false,
            autoFailed: false,
            autoFailReason: null,
            notes: '',
            recommendations: [],
            calibrationRequired: false
        };

        this.evaluations.set(evaluationId, evaluation);
        
        // Dispatch event
        this.dispatchEvent('evaluationCreated', { evaluation });
        
        return evaluationId;
    }

    /**
     * Initialize evaluation criteria with scores
     */
    initializeEvaluationCriteria(scorecard) {
        const criteria = [];
        
        for (const criterion of scorecard.criteria) {
            const criterionEvaluation = {
                id: criterion.id,
                name: criterion.name,
                description: criterion.description,
                weight: criterion.weight,
                maxScore: criterion.maxScore,
                required: criterion.required,
                autoFail: criterion.autoFail,
                score: 0,
                subCriteria: criterion.subCriteria.map(sub => ({
                    ...sub,
                    score: 0,
                    notes: ''
                })),
                notes: '',
                passed: false
            };
            
            criteria.push(criterionEvaluation);
        }
        
        return criteria;
    }

    /**
     * Score an evaluation criterion
     */
    scoreCriterion(evaluationId, criterionId, scores, notes = '') {
        const evaluation = this.evaluations.get(evaluationId);
        if (!evaluation) return false;

        const criterion = evaluation.criteria.find(c => c.id === criterionId);
        if (!criterion) return false;

        // Update sub-criteria scores
        let totalScore = 0;
        for (const subScore of scores) {
            const subCriterion = criterion.subCriteria.find(sub => sub.name === subScore.name);
            if (subCriterion) {
                subCriterion.score = subScore.score;
                totalScore += subScore.score;
            }
        }

        // Update criterion score
        criterion.score = totalScore;
        criterion.notes = notes;
        criterion.passed = totalScore >= (criterion.maxScore * 0.8); // 80% threshold

        // Check for auto-fail
        if (criterion.autoFail && !criterion.passed) {
            evaluation.autoFailed = true;
            evaluation.autoFailReason = criterion.name;
        }

        // Recalculate total scores
        this.calculateEvaluationScores(evaluation);

        // Update evaluation status
        if (evaluation.autoFailed) {
            evaluation.status = 'auto_failed';
        } else if (evaluation.criteria.every(c => c.score > 0)) {
            evaluation.status = 'completed';
        }

        // Dispatch event
        this.dispatchEvent('criterionScored', { evaluationId, criterionId, criterion });

        return true;
    }

    /**
     * Calculate evaluation scores
     */
    calculateEvaluationScores(evaluation) {
        let totalScore = 0;
        let weightedScore = 0;
        let totalWeight = 0;

        for (const criterion of evaluation.criteria) {
            totalScore += criterion.score;
            weightedScore += (criterion.score / criterion.maxScore) * criterion.weight;
            totalWeight += criterion.weight;
        }

        evaluation.totalScore = totalScore;
        evaluation.weightedScore = totalWeight > 0 ? (weightedScore / totalWeight) * 100 : 0;
        
        // Determine if passed
        const scorecard = this.scorecards.get(evaluation.scorecardId);
        if (scorecard) {
            evaluation.passed = evaluation.weightedScore >= scorecard.passingScore && !evaluation.autoFailed;
        }
    }

    /**
     * Complete an evaluation
     */
    completeEvaluation(evaluationId, finalNotes = '', recommendations = []) {
        const evaluation = this.evaluations.get(evaluationId);
        if (!evaluation) return false;

        evaluation.status = 'completed';
        evaluation.notes = finalNotes;
        evaluation.recommendations = recommendations;
        evaluation.completedAt = Date.now();

        // Update QA agent stats
        this.updateQAAgentStats(evaluation.qaAgentId, evaluation.weightedScore);

        // Check if calibration is needed
        this.checkCalibrationNeeded(evaluation);

        // Dispatch event
        this.dispatchEvent('evaluationCompleted', { evaluation });

        return true;
    }

    /**
     * Update QA agent statistics
     */
    updateQAAgentStats(qaAgentId, score) {
        const qaAgent = this.qaAgents.get(qaAgentId);
        if (!qaAgent) return;

        qaAgent.evaluationsCompleted++;
        
        // Calculate running average
        const currentTotal = qaAgent.averageScore * (qaAgent.evaluationsCompleted - 1);
        qaAgent.averageScore = (currentTotal + score) / qaAgent.evaluationsCompleted;
    }

    /**
     * Check if calibration is needed
     */
    checkCalibrationNeeded(evaluation) {
        // Check for significant score deviations
        const qaAgent = this.qaAgents.get(evaluation.qaAgentId);
        if (!qaAgent) return;

        const scoreDeviation = Math.abs(evaluation.weightedScore - qaAgent.averageScore);
        if (scoreDeviation > 15) { // More than 15% deviation
            evaluation.calibrationRequired = true;
            
            // Dispatch calibration alert
            this.dispatchEvent('calibrationRequired', { 
                evaluationId: evaluation.id,
                qaAgentId: evaluation.qaAgentId,
                scoreDeviation: scoreDeviation
            });
        }
    }

    /**
     * Generate evaluation ID
     */
    generateEvaluationId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `eval_${timestamp}_${random}`;
    }

    /**
     * Get evaluation by ID
     */
    getEvaluation(evaluationId) {
        return this.evaluations.get(evaluationId);
    }

    /**
     * Get all evaluations
     */
    getAllEvaluations() {
        return Array.from(this.evaluations.values());
    }

    /**
     * Get evaluations by agent
     */
    getEvaluationsByAgent(agentId) {
        return Array.from(this.evaluations.values()).filter(e => e.agentId === agentId);
    }

    /**
     * Get quality metrics
     */
    getQualityMetrics() {
        const metrics = {};
        
        for (const [metricId, metric] of this.qualityMetrics) {
            metrics[metricId] = {
                ...metric,
                currentValue: this.calculateMetricValue(metricId)
            };
        }
        
        return metrics;
    }

    /**
     * Calculate current metric value
     */
    calculateMetricValue(metricId) {
        switch (metricId) {
            case 'agent_performance':
                return this.calculateAgentPerformanceMetrics();
            case 'qa_operations':
                return this.calculateQAOperationsMetrics();
            default:
                return null;
        }
    }

    /**
     * Calculate agent performance metrics
     */
    calculateAgentPerformanceMetrics() {
        const evaluations = Array.from(this.evaluations.values());
        if (evaluations.length === 0) return {};

        const totalEvaluations = evaluations.length;
        const passedEvaluations = evaluations.filter(e => e.passed).length;
        const autoFailedEvaluations = evaluations.filter(e => e.autoFailed).length;

        return {
            totalEvaluations,
            passedEvaluations,
            autoFailedEvaluations,
            passRate: (passedEvaluations / totalEvaluations) * 100,
            autoFailRate: (autoFailedEvaluations / totalEvaluations) * 100,
            averageScore: evaluations.reduce((sum, e) => sum + e.weightedScore, 0) / totalEvaluations
        };
    }

    /**
     * Calculate QA operations metrics
     */
    calculateQAOperationsMetrics() {
        const evaluations = Array.from(this.evaluations.values());
        if (evaluations.length === 0) return {};

        const totalEvaluations = evaluations.length;
        const calibrationRequired = evaluations.filter(e => e.calibrationRequired).length;
        const averageTurnaroundTime = this.calculateAverageTurnaroundTime(evaluations);

        return {
            totalEvaluations,
            calibrationRequired,
            calibrationRate: (calibrationRequired / totalEvaluations) * 100,
            averageTurnaroundTime
        };
    }

    /**
     * Calculate average turnaround time
     */
    calculateAverageTurnaroundTime(evaluations) {
        const completedEvaluations = evaluations.filter(e => e.status === 'completed' && e.completedAt);
        if (completedEvaluations.length === 0) return 0;

        const totalTime = completedEvaluations.reduce((sum, e) => {
            return sum + (e.completedAt - e.timestamp);
        }, 0);

        return totalTime / completedEvaluations.length / (1000 * 60 * 60); // Convert to hours
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Listen for evaluation events
        document.addEventListener('evaluationCreated', (e) => {
            this.handleEvaluationCreated(e.detail.evaluation);
        });

        document.addEventListener('evaluationCompleted', (e) => {
            this.handleEvaluationCompleted(e.detail.evaluation);
        });

        document.addEventListener('calibrationRequired', (e) => {
            this.handleCalibrationRequired(e.detail);
        });
    }

    /**
     * Handle evaluation created event
     */
    handleEvaluationCreated(evaluation) {
        console.log(`QA Evaluation created: ${evaluation.id} for agent ${evaluation.agentId}`);
        // Additional handling logic can be added here
    }

    /**
     * Handle evaluation completed event
     */
    handleEvaluationCompleted(evaluation) {
        console.log(`QA Evaluation completed: ${evaluation.id} with score ${evaluation.weightedScore}`);
        // Additional handling logic can be added here
    }

    /**
     * Handle calibration required event
     */
    handleCalibrationRequired(detail) {
        console.log(`Calibration required for QA agent ${detail.qaAgentId} with ${detail.scoreDeviation}% deviation`);
        // Additional handling logic can be added here
    }

    /**
     * Dispatch custom events
     */
    dispatchEvent(eventName, detail) {
        const event = new CustomEvent(eventName, { detail });
        document.dispatchEvent(event);
    }

    /**
     * Export QA system data
     */
    exportQASystemData() {
        return {
            scorecards: Array.from(this.scorecards.values()),
            evaluations: Array.from(this.evaluations.values()),
            qualityMetrics: Array.from(this.qualityMetrics.values()),
            qaAgents: Array.from(this.qaAgents.values()),
            calibrationSessions: this.calibrationSessions,
            qualityIndex: this.qualityIndex,
            exportTimestamp: Date.now()
        };
    }

    /**
     * Get system status and health
     */
    getSystemStatus() {
        const totalEvaluations = this.evaluations.size;
        const completedEvaluations = Array.from(this.evaluations.values()).filter(e => e.status === 'completed').length;
        const pendingEvaluations = Array.from(this.evaluations.values()).filter(e => e.status === 'in_progress').length;
        
        return {
            totalEvaluations,
            completedEvaluations,
            pendingEvaluations,
            completionRate: totalEvaluations > 0 ? (completedEvaluations / totalEvaluations) * 100 : 0,
            systemHealth: pendingEvaluations < 10 ? 'healthy' : 'backlogged',
            lastUpdated: Date.now()
        };
    }
}

// Export for use in other modules
window.QualityAssuranceSystem = QualityAssuranceSystem;
