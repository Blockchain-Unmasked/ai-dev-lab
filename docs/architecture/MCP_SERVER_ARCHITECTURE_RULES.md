# MCP Server Architecture Rules & Boundaries

## 🏗️ **MCP Server Hierarchy & Classification**

### **1. Lab MCP Servers (Core Infrastructure)**
**Location**: `/mcp-server/` (root level)
**Purpose**: Core development tools, project management, and system-wide capabilities
**Scope**: Repository-wide, affects entire AI/DEV Lab ecosystem

#### **Lab MCP Server Types**
- **Main Lab Server** (`mcp-server/server.py`)
  - Development assistance tools
  - Project management capabilities
  - Research and analysis tools
  - System-wide configuration management

- **Enhanced Lab Server** (`mcp-server/enhanced_server.py`)
  - Web scraping and analysis tools
  - Terminal automation capabilities
  - Cross-project utilities
  - Infrastructure management tools

#### **Lab MCP Server Rules**
- **Access Level**: Full system access
- **Permissions**: Can modify repository files, run system commands
- **Scope**: Repository-wide operations
- **Security**: High security requirements, full audit logging
- **Dependencies**: Can access all project resources

---

### **2. App MCP Servers (Application-Specific)**
**Location**: `/app/mcp-servers/` (application level)
**Purpose**: Specific to individual applications, limited scope
**Scope**: Single application or feature set

#### **App MCP Server Types**
- **App Demo Server** (`app/mcp-servers/app-demo-server/server.py`)
  - AI Intake/Support Agent demo tools
  - Chat analysis and response generation
  - A/B testing capabilities
  - Demo-specific resources

- **Database Server** (`app/mcp-servers/database-server/server.py`)
  - Content storage and retrieval
  - User data management
  - A/B testing metrics
  - Data export capabilities

- **Website Audit Server** (`app/mcp-servers/website-audit/server.py`)
  - Web scraping tools
  - Content extraction
  - Screenshot capture
  - Audit data management

- **Content Archive Server** (`app/mcp-servers/content-archive/server.py`)
  - Historical content access
  - Search and retrieval
  - Content relationships
  - Archive management

#### **App MCP Server Rules**
- **Access Level**: Limited to application scope
- **Permissions**: Cannot modify system files outside app directory
- **Scope**: Single application or feature
- **Security**: Application-level security, sandboxed
- **Dependencies**: Limited to app-specific resources

---

## 🔒 **Security Boundaries & Access Control**

### **Lab MCP Servers - Full Access**
```python
# Lab servers can access:
- Repository root directory
- System commands and terminal
- All project files
- Environment variables
- Network resources
- File system operations
```

### **App MCP Servers - Restricted Access**
```python
# App servers can access:
- App-specific directories only
- App-specific databases
- App-specific configuration
- Limited file system access
- No system-level operations
- No repository-wide modifications
```

---

## 📁 **Directory Structure & Naming Conventions**

### **Lab MCP Servers**
```
mcp-server/
├── server.py              # Main lab server
├── enhanced_server.py     # Enhanced capabilities
├── config.yaml           # Lab configuration
├── requirements.txt      # Lab dependencies
└── README.md            # Lab documentation
```

### **App MCP Servers**
```
app/
├── mcp-server/           # App demo server
│   ├── server.py
│   ├── config.yaml
│   └── requirements.txt
├── mcp-servers/          # Additional app servers
│   ├── database-server/
│   ├── website-audit/
│   └── content-archive/
└── frontend/             # App frontend
```

---

## 🚫 **Strict Prohibition Rules**

### **App MCP Servers CANNOT:**
1. **Access repository root** (`/Users/hazael/Code/ai-dev-lab/`)
2. **Execute system commands** (terminal, shell)
3. **Modify system files** outside app directory
4. **Access environment variables** (except app-specific)
5. **Install system packages** or modify system configuration
6. **Access other applications** or cross-app data
7. **Perform network operations** outside app scope
8. **Modify MCP server configurations** of other servers

### **Lab MCP Servers CAN:**
1. **Access entire repository** and all subdirectories
2. **Execute system commands** and terminal operations
3. **Modify system files** and configurations
4. **Access all environment variables**
5. **Install packages** and manage dependencies
6. **Coordinate between applications** and MCP servers
7. **Perform network operations** and external API calls
8. **Manage and configure** all MCP servers

---

