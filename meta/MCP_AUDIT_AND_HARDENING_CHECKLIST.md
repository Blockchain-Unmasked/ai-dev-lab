# MCP Audit & Hardening Checklist - AI/DEV Lab Project

## 🎯 **Audit Overview**
This checklist ensures your MCP servers are secure, compliant, and fully functional with Cursor IDE integration.

**Target Servers:**
- **Lab MCP Servers**: `mcp-server/`, system-wide development tools
- **App MCP Servers**: `app/mcp-servers/`, application-specific functionality

---

## 📋 **Phase 1: Cursor Rules Validation (5 minutes)**

### ✅ **Rules Panel Check**
- [ ] Open **Project → Rules** in Cursor
- [ ] Verify no warnings for any `.mdc` files
- [ ] Confirm rule types display correctly:
  - `mcp_server_usage.mdc` → **Always**
  - `enterprise_mode.mdc` → **Agent Requested** 
  - `free_mode.mdc` → **Agent Requested**

### ✅ **Rule Behavior Verification**
Run these prompts in Cursor chat to test each rule:

#### **Test 1: Always Rule (mcp_server_usage)**
```
List all project rules, their types (Always/Auto/Agent), and when you will apply each. 
Are any rules missing descriptions or globs? If so, propose fixes.
```
**Expected:** `mcp_server_usage` guidance appears automatically

#### **Test 2: Agent Requested Rules**
```
For this task, evaluate whether loading 'enterprise_mode' helps. 
If yes, load it and explain the additional steps you'll take.
```
**Expected:** Model can see and opt into enterprise_mode

#### **Test 3: Path-Specific Behavior**
```
Given I'm editing 'app/backend/models.py', which rules are auto-attached right now and why?
```
**Expected:** Only `mcp_server_usage` (Always rule) should be active

---

## 🔧 **Phase 2: MCP Server Conformance Testing (15 minutes)**

### ✅ **Lab MCP Server Validation**
```bash
# Navigate to lab MCP server directory
cd mcp-server/

# Test server startup and tool listing
python server.py --help
python -m mcp.server server.py --help

# If using Python SDK client
python -c "
from mcp import ClientSession, StdioServerParameters
import asyncio

async def test_lab_server():
    params = StdioServerParameters(command='python', args=['server.py'])
    async with ClientSession(params) as session:
        tools = await session.list_tools()
        print(f'Lab Server Tools: {len(tools.tools)}')
        for tool in tools.tools:
            print(f'  - {tool.name}: {tool.description}')
        
        prompts = await session.list_prompts()
        print(f'Lab Server Prompts: {len(prompts.prompts)}')
        
        resources = await session.list_resources()
        print(f'Lab Server Resources: {len(resources.resources)}')

asyncio.run(test_lab_server())
"
```

**Expected Results:**
- [ ] Server starts without errors
- [ ] Tools list includes: `run_terminal_command`, `install_package`, `scrape_webpage`, etc.
- [ ] No authentication/security errors
- [ ] Tool schemas are properly defined

### ✅ **App MCP Server Validation**
```bash
# Navigate to app MCP servers
cd app/mcp-servers/

# Test each app server individually
for server_dir in */; do
    echo "Testing $server_dir"
    cd "$server_dir"
    
    # Check if server has main.py or server.py
    if [ -f "main.py" ]; then
        python main.py --help
    elif [ -f "server.py" ]; then
        python server.py --help
    fi
    
    cd ..
done
```

**Expected Results:**
- [ ] Each app server starts without errors
- [ ] App servers only expose app-specific tools
- [ ] No system-level or cross-project tools visible

---

## 🛡️ **Phase 3: Security Hardening (10 minutes)**

### ✅ **Terminal Command Security**
Check each MCP server that has terminal execution capabilities:

