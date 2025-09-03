# MCP Server Usage Rules Summary

## 🎯 **Overview**

This document summarizes all the rules, configurations, and boundaries that have been established to ensure proper usage of MCP servers in the AI/DEV Lab project.

---

## 🏗️ **Server Type Definitions**

### **Lab MCP Servers**
- **Purpose**: Overall lab development and Cursor chat operations
- **Scope**: Repository-wide operations and development tasks
- **Access Level**: Full system access for lab development needs
- **Usage Context**: Cursor chat, lab development, system administration

### **App MCP Servers**
- **Purpose**: App-specific functionality only
- **Scope**: Limited to app directory and app-specific operations
- **Access Level**: Sandboxed, application-scoped access only
- **Usage Context**: Within the app only, NOT for lab development

---

## 📁 **Server Configuration Files**

### **1. Cursor Rules** (`.cursor/rules/mcp_server_usage.mdc`)
- **Purpose**: Comprehensive usage rules and examples
- **Enforcement**: Manual compliance and guidance
- **Coverage**: Complete usage boundaries and restrictions

### **2. Environment Configuration** (`.cursor/environment.json`)
- **Purpose**: System-level MCP server rules
- **Enforcement**: Automatic boundary enforcement
- **Coverage**: Security policies and access control

### **3. MCP Configuration** (`.cursor/mcp.json`)
- **Purpose**: Server definitions and usage policies
- **Enforcement**: Server-level access control
- **Coverage**: Individual server capabilities and restrictions

---

## 🔒 **Security Boundaries & Enforcement**

### **Automatic Enforcement**
```json
{
  "mcp_server_rules": {
    "enforce_boundaries": true,
    "lab_servers_for_development": true,
    "app_servers_for_app_only": true,
    "cross_server_operations_blocked": true,
    "security_violations_logged": true
  }
}
```

### **Boundary Enforcement**
```json
{
  "boundary_enforcement": {
    "cross_server_operations_blocked": true,
    "security_violations_logged": true,
    "automatic_boundary_checking": true
  }
}
```

---

## 📋 **Server Definitions**

### **Lab MCP Servers**

#### **1. ai-dev-lab-core**
```json
{
  "server_type": "lab",
  "usage": "overall_lab_development_and_cursor_chat",
  "scope": "repository_wide",
  "restrictions": "none",
  "capabilities": ["tools", "resources", "prompts"]
}
```

#### **2. ai-dev-lab-enhanced**
```json
{
  "server_type": "lab",
  "usage": "overall_lab_development_and_cursor_chat",
  "scope": "repository_wide",
  "restrictions": "none",
  "capabilities": ["tools", "resources", "prompts"],
  "special_features": ["mission_system", "web_scraping", "terminal_operations"]
}
```

### **App MCP Servers**

#### **1. ai-dev-lab-app-demo**
```json
{
  "server_type": "app",
  "usage": "app_specific_functionality_only",
  "scope": "app_directory_only",
  "restrictions": "app_directory_only",
  "capabilities": ["tools", "resources"],
  "security": {
    "app_directory_only": true,
    "no_system_access": true
  }
}
```

---

## 🚫 **Usage Restrictions**

### **Lab MCP Server Restrictions**
- **Cannot be used for**: App-specific operations that should use App MCP servers
- **Must respect**: Repository boundaries and security policies
- **Requires approval**: For sensitive operations and system changes

### **App MCP Server Restrictions**
- **Cannot be used for**: Lab development, system operations, or Cursor chat tasks
- **Must stay within**: App directory boundaries
- **Cannot access**: System resources outside app scope

### **Cross-Server Usage Rules**
```python
# ALLOWED: Lab → App coordination
lab_server.manage_mcp_servers(action="start", server_name="app-demo-server")

# ALLOWED: Lab → App data access (through proper channels)
lab_server.run_terminal_command("ls app/mcp-servers/")

# FORBIDDEN: App → Lab operations
app_server.run_terminal_command("pip install package")  # ❌ BLOCKED

# FORBIDDEN: App → System access
app_server.access_system_files()  # ❌ BLOCKED
```

---

## 📋 **Usage Examples**

### **Correct Lab MCP Server Usage**
```python
# ✅ CORRECT: Lab development task
await lab_mcp_server.run_terminal_command({
    "command": "pip install requests",
    "working_directory": "/Users/hazael/Code/ai-dev-lab"
})

# ✅ CORRECT: Mission system operation
await lab_mcp_server.create_mission({
    "mission_name": "Website Audit Project",
    "mission_type": "AUDIT",
    "mission_description": "Audit blockchainunmasked.com website"
})

# ✅ CORRECT: Web scraping for lab project
await lab_mcp_server.scrape_webpage({
    "url": "https://example.com",
    "extract_type": "all"
})
```

### **Correct App MCP Server Usage**
```python
# ✅ CORRECT: App-specific operation
await app_mcp_server.audit_webpage({
    "url": "https://blockchainunmasked.com",
    "audit_type": "content"
})

# ✅ CORRECT: App data management
await app_mcp_server.store_conversation({
    "user_id": "user123",
    "conversation_data": {...}
})

# ✅ CORRECT: App metrics
await app_mcp_server.record_ab_metric({
    "test_id": "test001",
    "variant": "A",
    "metric": "conversion_rate"
})
```