## 🔧 **Implementation Guidelines**

### **Creating New Lab MCP Servers**
```python
# Lab server template
class LabMCPServer:
    def __init__(self):
        self.server = Server("ai-dev-lab-core")
        self.access_level = "full_system"
        self.scope = "repository_wide"
        self.security_level = "high"
        
    def setup_capabilities(self):
        # Full system access tools
        # Repository-wide operations
        # System management capabilities
```

### **Creating New App MCP Servers**
```python
# App server template
class AppMCPServer:
    def __init__(self):
        self.server = Server("ai-dev-lab-app-specific")
        self.access_level = "application_scope"
        self.scope = "single_application"
        self.security_level = "sandboxed"
        
    def setup_capabilities(self):
        # App-specific tools only
        # Limited file system access
        # Application-scoped operations
```

---

## 🔍 **Validation & Enforcement**

### **Access Validation**
```python
def validate_access_path(server_type, requested_path):
    if server_type == "app":
        # Must be within app directory
        if not requested_path.startswith("/app/"):
            raise SecurityError("App servers cannot access paths outside app directory")
    elif server_type == "lab":
        # Can access any path
        pass
```

### **Permission Checking**
```python
def check_permissions(server_type, operation):
    if server_type == "app":
        if operation in ["system_command", "file_modification", "env_access"]:
            raise PermissionError("App servers cannot perform system operations")
    elif server_type == "lab":
        # All operations allowed
        pass
```

---

## 📋 **Configuration Examples**

### **Lab MCP Server Configuration**
```json
{
  "mcpServers": {
    "ai-dev-lab-core": {
      "command": "python3",
      "args": ["/path/to/mcp-server/server.py"],
      "env": {},
      "access_level": "full_system",
      "scope": "repository_wide"
    }
  }
}
```

### **App MCP Server Configuration**
```json
{
  "mcpServers": {
    "ai-dev-lab-app-demo": {
      "command": "python3",
      "args": ["/path/to/app/mcp-servers/app-demo-server/server.py"],
      "env": {},
      "access_level": "application_scope",
      "scope": "single_application",
      "restricted_paths": ["/app/"]
    }
  }
}
```

---

## 🚨 **Security Violations & Consequences**

### **Immediate Actions**
1. **Server Termination**: Violating servers are immediately stopped
2. **Access Revocation**: Server loses all permissions
3. **Audit Logging**: All violations are logged and reported
4. **Investigation**: Security team investigates the violation

### **Recovery Procedures**
1. **Server Isolation**: Violating server is isolated
2. **Code Review**: Security team reviews server code
3. **Permission Reset**: Server permissions are reset to safe defaults
4. **Testing**: Server is tested in sandbox before reactivation

---

## 📊 **Monitoring & Compliance**

### **Continuous Monitoring**
- **Access Logs**: All server operations are logged
- **Permission Checks**: Real-time permission validation
- **Path Monitoring**: File system access tracking
- **Command Logging**: System command execution logging

### **Compliance Reporting**
- **Daily Reports**: Access violation summaries
- **Weekly Reviews**: Security compliance assessments
- **Monthly Audits**: Comprehensive security audits
- **Quarterly Reviews**: Architecture and security reviews

---

## 🔄 **Update & Maintenance Procedures**

### **Lab MCP Server Updates**
1. **Full Testing**: Complete functionality testing
2. **Security Review**: Security team approval required
3. **Rollout**: Gradual rollout with rollback capability
4. **Documentation**: Update architecture documentation

### **App MCP Server Updates**
1. **Scope Validation**: Ensure updates don't expand scope
2. **Permission Review**: Verify no new permissions added
3. **Testing**: Sandbox testing before deployment
4. **Documentation**: Update app-specific documentation

---

## 📚 **Documentation Requirements**

### **Lab MCP Servers**
- **Architecture Documentation**: Complete system architecture
- **Security Documentation**: Security protocols and procedures
- **API Documentation**: All available tools and capabilities
- **Maintenance Procedures**: Update and maintenance guides

### **App MCP Servers**
- **Application Documentation**: App-specific functionality
- **Scope Documentation**: Clear boundaries and limitations
- **API Documentation**: Available tools and resources
- **User Guides**: End-user documentation and examples

---

**Document Version**: 1.0  
**Last Updated**: August 26, 2025  
**Next Review**: Monthly  
**Approval Status**: Approved by Security Team
