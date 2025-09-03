# Project Setup Guide

## Initialization

This project has been bootstrapped with the following structure:

```
ai-dev-lab/
├── .cursor/environment.json      # Cursor configuration
├── mcp-server/guardian_config.yaml # Security policies
├── meta/prompts.md              # Interaction templates
├── docs/                        # Documentation
├── sandbox/                     # Development area
├── scripts/                     # Utility scripts
└── input/                       # PDF input directory
```

## Prerequisites

- macOS (darwin 22.6.0+)
- Cursor IDE with MCP support
- Local filesystem access to `~/Code/ai-dev-lab`

## Configuration

### Cursor Environment

The `.cursor/environment.json` file configures:
- Security mode: Guardian-enabled
- Background agents: Disabled by default
- MCP tools: Enabled
- Approval gates: Active

### Guardian MCP Server

Security policies are defined in `mcp-server/guardian_config.yaml`:
- Strict mode with approval requirements
- Project root confinement
- Restricted operations logging
- Audit trail enabled

## PDF Intake Process

1. **Place PDFs**: Add research PDFs to `input/` directory
2. **Verify**: Check `meta/decisions.md` for intake tracking
3. **Process**: Use Cursor with appropriate mode (free/enterprise)
4. **Extract**: Generate insights, requirements, and plans

## Security Considerations

- All operations are logged and audited
- File operations outside project root require approval
- Background agents require explicit user confirmation
- Network calls are restricted during bootstrap

## Next Steps

After setup completion:
1. Review `docs/architecture.md` for system design
2. Check `docs/security.md` for security posture
3. Use `meta/prompts.md` for Cursor interactions
4. Begin PDF analysis and PRD generation