### **Incorrect Usage (Will Be Blocked)**
```python
# ❌ INCORRECT: App server trying system operations
await app_mcp_server.run_terminal_command("pip install package")  # BLOCKED

# ❌ INCORRECT: App server accessing system files
await app_mcp_server.access_system_file("/etc/passwd")  # BLOCKED

# ❌ INCORRECT: Lab server for app-specific tasks
await lab_mcp_server.audit_webpage({...})  # WRONG SERVER TYPE
```

---

## 🎯 **Cursor Chat Guidelines**

### **For Lab Development Tasks**
1. **Use Lab MCP Servers**: For system operations, development tasks
2. **Full Context**: Access to repository-wide resources
3. **System Operations**: Terminal commands, package installation
4. **Mission Coordination**: Mission system operations

### **For App-Specific Tasks**
1. **Use App MCP Servers**: For app functionality and data
2. **Limited Scope**: App directory operations only
3. **App Operations**: User management, data storage, app metrics
4. **No System Access**: Cannot perform system-level operations

### **Task Classification**
```python
def classify_task(task_description):
    if any(keyword in task_description.lower() for keyword in [
        "system", "repository", "development", "install", "terminal", "mission"
    ]):
        return "LAB_MCP_SERVER"
    elif any(keyword in task_description.lower() for keyword in [
        "app", "user", "conversation", "audit", "metrics", "data"
    ]):
        return "APP_MCP_SERVER"
    else:
        return "UNKNOWN"
```

---

## 🚨 **Violation Handling**

### **Immediate Actions**
1. **Operation Blocked**: Violating operations are immediately stopped
2. **Logging**: All violations are logged with full context
3. **User Notification**: Clear explanation of why operation was blocked
4. **Corrective Guidance**: Suggest proper server usage

### **Violation Examples**
```python
# ❌ VIOLATION: App server trying system access
app_server.run_terminal_command("rm -rf /")  # BLOCKED + LOGGED

# ❌ VIOLATION: Lab server for app-specific data
lab_server.store_conversation({...})  # WRONG SERVER + GUIDANCE

# ❌ VIOLATION: Cross-boundary access
app_server.access_lab_files()  # BLOCKED + SECURITY ALERT
```

---

## 📚 **Documentation & Training**

### **Required Knowledge**
- **All Users**: Must understand Lab vs App MCP server boundaries
- **Developers**: Must know which server type for which tasks
- **Reviewers**: Must validate server usage in code reviews

### **Training Resources**
- **Architecture Rules**: `MCP_SERVER_ARCHITECTURE_RULES.md`
- **Differentiation Guide**: `MCP_SERVER_DIFFERENTIATION_SUMMARY.md`
- **Best Practices**: `REPOSITORY_CLEANUP_AND_BEST_PRACTICES.md`
- **Usage Rules**: `.cursor/rules/mcp_server_usage.mdc`

---

## ✅ **Compliance Checklist**

### **Before Using Any MCP Server**
- [ ] **Task Classification**: Is this a lab development or app operation?
- [ ] **Server Selection**: Am I using the correct server type?
- [ ] **Scope Validation**: Is the operation within the server's scope?
- [ ] **Security Check**: Does this operation respect security boundaries?
- [ ] **Approval Required**: Do I need approval for this operation?

### **After Using MCP Server**
- [ ] **Operation Logged**: Is the operation properly logged?
- [ ] **Results Documented**: Are results documented appropriately?
- [ ] **Security Maintained**: Were security boundaries respected?
- [ ] **Next Steps Clear**: Are next steps clearly defined?

---

## 🔧 **Configuration Files Summary**

### **Files Modified/Created**
1. **`.cursor/rules/mcp_server_usage.mdc`** - Comprehensive usage rules
2. **`.cursor/environment.json`** - System-level MCP server rules
3. **`.cursor/mcp.json`** - Server definitions and usage policies
4. **`MCP_SERVER_USAGE_RULES_SUMMARY.md`** - This summary document

### **Rules Enforcement Levels**
1. **Cursor Rules** (`.mdc`) - Manual compliance and guidance
2. **Environment Config** (`.json`) - System-level enforcement
3. **MCP Config** (`.json`) - Server-level access control
4. **Code Implementation** - Runtime boundary checking

---

## 🎯 **Key Takeaways**

### **Remember These Rules**
- **Lab MCP Servers** = Overall lab development and Cursor chat operations
- **App MCP Servers** = App-specific functionality only
- **Clear boundaries** = Secure, maintainable, and efficient development
- **When in doubt** = Use Lab MCP servers for development, App MCP servers for app operations

### **Security Benefits**
- **Prevents privilege escalation** between server types
- **Maintains clear access boundaries** for different contexts
- **Enables proper audit logging** of all operations
- **Ensures compliance** with security policies

### **Development Benefits**
- **Clear separation of concerns** between lab and app operations
- **Easier maintenance** with well-defined server purposes
- **Better scalability** for adding new servers
- **Improved debugging** with clear operation boundaries

---

**Result**: Comprehensive MCP server usage rules have been established across all configuration files, ensuring clear boundaries between Lab MCP servers (for overall lab development and Cursor chat) and App MCP servers (for app-specific functionality only). All rules are enforced at multiple levels for maximum security and compliance.
