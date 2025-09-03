# App-Specific MCP Server

## Overview

This is a dedicated MCP (Model Context Protocol) server specifically designed for the **AI Intake/Support Agent Demo** application. It provides tools, resources, and prompts tailored to the demo's needs, separate from the main repository MCP server.

## 🎯 Purpose

- **Focused Functionality**: Tools specifically for chat analysis, response generation, and A/B testing
- **Demo-Specific Resources**: Templates, guidelines, and configurations for the support agent
- **Lightweight**: Minimal dependencies and focused scope
- **Modular**: Can be used independently or alongside the main MCP server

## 🛠️ Available Tools

### 1. `analyze_chat_conversation`
Analyzes chat conversations for sentiment, intent, and key metrics.

**Input**: Array of conversation messages with role, content, and timestamp
**Output**: Analysis including message count, sentiment, and conversation length

### 2. `generate_response_template`
Generates response templates based on user intent and context.

**Input**: User intent, context, and desired response type
**Output**: Appropriate response template for the situation

### 3. `calculate_response_metrics`
Calculates quality metrics for A/B testing analysis.

**Input**: Array of response data (time, satisfaction, resolution time)
**Output**: Average metrics and performance statistics

## 📚 Available Resources

### `app://chat-templates`
Predefined response templates for common scenarios:
- Greetings
- Problem acknowledgments
- Closings

### `app://qa-guidelines`
Quality assurance guidelines for agent responses:
- Response quality standards
- Escalation criteria
- Response time targets

### `app://ab-testing-config`
A/B testing configuration:
- Test scenarios
- Metrics to track
- Sample size requirements

## 🎭 Available Prompts

### `customer_greeting`
Generates friendly greetings for new customers.

### `problem_escalation`
Creates escalation responses for complex issues.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Quick Start
```bash
# Navigate to the app MCP server directory
cd app/mcp-server

# Make startup script executable (if not already)
chmod +x start.sh

# Start the server
./start.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python3 server.py
```

## 🔧 Configuration

The server configuration is in `config.yaml` and includes:
- Server metadata
- Capability definitions
- Performance settings
- Security settings
- Demo feature flags

## 🔌 Integration

### With Cursor IDE
Add to your `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "ai-dev-lab-app": {
      "command": "python3",
      "args": ["/path/to/app/mcp-servers/app-demo-server/server.py"],
      "env": {}
    }
  }
}
```

### With Frontend App
The frontend can communicate with this MCP server through:
- Direct HTTP requests (if extended with HTTP endpoints)
- WebSocket connections (if extended)
- Through Cursor IDE integration

## 🧪 Testing

### Test the Server
```bash
# Start the server
python3 server.py

# In another terminal, test with MCP client
# (You can use the main repo's test scripts)
```

### Test Individual Tools
```python
# Example tool call
{
  "name": "analyze_chat_conversation",
  "arguments": {
    "conversation": [
      {"role": "user", "content": "Hello", "timestamp": "2024-01-01T00:00:00Z"},
      {"role": "agent", "content": "Hi there! How can I help?", "timestamp": "2024-01-01T00:00:01Z"}
    ]
  }
}
```

## 🔄 Development

### Adding New Tools
1. Add tool definition to `setup_capabilities()`
2. Implement tool logic in a new method
3. Add handler in `handle_call_tool()`
4. Update configuration and documentation

### Adding New Resources
1. Add resource definition to `setup_capabilities()`
2. Implement resource content method
3. Add handler in `handle_read_resource()`
4. Update configuration and documentation

## 📁 File Structure

```
app/mcp-server/
├── server.py          # Main server implementation
├── config.yaml        # Server configuration
├── requirements.txt   # Python dependencies
├── start.sh          # Startup script
└── README.md         # This documentation
```

## 🔗 Relationship to Main MCP Server

- **Main Repo MCP Server**: General development tools, project management, research capabilities
- **App MCP Server**: Demo-specific tools, chat analysis, support agent functionality

Both can run simultaneously and serve different purposes in your development workflow.

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure MCP package is installed (`pip install mcp`)
2. **Version Conflicts**: Use virtual environment to isolate dependencies
3. **Permission Denied**: Make startup script executable (`chmod +x start.sh`)

### Debug Mode
Set logging level to DEBUG in `config.yaml` for detailed output.

## 📞 Support

For issues specific to this app MCP server, check:
1. Python version compatibility
2. MCP package installation
3. Virtual environment setup
4. Configuration file syntax

For general MCP questions, refer to the main repository documentation.