#### **Lab Server Terminal Tools**
```python
# In mcp-server/server.py, verify these security measures:
# 1. Path whitelisting
ALLOWED_PATHS = [
    "/Users/hazael/Code/ai-dev-lab",
    "/Users/hazael/Code/ai-dev-lab/app",
    "/Users/hazael/Code/ai-dev-lab/mcp-server"
]

# 2. Command allow-listing
ALLOWED_COMMANDS = [
    "git", "python", "pip", "npm", "node",
    "ls", "cat", "head", "tail", "grep",
    "mkdir", "touch", "cp", "mv", "rm"
]

# 3. No dangerous commands
BLOCKED_COMMANDS = [
    "sudo", "rm -rf", "chmod 777", "dd",
    "format", "fdisk", "mkfs"
]
```

**Security Checklist:**
- [ ] Terminal tools validate working directory against whitelist
- [ ] Commands are checked against allow-list before execution
- [ ] No `sudo` or destructive commands allowed
- [ ] Working directory is restricted to project paths only

### ✅ **File System Access Control**
```python
# Verify file operations are sandboxed
ALLOWED_FILE_OPERATIONS = [
    "read_file", "edit_file", "search_replace",
    "list_dir", "file_search", "grep_search"
]

BLOCKED_FILE_OPERATIONS = [
    "delete_file", "run_terminal_cmd",  # Unless properly secured
    "system", "eval", "exec"
]
```

**File Security Checklist:**
- [ ] File operations restricted to project directory
- [ ] No access to system files outside project
- [ ] Sensitive directories (`.git`, `secrets/`) are protected
- [ ] File deletion requires explicit confirmation

### ✅ **Network & External Access**
```python
# Check web scraping and external API tools
ALLOWED_DOMAINS = [
    "github.com", "docs.cursor.com", "modelcontextprotocol.io"
]

BLOCKED_ACCESS = [
    "internal.company.com", "localhost:8080",  # Internal services
    "file://", "ftp://", "ssh://"  # Local protocols
]
```

**Network Security Checklist:**
- [ ] Web scraping limited to public, safe domains
- [ ] No access to internal/private services
- [ ] Rate limiting on external API calls
- [ ] No local network protocol access

---

## 🔍 **Phase 4: Cursor MCP Integration Test (5 minutes)**

### ✅ **Cursor MCP Configuration**
Check `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "lab-development": {
      "command": "python",
      "args": ["mcp-server/server.py"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    "app-demo": {
      "command": "python", 
      "args": ["app/mcp-servers/demo-server/main.py"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/app"
      }
    }
  }
}
```

**Integration Checklist:**
- [ ] All MCP servers appear in Cursor's MCP panel
- [ ] Tools are invokable from Cursor chat
- [ ] No connection errors or timeouts
- [ ] Server logs show proper Cursor integration

### ✅ **Tool Invocation Test**
In Cursor chat, test each MCP server:

```
# Test Lab Server
@mcp_server_usage
List all available MCP tools and their capabilities.

# Test App Server (if applicable)
What MCP tools are available for app-specific operations?
```

**Expected Results:**
- [ ] Lab tools show system-wide capabilities
- [ ] App tools show only app-scoped operations
- [ ] No cross-boundary tool access
- [ ] Proper error handling for unauthorized operations

---

## 📊 **Phase 5: Performance & Reliability (5 minutes)**

### ✅ **Server Response Times**
```bash
# Test server responsiveness
time python -c "
import asyncio
from mcp import ClientSession, StdioServerParameters

async def performance_test():
    params = StdioServerParameters(command='python', args=['server.py'])
    start = asyncio.get_event_loop().time()
    
    async with ClientSession(params) as session:
        tools = await session.list_tools()
        end = asyncio.get_event_loop().time()
        print(f'Response time: {(end - start) * 1000:.2f}ms')
        print(f'Tools returned: {len(tools.tools)}')

asyncio.run(performance_test())
"
```

