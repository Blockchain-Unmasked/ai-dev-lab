// File: ab-testing.js
// Author: AI/DEV Lab
// Description: A/B testing module for AI Intake/Support Agent demo
// Standards: OCINT compliant, modern ES6+, testing best practices

/**
 * A/B Testing Controller
 * Manages A/B testing logic, metrics collection, and view switching
 */
class ABTestingController {
  constructor() {
    this.currentTest = null;
    this.testGroups = new Map();
    this.metrics = {
      customer: {},
      qa: {}
    };
    this.testHistory = [];
    
    this.init();
  }
  
  /**
   * Initialize the A/B testing controller
   */
  async init() {
    try {
      console.log('🧪 Initializing A/B Testing Controller...');
      
      // Setup event listeners
      this.setupEventListeners();
      
      // Load test configuration
      this.loadTestConfiguration();
      
      // Start default test
      this.startTest('ai-support-agent-v1');
      
      console.log('✅ A/B Testing Controller initialized');
      
    } catch (error) {
      console.error('❌ Failed to initialize A/B Testing Controller:', error);
    }
  }
  
  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Listen for view changes
    document.addEventListener('view:changed', (event) => {
      this.handleViewChange(event.detail);
    });
    
    // Listen for agent mode changes
    document.addEventListener('agent:mode-changed', (event) => {
      this.handleAgentModeChange(event.detail);
    });
    
    // Listen for chat interactions
    document.addEventListener('chat:message-sent', (event) => {
      this.recordInteraction(event.detail);
    });
    
    // Listen for chat responses
    document.addEventListener('chat:response-received', (event) => {
      this.recordResponse(event.detail);
    });
    
