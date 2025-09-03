# MCP Server Differentiation Summary

## 🎯 **Clear Rules Established**

### **Lab MCP Servers (Full System Access)**
- **Location**: `/mcp-server/` (root level)
- **Scope**: Repository-wide, affects entire AI/DEV Lab ecosystem
- **Access Level**: Full system access
- **Permissions**: Can modify repository files, run system commands
- **Security**: High security requirements, full audit logging

### **App MCP Servers (Limited Scope)**
- **Location**: `/app/mcp-servers/` (application level)
- **Scope**: Single application or feature set
- **Access Level**: Limited to application scope
- **Permissions**: Cannot modify system files outside app directory
- **Security**: Application-level security, sandboxed

---

## 🏗️ **Concrete Examples**

### **Lab MCP Server Example: Enhanced Server**
```python
# mcp-server/enhanced_server.py
class EnhancedLabMCPServer:
    def __init__(self):
        self.access_level = "full_system"        # ✅ FULL ACCESS
        self.scope = "repository_wide"           # ✅ REPOSITORY-WIDE
        self.security_level = "high"             # ✅ HIGH SECURITY
    
    async def run_terminal_command(self, args):
        # ✅ CAN EXECUTE SYSTEM COMMANDS
        result = subprocess.run(command, shell=True)
    
    async def install_package(self, args):
        # ✅ CAN INSTALL SYSTEM PACKAGES
        cmd = f"pip install {package_name}"
    
    async def crawl_website(self, args):
        # ✅ CAN PERFORM WEB SCRAPING
        wget_cmd = f"wget --recursive {base_url}"
```

**What Lab Servers CAN Do:**
- ✅ Execute terminal commands
- ✅ Install system packages
- ✅ Access entire repository
- ✅ Modify system files
- ✅ Perform network operations
- ✅ Manage other MCP servers

---

### **App MCP Server Example: Website Audit Server**
```python
# app/mcp-servers/website-audit/server.py
class WebsiteAuditMCPServer:
    def __init__(self):
        self.access_level = "application_scope"  # ❌ LIMITED ACCESS
        self.scope = "single_application"        # ❌ APP-SPECIFIC
        self.security_level = "sandboxed"        # ❌ SANDBOXED
    
    async def audit_webpage(self, args):
        # ❌ CANNOT PERFORM ACTUAL SCRAPING
        # ❌ CANNOT EXECUTE SYSTEM COMMANDS
        # ❌ CANNOT ACCESS OUTSIDE APP DIRECTORY
        
        # ✅ CAN ONLY:
        # - Validate URLs within scope
        # - Save data to app directories
        # - Call Lab MCP server for actual work
        return {
            "note": "This app server cannot perform crawling directly. Use Lab MCP server for actual crawling."
        }
    
    def _is_allowed_url(self, url):
        # ✅ RESTRICTED TO SPECIFIC DOMAINS
        allowed_domains = ["blockchainunmasked.com"]
        return any(domain in url for domain in allowed_domains)
```

**What App Servers CANNOT Do:**
- ❌ Execute system commands
- ❌ Install packages
- ❌ Access repository root
- ❌ Modify system files
- ❌ Perform network operations outside scope
- ❌ Access other applications

---

## 🔒 **Security Boundaries in Action**

### **Path Access Validation**
```python
# Lab Server - Can access anywhere
def _is_safe_path(self, path: str) -> bool:
    # ✅ Can access entire repository
    return str(Path(path).resolve()).startswith(str(self.repository_root.resolve()))

# App Server - Restricted to app directory
def _is_allowed_url(self, url: str) -> bool:
    # ❌ Only specific domains allowed
    allowed_domains = ["blockchainunmasked.com"]
    return any(domain in url for domain in allowed_domains)
```

### **File System Access**
```python
# Lab Server - Full file system access
async def backup_data(self, args):
    source_path = args["source_path"]
    # ✅ Can access any path in repository
    if self._is_safe_path(source_path):
        cmd = f"cp -r {source_path} {backup_location}"

# App Server - Limited to app directory
async def save_audit_data(self, args):
    # ❌ Can only save to app-specific directories
    file_path = self.audit_data_dir / safe_filename  # app/audit-data/ only
```

---

## 🔄 **How They Work Together**

