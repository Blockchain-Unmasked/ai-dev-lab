// AI/DEV Lab App - Frontend Environment Configuration Example
// =========================================================
// Copy this file to env.js and fill in your actual values
// NEVER commit env.js files to version control

const config = {
  // =============================================================================
  // APP CONFIGURATION
  // =============================================================================
  app: {
    name: 'AI_DEV_LAB_DEMO',
    version: '2.0.0',
    environment: 'development',
    debug: true,
    host: 'localhost',
    port: 8000
  },

  // =============================================================================
  // AI API CONFIGURATION
  // =============================================================================
  ai: {
    // Google Gemini API
    gemini: {
      apiKey: 'your-gemini-api-key-here',
      model: 'gemini-pro',
      temperature: 0.7,
      maxTokens: 2048,
      baseURL: 'https://generativelanguage.googleapis.com'
    },

    // OpenAI API (Alternative)
    openai: {
      apiKey: 'your-openai-api-key-here',
      model: 'gpt-4',
      temperature: 0.7,
      maxTokens: 2048,
      baseURL: 'https://api.openai.com'
    },

    // Anthropic Claude API (Alternative)
    anthropic: {
      apiKey: 'your-anthropic-api-key-here',
      model: 'claude-3-sonnet-20240229',
      maxTokens: 4096,
      baseURL: 'https://api.anthropic.com'
    }
  },

  // =============================================================================
  // MCP SERVER CONFIGURATION
  // =============================================================================
  mcp: {
    host: 'localhost',
    port: 8001,
    timeout: 30000,
    retryAttempts: 3,

    // Lab MCP Server
    labServer: {
      url: 'http://localhost:8002',
      apiKey: 'your-lab-mcp-api-key'
    },

    // App MCP Server
    appServer: {
      url: 'http://localhost:8003',
      apiKey: 'your-app-mcp-api-key'
    }
  },

  // =============================================================================
  // SECURITY CONFIGURATION
  // =============================================================================
  security: {
    enabled: true,
    corsAllowedOrigins: ['http://localhost:3000', 'http://localhost:8000'],
    sessionTimeout: 1800000, // 30 minutes
    maxLoginAttempts: 5,
    lockoutDuration: 900000 // 15 minutes
  },

  // =============================================================================
  // QUEUE SYSTEM CONFIGURATION
  // =============================================================================
  queue: {
    enabled: true,
    maxConcurrentSessions: 10,
    sessionTimeout: 300000, // 5 minutes
    priorityLevels: 5,
    autoEscalation: true
  },

  // =============================================================================
  // AGENT SYSTEM CONFIGURATION
  // =============================================================================
  agent: {
    enabled: true,
    maxTiers: 4,
    escalationEnabled: true,
    qaEnabled: true,
    stealthModeEnabled: true,
    humanTimingSimulation: true
  },

  // =============================================================================
  // PROMPT ENGINE CONFIGURATION
  // =============================================================================
  promptEngine: {
    enabled: true,
    mode: 'enhanced',
    templatesPath: 'app/meta/templates/',
    schemasPath: 'app/meta/schemas/',
    maxTokens: 4096
  },

  // =============================================================================
  // MONITORING AND ANALYTICS
  // =============================================================================
  monitoring: {
    enabled: true,
    metricsCollection: true,
    performanceMonitoring: true,
    errorTracking: true,
    userAnalytics: true
  },

  // =============================================================================
  // EXTERNAL SERVICES
  // =============================================================================
  external: {
    // Web Scraping Services
    scraping: {
      enabled: true,
      rateLimit: 10,
      userAgent: 'Mozilla/5.0 (AI/DEV Lab Bot)'
    },

    // File Storage
    storage: {
      type: 'local',
      path: 'app/storage/',
      maxSize: 1073741824 // 1GB
    }
  },

  // =============================================================================
  // DEVELOPMENT AND TESTING
  // =============================================================================
  development: {
    testing: true,
    mockAIResponses: true,
    debugMode: true,
    hotReload: true,
    logLevel: 'debug'
  },

  // =============================================================================
  // FEATURE FLAGS
  // =============================================================================
  features: {
    aTesting: true,
    queueSystem: true,
    tieredAgents: true,
    qualityAssurance: true,
    stealthMode: true,
    promptEngine: true,
    monitoring: true
  },

  // =============================================================================
  // UI CONFIGURATION
  // =============================================================================
  ui: {
    theme: 'auto', // auto, light, dark
    language: 'en',
    timezone: 'UTC',
    dateFormat: 'YYYY-MM-DD',
    timeFormat: 'HH:mm:ss',
    currency: 'USD'
  },

  // =============================================================================
  // NOTIFICATIONS
  // =============================================================================
  notifications: {
    enabled: true,
    sound: true,
    desktop: true,
    email: false,
    slack: false
  }
};

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
  // Node.js environment
  module.exports = config;
} else if (typeof window !== 'undefined') {
  // Browser environment
  window.APP_CONFIG = config;
}

// Development helper functions
if (config.development.debugMode) {
  console.log('🔧 App Configuration Loaded:', config);
  
  // Helper function to get config values
  window.getConfig = (path) => {
    return path.split('.').reduce((obj, key) => obj && obj[key], config);
  };
  
  // Helper function to set config values
  window.setConfig = (path, value) => {
    const keys = path.split('.');
    const lastKey = keys.pop();
    const obj = keys.reduce((obj, key) => obj && obj[key], config);
    if (obj) {
      obj[lastKey] = value;
      console.log(`🔧 Config updated: ${path} = ${value}`);
    }
  };
}
