# AI/DEV Lab Environment Control System

## Overview
The Environment Control System provides comprehensive management of the AI/DEV Lab development environment through MCP server integration.

## Features

### 🚀 **Development Environment Management**
- **Start Environment**: `start_development_environment`
- **Stop Environment**: `stop_development_environment`  
- **Health Monitoring**: `check_environment_health`

### 🔧 **Integration with start_dev.sh**
The system now properly integrates with the `app/start_dev.sh` script to:
- Set proper environment variables
- Create process groups for clean management
- Handle virtual environment activation
- Manage both frontend and backend services
- **Start app-specific MCP servers** for agent functionality
- Provide comprehensive health monitoring

### 🔌 **App MCP Servers Started**
The system now automatically starts these MCP servers for app agents:

- **app-demo-server**: Provides chat analysis, response templates, and metrics tools
- **database-server**: Handles conversation storage, user management, and A/B testing metrics

## Usage Examples

### Starting the Development Environment

```python
# Start complete development environment
result = await mcp_server.start_development_environment({
    "environment": "development",
    "services": ["frontend", "backend", "mcp"],
    "wait_for_ready": True
})

# Response includes:
# - Process IDs and process group IDs
# - Health status of all services
# - Endpoint URLs for testing
# - Script path used for startup
# - MCP server endpoints for app agents
```

### Stopping the Development Environment

```python
# Stop all development services
result = await mcp_server.stop_development_environment({
    "force": False,  # Graceful shutdown
    "cleanup": True  # Clean up processes
})
```

### Checking Environment Health

```python
# Check health of all services
health = await mcp_server.check_environment_health({
    "detailed": True,
    "services": ["frontend", "backend", "mcp"]
})
```

## Environment Variables Set

The system automatically sets these environment variables when starting:

```bash
AI_DEV_PROJECT_ROOT=/path/to/ai-dev-lab
AI_DEV_MCP_MODE=development
AI_DEV_GUARDIAN_CONFIG=/path/to/guardian_config.yaml
PYTHONPATH=/path/to/ai-dev-lab/app/backend:$PYTHONPATH
MCP_APP_SERVERS_ENABLED=true
```

## Service Endpoints

When the environment is running, these endpoints are available:

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### MCP Server Endpoints

- **app-demo-server**: stdio://app/mcp-servers/app-demo-server
- **database-server**: stdio://app/mcp-servers/database-server

## Process Management

### Process Group Creation
- Uses `os.setsid` to create new process groups
- Enables clean shutdown of all related processes
- Prevents orphaned processes

### Services Started
1. **Backend**: FastAPI server on port 8000
2. **Frontend**: HTTP server on port 3000
3. **App MCP Servers**: stdio-based servers for agent tools
4. **Process Monitoring**: All processes tracked for cleanup

### Cleanup Strategy
1. Stop main process group first
2. Check for processes on common ports
3. Stop MCP server processes
4. Force kill if graceful shutdown fails
5. Log all stopped processes

## Security Features

- **Trusted Host Middleware**: Restricts access to localhost
- **CORS Configuration**: Development-friendly CORS settings
- **Process Isolation**: Separate process groups for security
- **Environment Validation**: Checks script existence and permissions

## Error Handling

- **Script Validation**: Ensures start_dev.sh exists and is executable
- **Process Monitoring**: Tracks startup progress
- **Health Verification**: Confirms services are responding
- **MCP Server Validation**: Ensures app MCP servers start correctly
- **Graceful Fallbacks**: Handles startup failures gracefully

## Testing

Test the environment control system:

```bash
# Test startup
python test_environment_control.py

# Test focused functionality
python test_environment_control_focused.py

# Test comprehensive MCP features
python test_comprehensive_mcp.py
```

## Troubleshooting

### Common Issues

1. **Script Not Found**: Ensure `app/start_dev.sh` exists and is executable
2. **Port Conflicts**: Check if ports 3000, 8000 are already in use
3. **Virtual Environment**: Ensure Python venv is properly set up
4. **Permissions**: Script must have execute permissions (755)
5. **MCP Server Dependencies**: Ensure MCP requirements are installed

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Architecture

```
MCP Server → Environment Control → start_dev.sh → Services
     ↓              ↓                ↓           ↓
  Commands    Process Mgmt    Script Exec   Frontend/Backend
                                    ↓
                              App MCP Servers
                                    ↓
                              Agent Tools
```

## Future Enhancements

- **Service Discovery**: Automatic service detection
- **Load Balancing**: Multiple backend instances
- **Health Alerts**: Proactive health monitoring
- **Auto-restart**: Automatic service recovery
- **Metrics Collection**: Performance monitoring
- **MCP Server Health**: Individual MCP server monitoring
