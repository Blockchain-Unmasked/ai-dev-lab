# Cursor Usage Guide

## Overview

This guide outlines best practices for using Cursor in the AI/DEV Lab project, including @reference discipline, memory management, and rule-based interactions.

## @Reference Discipline

### Core Principles
1. **Prefer @file over long pastes**: Use `@file` references to provide context without overwhelming responses
2. **Keep messages concise**: Focus on specific questions and targeted edits
3. **Link to relevant files**: Reference documentation and code files for context

### Usage Patterns
- **Context Provision**: `@file docs/architecture.md` for system overview
- **Code Reference**: `@file meta/prompts.md` for interaction templates
- **Security Check**: `@file docs/security.md` for policy compliance

### Examples
```markdown
# Good: Using @file references
@file docs/architecture.md shows the current system design. 
How should we modify the data flow for PDF processing?

# Avoid: Long code pastes
Here's the entire architecture file content...
[long paste of file content]
```

## Memory Management

### Project Memories
- **Bootstrap Phase**: Project initialization and security setup
- **PDF Intake**: Research document processing workflow
- **Security Posture**: Guardian configuration and approval gates
- **Mode Selection**: Free vs Enterprise interaction patterns

### Memory Guidelines
- **Keep memories focused**: Store only relevant, actionable information
- **Update regularly**: Refresh memories as project evolves
- **Link to sources**: Reference specific files and decisions
- **Avoid duplication**: Consolidate related information

### Memory Structure
```
Project State:
- Current Phase: Bootstrap Complete
- Security Status: Guardian Active
- Next Steps: PDF Intake

Key Decisions:
- Guardian MCP server configuration
- Dual-mode prompt templates
- Security approval workflow
```

## Rule-Based Interactions

### Free Mode Rules
1. **Concise responses**: Keep answers brief and focused
2. **Limited tools**: Use only essential operations
3. **No background agents**: Avoid resource-intensive operations
4. **@file context**: Rely on file references for information

### Enterprise Mode Rules
1. **Thorough analysis**: Provide comprehensive responses
2. **Approval workflow**: Request explicit approval for background agents
3. **Security focus**: Highlight security considerations
4. **Documentation**: Generate comprehensive documentation

### Security Rules
1. **Path validation**: Never operate outside project root
2. **Approval gates**: Respect Guardian security policies
3. **Audit logging**: All operations are logged
4. **Policy compliance**: Follow established security guidelines

## Research Intake Workflow

### Phase 1: PDF Placement
1. **Verify input directory**: Check `input/` for PDF files
2. **Update tracking**: Record filenames in `meta/decisions.md`
3. **Validate format**: Ensure PDFs are readable and accessible

### Phase 2: Analysis Planning
1. **Select mode**: Choose free or enterprise based on complexity
2. **Define scope**: Determine analysis depth and deliverables
3. **Set priorities**: Identify key insights and requirements

### Phase 3: Processing
1. **Extract insights**: Use Cursor to analyze PDF content
2. **Generate summaries**: Create objective and recommendation summaries
3. **Identify patterns**: Find common themes and requirements

### Phase 4: Output Generation
1. **PRD updates**: Modify `docs/architecture.md` with new insights
2. **Task planning**: Create actionable tasks in `meta/feature_grid.md`
3. **Documentation**: Update relevant documentation files

## Best Practices

### Communication
- **Be specific**: Ask targeted questions with clear scope
- **Use @file**: Reference relevant files for context
- **Provide examples**: Include concrete examples when possible
- **Follow up**: Clarify unclear responses or requirements

### File Management
- **Small edits**: Make focused, reversible changes
- **Version control**: Use Git for tracking changes
- **Backup strategy**: Maintain backup copies of important files
- **Documentation**: Update docs when making changes

### Security
- **Policy compliance**: Follow Guardian security policies
- **Approval workflow**: Request approval for restricted operations
- **Audit trail**: Maintain complete operation logging
- **Regular reviews**: Periodically review security posture

## Troubleshooting

### Common Issues
1. **@file not working**: Verify file path and accessibility
2. **Permission denied**: Check Guardian configuration and approval gates
3. **Memory conflicts**: Clear and rebuild project memories
4. **Security blocks**: Review Guardian policies and approval requirements

### Resolution Steps
1. **Identify issue**: Determine root cause of problem
2. **Check policies**: Verify Guardian configuration and policies
3. **Request approval**: Get explicit approval for restricted operations
4. **Update documentation**: Record solutions for future reference

## Next Steps

### Immediate Actions
1. **Review setup**: Verify all files and configurations are correct
2. **Test Guardian**: Validate security policies and approval gates
3. **Prepare for PDFs**: Ensure input directory is ready for research documents

### Future Enhancements
1. **Memory optimization**: Improve memory management and retrieval
2. **Workflow automation**: Streamline PDF processing workflow
3. **Security hardening**: Enhance Guardian configuration and policies
4. **Team collaboration**: Prepare for multi-user development
