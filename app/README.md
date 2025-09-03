# AI Intake/Support Agent Demo

## Overview

This is a **super simple, barebones MVP** demo of an AI intake/support agent system. It's designed to test three different AI APIs (starting with Google Gemini) and includes A/B testing capabilities.

## 🎯 Features

### **Dual-Mode Support**
- **AI Mode**: Uses Google Gemini API (when configured) or smart mock responses
- **Canned Responses**: Predefined responses for testing without AI

### **A/B Testing Interface**
- **View A**: Customer-facing simple chat interface
- **View B**: Quality assurance view showing full agent operation details

### **Progressive Enhancement**
- **Works immediately** without any setup (mock responses)
- **Enhanced with real AI** when API key is added
- **Configurable** model selection and parameters

## 🚀 Getting Started

### **Immediate Demo (No Setup Required)**
1. **Start the server**: `python3 -m http.server 3000`
2. **Open browser**: Navigate to `http://localhost:3000`
3. **Start chatting**: Everything works out of the box!

### **With Real Gemini API**
1. **Get API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Click "Configure"** in the demo
3. **Enter your API key** and model preferences
4. **Enjoy real AI responses**!

## 🏗️ Architecture

### **Pure Web Standards**
- **No frameworks** - just HTML5, CSS3, ES2023+
- **Web Components** for modularity
- **CSS Custom Properties** for theming
- **Modern JavaScript** with modules

### **Component Structure**
```
app/frontend/
├── index.html              # Main HTML document
├── assets/css/main.css     # Pure CSS architecture
├── scripts/
│   ├── main.js            # Application controller
│   ├── chat-agent.js      # Chat interface management
│   ├── gemini-api.js      # AI API integration
│   └── ab-testing.js      # A/B testing logic
```

## 🔧 Configuration

### **AI Settings**
- **API Key**: Your Google Gemini API key
- **Model**: Gemini Pro or Gemini Flash
- **Temperature**: Response creativity (0.0 - 1.0)

### **A/B Testing**
- **Test Groups**: Automatic assignment
- **Metrics**: Response time, satisfaction, resolution rate
- **Data Export**: CSV format for analysis

## 🧪 Testing

### **Test Scenarios**
1. **Mock AI Responses**: Test without API key
2. **Canned Responses**: Test predefined responses
3. **Real AI**: Test with Gemini API
4. **A/B Testing**: Compare customer vs QA views

### **Quality Assurance**
- **Response Time**: Track performance metrics
- **User Satisfaction**: Monitor quality scores
- **Resolution Rate**: Measure effectiveness

## 🔌 MCP Server Integration

### **App-Specific MCP Server**
Located in `app/mcp-server/`, this provides:

#### **Tools**
- `analyze_chat_conversation` - Chat sentiment and intent analysis
- `generate_response_template` - Response template generation
- `calculate_response_metrics` - A/B testing metrics calculation

#### **Resources**
- `app://chat-templates` - Predefined response templates
- `app://qa-guidelines` - Quality assurance guidelines
- `app://ab-testing-config` - A/B testing configuration

#### **Prompts**
- `customer_greeting` - Friendly customer greetings
- `problem_escalation` - Escalation response generation

### **Using the App MCP Server**

#### **Start the Server**
```bash
cd app/mcp-server
./start.sh
```

#### **Test Functionality**
```bash
python3 test_server.py
```

#### **Integration with Cursor IDE**
Add to `.cursor/mcp.json`:
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

## 📊 A/B Testing

### **What Gets Tested**
- **Response Styles**: Formal vs Casual
- **Response Length**: Concise vs Detailed
- **Interaction Patterns**: Different conversation flows

### **Metrics Collected**
- **Response Time**: How fast the agent responds
- **User Satisfaction**: Quality ratings
- **Resolution Rate**: Problem-solving success
- **Engagement**: Message count and depth

### **Data Export**
- **CSV Format**: Easy analysis in Excel/Google Sheets
- **Real-time Updates**: Live metrics during testing
- **Historical Data**: Track improvements over time

## 🎨 Customization

### **Styling**
- **CSS Variables**: Easy color and spacing changes
- **Responsive Design**: Mobile-first approach
- **Theme Support**: Light/dark mode ready

### **Functionality**
- **Modular JavaScript**: Easy to extend
- **Event-Driven**: Clean component communication
- **Configurable**: Settings panel for customization

## 🚨 Troubleshooting

### **Common Issues**

#### **App Not Loading**
- Check if server is running on port 3000
- Verify all JavaScript files are loading
- Check browser console for errors

#### **AI Not Working**
- Verify API key is correct
- Check network connectivity
- Ensure model selection is valid

#### **A/B Testing Issues**
- Clear browser storage if needed
- Check if metrics are being recorded
- Verify view switching is working

### **Debug Mode**
- **Browser Console**: Full error logging
- **Network Tab**: API request monitoring
- **Local Storage**: Configuration inspection

## 🔮 Future Enhancements

### **Planned Features**
- **Multi-AI Support**: OpenAI, Anthropic, etc.
- **Advanced Analytics**: Detailed conversation insights
- **Human Handoff**: Seamless escalation to humans
- **Voice Support**: Speech-to-text integration

### **Integration Possibilities**
- **CRM Systems**: Customer data integration
- **Knowledge Base**: Dynamic response generation
- **Analytics Platforms**: Advanced reporting
- **Mobile Apps**: Native mobile support

## 📚 Resources

### **Documentation**
- [App MCP Server README](mcp-server/README.md)
- [Frontend Architecture](frontend/README.md)
- [API Integration Guide](frontend/scripts/gemini-api.js)

### **External Links**
- [Google Gemini API](https://ai.google.dev/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Web Components](https://developer.mozilla.org/en-US/docs/Web/Web_Components)

## 🤝 Contributing

### **Development Setup**
1. **Clone repository**
2. **Install dependencies**: `npm install` (if adding packages)
3. **Start development server**: `python3 -m http.server 3000`
4. **Make changes** and test in browser

### **Code Standards**
- **Pure Web Standards**: No frameworks
- **ES2023+**: Modern JavaScript features
- **Semantic HTML**: Accessible markup
- **Responsive CSS**: Mobile-first design

---

**Ready to test? Start the server and begin chatting!** 🚀
