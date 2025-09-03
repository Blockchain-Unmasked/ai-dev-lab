#!/usr/bin/env python3
"""
Super Auto Prompt (SAP) Loader for AI/DEV Lab
Dynamically generates prompts from SAP JSON configuration
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class SAPLoader:
    """Super Auto Prompt loader for dynamic prompt generation"""
    
    def __init__(self, sap_config_path: str):
        self.sap_config_path = Path(sap_config_path)
        self.config = self._load_sap_config()
        
    def _load_sap_config(self) -> Dict[str, Any]:
        """Load SAP configuration from JSON file"""
        try:
            with open(self.sap_config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"✅ Loaded SAP config: {config.get('sap_id', 'unknown')}")
            return config
        except Exception as e:
            logger.error(f"❌ Failed to load SAP config: {e}")
            return {}
    
    def generate_prompt(self, 
                       user_message: str, 
                       mode: Optional[str] = None,
                       context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a structured prompt from SAP configuration"""
        
        # Use provided mode or default
        active_mode = mode or self.config.get('modes', {}).get('default', 'support')
        mode_config = self.config.get('modes', {}).get('profiles', {}).get(active_mode, {})
        
        # Build the prompt
        prompt_parts = []
        
        # 1. Role and objectives
        prompt_parts.append(self._build_role_section())
        
        # 2. Mode-specific behavior
        prompt_parts.append(self._build_behavior_section(mode_config))
        
        # 3. Constraints and safety
        prompt_parts.append(self._build_constraints_section())
        
        # 4. Crypto theft specific guidance
        prompt_parts.append(self._build_crypto_theft_section())
        
        # 5. Output format requirements
        prompt_parts.append(self._build_output_section())
        
        # 6. User message and context
        prompt_parts.append(self._build_user_message_section(user_message, context))
        
        return "\n\n".join(prompt_parts)
    
    def _build_role_section(self) -> str:
        """Build the role and objectives section"""
        objectives = self.config.get('objectives', [])
        audience = self.config.get('audience', [])
        
        return f"""You are an expert AI customer support agent specializing in crypto theft cases. You serve {', '.join(audience)} and your objectives are:
{chr(10).join(f"- {obj}" for obj in objectives)}"""
    
    def _build_behavior_section(self, mode_config: Dict[str, Any]) -> str:
        """Build mode-specific behavior section"""
        behavior = mode_config.get('behavior', {})
        style = behavior.get('style', 'professional')
        
        behavior_rules = []
        if behavior.get('ask_for_missing_context'):
            behavior_rules.append("- Ask for missing context when needed")
        if behavior.get('prefer_structured_guidance'):
            behavior_rules.append("- Provide structured, actionable guidance")
        if behavior.get('use_tools_proactively'):
            behavior_rules.append("- Use available tools proactively")
        if behavior.get('attach_citations_and_rationales'):
            behavior_rules.append("- Include citations and rationales for recommendations")
        
        return f"""BEHAVIOR GUIDELINES:
- Maintain a {style} tone
{chr(10).join(behavior_rules)}"""
    
    def _build_constraints_section(self) -> str:
        """Build constraints and safety section"""
        constraints = self.config.get('constraints', {})
        safety = constraints.get('safety', {})
        
        forbidden = safety.get('forbid', [])
        red_flags = safety.get('red_flags', [])
        
        return f"""CONSTRAINTS AND SAFETY:
- Token budget: {constraints.get('token_budget_hint', 1500)}
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
    
    def _build_output_section(self) -> str:
        """Build output format requirements section"""
        output_contract = self.config.get('output_contract', {})
        sections = output_contract.get('sections', [])
        
        return f"""OUTPUT FORMAT REQUIREMENTS:
Your response must include these sections:
{chr(10).join(f"- {section.replace('_', ' ').title()}" for section in sections)}

Format: {output_contract.get('format', 'structured_response')}"""
    
    def _build_user_message_section(self, user_message: str, context: Optional[Dict[str, Any]]) -> str:
        """Build user message and context section"""
        section = f"USER MESSAGE: \"{user_message}\"\n\n"
        
        if context:
            section += "ADDITIONAL CONTEXT:\n"
            for key, value in context.items():
                section += f"- {key}: {value}\n"
            section += "\n"
        
        section += "RESPONSE REQUIREMENTS:\n"
        section += "- Address the user's crypto theft concern directly\n"
        section += "- Provide immediate security steps first\n"
        section += "- MANDATORY: Explain the three-tier reporting structure (LEO, Service Provider, OCINT)\n"
        section += "- MANDATORY: Mention all three reporting requirements in your response\n"
        section += "- Include OCINT comprehensive investigation details\n"
        section += "- Maintain realistic expectations about law enforcement\n"
        section += "- Be empathetic but professional\n"
        section += "- Keep response concise but thorough (2-4 sentences)\n"
        
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
    
    def update_mode(self, new_mode: str) -> bool:
        """Update the default mode"""
        if new_mode in self.config.get('modes', {}).get('profiles', {}):
            self.config['modes']['default'] = new_mode
            return True
        return False

# Global SAP loader instance
sap_loader = None

def initialize_sap_loader(config_path: str = "app/agents/crypto-theft-agent.sap.json"):
    """Initialize the global SAP loader"""
    global sap_loader
    sap_loader = SAPLoader(config_path)
    return sap_loader

def get_sap_loader() -> Optional[SAPLoader]:
    """Get the global SAP loader instance"""
    return sap_loader
