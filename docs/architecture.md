# System Architecture

## Overview

The AI/DEV Lab project implements a local, MCP-aligned Cursor workspace with security guardrails and PDF-driven planning capabilities.

## Core Components

### 1. Cursor Integration Layer
- **Environment Configuration**: `.cursor/environment.json`
- **Security Mode**: Guardian-enabled with approval gates
- **MCP Support**: Enabled for tool integration
- **Background Agents**: Disabled by default, requires approval
- **Dual-Mode Support**: Free vs Enterprise interaction patterns
- **Context Management**: Optimized window sizing and indexing

### 2. Guardian MCP Server
- **Security Policies**: Strict mode with comprehensive logging
- **Approval Gates**: File operations, system commands, background agents
- **Path Restrictions**: Project root confinement
- **Audit Trail**: Complete operation logging
- **MCP Compliance**: Latest spec (2025-06-18) with Tools, Resources, Prompts
- **Transport Support**: STDIO (local) and HTTP (remote) with OAuth2

### 3. Document Processing Pipeline
- **Input**: Research documents (PDF → Text conversion)
- **Processing**: Cursor-based analysis and extraction
- **Output**: PRD, plans, and actionable tasks
- **Storage**: Local filesystem with version control
- **Analysis Complete**: Three research documents processed
- **Insights Extracted**: MCP requirements, Cursor best practices, security strategies

## Data Flow

```
PDF Input → Cursor Analysis → Insight Extraction → PRD Generation → Task Planning
    ↓              ↓              ↓              ↓              ↓
  input/      free/enterprise   meta/decisions  docs/architecture  meta/feature_grid
```

## Security Architecture

### Access Control
- **Project Root**: `~/Code/ai-dev-lab`
- **Allowed Paths**: Explicitly defined in Guardian config
- **Forbidden Paths**: System directories, credentials, secrets

### Operation Restrictions
- **Local Only**: No network calls during bootstrap
- **Approval Required**: Destructive operations, background agents
- **Logging**: Complete audit trail for compliance

## Modes of Operation

### Free Mode
- **Scope**: Quick tasks, simple edits
- **Resources**: Limited tools, no background agents
- **Use Case**: Basic file operations, simple queries

### Enterprise Mode
- **Scope**: Complex tasks, architecture decisions
- **Resources**: Full tool access with approvals
- **Use Case**: PDF analysis, PRD generation, security reviews

## Integration Points

### MCP Tools
- **Guardian**: Security and approval gateway
- **File Operations**: Read/write within project bounds
- **Search**: Codebase exploration and analysis

### Cursor Features
- **Ask Mode**: Primary interaction method
- **@file References**: Context-aware file linking
- **Background Agents**: Available with explicit approval

## Scalability Considerations

### Current State
- Single developer workspace
- Local filesystem storage
- Manual approval workflow

### Future Enhancements
- Team collaboration features
- Automated approval workflows
- Enhanced MCP tool integration
- Cloud storage integration (with security review)

## Technology Stack

- **Platform**: macOS (darwin 22.6.0+)
- **IDE**: Cursor with MCP support
- **Security**: Guardian MCP server
- **Storage**: Local filesystem
- **Version Control**: Git (recommended)

## Research Findings & Implementation Roadmap

### Key Insights from Research Analysis
1. **MCP Server Requirements**: Tools, Resources, and Prompts implementation
2. **Cursor Dual-Mode Support**: Free vs Enterprise interaction patterns
3. **Background Agent Security**: Approval workflows and supervision requirements
4. **Best Practices**: Context management, @references, Bugbot integration
5. **Security Hardening**: MCP Guardian, SafetyScanner, threat taxonomy

### Implementation Priorities
1. **Phase 1**: MCP server with basic Tools and Resources
2. **Phase 2**: Cursor dual-mode configuration and rules
3. **Phase 3**: Background agent security and approval gates
4. **Phase 4**: Advanced features (Bugbot, memories, context optimization)

### Technical Specifications
- **MCP Version**: 2025-06-18 (latest spec compliance)
- **Transport**: STDIO for local development, HTTP for remote deployment
- **Authentication**: OAuth2 for remote access, token-based for local
- **Security**: User-in-the-loop approval for all tool executions
