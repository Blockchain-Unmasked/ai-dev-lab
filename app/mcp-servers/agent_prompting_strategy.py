#!/usr/bin/env python3
"""
AI/DEV Lab - Agent Prompting Strategy
Combines contact center research with Gemini prompting best practices
to create a comprehensive agent system with clear mission and rules.
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class AgentTier(Enum):
    """Agent tier levels based on contact center research"""
    TIER_1 = "tier_1"  # Entry Level Agent
    TIER_2 = "tier_2"  # Intermediate Agent  
    TIER_3 = "tier_3"  # Senior Agent
    SUPERVISOR = "supervisor"  # Supervisor/Manager
    FLOOR_MANAGER = "floor_manager"  # Floor Manager

class InteractionType(Enum):
    """Types of customer interactions"""
    BASIC_INQUIRY = "basic_inquiry"
    TECHNICAL_SUPPORT = "technical_support"
    BILLING_ISSUE = "billing_issue"
    COMPLAINT = "complaint"
    ESCALATION = "escalation"
    VIP_SUPPORT = "vip_support"

@dataclass
class AgentCapabilities:
    """Agent capabilities based on tier"""
    tier: AgentTier
    responsibilities: List[str]
    knowledge_access: List[str]
    tools_available: List[str]
    escalation_triggers: List[str]
    max_complexity: str

@dataclass
class PromptingStrategy:
    """Comprehensive prompting strategy for AI agents"""
    system_prompt: str
    context_prompt: str
    task_prompt: str
    constraints: List[str]
    examples: List[Dict[str, str]]
    fallback_responses: List[str]

class AgentPromptingEngine:
    """
    Advanced prompting engine that combines contact center research
    with Gemini prompting best practices for optimal agent performance.
    """
    
    def __init__(self, research_data_path: Optional[str] = None):
        self.research_data = self._load_research_data(research_data_path)
        self.agent_capabilities = self._build_agent_capabilities()
        self.prompting_strategies = self._build_prompting_strategies()
    
    def _load_research_data(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Load contact center research data"""
        if not path:
            # Default path to research data
            path = Path(__file__).parent.parent.parent / "missions" / "contact_center_research"
        
        research_path = Path(path)
        research_data = {}
        
        try:
            # Load comprehensive research report
            with open(research_path / "comprehensive_research_report.json", 'r') as f:
                research_data["comprehensive"] = json.load(f)
            
            # Load individual research components
            for component in ["agent_tier_system_research.json", "qa_process_research.json", 
                            "kb_architecture_research.json", "workflow_integration_research.json"]:
                with open(research_path / component, 'r') as f:
                    key = component.replace("_research.json", "")
                    research_data[key] = json.load(f)
                    
        except FileNotFoundError as e:
            print(f"Warning: Could not load research data: {e}")
            research_data = {}
        
        return research_data
    
    def _build_agent_capabilities(self) -> Dict[AgentTier, AgentCapabilities]:
        """Build agent capabilities based on research data"""
        capabilities = {}
        
        if "comprehensive" in self.research_data:
            tier_data = self.research_data["comprehensive"]["detailed_findings"]["phases"]["agent_tier_systems"]["tier_definitions"]
            
            # Tier 1 - Entry Level Agent
            capabilities[AgentTier.TIER_1] = AgentCapabilities(
                tier=AgentTier.TIER_1,
                responsibilities=tier_data["tier_1"]["responsibilities"],
                knowledge_access=tier_data["tier_1"]["knowledge_access"],
                tools_available=tier_data["tier_1"]["tools_available"],
                escalation_triggers=tier_data["tier_1"]["escalation_triggers"],
                max_complexity="Basic customer inquiries and standard procedures"
            )
            
            # Tier 2 - Intermediate Agent
            capabilities[AgentTier.TIER_2] = AgentCapabilities(
                tier=AgentTier.TIER_2,
                responsibilities=tier_data["tier_2"]["responsibilities"],
                knowledge_access=tier_data["tier_2"]["knowledge_access"],
                tools_available=tier_data["tier_2"]["tools_available"],
                escalation_triggers=tier_data["tier_2"]["escalation_triggers"],
                max_complexity="Moderate technical issues and training responsibilities"
            )
            
            # Tier 3 - Senior Agent
            capabilities[AgentTier.TIER_3] = AgentCapabilities(
                tier=AgentTier.TIER_3,
                responsibilities=tier_data["tier_3"]["responsibilities"],
                knowledge_access=tier_data["tier_3"]["knowledge_access"],
                tools_available=tier_data["tier_3"]["tools_available"],
                escalation_triggers=tier_data["tier_3"]["escalation_triggers"],
                max_complexity="Complex issues, VIP support, and process improvement"
            )
        
        return capabilities
    
    def _build_prompting_strategies(self) -> Dict[AgentTier, PromptingStrategy]:
        """Build prompting strategies for each agent tier"""
        strategies = {}
        
        for tier in AgentTier:
            if tier in self.agent_capabilities:
                strategies[tier] = self._create_tier_strategy(tier)
        
        return strategies
    
    def _create_tier_strategy(self, tier: AgentTier) -> PromptingStrategy:
        """Create prompting strategy for specific tier"""
        capabilities = self.agent_capabilities[tier]
        
        # System prompt - defines the agent's identity and core mission
        system_prompt = self._build_system_prompt(tier, capabilities)
        
        # Context prompt - provides situational awareness
        context_prompt = self._build_context_prompt(tier, capabilities)
        
        # Task prompt - defines specific task instructions
        task_prompt = self._build_task_prompt(tier, capabilities)
        
        # Constraints - defines what the agent should and shouldn't do
        constraints = self._build_constraints(tier, capabilities)
        
        # Examples - provides few-shot learning examples
        examples = self._build_examples(tier, capabilities)
        
        # Fallback responses - handles edge cases
        fallback_responses = self._build_fallback_responses(tier, capabilities)
        
        return PromptingStrategy(
            system_prompt=system_prompt,
            context_prompt=context_prompt,
            task_prompt=task_prompt,
            constraints=constraints,
            examples=examples,
            fallback_responses=fallback_responses
        )
    
    def _build_system_prompt(self, tier: AgentTier, capabilities: AgentCapabilities) -> str:
        """Build system prompt using Gemini prompting best practices"""
        
        tier_names = {
            AgentTier.TIER_1: "Entry Level Customer Support Agent",
            AgentTier.TIER_2: "Intermediate Customer Support Agent", 
            AgentTier.TIER_3: "Senior Customer Support Agent",
            AgentTier.SUPERVISOR: "Customer Support Supervisor",
            AgentTier.FLOOR_MANAGER: "Floor Manager"
        }
        
        return f"""You are an AI-powered {tier_names[tier]} in an enterprise contact center. Your mission is to provide exceptional customer support while maintaining the highest standards of professionalism and efficiency.

## CORE IDENTITY
- **Role**: {tier_names[tier]}
- **Tier Level**: {tier.value.upper()}
- **Primary Mission**: Deliver outstanding customer service within your tier's capabilities
- **Max Complexity**: {capabilities.max_complexity}

## YOUR RESPONSIBILITIES
{self._format_list(capabilities.responsibilities)}

## KNOWLEDGE ACCESS
You have access to:
{self._format_list(capabilities.knowledge_access)}

## AVAILABLE TOOLS
You can use:
{self._format_list(capabilities.tools_available)}

## ESCALATION TRIGGERS
You must escalate when encountering:
{self._format_list(capabilities.escalation_triggers)}

## CORE PRINCIPLES
1. **Customer First**: Always prioritize customer satisfaction and resolution
2. **Professional Communication**: Maintain a helpful, empathetic, and professional tone
3. **Accurate Information**: Only provide information you're confident about
4. **Efficient Resolution**: Work to resolve issues quickly and effectively
5. **Documentation**: Properly document all interactions and resolutions
6. **Escalation**: Know when to escalate and do so promptly
7. **Continuous Learning**: Learn from each interaction to improve service

You are part of a sophisticated AI-powered contact center system designed to provide enterprise-grade customer support."""
    
    def _build_context_prompt(self, tier: AgentTier, capabilities: AgentCapabilities) -> str:
        """Build context prompt for situational awareness"""
        
        return f"""## CURRENT SESSION CONTEXT
- **Agent Tier**: {tier.value.upper()}
- **Session Type**: Customer Support Interaction
- **Available Capabilities**: {len(capabilities.tools_available)} tools, {len(capabilities.knowledge_access)} knowledge areas
- **Escalation Authority**: Can escalate to higher tiers when needed

## INTERACTION GUIDELINES
- **Response Time**: Aim for quick, accurate responses
- **Tone**: Professional, helpful, and empathetic
- **Documentation**: Always document key points and resolutions
- **Follow-up**: Ensure customer satisfaction before closing

## QUALITY STANDARDS
- **Accuracy**: Provide correct information only
- **Completeness**: Address all aspects of customer inquiry
- **Clarity**: Use clear, understandable language
- **Efficiency**: Resolve issues in minimum time possible"""
    
    def _build_task_prompt(self, tier: AgentTier, capabilities: AgentCapabilities) -> str:
        """Build task-specific prompt instructions"""
        
        return f"""## TASK INSTRUCTIONS
Based on your tier level ({tier.value.upper()}), handle the customer inquiry with the following approach:

### STEP 1: ASSESS THE INQUIRY
- Identify the type of customer issue
- Determine if it's within your tier's capabilities
- Check if escalation is needed

### STEP 2: PROVIDE ASSISTANCE
- Use your available knowledge and tools
- Follow standard operating procedures
- Maintain professional communication

### STEP 3: RESOLVE OR ESCALATE
- If within capabilities: Provide complete resolution
- If beyond capabilities: Escalate to appropriate tier
- Document the interaction thoroughly

### STEP 4: ENSURE SATISFACTION
- Confirm customer understanding
- Ask if additional help is needed
- Document resolution and follow-up actions

## RESPONSE FORMAT
Structure your response as:
1. **Greeting & Acknowledgment**
2. **Issue Understanding** 
3. **Solution/Assistance**
4. **Confirmation & Follow-up**
5. **Documentation Notes** (internal)"""
    
    def _build_constraints(self, tier: AgentTier, capabilities: AgentCapabilities) -> List[str]:
        """Build constraints based on Gemini prompting best practices"""
        
        base_constraints = [
            "Always maintain a professional and helpful tone",
            "Never provide information you're not confident about",
            "Always ask for clarification when needed",
            "Never make promises you cannot keep",
            "Always document interactions properly",
            "Never share internal system information with customers",
            "Always follow escalation procedures when appropriate"
        ]
        
        tier_specific = {
            AgentTier.TIER_1: [
                "Stay within basic knowledge scope",
                "Escalate complex technical issues immediately",
                "Use only approved scripts and responses",
                "Never attempt advanced troubleshooting"
            ],
            AgentTier.TIER_2: [
                "Handle moderate complexity issues",
                "Provide technical support within scope",
                "Mentor and guide Tier 1 agents when needed",
                "Escalate only when truly necessary"
            ],
            AgentTier.TIER_3: [
                "Handle complex and VIP customer issues",
                "Provide expert-level support and guidance",
                "Make process improvement recommendations",
                "Train and mentor all lower tiers"
            ]
        }
        
        return base_constraints + tier_specific.get(tier, [])
    
    def _build_examples(self, tier: AgentTier, capabilities: AgentCapabilities) -> List[Dict[str, str]]:
        """Build few-shot learning examples"""
        
        examples = []
        
        # Basic inquiry example
        examples.append({
            "input": "Customer: Hi, I need help with my account password",
            "output": "Hello! I'd be happy to help you with your password issue. Let me assist you with resetting your password. First, I'll need to verify your account for security purposes. Can you please provide your account email address or username?"
        })
        
        # Escalation example
        examples.append({
            "input": "Customer: I'm having a complex technical issue with your API integration",
            "output": "I understand you're experiencing a complex technical issue with our API integration. This type of technical problem requires specialized expertise. Let me escalate this to our technical support team who can provide you with the detailed assistance you need. I'll transfer you to a Tier 2 technical specialist right away."
        })
        
        # Resolution example
        examples.append({
            "input": "Customer: I can't find my billing information",
            "output": "I can help you locate your billing information. Let me guide you through accessing your account billing details. You can find this information by logging into your account and navigating to the 'Billing' section in your dashboard. Would you like me to walk you through the steps to access this information?"
        })
        
        return examples
    
    def _build_fallback_responses(self, tier: AgentTier, capabilities: AgentCapabilities) -> List[str]:
        """Build fallback responses for edge cases"""
        
        return [
            "I apologize, but I'm experiencing some technical difficulties. Let me connect you with a human agent who can assist you immediately.",
            "I want to make sure I provide you with the most accurate information. Let me escalate this to a specialist who can give you the detailed help you need.",
            "I understand this is important to you. Let me transfer you to our senior support team who can provide the expert assistance you require.",
            "I'm here to help, but I want to ensure you get the best possible support. Let me connect you with a specialist who can address your specific needs."
        ]
    
    def _format_list(self, items: List[str]) -> str:
        """Format list items for prompt readability"""
        return "\n".join([f"- {item}" for item in items])
    
    def generate_agent_prompt(self, tier: AgentTier, interaction_type: InteractionType, 
                            customer_message: str, additional_context: Optional[Dict] = None) -> str:
        """Generate complete prompt for agent interaction"""
        
        if tier not in self.prompting_strategies:
            raise ValueError(f"No prompting strategy available for tier: {tier}")
        
        strategy = self.prompting_strategies[tier]
        
        # Build complete prompt following Gemini best practices
        prompt_parts = [
            strategy.system_prompt,
            "",
            strategy.context_prompt,
            "",
            strategy.task_prompt,
            "",
            "## CONSTRAINTS",
            *[f"- {constraint}" for constraint in strategy.constraints],
            "",
            "## EXAMPLES",
        ]
        
        # Add examples
        for i, example in enumerate(strategy.examples[:3], 1):  # Limit to 3 examples
            prompt_parts.extend([
                f"### Example {i}:",
                f"**Input**: {example['input']}",
                f"**Output**: {example['output']}",
                ""
            ])
        
        # Add current interaction
        prompt_parts.extend([
            "## CURRENT INTERACTION",
            f"**Customer Message**: {customer_message}",
            f"**Interaction Type**: {interaction_type.value}",
            "",
            "## YOUR RESPONSE",
            "Please respond to the customer following your tier guidelines and the examples above:"
        ])
        
        # Add additional context if provided
        if additional_context:
            prompt_parts.extend([
                "",
                "## ADDITIONAL CONTEXT",
                json.dumps(additional_context, indent=2)
            ])
        
        return "\n".join(prompt_parts)
    
    def get_escalation_decision(self, tier: AgentTier, customer_message: str, 
                              interaction_context: Dict) -> Dict[str, Any]:
        """Determine if escalation is needed based on research criteria"""
        
        if tier not in self.agent_capabilities:
            return {"escalate": False, "reason": "Unknown tier"}
        
        capabilities = self.agent_capabilities[tier]
        
        # Check escalation triggers
        escalation_needed = False
        escalation_reason = ""
        
        for trigger in capabilities.escalation_triggers:
            if any(keyword in customer_message.lower() for keyword in trigger.lower().split()):
                escalation_needed = True
                escalation_reason = f"Trigger detected: {trigger}"
                break
        
        # Check complexity indicators
        complexity_indicators = [
            "complex", "advanced", "technical", "integration", "api", "system",
            "critical", "urgent", "vip", "executive", "legal", "compliance"
        ]
        
        if any(indicator in customer_message.lower() for indicator in complexity_indicators):
            if tier == AgentTier.TIER_1:  # Tier 1 should escalate complex issues
                escalation_needed = True
                escalation_reason = "Complex issue beyond Tier 1 capabilities"
        
        return {
            "escalate": escalation_needed,
            "reason": escalation_reason,
            "recommended_tier": self._get_next_tier(tier) if escalation_needed else tier,
            "confidence": 0.8 if escalation_needed else 0.9
        }
    
    def _get_next_tier(self, current_tier: AgentTier) -> AgentTier:
        """Get the next tier for escalation"""
        escalation_map = {
            AgentTier.TIER_1: AgentTier.TIER_2,
            AgentTier.TIER_2: AgentTier.TIER_3,
            AgentTier.TIER_3: AgentTier.SUPERVISOR,
            AgentTier.SUPERVISOR: AgentTier.FLOOR_MANAGER
        }
        return escalation_map.get(current_tier, AgentTier.SUPERVISOR)
    
    def get_quality_metrics(self, tier: AgentTier) -> Dict[str, Any]:
        """Get quality metrics based on research findings"""
        
        if "qa_process" in self.research_data:
            qa_data = self.research_data["qa_process"]
            return {
                "evaluation_criteria": qa_data.get("qa_methodologies", {}).get("call_monitoring", {}).get("evaluation_criteria", []),
                "scoring_system": qa_data.get("qa_methodologies", {}).get("call_monitoring", {}).get("scoring_system", "1-5 scale"),
                "frequency": qa_data.get("qa_methodologies", {}).get("call_monitoring", {}).get("frequency", "Random sampling")
            }
        
        return {
            "evaluation_criteria": [
                "Greeting and introduction",
                "Problem identification", 
                "Solution provision",
                "Customer satisfaction",
                "Documentation quality"
            ],
            "scoring_system": "1-5 scale with specific criteria for each level",
            "frequency": "Random sampling + targeted monitoring"
        }

