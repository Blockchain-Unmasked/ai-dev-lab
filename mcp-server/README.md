# AI/DEV Lab MCP Server

A Model Context Protocol (MCP) server implementation for the AI/DEV Lab project, providing Tools, Resources, and Prompts for Cursor IDE integration.

## Features

### 🛠️ **Tools (AI Actions)**
- **`get_project_status`**: Get current project status and phase information
- **`analyze_research_document`**: Analyze research documents and extract insights
- **`generate_task_list`**: Generate actionable task lists from research insights

### 📚 **Resources (Context Data)**
- **`ai-dev://project/overview`**: Current project status and overview
- **`ai-dev://research/insights`**: Key insights extracted from research documents
- **`ai-dev://implementation/roadmap`**: Implementation roadmap and phases

### 💬 **Prompts (Interaction Templates)**
- **`research_analysis`**: Template for analyzing research documents
- **`task_generation`**: Template for generating actionable tasks
- **`security_review`**: Template for conducting security reviews

## Architecture

### MCP Compliance
- **Protocol Version**: 2025-06-18 (latest spec)
- **Transport**: STDIO (local development), HTTP (future remote deployment)
- **Security**: Guardian integration with approval workflows
- **Capabilities**: Tools, Resources, and Prompts fully supported

### Security Features
- **Approval Gates**: Sensitive operations require user approval
- **Guardian Integration**: MCP server security policies enforced
- **Audit Logging**: Complete operation logging for compliance
- **Project Root Confinement**: Operations restricted to project boundaries

## Quick Start

### Prerequisites
- Python 3.7+ (for dataclasses support)
- macOS/Linux/Windows
- Cursor IDE with MCP support

### Installation
1. **Clone the repository** (if not already done)
   ```bash
   cd ~/Code/ai-dev-lab
   ```

2. **Navigate to MCP server directory**
   ```bash
   cd mcp-server
   ```

3. **Start the server**
   ```bash
   # macOS/Linux
   ./start_server.sh
   
   # Windows
   start_server.bat
   ```

### Manual Start
```bash
cd mcp-server
python3 server.py
```

## Configuration

### Server Configuration (`config.yaml`)
- **Transport Mode**: STDIO (local) or HTTP (remote)
- **Security Settings**: Approval requirements and Guardian integration
- **Logging**: Log level, format, and file rotation
- **Capabilities**: Feature enable/disable settings

### Environment Variables
- `AI_DEV_PROJECT_ROOT`: Project root directory
- `AI_DEV_MCP_MODE`: Development/production mode
- `AI_DEV_GUARDIAN_CONFIG`: Guardian configuration path

## Development

### Project Structure
```
mcp-server/
├── server.py              # Main MCP server implementation
├── config.yaml            # Server configuration
├── requirements.txt       # Python dependencies
├── start_server.sh        # Unix startup script
├── start_server.bat       # Windows startup script
├── logs/                  # Log files directory
└── README.md             # This file
```

### Adding New Tools
1. **Define the tool** in `initialize_capabilities()`
2. **Implement execution logic** in `_execute_*` methods
3. **Add to approval workflow** if required
4. **Update configuration** in `config.yaml`

### Adding New Resources
1. **Define the resource** in `initialize_capabilities()`
2. **Implement data access** in `handle_resources_read()`
3. **Update URI mapping** for new resources

### Adding New Prompts
1. **Define the prompt** in `initialize_capabilities()`
2. **Create template** with parameter placeholders
3. **Document usage** in this README

## Testing

### Manual Testing
1. Start the MCP server
2. Use MCP Inspector or Cursor IDE to connect
3. Test tools, resources, and prompts
4. Verify approval workflows

### Automated Testing (Future)
- Unit tests for individual components
- Integration tests for MCP protocol compliance
- Security tests for approval workflows
- Performance tests for large operations

## Deployment

### Local Development
- **Transport**: STDIO (recommended for development)
- **Security**: Guardian policies enforced
- **Logging**: Local file logging

### Remote Deployment (Future)
- **Transport**: HTTP with OAuth2 authentication
- **Security**: Enhanced security with SSL/TLS
- **Monitoring**: Centralized logging and metrics

## Troubleshooting

### Common Issues

#### Server Won't Start
- **Check Python version**: Ensure Python 3.7+ is installed
- **Check permissions**: Ensure startup scripts are executable
- **Check dependencies**: Verify all required modules are available

#### Connection Issues
- **Check transport mode**: Verify STDIO vs HTTP configuration
- **Check Guardian config**: Ensure Guardian policies are correct
- **Check logs**: Review `logs/mcp_server.log` for errors

#### Tool Execution Issues
- **Check approval workflow**: Verify tool approval requirements
- **Check input schema**: Ensure tool arguments match expected format
- **Check Guardian policies**: Verify operation is allowed

### Log Files
- **Location**: `mcp-server/logs/mcp_server.log`
- **Rotation**: Automatic with 10MB max size, 5 backups
- **Level**: Configurable (INFO by default)

## Security Considerations

### Approval Workflows
- **Sensitive Operations**: All destructive operations require approval
- **User Consent**: Guardian ensures user-in-the-loop for critical actions
- **Audit Trail**: Complete logging of all operations

### Guardian Integration
- **Policy Enforcement**: MCP server respects Guardian security policies
- **Path Restrictions**: Operations confined to project boundaries
- **Access Control**: User permissions enforced through Guardian

### Best Practices
- **Never bypass approval**: Always require approval for sensitive operations
- **Log everything**: Maintain complete audit trail
- **Test security**: Regularly test approval workflows and policies

## Future Enhancements

### Planned Features
- **HTTP Transport**: Remote deployment support
- **Enhanced Security**: OAuth2 and SSL/TLS support
- **Performance**: Async operations and caching
- **Monitoring**: Metrics and health checks

### Integration Opportunities
- **Cursor IDE**: Enhanced integration with dual-mode support
- **Background Agents**: Secure agent management
- **Bugbot**: Automated code review integration
- **Team Collaboration**: Multi-user support and permissions

## Contributing

### Development Guidelines
1. **Follow MCP spec**: Ensure compliance with latest protocol version
2. **Security first**: Always implement proper approval workflows
3. **Document changes**: Update README and configuration files
4. **Test thoroughly**: Verify functionality and security

### Code Style
- **Python**: Follow PEP 8 guidelines
- **Documentation**: Use docstrings for all public methods
- **Error Handling**: Implement proper exception handling
- **Logging**: Use structured logging for all operations

## License

This MCP server is part of the AI/DEV Lab project and follows the project's licensing terms.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the project documentation
3. Check the Guardian configuration
4. Review the MCP server logs

---

*AI/DEV Lab MCP Server - Enabling secure, efficient AI development workflows*
