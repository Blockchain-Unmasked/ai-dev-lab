// File: gemini-api.js
// Author: AI/DEV Lab
// Description: Google Gemini API integration for AI Intake/Support Agent demo
// Standards: OCINT compliant, modern ES6+, secure API handling

/**
 * Gemini API Integration
 * Handles communication with Google's Gemini API for AI responses
 */
class GeminiAPI {
  constructor() {
    this.apiKey = null;
    this.model = 'gemini-1.5-pro';
    this.temperature = 0.7;
    this.baseURL = 'https://generativelanguage.googleapis.com/v1beta/models';
    this._configured = false;
    
    this.init();
  }
  
  /**
   * Initialize the Gemini API
   */
  async init() {
    try {
      console.log('🔌 Initializing Gemini API Integration...');
      
      // Load saved configuration
      this.loadConfiguration();
      
      // Check if API key is available
      if (this.apiKey) {
        this._configured = true;
        console.log('✅ Gemini API configured with saved key');
      } else {
        console.log('⚠️ Gemini API not configured - using mock responses');
      }
      
    } catch (error) {
      console.error('❌ Failed to initialize Gemini API:', error);
    }
  }
  
  /**
   * Load configuration from localStorage
   */
  loadConfiguration() {
    try {
      const savedConfig = localStorage.getItem('ai-dev-lab-config');
      if (savedConfig) {
        const config = JSON.parse(savedConfig);
        this.apiKey = config.apiKey || null;
        this.model = config.model || 'gemini-pro';
        this.temperature = config.temperature || 0.7;
        
        // Update UI if elements exist
        this.updateConfigurationUI(config);
      }
    } catch (error) {
      console.error('❌ Error loading configuration:', error);
    }
  }
  
  /**
   * Update configuration UI elements
   */
  updateConfigurationUI(config) {
    try {
      const apiKeyInput = document.getElementById('api-key');
      const modelSelect = document.getElementById('model-select');
      const temperatureRange = document.getElementById('temperature');
      const temperatureValue = document.getElementById('temperature-value');
      
      if (apiKeyInput && config.apiKey) {
        apiKeyInput.value = config.apiKey;
      }
      
      if (modelSelect && config.model) {
        modelSelect.value = config.model;
      }
      
      if (temperatureRange && config.temperature) {
        temperatureRange.value = config.temperature;
      }
      
      if (temperatureValue && config.temperature) {
        temperatureValue.textContent = config.temperature;
      }
      
    } catch (error) {
      console.error('❌ Error updating configuration UI:', error);
    }
  }
  
  /**
   * Update configuration
   */
  updateConfiguration(config) {
    try {
      this.apiKey = config.apiKey || this.apiKey;
      this.model = config.model || this.model;
      this.temperature = config.temperature || this.temperature;
      
      this._configured = !!this.apiKey;
      
      console.log('✅ Gemini API configuration updated:', {
        model: this.model,
        temperature: this.temperature,
        isConfigured: this.isConfigured
      });
      
    } catch (error) {
      console.error('❌ Error updating configuration:', error);
    }
  }
  
  /**
   * Check if API is properly configured
   */
  isConfigured() {
    return this._configured && !!this.apiKey;
  }
  
  /**
   * Generate AI response using Gemini API
   */
  async generateResponse(customerMessage) {
    try {
      if (!this.isConfigured()) {
        throw new Error('Gemini API not configured');
      }
      
      console.log('🧠 Generating Gemini response for:', customerMessage);
      
      const startTime = Date.now();
      
      // Prepare the request payload
      const requestPayload = {
        contents: [
          {
            parts: [
              {
                text: this.buildPrompt(customerMessage)
              }
            ]
          }
        ],
        generationConfig: {
          temperature: this.temperature,
          topK: 40,
          topP: 0.95,
          maxOutputTokens: 1024,
        },
        safetySettings: [
          {
            category: "HARM_CATEGORY_HARASSMENT",
            threshold: "BLOCK_MEDIUM_AND_ABOVE"
          },
          {
            category: "HARM_CATEGORY_HATE_SPEECH",
            threshold: "BLOCK_MEDIUM_AND_ABOVE"
          },
          {
            category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold: "BLOCK_MEDIUM_AND_ABOVE"
          },
          {
            category: "HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold: "BLOCK_MEDIUM_AND_ABOVE"
          }
        ]
      };
      
      // Make API request
      const response = await this.makeAPIRequest(requestPayload);
      
      const processingTime = Date.now() - startTime;
      
      // Parse and return response
      const result = {
        text: response.text,
        confidence: this.calculateConfidence(response),
        quality: this.calculateQuality(response),
        model: this.model,
        processingTime: processingTime,
        usage: response.usage
      };
      
      console.log('✅ Gemini response generated:', result);
      return result;
      
    } catch (error) {
      console.error('❌ Error generating Gemini response:', error);
      throw error;
    }
  }
  
