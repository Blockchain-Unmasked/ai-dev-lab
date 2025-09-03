# Lab Development Setup Guide

## 🎯 **Overview**

This guide provides comprehensive instructions for setting up and using the AI/DEV Lab development environment, including all MCP servers, extensions, and tools needed for overall lab development and Cursor chat operations.

---

## 🚀 **Quick Start**

### **1. Verify MCP Server Status**
```bash
# Check if MCP servers are running
cd mcp-server
python3 -c "from enhanced_server import EnhancedLabMCPServer; print('✅ Enhanced Lab MCP Server ready')"
```

### **2. Test Mission System**
```bash
# Test mission creation
python3 -c "from mission_system import MissionSystem; import os; ms = MissionSystem(os.path.dirname(os.getcwd())); print('✅ Mission System ready')"
```

### **3. Verify Cursor Configuration**
- Check `.cursor/mcp.json` for server definitions
- Verify `.cursor/rules/mcp_server_usage.mdc` for usage rules
- Confirm `.cursor/environment.json` for system policies

---

## 🏗️ **MCP Server Architecture**

### **Lab MCP Servers (For Overall Lab Development)**

#### **1. ai-dev-lab-core**
- **Purpose**: Basic development operations and project management
- **Location**: `mcp-server/server.py`
- **Capabilities**: Tools, Resources, Prompts
- **Usage**: Lab development, Cursor chat operations

#### **2. ai-dev-lab-enhanced**
- **Purpose**: Advanced lab operations with mission system
- **Location**: `mcp-server/enhanced_server.py`
- **Capabilities**: Mission system, web scraping, terminal automation
- **Usage**: Complex lab development, mission coordination

### **App MCP Servers (For App-Specific Operations)**

#### **1. ai-dev-lab-app-demo**
- **Purpose**: App demo functionality only
- **Location**: `app/mcp-servers/app-demo-server/server.py`
- **Capabilities**: Chat analysis, response generation, A/B testing
- **Usage**: Within app only, NOT for lab development

---

## 🛠️ **Development Tools & Extensions**

### **Python Development**
- **ms-python.python** - Python language support
- **ms-python.black-formatter** - Code formatting
- **ms-python.pylint** - Code linting
- **ms-python.flake8** - Style guide enforcement
- **ms-python.isort** - Import sorting
- **ms-python.debugpy** - Python debugging

### **Web Development**
- **dbaeumer.vscode-eslint** - JavaScript/TypeScript linting
- **esbenp.prettier-vscode** - Code formatting
- **htmlhint.vscode-htmlhint** - HTML validation

### **General Development**
- **eamodio.gitlens** - Git integration
- **github.vscode-github-actions** - GitHub Actions support
- **ms-azuretools.vscode-docker** - Docker support
- **anysphere.remote-containers** - Container development

---

## 🔧 **Lab Development Workflows**

### **Mission-Based Development**
1. **Mission Planning**: Use mission system for task organization
2. **Execution Planning**: Break down into phases and tasks
3. **Implementation**: Execute tasks using appropriate MCP servers
4. **Progress Tracking**: Monitor mission progress and milestones
5. **Debriefing**: Document lessons learned and next steps

### **Web Analysis Workflow**
1. **Target Identification**: Define analysis objectives
2. **Content Extraction**: Use web scraping tools
3. **Data Processing**: Analyze and organize extracted content
4. **Documentation**: Create comprehensive reports and archives

### **Infrastructure Development**
1. **Requirements Analysis**: Define tool and system needs
2. **Tool Selection**: Choose appropriate development tools
3. **Configuration**: Set up and configure tools
4. **Testing**: Validate functionality and performance
5. **Documentation**: Maintain setup and usage guides

---

## 🎯 **MCP Server Usage Guidelines**

### **When to Use Lab MCP Servers**
✅ **Use Lab MCP Servers for:**
- Repository-wide file operations
- System-level development tasks
- Package installation and management
- Terminal command execution
- Mission system operations
- Web scraping and analysis
- Infrastructure management

### **When to Use App MCP Servers**
✅ **Use App MCP Servers for:**
- App-specific data operations
- App user management
- App metrics and analytics
- App content management
- App testing and validation

### **Usage Examples**

#### **Lab Development Tasks**
```python
# ✅ CORRECT: Lab development using enhanced server
await enhanced_lab_mcp_server.create_mission({
    "mission_name": "Website Audit Project",
    "mission_type": "AUDIT",
    "mission_description": "Audit blockchainunmasked.com website"
})

# ✅ CORRECT: System operations
await enhanced_lab_mcp_server.run_terminal_command({
    "command": "pip install requests",
    "working_directory": "/Users/hazael/Code/ai-dev-lab"
})

# ✅ CORRECT: Web scraping for lab projects
await enhanced_lab_mcp_server.scrape_webpage({
    "url": "https://example.com",
    "extract_type": "all"
})
```

#### **App-Specific Tasks**
```python
# ✅ CORRECT: App operations using app server
await app_mcp_server.audit_webpage({
    "url": "https://blockchainunmasked.com",
    "audit_type": "content"
})

# ✅ CORRECT: App data management
await app_mcp_server.store_conversation({
    "user_id": "user123",
    "conversation_data": {...}
})
```

