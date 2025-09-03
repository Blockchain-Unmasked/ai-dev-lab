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
    this.backendURL = window.location.origin.replace('3000', '8000') || 'http://localhost:8000';
    this._configured = false;
    this._backendConfigured = false;
    
    this.init();
  }
  
  /**
   * Initialize the Gemini API
   */
  async init() {
    try {
      console.log('🔌 Initializing Gemini API Integration...');
      
      // First, try to get configuration from backend
      await this.loadBackendConfiguration();
      
      // If no backend config, load saved configuration
      if (!this.apiKey) {
        this.loadConfiguration();
      }
      
      // Check if API key is available (either frontend or backend)
      if (this.apiKey || this._backendConfigured) {
        this._configured = true;
        if (this._backendConfigured) {
          console.log('✅ Gemini API configured (backend)');
        } else {
          console.log('✅ Gemini API configured (frontend)');
        }
      } else {
        console.log('⚠️ Gemini API not configured - using mock responses');
      }
      
    } catch (error) {
      console.error('❌ Failed to initialize Gemini API:', error);
    }
  }
  
  /**
   * Load configuration from backend
   */
  async loadBackendConfiguration() {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
      
      const response = await fetch(`${this.backendURL}/api/v1/ai/config`, {
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        const config = await response.json();
        if (config.gemini && config.gemini.api_key_configured) {
          // Backend has API key configured, but we can't access it directly
          // We'll use a special flag to indicate backend configuration
          this._backendConfigured = true;
          this.model = config.gemini.model || this.model;
          this.temperature = config.gemini.temperature || this.temperature;
          console.log('✅ Backend has Gemini API configured');
        }
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('ℹ️ Backend configuration request timed out');
      } else {
        console.log('ℹ️ Backend configuration not available:', error.message);
      }
    }
  }

  /**
   * Load configuration from localStorage (excluding API keys for security)
   */
  loadConfiguration() {
    try {
      const savedConfig = localStorage.getItem('ai-dev-lab-config');
      if (savedConfig) {
        const config = JSON.parse(savedConfig);
        // Don't load API key from localStorage for security reasons
        // API keys should only be configured through backend or secure methods
        this.model = config.model || 'gemini-1.5-pro';
        this.temperature = config.temperature || 0.7;
        
        // Update UI if elements exist (without API key)
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
      
      // Don't populate API key field for security reasons
      if (apiKeyInput) {
        apiKeyInput.value = '';
        apiKeyInput.placeholder = 'API key configured via backend';
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
      
      this._configured = !!this.apiKey || this._backendConfigured;
      
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
    return (this._configured && !!this.apiKey) || this._backendConfigured;
  }
  
  /**
   * Generate AI response using Gemini API
   */
  async generateResponse(customerMessage) {
    try {
      // Input validation
      if (!customerMessage || typeof customerMessage !== 'string') {
        throw new Error('Invalid customer message provided');
      }
      
      if (customerMessage.trim().length === 0) {
        throw new Error('Customer message cannot be empty');
      }
      
      if (customerMessage.length > 1000) {
        throw new Error('Customer message too long (max 1000 characters)');
      }
      
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
    // Sanitize the customer message to prevent prompt injection
    const sanitizedMessage = customerMessage
      .replace(/[<>]/g, '') // Remove potential HTML tags
      .replace(/[\r\n\t]/g, ' ') // Replace line breaks with spaces
      .trim();
    
    return `You are an expert AI customer support agent for a technology company. You have deep knowledge of technology, software, hardware, and customer service best practices.

Customer Message: "${sanitizedMessage}"

Please provide an intelligent, helpful response that:
1. **Directly addresses** the customer's specific question or concern
2. **Shows understanding** of their situation and demonstrates expertise
3. **Provides actionable solutions** or step-by-step guidance when possible
4. **Asks clarifying questions** if you need more information to help effectively
5. **Maintains a professional yet friendly tone** that builds trust
6. **Demonstrates technical knowledge** when relevant to their issue
7. **Offers additional help** or resources if appropriate

Guidelines:
- Be specific and detailed in your responses
- Use technical terms appropriately but explain when needed
- Show empathy for their situation
- Provide multiple solution options when possible
- Keep responses concise (2-4 sentences) but thorough
- Focus on being genuinely helpful rather than generic

Remember: You're not just responding to text - you're helping a real person solve a real problem.`;
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
      
      // If backend is configured, test through backend
      if (this._backendConfigured && !this.apiKey) {
        return await this.testBackendConnection();
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
   * Test backend API connection
   */
  async testBackendConnection() {
    try {
      console.log('🧪 Testing backend Gemini API connection...');
      
      const response = await fetch(`${this.backendURL}/api/v1/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: 'Hello, this is a test message. Please respond with "Test successful" if you can see this.'
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        return {
          success: true,
          message: 'Backend API connection successful',
          response: data.response || 'Test successful'
        };
      } else {
        return {
          success: false,
          error: `Backend API error: ${response.statusText}`
        };
      }
      
    } catch (error) {
      console.error('❌ Backend API connection test failed:', error);
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
      isConfigured: this.isConfigured(),
      isBackendConfigured: this._backendConfigured,
      model: this.model,
      temperature: this.temperature,
      hasApiKey: !!this.apiKey,
      baseURL: this.baseURL,
      backendURL: this.backendURL
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
   * Set API key (deprecated - use backend configuration instead)
   */
  setApiKey(apiKey) {
    try {
      console.warn('⚠️ Setting API key directly is deprecated. Use backend configuration instead.');
      if (this.validateApiKey(apiKey)) {
        this.apiKey = apiKey;
        this._configured = true;
        console.log('✅ API key set successfully (consider using backend configuration)');
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
      // Only set _configured to false if we're not using backend configuration
      if (!this._backendConfigured) {
        this._configured = false;
      }
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
        id: 'gemini-1.5-pro',
        name: 'Gemini 1.5 Pro',
        description: 'Most capable model for complex tasks',
        maxTokens: 8192
      },
      {
        id: 'gemini-1.5-flash',
        name: 'Gemini 1.5 Flash',
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

// Make GeminiAPI available globally
window.GeminiAPI = GeminiAPI;
