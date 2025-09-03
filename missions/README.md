# Missions Directory

This directory serves as the **Mission Control Center** for the AI/DEV Lab project. It contains all mission definitions, execution plans, super prompts, and mission-related data.

## Directory Structure

### Mission Files
- **`DEV-*.json`** - Development missions for app features and enhancements
- **`AUD-*.json`** - Audit missions for security and compliance reviews
- **`RES-*.json`** - Research missions for data gathering and analysis
- **`TES-*.json`** - Testing missions for quality assurance

### Mission Components
- **`*_PRD.json`** - Product Requirements Documents for missions
- **`*_IMPLEMENTATION_PLAN.json`** - Detailed implementation plans
- **`*_SUPER_AUTO_PROMPT.json`** - Automated execution prompts for agents

### Specialized Directories

#### `contact_center_research/`
Contains research missions and findings related to contact center operations:
- Agent tier system research
- Knowledge base architecture research
- QA process research
- Workflow integration research
- Comprehensive research reports

#### `website_audit/`
Contains website audit missions and results:
- Audit configurations and results
- Client onboarding analysis
- Crypto theft reporting analysis
- Content backup and archival

#### `contexts/`
Contains mission context files that provide background information for mission execution.

#### `logs/`
Contains mission execution logs:
- Context changes log
- Mission activities log
- Tool usage log

#### `tool_loadouts/`
Contains tool configuration files for different mission types.

## Mission Types

### Development Missions (DEV-*)
- **Purpose**: App feature development and enhancement
- **Scope**: Customer support AI agent improvements
- **Examples**: Frontend overhaul, demo implementation, MCP integration fixes

### Audit Missions (AUD-*)
- **Purpose**: Security, compliance, and quality audits
- **Scope**: System-wide security and performance reviews
- **Examples**: Security audits, performance reviews, compliance checks

### Research Missions (RES-*)
- **Purpose**: Data gathering and analysis
- **Scope**: Market research, competitor analysis, best practices
- **Examples**: Contact center research, enterprise research, market analysis

### Testing Missions (TES-*)
- **Purpose**: Quality assurance and testing
- **Scope**: App functionality, performance, and integration testing
- **Examples**: End-to-end testing, performance testing, integration testing

## Mission Lifecycle

1. **Mission Creation**: PRD and implementation plan created
2. **Mission Planning**: Super auto prompts generated for agent execution
3. **Mission Execution**: Agents execute missions using provided prompts
4. **Mission Monitoring**: Progress tracked through logs and contexts
5. **Mission Completion**: Results documented and archived

## Usage

### For AI Agents
- Use super auto prompts for automated mission execution
- Reference mission contexts for background information
- Update mission logs during execution
- Follow mission-specific tool loadouts

### For Developers
- Create new missions using the established naming convention
- Document mission requirements in PRD files
- Generate implementation plans and super prompts
- Monitor mission progress through logs

### For Project Managers
- Review mission status and progress
- Coordinate between different mission types
- Ensure mission alignment with project goals
- Track mission completion and results

## Mission Naming Convention

- **DEV-YYYY-XXXXXXXX**: Development missions
- **AUD-YYYY-XXXXXXXX**: Audit missions  
- **RES-YYYY-XXXXXXXX**: Research missions
- **TES-YYYY-XXXXXXXX**: Testing missions

Where:
- `YYYY` = Year (e.g., 2025)
- `XXXXXXXX` = 8-character unique identifier

## Integration with Meta Directory

This missions directory integrates with the `meta/` directory:
- Mission templates are stored in `meta/templates/`
- Mission decisions are documented in `meta/decisions/`
- Mission features are tracked in `meta/features/`

## Security and Access Control

- All missions are tracked in version control
- Mission contexts may contain sensitive information
- Access to mission logs is restricted to authorized personnel
- Mission execution follows guardian security policies

---

*This directory is the central hub for all AI/DEV Lab mission operations and serves as the primary interface between project planning and automated execution.*