# MCP Server Integration
class AgentPromptingMCP:
    """MCP Server integration for agent prompting strategy"""
    
    def __init__(self):
        self.prompting_engine = AgentPromptingEngine()
    
    def generate_prompt(self, tier: str, interaction_type: str, customer_message: str, 
                       additional_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate agent prompt via MCP"""
        try:
            tier_enum = AgentTier(tier)
            interaction_enum = InteractionType(interaction_type)
            
            prompt = self.prompting_engine.generate_agent_prompt(
                tier_enum, interaction_enum, customer_message, additional_context
            )
            
            return {
                "success": True,
                "prompt": prompt,
                "tier": tier,
                "interaction_type": interaction_type,
                "prompt_length": len(prompt),
                "tokens_estimated": len(prompt.split()) * 1.3  # Rough token estimation
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tier": tier,
                "interaction_type": interaction_type
            }
    
    def check_escalation(self, tier: str, customer_message: str, 
                        interaction_context: Dict) -> Dict[str, Any]:
        """Check if escalation is needed via MCP"""
        try:
            tier_enum = AgentTier(tier)
            decision = self.prompting_engine.get_escalation_decision(
                tier_enum, customer_message, interaction_context
            )
            
            return {
                "success": True,
                "escalation_decision": decision
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_agent_capabilities(self, tier: str) -> Dict[str, Any]:
        """Get agent capabilities via MCP"""
        try:
            tier_enum = AgentTier(tier)
            capabilities = self.prompting_engine.agent_capabilities.get(tier_enum)
            
            if capabilities:
                return {
                    "success": True,
                    "tier": tier,
                    "capabilities": {
                        "responsibilities": capabilities.responsibilities,
                        "knowledge_access": capabilities.knowledge_access,
                        "tools_available": capabilities.tools_available,
                        "escalation_triggers": capabilities.escalation_triggers,
                        "max_complexity": capabilities.max_complexity
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"No capabilities found for tier: {tier}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the prompting engine
    engine = AgentPromptingEngine()
    
    # Test prompt generation
    test_message = "I'm having trouble with my account login and need help with API integration"
    
    # Generate Tier 1 prompt
    tier1_prompt = engine.generate_agent_prompt(
        AgentTier.TIER_1, 
        InteractionType.TECHNICAL_SUPPORT, 
        test_message
    )
    
    print("=== TIER 1 PROMPT ===")
    print(tier1_prompt[:500] + "...")
    
    # Check escalation decision
    escalation = engine.get_escalation_decision(
        AgentTier.TIER_1, 
        test_message, 
        {"customer_type": "standard"}
    )
    
    print("\n=== ESCALATION DECISION ===")
    print(json.dumps(escalation, indent=2))
    
    # Test MCP integration
    mcp = AgentPromptingMCP()
    mcp_result = mcp.generate_prompt("tier_1", "technical_support", test_message)
    
    print("\n=== MCP RESULT ===")
    print(json.dumps(mcp_result, indent=2))
