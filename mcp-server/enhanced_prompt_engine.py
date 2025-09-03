#!/usr/bin/env python3
"""
Enhanced Prompt Engine for AI/DEV Lab
Implements comprehensive prompt engineering best practices with:
- Advanced template management
- Persona management system
- Context-aware generation
- Comprehensive guardrails
- Performance optimization
"""

import json
import logging
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import uuid

logger = logging.getLogger(__name__)

class PromptType(Enum):
    """Prompt type enumeration"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    CONTEXT = "context"

class PersonaType(Enum):
    """Persona type enumeration"""
    CUSTOMER_SERVICE = "customer_service"
    TECHNICAL_SUPPORT = "technical_support"
    SALES_AGENT = "sales_agent"
    MANAGER = "manager"
    SPECIALIST = "specialist"
    GENERAL = "general"

class GuardrailLevel(Enum):
    """Guardrail level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class PersonaProfile:
    """Persona profile configuration"""
    persona_id: str
    persona_name: str
    persona_type: PersonaType
    description: str
    personality_traits: List[str]
    expertise_areas: List[str]
    response_style: str
    formality_level: str
    emoji_usage: str
    response_length: str
    tone: str
    limitations: List[str]
    escalation_triggers: List[str]
    created_at: str
    updated_at: str
    version: str

@dataclass
class PromptTemplate:
    """Prompt template configuration"""
    template_id: str
    template_name: str
    template_type: PromptType
    template_content: str
    variables: List[Dict[str, Any]]
    persona_requirements: List[str]
    guardrail_level: GuardrailLevel
    performance_metrics: Dict[str, Any]
    created_at: str
    updated_at: str
    version: str

@dataclass
class ContextData:
    """Context data structure"""
    context_id: str
    session_id: str
    customer_profile: Dict[str, Any]
    conversation_history: List[Dict[str, Any]]
    current_topic: str
    customer_intent: str
    escalation_level: int
    agent_tier: int
    knowledge_base_access: List[str]
    timestamp: str
    version: str

@dataclass
class GuardrailResult:
    """Guardrail validation result"""
    passed: bool
    violations: List[str]
    risk_level: str
    recommendations: List[str]
    requires_escalation: bool
    escalation_reason: str