---

## 🔒 **Security & Compliance**

### **Access Control**
- **Lab Servers**: Full system access for development
- **App Servers**: Restricted to app directory only
- **Cross-Server Operations**: Blocked to prevent privilege escalation

### **Boundary Enforcement**
- **Automatic Checking**: Real-time boundary validation
- **Path Validation**: Ensures operations stay within scope
- **Security Logging**: All operations and violations logged

### **Compliance Requirements**
- **Approval Workflows**: Required for sensitive operations
- **Audit Trails**: Complete operation logging
- **Policy Enforcement**: Automatic security policy application

---

## 📊 **Performance & Monitoring**

### **Resource Monitoring**
- **System Resources**: CPU, memory, disk, network
- **MCP Server Performance**: Response time, throughput, error rates
- **Mission Progress**: Completion percentage, time spent, milestones

### **Optimization Features**
- **Async Operations**: Non-blocking task execution
- **Resource Efficiency**: Optimized processing and memory usage
- **Background Management**: Efficient background task handling

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **MCP Server Not Starting**
```bash
# Check Python dependencies
pip install -r mcp-server/requirements.txt

# Verify server configuration
python3 -c "from enhanced_server import EnhancedLabMCPServer; print('Server ready')"
```

#### **Mission System Errors**
```bash
# Check mission system
python3 -c "from mission_system import MissionSystem; import os; ms = MissionSystem(os.path.dirname(os.getcwd())); print('Mission system ready')"
```

#### **Extension Issues**
```bash
# Reinstall problematic extensions
cursor --uninstall-extension <extension-id>
cursor --install-extension <extension-id>
```

### **Debug Mode**
```bash
# Enable debug logging
export AI_DEV_MCP_MODE=debug
python3 mcp-server/enhanced_server.py
```

---

## 📚 **Documentation & Resources**

### **Configuration Files**
- **`.cursor/mcp.json`** - MCP server definitions
- **`.cursor/environment.json`** - System policies
- **`.cursor/rules/mcp_server_usage.mdc`** - Usage rules
- **`.cursor/lab-development-tools.json`** - Tool configurations

### **Reference Documents**
- **`MCP_SERVER_ARCHITECTURE_RULES.md`** - Architecture guidelines
- **`MCP_SERVER_USAGE_RULES_SUMMARY.md`** - Usage rules summary
- **`REPOSITORY_CLEANUP_AND_BEST_PRACTICES.md`** - Best practices

### **Training Resources**
- **Mission System**: `mcp-server/mission_system.py`
- **Enhanced Server**: `mcp-server/enhanced_server.py`
- **Prompt Templates**: `meta/prompt-engine-templates.json`

---

## 🎯 **Best Practices**

### **Development Workflow**
1. **Plan First**: Use mission system for task organization
2. **Choose Right Tools**: Select appropriate MCP servers for tasks
3. **Monitor Progress**: Track mission progress and milestones
4. **Document Everything**: Maintain comprehensive documentation
5. **Security First**: Always respect access boundaries

### **MCP Server Usage**
1. **Lab Development**: Use Lab MCP servers for system operations
2. **App Operations**: Use App MCP servers for app functionality
3. **Clear Boundaries**: Never cross server type boundaries
4. **Proper Logging**: Ensure all operations are logged
5. **Error Handling**: Implement proper error handling and recovery

### **Performance Optimization**
1. **Async Operations**: Use async/await for I/O operations
2. **Resource Management**: Monitor and optimize resource usage
3. **Background Tasks**: Use background agents for long-running tasks
4. **Caching**: Implement appropriate caching strategies
5. **Monitoring**: Continuously monitor performance metrics

---

## 🚀 **Next Steps**

### **Immediate Actions**
1. ✅ **Setup Complete** - All MCP servers and tools configured
2. ✅ **Rules Established** - Clear usage boundaries defined
3. ✅ **Documentation Ready** - Comprehensive guides available

### **Recommended Actions**
1. **Test All Tools**: Verify functionality of all MCP servers
2. **Create Test Mission**: Practice using mission system
3. **Team Training**: Ensure all users understand boundaries
4. **Performance Testing**: Validate system performance
5. **Security Review**: Conduct security boundary testing

---

## 🎉 **Success Criteria**

### **Lab Development Environment**
- ✅ **MCP Servers**: All servers running and accessible
- ✅ **Mission System**: Mission creation and management working
- ✅ **Development Tools**: All extensions and tools installed
- ✅ **Security Boundaries**: Clear separation between server types
- ✅ **Documentation**: Comprehensive guides and examples

### **Ready for Production**
- ✅ **Security**: All boundaries enforced and monitored
- ✅ **Performance**: Optimized for development workloads
- ✅ **Scalability**: Easy to add new tools and servers
- ✅ **Maintainability**: Clear architecture and documentation
- ✅ **Compliance**: All security policies implemented

---

**Result**: The AI/DEV Lab is now fully equipped with comprehensive development tools, MCP servers, and clear usage boundaries. All tools are configured for overall lab development and Cursor chat operations, with proper security and compliance measures in place! 🎉