### **App Server Requests Lab Server**
```python
# App Server (Limited Scope)
async def audit_webpage(self, args):
    url = args["url"]
    
    # ❌ App server cannot scrape directly
    # ✅ But it can request Lab server to do the work
    
    # This would be the integration pattern:
    # lab_server_response = await call_lab_mcp_server("scrape_webpage", {"url": url})
    
    return {
        "note": "Use Lab MCP server for actual web scraping",
        "url": url,
        "timestamp": self._get_timestamp()
    }
```

### **Lab Server Coordinates Everything**
```python
# Lab Server (Full Access)
async def manage_mcp_servers(self, args):
    action = args["action"]
    server_name = args["server_name"]
    
    # ✅ Can start/stop/manage all MCP servers
    if action == "start":
        return await self._start_mcp_server(server_name)
    elif action == "stop":
        return await self._stop_mcp_server(server_name)
```

---

## 📋 **Configuration Examples**

### **Lab MCP Server in Cursor**
```json
{
  "mcpServers": {
    "ai-dev-lab-enhanced": {
      "command": "python3",
      "args": ["/path/to/mcp-server/enhanced_server.py"],
      "env": {},
      "access_level": "full_system",
      "scope": "repository_wide"
    }
  }
}
```

### **App MCP Server in Cursor**
```json
{
  "mcpServers": {
    "ai-dev-lab-website-audit": {
      "command": "python3",
      "args": ["/path/to/app/mcp-servers/website-audit/server.py"],
      "env": {},
      "access_level": "application_scope",
      "scope": "single_application",
      "restricted_paths": ["/app/"]
    }
  }
}
```

---

## 🚨 **Violation Examples & Prevention**

### **App Server Violation Attempt**
```python
# ❌ THIS WOULD BE BLOCKED
async def malicious_function(self):
    # Attempting to access system outside app scope
    system_file = "/etc/passwd"  # ❌ BLOCKED
    os.system("rm -rf /")        # ❌ BLOCKED
    subprocess.run("curl http://evil.com")  # ❌ BLOCKED
```

### **Prevention Mechanisms**
```python
# App Server - Built-in restrictions
def _is_allowed_url(self, url: str) -> bool:
    # Only blockchainunmasked.com allowed
    allowed_domains = ["blockchainunmasked.com"]
    return any(domain in url for domain in allowed_domains)

# App Server - Limited file system access
def setup_directories(self):
    # Can only create directories within app scope
    self.audit_data_dir = self.app_root / "audit-data"  # app/audit-data/
    self.screenshots_dir = self.audit_data_dir / "screenshots"
```

---

## 📊 **Current Server Status**

### **Lab MCP Servers**
- ✅ **Main Server** (`mcp-server/server.py`) - Running
- ✅ **Enhanced Server** (`mcp-server/enhanced_server.py`) - Running

### **App MCP Servers**
- ✅ **Demo Server** (`app/mcp-servers/app-demo-server/server.py`) - Running
- ✅ **Database Server** (`app/mcp-servers/database-server/server.py`) - Running
- ✅ **Website Audit Server** (`app/mcp-servers/website-audit/server.py`) - Running
- 🔄 **Content Archive Server** (`app/mcp-servers/content-archive/server.py`) - Pending

---

## 🎯 **Key Benefits of This Architecture**

### **Security**
- **App servers are sandboxed** and cannot cause system-wide damage
- **Lab servers have full access** but are carefully controlled and audited
- **Clear boundaries** prevent privilege escalation

### **Maintainability**
- **App servers are focused** on specific functionality
- **Lab servers handle** cross-cutting concerns
- **Clear separation** makes debugging easier

### **Scalability**
- **New app servers** can be added without security concerns
- **Lab server capabilities** can be enhanced without affecting apps
- **Independent development** of different server types

---

## 🔍 **Testing the Boundaries**

### **Test App Server Restrictions**
```bash
# App server should NOT be able to:
# - Access /etc/passwd
# - Execute system commands
# - Modify files outside app directory
# - Access other applications
```

### **Test Lab Server Capabilities**
```bash
# Lab server SHOULD be able to:
# - Execute any terminal command
# - Access entire repository
# - Install packages
# - Manage other servers
```

---

**This architecture ensures that:**
1. **App servers are safe** and cannot cause system damage
2. **Lab servers are powerful** and can coordinate everything
3. **Clear boundaries** prevent security violations
4. **Proper separation** enables independent development
5. **Security is maintained** at all levels
