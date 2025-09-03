# AI/DEV Lab Port Configuration

## 🚀 **Complete Service Architecture**

### **Port 3000: Frontend**
- **Service**: HTTP Server (Vanilla JS + Web Components)
- **Purpose**: User interface for the web application
- **URL**: http://localhost:3000
- **Status**: ✅ Active in development mode

### **Port 8000: Backend API**
- **Service**: FastAPI Server (Python)
- **Purpose**: Main application logic and API endpoints
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Status**: ✅ Active in development mode

### **Port 8001: Lab MCP Server**
- **Service**: HTTP-based MCP Server
- **Purpose**: Lab-wide MCP tools and development assistance
- **URL**: http://localhost:8001
- **Health Check**: http://localhost:8001/health
- **Status**: ✅ Active in development mode

### **stdio-based MCP Servers (No Ports)**

#### **App Demo Server**
- **Service**: stdio-based MCP Server
- **Purpose**: Chat analysis, response templates, metrics tools
- **Location**: `app/mcp-servers/app-demo-server/`
- **Protocol**: stdio (Model Context Protocol)
- **Status**: ✅ Active in background

#### **Database Server**
- **Service**: stdio-based MCP Server
- **Purpose**: Conversation storage, user management, A/B testing
- **Location**: `app/mcp-servers/database-server/`
- **Protocol**: stdio (Model Context Protocol)
- **Status**: ✅ Active in background

## 🔧 **Startup Script: start_dev.sh**

The `start_dev.sh` script now provides:

### **Automatic Service Startup**
1. **Backend**: FastAPI server with proper PYTHONPATH
2. **Frontend**: HTTP server for static files
3. **Lab MCP**: HTTP server on port 8001
4. **App MCP Servers**: stdio-based servers in background

### **Health Monitoring**
- Real-time health checks for HTTP services
- Process ID tracking for all services
- Comprehensive status display

### **Error Handling**
- Virtual environment creation if missing
- Dependency installation
- Graceful shutdown procedures

## 📊 **Service Status Commands**

### **Check All Services**
```bash
# Check HTTP services
curl http://localhost:3000          # Frontend
curl http://localhost:8000/health   # Backend
curl http://localhost:8001/health   # Lab MCP

# Check MCP server processes
ps aux | grep -E "(app-demo|database-server)"
```

### **Process Management**
```bash
# View all running services
ps aux | grep -E "(uvicorn|http.server|start_dev)"

# Stop all services
pkill -f start_dev.sh
```

## 🌐 **Complete URL Reference**

| Service | Type | URL | Status |
|---------|------|-----|---------|
| Frontend | HTTP | http://localhost:3000 | ✅ Active |
| Backend API | HTTP | http://localhost:8000 | ✅ Active |
| API Docs | HTTP | http://localhost:8000/docs | ✅ Active |
| Health Check | HTTP | http://localhost:8000/health | ✅ Active |
| Lab MCP | HTTP | http://localhost:8001 | ✅ Active |
| App Demo MCP | stdio | stdio://app/mcp-servers/app-demo-server | ✅ Active |
| Database MCP | stdio | stdio://app/mcp-servers/database-server | ✅ Active |

## 🔒 **Security Notes**

- **Development Mode**: All services run on localhost only
- **CORS**: Enabled for development with localhost origins
- **Authentication**: Bearer token required for protected endpoints
- **Demo Credentials**: username: `demo`, password: `demo123`

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Port Conflicts**: Ensure ports 3000, 8000, 8001 are free
2. **Import Errors**: Backend now uses proper PYTHONPATH
3. **MCP Server Issues**: Check virtual environments and dependencies
4. **Permission Errors**: Ensure start_dev.sh is executable (chmod +x)

### **Debug Commands**

```bash
# Check service status
./start_dev.sh

# View logs
tail -f backend/app.log
tail -f backend/backend.log

# Check specific service
lsof -i :8000  # Backend
lsof -i :8001  # Lab MCP
```

## 📈 **Performance Notes**

- **Backend**: FastAPI with auto-reload enabled
- **Frontend**: Static file serving optimized
- **MCP Servers**: stdio-based for minimal overhead
- **Health Checks**: Non-blocking status monitoring

---

**Last Updated**: 2025-08-28  
**Script Version**: 2.0 (Enhanced MCP Integration)  
**Status**: ✅ All services operational