**Performance Targets:**
- [ ] Server startup: < 2 seconds
- [ ] Tool listing: < 500ms
- [ ] Tool execution: < 1 second (for simple operations)
- [ ] No memory leaks or resource accumulation

### ✅ **Error Handling & Recovery**
```python
# Test error scenarios
ERROR_TEST_CASES = [
    "Invalid tool name",
    "Missing required parameters", 
    "Network timeout",
    "File not found",
    "Permission denied"
]

# Each should return proper error messages, not crash
```

**Error Handling Checklist:**
- [ ] Invalid tool calls return descriptive errors
- [ ] Network failures are handled gracefully
- [ ] File operations fail safely with clear messages
- [ ] Server recovers from errors without restart

---

## 📝 **Phase 6: Documentation & Compliance (5 minutes)**

### ✅ **Security Documentation**
```markdown
# Update docs/security/mcp_security.md with:

## MCP Server Security Model
- **Lab Servers**: Full system access for development
- **App Servers**: Sandboxed, app-only access
- **Security Boundaries**: Clear separation enforced

## Access Control Matrix
| Server Type | File Access | Terminal Access | Network Access |
|-------------|-------------|-----------------|----------------|
| Lab         | Project-wide| Restricted      | Public APIs    |
| App         | App-only    | None            | App APIs       |

## Security Checklist
- [ ] Path whitelisting implemented
- [ ] Command allow-listing active
- [ ] Network access restricted
- [ ] File operations sandboxed
```

### ✅ **Compliance Verification**
```bash
# Generate compliance report
echo "=== MCP Security Compliance Report ===" > mcp_compliance_report.md
echo "Generated: $(date)" >> mcp_compliance_report.md
echo "" >> mcp_compliance_report.md

# Check each security requirement
echo "## Security Requirements" >> mcp_compliance_report.md
echo "- [ ] Path whitelisting: $(grep -r 'ALLOWED_PATHS' mcp-server/ | wc -l) instances" >> mcp_compliance_report.md
echo "- [ ] Command allow-listing: $(grep -r 'ALLOWED_COMMANDS' mcp-server/ | wc -l) instances" >> mcp_compliance_report.md
echo "- [ ] Network restrictions: $(grep -r 'ALLOWED_DOMAINS' mcp-server/ | wc -l) instances" >> mcp_compliance_report.md

echo "## MCP Server Status" >> mcp_compliance_report.md
echo "- Lab Server: $(python mcp-server/server.py --help 2>/dev/null && echo 'OK' || echo 'FAILED')" >> mcp_compliance_report.md
echo "- App Servers: $(ls app/mcp-servers/ | wc -l) configured" >> mcp_compliance_report.md

cat mcp_compliance_report.md
```

---

## 🎯 **Final Validation Checklist**

### ✅ **All Phases Complete**
- [ ] **Phase 1**: Cursor rules working without warnings
- [ ] **Phase 2**: MCP servers conform to protocol
- [ ] **Phase 3**: Security hardening implemented
- [ ] **Phase 4**: Cursor integration functional
- [ ] **Phase 5**: Performance meets targets
- [ ] **Phase 6**: Documentation updated

### ✅ **Security Status**
- [ ] No unauthorized system access
- [ ] Terminal commands properly restricted
- [ ] File operations sandboxed
- [ ] Network access controlled
- [ ] Error handling secure

### ✅ **Compliance Status**
- [ ] MCP protocol compliance verified
- [ ] Cursor integration working
- [ ] Security boundaries enforced
- [ ] Performance targets met
- [ ] Documentation complete

---

## 🚀 **Next Steps After Audit**

1. **Fix any issues** found during the audit
2. **Update security policies** based on findings
3. **Test in production environment** if applicable
4. **Schedule regular security reviews** (monthly recommended)
5. **Monitor MCP server logs** for security events

---

*This checklist ensures your AI/DEV Lab MCP servers are secure, compliant, and fully functional with Cursor IDE integration.*
