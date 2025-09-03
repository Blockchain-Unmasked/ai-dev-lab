#!/usr/bin/env python3
"""
App-Specific Super Auto Prompt (SAP) Loader
Optimized for crypto theft support and MCP server integration
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class AppSAPLoader:
    """App-specific SAP loader for crypto theft support and MCP integration"""
    
    def __init__(self, sap_config_path: str = "agents/app-agent-sap.json"):
        self.sap_config_path = Path(sap_config_path)
        self.config = self._load_sap_config()
        self.mcp_integration = self.config.get('mcp_integration', {})
        
    def _load_sap_config(self) -> Dict[str, Any]:
        """Load SAP configuration from JSON file"""
        try:
            with open(self.sap_config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"✅ Loaded App SAP config: {config.get('sap_id', 'unknown')}")
            return config
        except Exception as e:
            logger.error(f"❌ Failed to load App SAP config: {e}")
            return {}
    
    def generate_app_prompt(self, 
                           user_message: str, 
                           structured_message: Dict[str, Any],
                           mode: Optional[str] = None,
                           mcp_context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a structured prompt optimized for app context and MCP integration"""
        
        # Use provided mode or determine from structured message
        active_mode = mode or self._determine_mode_from_message(structured_message)
        mode_config = self.config.get('modes', {}).get('profiles', {}).get(active_mode, {})
        
        # Build the prompt
        prompt_parts = []
        
        # 1. Role and objectives
        prompt_parts.append(self._build_app_role_section())
        
        # 2. Mode-specific behavior
        prompt_parts.append(self._build_app_behavior_section(mode_config))
        
        # 3. MCP integration context
        if mcp_context:
            prompt_parts.append(self._build_mcp_context_section(mcp_context))
        
        # 4. Structured message context
        prompt_parts.append(self._build_structured_message_section(structured_message))
        
        # 5. Constraints and safety
        prompt_parts.append(self._build_app_constraints_section())
        
        # 6. Crypto theft specific guidance
        prompt_parts.append(self._build_crypto_theft_section())
        
        # 7. Output format requirements
        prompt_parts.append(self._build_app_output_section())
        
        # 8. User message and response requirements
        prompt_parts.append(self._build_app_user_message_section(user_message, structured_message))
        
        # Add final instruction to ensure natural response
        final_instruction = "\n\nFINAL INSTRUCTION: You are a human customer service agent. Write your response as if you are speaking directly to the customer. Do not use any technical formatting, JSON, code blocks, or structured data. Write in plain, conversational English with natural paragraphs. Your response should sound like a helpful human agent, not a technical system."
        
        return "\n\n".join(prompt_parts) + final_instruction
    
    def _determine_mode_from_message(self, structured_message: Dict[str, Any]) -> str:
        """Determine the appropriate mode from structured message"""
        message_type = structured_message.get('message_type', 'general_support')
        urgency_level = structured_message.get('urgency_level', 'medium')
        
        if message_type == 'crypto_theft':
            if urgency_level == 'critical':
                return 'emergency'
            else:
                return 'investigation'
        else:
            return 'support'
    
    def _build_app_role_section(self) -> str:
        """Build the app-specific role section"""
        objectives = self.config.get('objectives', [])
        audience = self.config.get('audience', [])
        
        return f"""You are an expert AI customer support agent specializing in crypto theft cases and customer service. You serve {', '.join(audience)} and your objectives are:
{chr(10).join(f"- {obj}" for obj in objectives)}

You are integrated with the Model Context Protocol (MCP) server and have access to specialized tools for crypto analysis, evidence processing, and comprehensive investigation support."""
    
    def _build_app_behavior_section(self, mode_config: Dict[str, Any]) -> str:
        """Build mode-specific behavior section"""
        behavior = mode_config.get('behavior', {})
        capabilities = mode_config.get('capabilities', {})
        style = behavior.get('style', 'professional')
        
        behavior_rules = []
        if behavior.get('ask_for_missing_context'):
            behavior_rules.append("- Ask for missing context when needed")
        if behavior.get('prefer_structured_guidance'):
            behavior_rules.append("- Provide structured, actionable guidance")
        if behavior.get('use_tools_proactively'):
            behavior_rules.append("- Use available MCP tools proactively")
        if behavior.get('attach_citations_and_rationales'):
            behavior_rules.append("- Include citations and rationales for recommendations")
        if behavior.get('use_mcp_tools'):
            behavior_rules.append("- Leverage MCP server tools and context")
        if behavior.get('prioritize_security'):
            behavior_rules.append("- Prioritize security measures first")
        if behavior.get('escalate_when_needed'):
            behavior_rules.append("- Escalate to human support when appropriate")
        
        capabilities_list = []
        if capabilities.get('mcp_integration'):
            capabilities_list.append("MCP server integration")
        if capabilities.get('crypto_analysis'):
            capabilities_list.append("crypto analysis")
        if capabilities.get('evidence_processing'):
            capabilities_list.append("evidence processing")
        if capabilities.get('blockchain_analysis'):
            capabilities_list.append("blockchain analysis")
        
        return f"""BEHAVIOR GUIDELINES:
- Maintain a {style} tone
- Available capabilities: {', '.join(capabilities_list)}
{chr(10).join(behavior_rules)}"""
    
    def _build_mcp_context_section(self, mcp_context: Dict[str, Any]) -> str:
        """Build MCP integration context section"""
        return f"""MCP SERVER CONTEXT:
- Server Status: {mcp_context.get('status', 'active')}
- Available Tools: {', '.join(mcp_context.get('available_tools', []))}
- Session Context: {mcp_context.get('session_id', 'unknown')}
- Integration Level: {mcp_context.get('integration_level', 'standard')}

Use MCP tools when appropriate for crypto analysis, evidence processing, and context management."""
    
    def _build_structured_message_section(self, structured_message: Dict[str, Any]) -> str:
        """Build structured message context section"""
        message_type = structured_message.get('message_type', 'unknown')
        urgency_level = structured_message.get('urgency_level', 'medium')
        entities = structured_message.get('extracted_entities', {})
        intent = structured_message.get('intent_analysis', {})
        
        section = f"STRUCTURED MESSAGE ANALYSIS:\n"
        section += f"- Message Type: {message_type}\n"
        section += f"- Urgency Level: {urgency_level}\n"
        section += f"- Primary Intent: {intent.get('primary_intent', 'unknown')}\n"
        section += f"- Emotional State: {intent.get('emotional_state', 'unknown')}\n"
        
        # Show extracted entities
        if any(entities.values()):
            section += "\nExtracted Entities:\n"
            for entity_type, values in entities.items():
                if values:
                    section += f"  {entity_type}: {values}\n"
        
        # Show three-tier analysis if applicable
        three_tier = structured_message.get('three_tier_analysis')
        if three_tier:
            section += "\nThree-Tier Analysis:\n"
            section += f"  Is Crypto Theft: {three_tier.get('is_crypto_theft', False)}\n"
            section += f"  Service Provider: {three_tier.get('tier_2_service_provider', 'unknown')}\n"
            section += f"  Evidence Status: {three_tier.get('evidence_status', 'unknown')}\n"
        
        return section
    
    def _build_app_constraints_section(self) -> str:
        """Build app-specific constraints section"""
        constraints = self.config.get('constraints', {})
        safety = constraints.get('safety', {})
        
        forbidden = safety.get('forbid', [])
        red_flags = safety.get('red_flags', [])
        
        return f"""CONSTRAINTS AND SAFETY:
- Token budget: {constraints.get('token_budget_hint', 1500)}
- MCP integration: {constraints.get('mcp_server_integration', True)}
- No background work: {constraints.get('no_background_work', True)}
- No unapproved side effects: {constraints.get('no_unapproved_side_effects', True)}

FORBIDDEN ACTIONS:
{chr(10).join(f"- {action}" for action in forbidden)}

RED FLAGS TO WATCH FOR:
{chr(10).join(f"- {flag}" for flag in red_flags)}"""
    
    def _build_crypto_theft_section(self) -> str:
        """Build crypto theft specific guidance section"""
        crypto_specific = self.config.get('crypto_theft_specific', {})
        three_tier = crypto_specific.get('three_tier_reporting', {})
        security_approach = crypto_specific.get('security_first_approach', {})
        realistic_guidance = crypto_specific.get('realistic_guidance', {})
        
        section = "CRYPTO THEFT GUIDANCE:\n\n"
        
        # Three-tier reporting structure
        section += "THREE-TIER REPORTING STRUCTURE:\n"
        for tier_key, tier_info in three_tier.items():
            section += f"1. {tier_info.get('name', 'Unknown')}: {tier_info.get('purpose', 'Unknown purpose')}\n"
            section += f"   Requirements: {', '.join(tier_info.get('requirements', []))}\n"
            section += f"   Realistic expectations: {tier_info.get('realistic_expectations', 'Unknown')}\n\n"
        
        # Security-first approach
        section += "SECURITY-FIRST APPROACH:\n"
        section += "Immediate steps:\n"
        for step in security_approach.get('immediate_steps', []):
            section += f"- {step}\n"
        
        section += "\nEvidence gathering:\n"
        for item in security_approach.get('evidence_gathering', []):
            section += f"- {item}\n"
        
        # Realistic guidance
        section += "\nREALISTIC GUIDANCE:\n"
        for key, value in realistic_guidance.items():
            section += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        # Mandatory three-tier response
        mandatory_response = crypto_specific.get('mandatory_three_tier_response', '')
        if mandatory_response:
            section += f"\nMANDATORY REQUIREMENT:\n{mandatory_response}\n"
        
        return section
    
    def _build_app_output_section(self) -> str:
        """Build app-specific output format requirements section"""
        output_contract = self.config.get('output_contract', {})
        sections = output_contract.get('sections', [])
        
        return f"""RESPONSE FORMAT:
You are a human customer service agent. Write your response in natural, conversational English. Include these topics naturally in your conversation:
{chr(10).join(f"- {section.replace('_', ' ').title()}" for section in sections)}

Write as a helpful human would speak to a customer - empathetic, clear, and supportive. Use natural paragraphs and flow."""
    
    def _build_app_user_message_section(self, user_message: str, structured_message: Dict[str, Any]) -> str:
        """Build user message and response requirements section"""
        response_guidance = structured_message.get('response_guidance', {})
        context_requirements = structured_message.get('context_requirements', {})
        
        section = f"USER MESSAGE: \"{user_message}\"\n\n"
        
        section += "RESPONSE REQUIREMENTS:\n"
        section += "- Write as a HUMAN customer service agent - natural, conversational, empathetic\n"
        section += "- Address the user's concern directly with empathy and understanding\n"
        section += "- Provide immediate security steps first (if crypto theft)\n"
        section += "- MANDATORY: Explain the three-tier reporting structure (if crypto theft)\n"
        section += "- MANDATORY: Mention all three reporting requirements (LEO, Service Provider, OCINT)\n"
        section += "- Include OCINT comprehensive investigation details\n"
        section += "- Maintain realistic expectations about law enforcement\n"
        section += f"- Use {response_guidance.get('tone_guidance', 'professional')} tone\n"
        section += f"- Keep response {response_guidance.get('length_guidance', 'moderate')} but thorough\n"
        section += "- DO NOT use JSON, structured data, or technical formatting\n"
        section += "- DO NOT include any code blocks, JSON objects, or structured responses\n"
        section += "- Write in natural paragraphs with proper flow and conversation\n"
        section += "- End your response naturally - do not append any technical data or formatting\n"
        
        # Show required workflows
        workflows = context_requirements.get('required_workflows', [])
        if workflows:
            section += f"- Required workflows: {', '.join(workflows)}\n"
        
        # Show missing information
        missing_info = context_requirements.get('missing_information', [])
        if missing_info:
            section += f"- Missing information to gather: {', '.join(missing_info)}\n"
        
        return section
    
    def get_workflow(self, workflow_name: str) -> Optional[List[str]]:
        """Get a specific workflow by name"""
        workflows = self.config.get('workflows', [])
        for workflow in workflows:
            if workflow.get('name') == workflow_name:
                return workflow.get('steps', [])
        return None
    
    def get_mode_capabilities(self, mode: str) -> Dict[str, Any]:
        """Get capabilities for a specific mode"""
        return self.config.get('modes', {}).get('profiles', {}).get(mode, {}).get('capabilities', {})
    
    def get_mcp_integration_config(self) -> Dict[str, Any]:
        """Get MCP integration configuration"""
        return self.mcp_integration
    
    def update_mode(self, new_mode: str) -> bool:
        """Update the default mode"""
        if new_mode in self.config.get('modes', {}).get('profiles', {}):
            self.config['modes']['default'] = new_mode
            return True
        return False

# Global App SAP loader instance
app_sap_loader = None

def initialize_app_sap_loader(config_path: str = "agents/app-agent-sap.json"):
    """Initialize the global App SAP loader"""
    global app_sap_loader
    app_sap_loader = AppSAPLoader(config_path)
    return app_sap_loader

def get_app_sap_loader() -> Optional[AppSAPLoader]:
    """Get the global App SAP loader instance"""
    return app_sap_loader