  /**
   * Build the prompt for the AI
   */
  buildPrompt(customerMessage) {
    return `You are an AI support agent for a technology company. Your role is to help customers with their questions and issues in a helpful, professional, and empathetic manner.

Customer Message: "${customerMessage}"

Please provide a helpful response that:
1. Addresses the customer's question or concern directly
2. Is professional yet friendly in tone
3. Provides actionable advice or solutions when possible
4. Asks clarifying questions if more information is needed
5. Maintains a helpful and supportive attitude

Keep your response concise but thorough (2-4 sentences). Focus on being genuinely helpful rather than just providing generic responses.`;
  }
  
  /**
   * Make the actual API request to Gemini
   */
  async makeAPIRequest(payload) {
    try {
      const url = `${this.baseURL}/${this.model}:generateContent?key=${this.apiKey}`;
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Gemini API error: ${errorData.error?.message || response.statusText}`);
      }
      
      const data = await response.json();
      
      // Extract the generated text
      const generatedText = data.candidates?.[0]?.content?.parts?.[0]?.text;
      
      if (!generatedText) {
        throw new Error('No response text generated from Gemini API');
      }
      
      return {
        text: generatedText,
        usage: data.usageMetadata || {},
        safetyRatings: data.candidates?.[0]?.safetyRatings || []
      };
      
    } catch (error) {
      console.error('❌ Gemini API request failed:', error);
      throw error;
    }
  }
  
  /**
   * Calculate confidence score based on response characteristics
   */
  calculateConfidence(response) {
    try {
      // Simple confidence calculation based on response length and safety
      let confidence = 0.7; // Base confidence
      
      // Adjust based on response length (longer responses often indicate more thought)
      if (response.text.length > 100) confidence += 0.1;
      if (response.text.length > 200) confidence += 0.1;
      
      // Adjust based on safety ratings
      const safetyRatings = response.safetyRatings || [];
      const highSafetyCount = safetyRatings.filter(r => r.probability === 'NEGLIGIBLE').length;
      confidence += (highSafetyCount / safetyRatings.length) * 0.1;
      
      // Cap at 1.0
      return Math.min(confidence, 1.0);
      
    } catch (error) {
      console.error('❌ Error calculating confidence:', error);
      return 0.7; // Default confidence
    }
  }
  
  /**
   * Calculate quality score based on response characteristics
   */
  calculateQuality(response) {
    try {
      // Simple quality calculation
      let quality = 0.8; // Base quality
      
      // Adjust based on response length
      if (response.text.length > 50 && response.text.length < 500) quality += 0.1;
      
      // Adjust based on response structure (questions, solutions, etc.)
      if (response.text.includes('?')) quality += 0.05; // Shows engagement
      if (response.text.includes('help') || response.text.includes('assist')) quality += 0.05; // Shows helpfulness
      
      // Cap at 1.0
      return Math.min(quality, 1.0);
      
    } catch (error) {
      console.error('❌ Error calculating quality:', error);
      return 0.8; // Default quality
    }
  }
  
  /**
   * Test API connection
   */
  async testConnection() {
    try {
      if (!this.isConfigured()) {
        return {
          success: false,
          error: 'API not configured'
        };
      }
      
      console.log('🧪 Testing Gemini API connection...');
      
      const testPayload = {
        contents: [
          {
            parts: [
              {
                text: 'Hello, this is a test message. Please respond with "Test successful" if you can see this.'
              }
            ]
          }
        ],
        generationConfig: {
          temperature: 0.1,
          maxOutputTokens: 50,
        }
      };
      
      const response = await this.makeAPIRequest(testPayload);
      
      if (response.text.toLowerCase().includes('test successful')) {
        return {
          success: true,
          message: 'API connection successful',
          response: response.text
        };
      } else {
        return {
          success: true,
          message: 'API connected but unexpected response',
          response: response.text
        };
      }
      
    } catch (error) {
      console.error('❌ Gemini API connection test failed:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  /**
   * Get API status information
   */
  getStatus() {
    return {
      isConfigured: this._configured,
      model: this.model,
      temperature: this.temperature,
      hasApiKey: !!this.apiKey,
      baseURL: this.baseURL
    };
  }
  
  /**
   * Validate API key format
   */
  validateApiKey(apiKey) {
    try {
      // Basic validation for Gemini API key format
      if (!apiKey || typeof apiKey !== 'string') {
        return false;
      }
      
      // Gemini API keys are typically long alphanumeric strings
      if (apiKey.length < 20) {
        return false;
      }
      
      // Check if it looks like a valid API key format
      const apiKeyPattern = /^[A-Za-z0-9_-]+$/;
      return apiKeyPattern.test(apiKey);
      
    } catch (error) {
      console.error('❌ Error validating API key:', error);
      return false;
    }
  }
  
  /**
   * Set API key
   */
  setApiKey(apiKey) {
    try {
      if (this.validateApiKey(apiKey)) {
        this.apiKey = apiKey;
        this._configured = true;
        console.log('✅ API key set successfully');
        return true;
      } else {
        console.error('❌ Invalid API key format');
        return false;
      }
    } catch (error) {
      console.error('❌ Error setting API key:', error);
      return false;
    }
  }
  
  /**
   * Clear API key
   */
  clearApiKey() {
    try {
      this.apiKey = null;
      this._configured = false;
      console.log('✅ API key cleared');
    } catch (error) {
      console.error('❌ Error clearing API key:', error);
    }
  }
  
  /**
   * Get available models
   */
  getAvailableModels() {
    return [
      {
        id: 'gemini-pro',
        name: 'Gemini Pro',
        description: 'Most capable model for complex tasks',
        maxTokens: 30720
      },
      {
        id: 'gemini-flash',
        name: 'Gemini Flash',
        description: 'Fast and efficient for simple tasks',
        maxTokens: 8192
      }
    ];
  }
  
  /**
   * Get model information
   */
  getModelInfo(modelId) {
    const models = this.getAvailableModels();
    return models.find(m => m.id === modelId) || models[0];
  }
  
  /**
   * Update model
   */
  updateModel(modelId) {
    try {
      const modelInfo = this.getModelInfo(modelId);
      if (modelInfo) {
        this.model = modelId;
        console.log(`✅ Model updated to: ${modelInfo.name}`);
        return true;
      } else {
        console.error('❌ Invalid model ID:', modelId);
        return false;
      }
    } catch (error) {
      console.error('❌ Error updating model:', error);
      return false;
    }
  }
  
  /**
   * Update temperature setting
   */
  updateTemperature(temperature) {
    try {
      const temp = parseFloat(temperature);
      if (temp >= 0 && temp <= 2) {
        this.temperature = temp;
        console.log(`✅ Temperature updated to: ${temp}`);
        return true;
      } else {
        console.error('❌ Temperature must be between 0 and 2');
        return false;
      }
    } catch (error) {
      console.error('❌ Error updating temperature:', error);
      return false;
    }
  }
  
  /**
   * Get usage statistics
   */
  async getUsageStats() {
    try {
      if (!this.isConfigured()) {
        return null;
      }
      
      // Note: Gemini API doesn't provide usage stats in the same way as some other APIs
      // This would need to be implemented with your own tracking
      return {
        message: 'Usage statistics not available from Gemini API',
        note: 'Implement custom usage tracking for detailed analytics'
      };
      
    } catch (error) {
      console.error('❌ Error getting usage stats:', error);
      return null;
    }
  }
  
  /**
   * Cleanup resources
   */
  destroy() {
    try {
      // Clear sensitive data
      this.apiKey = null;
      this._configured = false;
      console.log('🧹 Gemini API Integration destroyed');
    } catch (error) {
      console.error('❌ Error destroying Gemini API Integration:', error);
    }
  }
}

// Initialize Gemini API Integration when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.geminiAPI = new GeminiAPI();
});

// Export for module usage
export default GeminiAPI;