    console.log('✅ A/B Testing event listeners configured');
  }
  
  /**
   * Load test configuration
   */
  loadTestConfiguration() {
    try {
      const savedConfig = localStorage.getItem('ai-dev-lab-ab-testing');
      if (savedConfig) {
        const config = JSON.parse(savedConfig);
        this.testGroups = new Map(config.testGroups || []);
        this.metrics = config.metrics || { customer: {}, qa: {} };
        this.testHistory = config.testHistory || [];
        
        console.log('✅ A/B testing configuration loaded');
      }
    } catch (error) {
      console.error('❌ Error loading A/B testing configuration:', error);
    }
  }
  
  /**
   * Save test configuration
   */
  saveTestConfiguration() {
    try {
      const config = {
        testGroups: Array.from(this.testGroups.entries()),
        metrics: this.metrics,
        testHistory: this.testHistory,
        timestamp: new Date().toISOString()
      };
      
      localStorage.setItem('ai-dev-lab-ab-testing', JSON.stringify(config));
      console.log('✅ A/B testing configuration saved');
      
    } catch (error) {
      console.error('❌ Error saving A/B testing configuration:', error);
    }
  }
  
  /**
   * Start a new A/B test
   */
  startTest(testId) {
    try {
      console.log(`🧪 Starting A/B test: ${testId}`);
      
      // Define test configuration
      const testConfig = this.getTestConfiguration(testId);
      
      if (!testConfig) {
        console.error('❌ Unknown test ID:', testId);
        return false;
      }
      
      // Create test instance
      this.currentTest = {
        id: testId,
        name: testConfig.name,
        description: testConfig.description,
        startTime: new Date(),
        variants: testConfig.variants,
        metrics: {},
        status: 'active'
      };
      
      // Initialize metrics for each variant
      testConfig.variants.forEach(variant => {
        this.currentTest.metrics[variant.id] = {
          views: 0,
          interactions: 0,
          responses: 0,
          satisfaction: 0,
          responseTime: 0,
          quality: 0
        };
      });
      
      // Add to test history
      this.testHistory.push({
        id: testId,
        startTime: this.currentTest.startTime,
        status: 'active'
      });
      
      // Save configuration
      this.saveTestConfiguration();
      
      console.log('✅ A/B test started:', this.currentTest);
      return true;
      
    } catch (error) {
      console.error('❌ Error starting A/B test:', error);
      return false;
    }
  }
  
  /**
   * Get test configuration by ID
   */
  getTestConfiguration(testId) {
    const configurations = {
      'ai-support-agent-v1': {
        name: 'AI Support Agent v1',
        description: 'Testing customer vs QA view performance',
        variants: [
          {
            id: 'customer',
            name: 'Customer View',
            description: 'Simple chat interface for customers',
            type: 'view'
          },
          {
            id: 'qa',
            name: 'QA View',
            description: 'Detailed view with agent internals',
            type: 'view'
          }
        ]
      },
      'ai-vs-human-v1': {
        name: 'AI vs Human Agent v1',
        description: 'Testing AI vs human fallback responses',
        variants: [
          {
            id: 'ai',
            name: 'AI Agent',
            description: 'Gemini-powered AI responses',
            type: 'mode'
          },
          {
            id: 'human',
            name: 'Human Agent',
            description: 'Human fallback responses',
            type: 'mode'
          }
        ]
      }
    };
    
    return configurations[testId];
  }
  
  /**
   * Handle view change (A/B testing)
   */
  handleViewChange(detail) {
    try {
      const { view } = detail;
      
      if (!this.currentTest) {
        return;
      }
      
      // Record view for current variant
      this.recordView(view);
      
      // Check if we should switch variants
      this.checkVariantSwitch(view);
      
      console.log(`📊 View change recorded: ${view}`);
      
    } catch (error) {
      console.error('❌ Error handling view change:', error);
    }
  }
  
  /**
   * Handle agent mode change
   */
  handleAgentModeChange(detail) {
    try {
      const { mode } = detail;
      
      if (!this.currentTest) {
        return;
      }
      
      // Record mode change
      this.recordModeChange(mode);
      
      console.log(`📊 Agent mode change recorded: ${mode}`);
      
    } catch (error) {
      console.error('❌ Error handling agent mode change:', error);
    }
  }
  
  /**
   * Record a view for a variant
   */
  recordView(variantId) {
    try {
      if (!this.currentTest || !this.currentTest.metrics[variantId]) {
        return;
      }
      
      // Increment view count
      this.currentTest.metrics[variantId].views++;
      
      // Update global metrics
      if (!this.metrics[variantId]) {
        this.metrics[variantId] = { views: 0, interactions: 0, responses: 0 };
      }
      this.metrics[variantId].views++;
      
      // Save configuration
      this.saveTestConfiguration();
      
      console.log(`📊 View recorded for variant: ${variantId}`);
      
    } catch (error) {
      console.error('❌ Error recording view:', error);
    }
  }
  
  /**
   * Record an interaction (message sent)
   */
  recordInteraction(detail) {
    try {
      const { viewType, messageType, timestamp } = detail;
      
      if (!this.currentTest) {
        return;
      }
      
      // Find the appropriate variant
      const variantId = this.getCurrentVariantId(viewType);
      
      if (variantId && this.currentTest.metrics[variantId]) {
        // Increment interaction count
        this.currentTest.metrics[variantId].interactions++;
        
        // Update global metrics
        if (!this.metrics[variantId]) {
          this.metrics[variantId] = { views: 0, interactions: 0, responses: 0 };
        }
        this.metrics[variantId].interactions++;
        
        // Save configuration
        this.saveTestConfiguration();
        
        console.log(`📊 Interaction recorded for variant: ${variantId}`);
      }
      
    } catch (error) {
      console.error('❌ Error recording interaction:', error);
    }
  }
  
  /**
   * Record a response (AI/human response received)
   */
  recordResponse(detail) {
    try {
      const { viewType, responseType, processingTime, quality, timestamp } = detail;
      
      if (!this.currentTest) {
        return;
      }
      
      // Find the appropriate variant
      const variantId = this.getCurrentVariantId(viewType);
      
      if (variantId && this.currentTest.metrics[variantId]) {
        // Increment response count
        this.currentTest.metrics[variantId].responses++;
        
        // Update response time (running average)
        const currentAvg = this.currentTest.metrics[variantId].responseTime;
        const currentCount = this.currentTest.metrics[variantId].responses;
        this.currentTest.metrics[variantId].responseTime = 
          (currentAvg * (currentCount - 1) + processingTime) / currentCount;
        
        // Update quality (running average)
        if (quality !== undefined) {
          const currentQualityAvg = this.currentTest.metrics[variantId].quality;
          this.currentTest.metrics[variantId].quality = 
            (currentQualityAvg * (currentCount - 1) + quality) / currentCount;
        }
        
        // Update global metrics
        if (!this.metrics[variantId]) {
          this.metrics[variantId] = { views: 0, interactions: 0, responses: 0 };
        }
        this.metrics[variantId].responses++;
        
        // Save configuration
        this.saveTestConfiguration();
        
        console.log(`📊 Response recorded for variant: ${variantId}`);
      }
      
    } catch (error) {
      console.error('❌ Error recording response:', error);
    }
  }
  
  /**
   * Record mode change
   */
  recordModeChange(mode) {
    try {
      if (!this.currentTest) {
        return;
      }
      
      // Find mode-based variant
      const modeVariant = this.currentTest.variants.find(v => v.type === 'mode' && v.id === mode);
      
      if (modeVariant) {
        this.recordView(modeVariant.id);
      }
      
    } catch (error) {
      console.error('❌ Error recording mode change:', error);
    }
  }
  
  /**
   * Get current variant ID based on view type
   */
  getCurrentVariantId(viewType) {
    try {
      if (!this.currentTest) {
        return null;
      }
      
      // Find view-based variant
      const viewVariant = this.currentTest.variants.find(v => v.type === 'view' && v.id === viewType);
      
      if (viewVariant) {
        return viewVariant.id;
      }
      
      // Fallback to view type
      return viewType;
      
    } catch (error) {
      console.error('❌ Error getting current variant ID:', error);
      return null;
    }
  }
  
  /**
   * Check if we should switch variants
   */
  checkVariantSwitch(currentVariantId) {
    try {
      if (!this.currentTest) {
        return;
      }
      
      // Simple variant switching logic
      // In a real implementation, this would use statistical significance
      const currentMetrics = this.currentTest.metrics[currentVariantId];
      const otherVariants = Object.keys(this.currentTest.metrics).filter(id => id !== currentVariantId);
      
      if (currentMetrics && otherVariants.length > 0) {
        // Check if current variant is underperforming
        const shouldSwitch = this.shouldSwitchVariant(currentVariantId, otherVariants);
        
        if (shouldSwitch) {
          this.switchToVariant(otherVariants[0]);
        }
      }
      
    } catch (error) {
      console.error('❌ Error checking variant switch:', error);
    }
  }
  
  /**
   * Determine if we should switch variants
   */
  shouldSwitchVariant(currentVariantId, otherVariants) {
    try {
      const currentMetrics = this.currentTest.metrics[currentVariantId];
      
      // Simple heuristic: switch if current variant has low engagement
      if (currentMetrics.views > 10) {
        const engagementRate = currentMetrics.interactions / currentMetrics.views;
        
        if (engagementRate < 0.3) { // Less than 30% engagement
          return true;
        }
      }
      
      return false;
      
    } catch (error) {
      console.error('❌ Error determining variant switch:', error);
      return false;
    }
  }
  
  /**
   * Switch to a different variant
   */
  switchToVariant(variantId) {
    try {
      console.log(`🔄 Switching to variant: ${variantId}`);
      
      // Update current test
      if (this.currentTest) {
        this.currentTest.currentVariant = variantId;
        this.currentTest.lastSwitch = new Date();
      }
      
      // Trigger variant switch event
      document.dispatchEvent(new CustomEvent('ab-test:variant-switched', {
        detail: { 
          variantId,
          testId: this.currentTest?.id,
          timestamp: new Date()
        }
      }));
      
      // Save configuration
      this.saveTestConfiguration();
      
    } catch (error) {
      console.error('❌ Error switching variants:', error);
    }
  }
  
  /**
   * Get test results
   */
  getTestResults() {
    try {
      if (!this.currentTest) {
        return null;
      }
      
      const results = {
        testId: this.currentTest.id,
        testName: this.currentTest.name,
        startTime: this.currentTest.startTime,
        duration: Date.now() - this.currentTest.startTime.getTime(),
        variants: {}
      };
      
      // Calculate metrics for each variant
      Object.entries(this.currentTest.metrics).forEach(([variantId, metrics]) => {
        const engagementRate = metrics.views > 0 ? metrics.interactions / metrics.views : 0;
        const responseRate = metrics.interactions > 0 ? metrics.responses / metrics.interactions : 0;
        
        results.variants[variantId] = {
          ...metrics,
          engagementRate: Math.round(engagementRate * 100) / 100,
          responseRate: Math.round(responseRate * 100) / 100,
          avgResponseTime: Math.round(metrics.responseTime),
          avgQuality: Math.round(metrics.quality * 100) / 100
        };
      });
      
      return results;
      
    } catch (error) {
      console.error('❌ Error getting test results:', error);
      return null;
    }
  }
  
  /**
   * End current test
   */
  endTest() {
    try {
      if (!this.currentTest) {
        return false;
      }
      
      console.log(`🏁 Ending A/B test: ${this.currentTest.id}`);
      
      // Update test status
      this.currentTest.status = 'completed';
      this.currentTest.endTime = new Date();
      this.currentTest.duration = this.currentTest.endTime - this.currentTest.startTime;
      
      // Update test history
      const historyEntry = this.testHistory.find(h => h.id === this.currentTest.id);
      if (historyEntry) {
        historyEntry.status = 'completed';
        historyEntry.endTime = this.currentTest.endTime;
        historyEntry.duration = this.currentTest.duration;
      }
      
      // Get final results
      const results = this.getTestResults();
      
      // Save configuration
      this.saveTestConfiguration();
      
      // Dispatch test completion event
      document.dispatchEvent(new CustomEvent('ab-test:completed', {
        detail: { 
          testId: this.currentTest.id,
          results,
          timestamp: new Date()
        }
      }));
      
      console.log('✅ A/B test ended:', results);
      
      // Clear current test
      this.currentTest = null;
      
      return true;
      
    } catch (error) {
      console.error('❌ Error ending A/B test:', error);
      return false;
    }
  }
  
  /**
   * Get testing dashboard data
   */
  getDashboardData() {
    try {
      const data = {
        currentTest: this.currentTest ? {
          id: this.currentTest.id,
          name: this.currentTest.name,
          status: this.currentTest.status,
          startTime: this.currentTest.startTime,
          duration: this.currentTest.startTime ? Date.now() - this.currentTest.startTime.getTime() : 0
        } : null,
        testHistory: this.testHistory.slice(-5), // Last 5 tests
        globalMetrics: this.metrics,
        recommendations: this.generateRecommendations()
      };
      
      return data;
      
    } catch (error) {
      console.error('❌ Error getting dashboard data:', error);
      return null;
    }
  }
  
  /**
   * Generate testing recommendations
   */
  generateRecommendations() {
    try {
      const recommendations = [];
      
      if (!this.currentTest) {
        recommendations.push({
          type: 'info',
          message: 'No active test running. Start a new test to begin A/B testing.',
          priority: 'low'
        });
        return recommendations;
      }
      
      // Analyze current test performance
      const results = this.getTestResults();
      if (!results) {
        return recommendations;
      }
      
      // Check for statistical significance
      const variants = Object.values(results.variants);
      if (variants.length >= 2) {
        const [variant1, variant2] = variants;
        
        // Engagement rate comparison
        if (Math.abs(variant1.engagementRate - variant2.engagementRate) > 0.1) {
          const betterVariant = variant1.engagementRate > variant2.engagementRate ? 
            Object.keys(results.variants)[0] : Object.keys(results.variants)[1];
          
          recommendations.push({
            type: 'success',
            message: `Variant ${betterVariant} shows better engagement (${Math.round(Math.max(variant1.engagementRate, variant2.engagementRate) * 100)}% vs ${Math.round(Math.min(variant1.engagementRate, variant2.engagementRate) * 100)}%)`,
            priority: 'medium'
          });
        }
        
        // Response time comparison
        if (Math.abs(variant1.avgResponseTime - variant2.avgResponseTime) > 1000) {
          const fasterVariant = variant1.avgResponseTime < variant2.avgResponseTime ? 
            Object.keys(results.variants)[0] : Object.keys(results.variants)[1];
          
          recommendations.push({
            type: 'info',
            message: `Variant ${fasterVariant} responds faster (${Math.round(Math.min(variant1.avgResponseTime, variant2.avgResponseTime))}ms vs ${Math.round(Math.max(variant1.avgResponseTime, variant2.avgResponseTime))}ms)`,
            priority: 'low'
          });
        }
      }
      
      // Check if test should end
      const totalViews = variants.reduce((sum, v) => sum + v.views, 0);
      if (totalViews > 100) {
        recommendations.push({
          type: 'warning',
          message: 'Test has collected sufficient data. Consider ending the test to analyze results.',
          priority: 'high'
        });
      }
      
      return recommendations;
      
    } catch (error) {
      console.error('❌ Error generating recommendations:', error);
      return [];
    }
  }
  
  /**
   * Export test data
   */
  exportTestData() {
    try {
      const data = {
        currentTest: this.currentTest,
        testHistory: this.testHistory,
        globalMetrics: this.metrics,
        exportTime: new Date().toISOString()
      };
      
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `ab-test-data-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      console.log('✅ Test data exported successfully');
      
    } catch (error) {
      console.error('❌ Error exporting test data:', error);
    }
  }
  
  /**
   * Reset all testing data
   */
  resetTestingData() {
    try {
      console.log('🔄 Resetting all A/B testing data...');
      
      // Clear all data
      this.currentTest = null;
      this.testGroups.clear();
      this.metrics = { customer: {}, qa: {} };
      this.testHistory = [];
      
      // Clear localStorage
      localStorage.removeItem('ai-dev-lab-ab-testing');
      
      console.log('✅ A/B testing data reset successfully');
      
    } catch (error) {
      console.error('❌ Error resetting testing data:', error);
    }
  }
  
  /**
   * Get current state
   */
  getState() {
    return {
      currentTest: this.currentTest,
      testGroups: Array.from(this.testGroups.entries()),
      metrics: this.metrics,
      testHistory: this.testHistory
    };
  }
  
  /**
   * Cleanup resources
   */
  destroy() {
    try {
      // Save configuration before destroying
      this.saveTestConfiguration();
      
      console.log('🧹 A/B Testing Controller destroyed');
    } catch (error) {
      console.error('❌ Error destroying A/B Testing Controller:', error);
    }
  }
}

// Initialize A/B Testing Controller when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.abTestingController = new ABTestingController();
});

// Export for module usage
export default ABTestingController;