class EnhancedPromptEngine:
    """
    Enhanced prompt engine with comprehensive features
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "meta/prompt-engine-templates.json"
        self.templates: Dict[str, PromptTemplate] = {}
        self.personas: Dict[str, PersonaProfile] = {}
        self.context_cache: Dict[str, ContextData] = {}
        self.performance_metrics: Dict[str, Any] = {}
        
        self.init()
    
    def init(self):
        """Initialize the prompt engine"""
        try:
            self.load_templates()
            self.load_personas()
            self.setup_default_configurations()
            logger.info("Enhanced Prompt Engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Enhanced Prompt Engine: {e}")
            self.setup_fallback_configurations()
    
    def load_templates(self):
        """Load prompt templates from configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for template_data in data.get("templates", []):
                    template = PromptTemplate(**template_data)
                    self.templates[template.template_id] = template
                    
                logger.info(f"Loaded {len(self.templates)} prompt templates")
            else:
                logger.warning(f"Template file not found: {self.config_path}")
                
        except Exception as e:
            logger.error(f"Failed to load templates: {e}")
    
    def load_personas(self):
        """Load persona profiles"""
        try:
            # Load from personas directory if it exists
            personas_dir = Path("meta/personas")
            if personas_dir.exists():
                for persona_file in personas_dir.glob("*.json"):
                    with open(persona_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        persona = PersonaProfile(**data)
                        self.personas[persona.persona_id] = persona
                        
                logger.info(f"Loaded {len(self.personas)} persona profiles")
            else:
                logger.info("Personas directory not found, using default personas")
                
        except Exception as e:
            logger.error(f"Failed to load personas: {e}")
    
    def setup_default_configurations(self):
        """Setup default configurations if none loaded"""
        if not self.personas:
            self.create_default_personas()
        
        if not self.templates:
            self.create_default_templates()
    
    def create_default_personas(self):
        """Create default persona profiles"""
        default_personas = [
            {
                "persona_id": "tier1_customer_service",
                "persona_name": "Tier 1 Customer Service Agent",
                "persona_type": PersonaType.CUSTOMER_SERVICE,
                "description": "Entry-level customer service agent with basic support capabilities",
                "personality_traits": ["helpful", "patient", "professional", "empathetic"],
                "expertise_areas": ["basic_support", "escalation_procedures", "company_policies"],
                "response_style": "friendly_professional",
                "formality_level": "professional",
                "emoji_usage": "minimal",
                "response_length": "concise",
                "tone": "helpful_and_supportive",
                "limitations": ["no_technical_details", "no_financial_advice", "escalation_required_for_complex_issues"],
                "escalation_triggers": ["technical_issues", "financial_concerns", "complaints", "escalation_requests"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            {
                "persona_id": "tier2_technical_support",
                "persona_name": "Tier 2 Technical Support Specialist",
                "persona_type": PersonaType.TECHNICAL_SUPPORT,
                "description": "Intermediate technical support specialist with advanced troubleshooting capabilities",
                "personality_traits": ["technical", "analytical", "helpful", "thorough"],
                "expertise_areas": ["technical_support", "troubleshooting", "system_configuration", "advanced_issues"],
                "response_style": "technical_friendly",
                "formality_level": "friendly_professional",
                "emoji_usage": "moderate",
                "response_length": "detailed",
                "tone": "technical_and_helpful",
                "limitations": ["no_system_administration", "limited_financial_authority"],
                "escalation_triggers": ["system_administration", "complex_technical_issues", "management_approval"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            {
                "persona_id": "tier3_senior_specialist",
                "persona_name": "Tier 3 Senior Specialist",
                "persona_type": PersonaType.SPECIALIST,
                "description": "Senior specialist with expert-level knowledge and complex issue resolution capabilities",
                "personality_traits": ["expert", "confident", "helpful", "efficient"],
                "expertise_areas": ["complex_issue_resolution", "quality_assurance", "agent_training", "process_improvement"],
                "response_style": "expert_friendly",
                "formality_level": "expert_friendly",
                "emoji_usage": "appropriate",
                "response_length": "comprehensive",
                "tone": "expert_and_helpful",
                "limitations": ["no_legal_advice", "compliance_with_company_policies"],
                "escalation_triggers": ["legal_issues", "compliance_violations", "management_approval"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        ]
        
        for persona_data in default_personas:
            persona = PersonaProfile(**persona_data)
            self.personas[persona.persona_id] = persona
    
    def create_default_templates(self):
        """Create default prompt templates"""
        default_templates = [
            {
                "template_id": "customer_greeting",
                "template_name": "Customer Greeting",
                "template_type": PromptType.SYSTEM,
                "template_content": "Hello {{customer_name}}! Welcome to {{company_name}} support. I'm {{agent_name}}, your {{agent_role}}. How can I assist you today?",
                "variables": [
                    {"name": "customer_name", "type": "string", "required": True},
                    {"name": "company_name", "type": "string", "required": True},
                    {"name": "agent_name", "type": "string", "required": True},
                    {"name": "agent_role", "type": "string", "required": True}
                ],
                "persona_requirements": ["tier1_customer_service", "tier2_technical_support"],
                "guardrail_level": GuardrailLevel.LOW,
                "performance_metrics": {"expected_response_time": 2.0, "quality_threshold": 0.8},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            {
                "template_id": "technical_issue_response",
                "template_name": "Technical Issue Response",
                "template_type": PromptType.ASSISTANT,
                "template_content": "I understand you're experiencing a technical issue with {{issue_description}}. Let me help you troubleshoot this step by step. First, let's verify {{first_step}}. Can you confirm if {{verification_question}}?",
                "variables": [
                    {"name": "issue_description", "type": "string", "required": True},
                    {"name": "first_step", "type": "string", "required": True},
                    {"name": "verification_question", "type": "string", "required": True}
                ],
                "persona_requirements": ["tier2_technical_support", "tier3_senior_specialist"],
                "guardrail_level": GuardrailLevel.MEDIUM,
                "performance_metrics": {"expected_response_time": 5.0, "quality_threshold": 0.9},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            {
                "template_id": "escalation_notice",
                "template_name": "Escalation Notice",
                "template_type": PromptType.SYSTEM,
                "template_content": "I understand this issue requires specialized attention. I'm escalating your case to our {{escalation_team}} team. {{escalation_reason}}. You'll be contacted by {{escalation_timeframe}} with a resolution or next steps.",
                "variables": [
                    {"name": "escalation_team", "type": "string", "required": True},
                    {"name": "escalation_reason", "type": "string", "required": True},
                    {"name": "escalation_timeframe", "type": "string", "required": True}
                ],
                "persona_requirements": ["tier1_customer_service", "tier2_technical_support"],
                "guardrail_level": GuardrailLevel.HIGH,
                "performance_metrics": {"expected_response_time": 3.0, "quality_threshold": 0.95},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            }
        ]
        
        for template_data in default_templates:
            template = PromptTemplate(**template_data)
            self.templates[template.template_id] = template
    
    def setup_fallback_configurations(self):
        """Setup fallback configurations if initialization fails"""
        logger.warning("Using fallback configurations")
        self.create_default_personas()
        self.create_default_templates()
    
    def generate_prompt(self, 
                       template_id: str, 
                       context: ContextData, 
                       persona_id: str,
                       variables: Dict[str, Any] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a prompt using the specified template and context
        
        Returns:
            Tuple of (generated_prompt, metadata)
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if template_id not in self.templates:
                raise ValueError(f"Template {template_id} not found")
            
            if persona_id not in self.personas:
                raise ValueError(f"Persona {persona_id} not found")
            
            template = self.templates[template_id]
            persona = self.personas[persona_id]
            
            # Validate persona requirements
            if not self._validate_persona_requirements(template, persona):
                raise ValueError(f"Persona {persona_id} does not meet requirements for template {template_id}")
            
            # Merge variables with context
            merged_variables = self._merge_variables_with_context(template, context, variables or {})
            
            # Generate prompt content
            prompt_content = self._replace_variables(template.template_content, merged_variables)
            
            # Apply persona characteristics
            prompt_content = self._apply_persona_characteristics(prompt_content, persona)
            
            # Apply guardrails
            guardrail_result = self._apply_guardrails(prompt_content, template.guardrail_level, context)
            
            # Generate metadata
            metadata = {
                "template_id": template_id,
                "persona_id": persona_id,
                "variables_used": merged_variables,
                "guardrail_result": asdict(guardrail_result),
                "generation_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
                "version": template.version
            }
            
            # Update performance metrics
            self._update_performance_metrics(template_id, metadata)
            
            return prompt_content, metadata
            
        except Exception as e:
            logger.error(f"Failed to generate prompt: {e}")
            # Return fallback prompt
            fallback_prompt = self._generate_fallback_prompt(context, persona_id)
            metadata = {
                "error": str(e),
                "fallback_used": True,
                "generation_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
            return fallback_prompt, metadata
    
    def _validate_persona_requirements(self, template: PromptTemplate, persona: PersonaProfile) -> bool:
        """Validate if persona meets template requirements"""
        if not template.persona_requirements:
            return True
        
        return persona.persona_id in template.persona_requirements
    
    def _merge_variables_with_context(self, template: PromptTemplate, context: ContextData, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Merge template variables with context and provided variables"""
        merged = {}
        
        # Add context data
        if context.customer_profile:
            merged.update(context.customer_profile)
        
        merged.update({
            "session_id": context.session_id,
            "current_topic": context.current_topic,
            "customer_intent": context.customer_intent,
            "escalation_level": context.escalation_level,
            "agent_tier": context.agent_tier
        })
        
        # Add provided variables
        merged.update(variables)
        
        # Add default values for missing required variables
        for var in template.variables:
            if var.get("required", False) and var["name"] not in merged:
                merged[var["name"]] = self._get_default_value(var)
        
        return merged
    
    def _get_default_value(self, var: Dict[str, Any]) -> Any:
        """Get default value for a variable"""
        var_type = var.get("type", "string")
        
        if var_type == "string":
            return var.get("default", "")
        elif var_type == "number":
            return var.get("default", 0)
        elif var_type == "boolean":
            return var.get("default", False)
        elif var_type == "list":
            return var.get("default", [])
        else:
            return var.get("default", "")
    
    def _replace_variables(self, content: str, variables: Dict[str, Any]) -> str:
        """Replace variables in template content"""
        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            if placeholder in content:
                content = content.replace(placeholder, str(var_value))
        
        return content
    
    def _apply_persona_characteristics(self, content: str, persona: PersonaProfile) -> str:
        """Apply persona characteristics to content"""
        # Apply formality level
        if persona.formality_level == "professional":
            content = self._make_professional(content)
        elif persona.formality_level == "friendly_professional":
            content = self._make_friendly_professional(content)
        elif persona.formality_level == "expert_friendly":
            content = self._make_expert_friendly(content)
        
        # Apply response length preferences
        if persona.response_length == "concise":
            content = self._make_concise(content)
        elif persona.response_length == "comprehensive":
            content = self._make_comprehensive(content)
        
        # Apply tone adjustments
        if persona.tone == "helpful_and_supportive":
            content = self._add_helpful_tone(content)
        elif persona.tone == "technical_and_helpful":
            content = self._add_technical_tone(content)
        
        return content
    
    def _make_professional(self, content: str) -> str:
        """Make content more professional"""
        # Ensure proper capitalization and punctuation
        content = content.strip()
        if content and not content.endswith(('.', '!', '?')):
            content += '.'
        return content
    
    def _make_friendly_professional(self, content: str) -> str:
        """Make content friendly but professional"""
        content = self._make_professional(content)
        
        # Add friendly touches
        friendly_prefixes = [
            "I understand your concern",
            "Let me help you with that",
            "I appreciate you bringing this to our attention"
        ]
        
        if not any(prefix.lower() in content.lower() for prefix in friendly_prefixes):
            prefix = friendly_prefixes[0]
            content = f"{prefix}. {content}"
        
        return content
    
    def _make_expert_friendly(self, content: str) -> str:
        """Make content expert-friendly"""
        content = self._make_friendly_professional(content)
        
        # Add expertise indicators
        expert_prefixes = [
            "Based on my experience",
            "From what I can see",
            "Let me analyze this for you"
        ]
        
        if not any(prefix.lower() in content.lower() for prefix in expert_prefixes):
            prefix = expert_prefixes[0]
            content = f"{prefix}, {content}"
        
        return content
    
    def _make_concise(self, content: str) -> str:
        """Make content more concise"""
        # Remove unnecessary words and phrases
        unnecessary_phrases = [
            "I would like to inform you that",
            "Please be advised that",
            "It is important to note that"
        ]
        
        for phrase in unnecessary_phrases:
            content = content.replace(phrase, "")
        
        return content.strip()
    
    def _make_comprehensive(self, content: str) -> str:
        """Make content more comprehensive"""
        # Add additional context and details
        if "troubleshoot" in content.lower():
            content += " I'll guide you through each step to ensure we resolve this completely."
        
        return content
    
    def _add_helpful_tone(self, content: str) -> str:
        """Add helpful tone to content"""
        if not any(word in content.lower() for word in ["help", "assist", "support"]):
            content += " I'm here to help you resolve this issue."
        
        return content
    
    def _add_technical_tone(self, content: str) -> str:
        """Add technical tone to content"""
        if "issue" in content.lower() and "technical" not in content.lower():
            content = content.replace("issue", "technical issue")
        
        return content
    
    def _apply_guardrails(self, content: str, guardrail_level: GuardrailLevel, context: ContextData) -> GuardrailResult:
        """Apply guardrails to content"""
        violations = []
        risk_level = "low"
        requires_escalation = False
        escalation_reason = ""
        
        # Content safety checks
        if self._contains_inappropriate_content(content):
            violations.append("inappropriate_content")
            risk_level = "high"
            requires_escalation = True
            escalation_reason = "Inappropriate content detected"
        
        # Compliance checks
        if self._violates_compliance(content, context):
            violations.append("compliance_violation")
            risk_level = "critical"
            requires_escalation = True
            escalation_reason = "Compliance violation detected"
        
        # Escalation level checks
        if context.escalation_level >= 3:
            violations.append("high_escalation_level")
            risk_level = "high"
            requires_escalation = True
            escalation_reason = "High escalation level reached"
        
        # Agent tier capability checks
        if not self._validate_agent_capabilities(content, context):
            violations.append("capability_exceeded")
            risk_level = "medium"
            requires_escalation = True
            escalation_reason = "Agent capability exceeded"
        
        passed = len(violations) == 0
        
        recommendations = self._generate_guardrail_recommendations(violations, content, context)
        
        return GuardrailResult(
            passed=passed,
            violations=violations,
            risk_level=risk_level,
            recommendations=recommendations,
            requires_escalation=requires_escalation,
            escalation_reason=escalation_reason
        )
    
    def _contains_inappropriate_content(self, content: str) -> bool:
        """Check if content contains inappropriate material"""
        inappropriate_patterns = [
            r'\b(hate|racist|discriminatory)\b',
            r'\b(violence|threat|harm)\b',
            r'\b(inappropriate|offensive)\b'
        ]
        
        for pattern in inappropriate_patterns:
            if re.search(pattern, content.lower()):
                return True
        
        return False
    
    def _violates_compliance(self, content: str, context: ContextData) -> bool:
        """Check if content violates compliance requirements"""
        # Check for financial advice if agent tier is too low
        if context.agent_tier < 2 and any(word in content.lower() for word in ["investment", "financial", "money", "profit"]):
            return True
        
        # Check for legal advice if agent tier is too low
        if context.agent_tier < 3 and any(word in content.lower() for word in ["legal", "law", "attorney", "court"]):
            return True
        
        return False
    
    def _validate_agent_capabilities(self, content: str, context: ContextData) -> bool:
        """Validate if agent has capabilities for the content"""
        # Check if agent can handle technical issues
        if context.agent_tier < 2 and any(word in content.lower() for word in ["technical", "system", "configuration", "admin"]):
            return False
        
        # Check if agent can handle complex issues
        if context.agent_tier < 3 and any(word in content.lower() for word in ["complex", "advanced", "expert", "specialized"]):
            return False
        
        return True
    
    def _generate_guardrail_recommendations(self, violations: List[str], content: str, context: ContextData) -> List[str]:
        """Generate recommendations for guardrail violations"""
        recommendations = []
        
        for violation in violations:
            if violation == "inappropriate_content":
                recommendations.append("Review and revise content to remove inappropriate language")
            elif violation == "compliance_violation":
                recommendations.append("Escalate to appropriate tier agent for compliance-sensitive content")
            elif violation == "high_escalation_level":
                recommendations.append("Immediate escalation to senior agent or supervisor required")
            elif violation == "capability_exceeded":
                recommendations.append("Transfer to agent with appropriate capabilities and training")
        
        return recommendations
    
    def _generate_fallback_prompt(self, context: ContextData, persona_id: str) -> str:
        """Generate fallback prompt if template generation fails"""
        return f"I apologize for the technical difficulty. I'm here to help you with your inquiry. How can I assist you today?"
    
    def _update_performance_metrics(self, template_id: str, metadata: Dict[str, Any]):
        """Update performance metrics"""
        if template_id not in self.performance_metrics:
            self.performance_metrics[template_id] = {
                "total_generations": 0,
                "successful_generations": 0,
                "failed_generations": 0,
                "average_generation_time": 0.0,
                "total_generation_time": 0.0
            }
        
        metrics = self.performance_metrics[template_id]
        metrics["total_generations"] += 1
        
        if "error" not in metadata:
            metrics["successful_generations"] += 1
        else:
            metrics["failed_generations"] += 1
        
        generation_time = metadata.get("generation_time", 0.0)
        metrics["total_generation_time"] += generation_time
        metrics["average_generation_time"] = metrics["total_generation_time"] / metrics["total_generations"]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.performance_metrics
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template IDs"""
        return list(self.templates.keys())
    
    def get_available_personas(self) -> List[str]:
        """Get list of available persona IDs"""
        return list(self.personas.keys())
    
    def add_template(self, template: PromptTemplate):
        """Add a new template"""
        self.templates[template.template_id] = template
        logger.info(f"Added template: {template.template_id}")
    
    def add_persona(self, persona: PersonaProfile):
        """Add a new persona"""
        self.personas[persona.persona_id] = persona
        logger.info(f"Added persona: {persona.persona_id}")
    
    def export_configuration(self) -> Dict[str, Any]:
        """Export current configuration"""
        return {
            "templates": {tid: asdict(template) for tid, template in self.templates.items()},
            "personas": {pid: asdict(persona) for pid, persona in self.personas.items()},
            "performance_metrics": self.performance_metrics,
            "export_timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }

# Export for use in other modules
if __name__ == "__main__":
    # Test the enhanced prompt engine
    engine = EnhancedPromptEngine()
    
    # Create test context
    test_context = ContextData(
        context_id="test_context_1",
        session_id="test_session_1",
        customer_profile={"customer_name": "John Doe", "company_name": "OCINT"},
        conversation_history=[],
        current_topic="technical_support",
        customer_intent="resolve_issue",
        escalation_level=1,
        agent_tier=2,
        knowledge_base_access=["technical_support", "troubleshooting"],
        timestamp=datetime.now().isoformat(),
        version="1.0"
    )
    
    # Test prompt generation
    prompt, metadata = engine.generate_prompt(
        template_id="customer_greeting",
        context=test_context,
        persona_id="tier2_technical_support",
        variables={"agent_name": "Sarah", "agent_role": "Technical Support Specialist"}
    )
    
    print("Generated Prompt:")
    print(prompt)
    print("\nMetadata:")
    print(json.dumps(metadata, indent=2))
