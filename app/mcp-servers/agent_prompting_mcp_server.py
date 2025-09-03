#!/usr/bin/env python3
"""
AI/DEV Lab - Agent Prompting MCP Server
MCP server for agent prompting strategy and contact center operations
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    CallToolRequest, CallToolResult, ListResourcesRequest, ListResourcesResult,
    ListToolsRequest, ListToolsResult, ReadResourceRequest, ReadResourceResult
)

from agent_prompting_strategy import AgentPromptingMCP, AgentTier, InteractionType

# Initialize the MCP server
app = Server("agent-prompting-strategy")

# Initialize the prompting engine
prompting_mcp = AgentPromptingMCP()

@app.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="agent://prompting-strategy/tier-capabilities",
            name="Agent Tier Capabilities",
            description="Comprehensive agent tier capabilities and responsibilities",
            mimeType="application/json"
        ),
        Resource(
            uri="agent://prompting-strategy/quality-metrics",
            name="Quality Assurance Metrics",
            description="QA metrics and evaluation criteria for agent performance",
            mimeType="application/json"
        ),
        Resource(
            uri="agent://prompting-strategy/escalation-workflows",
            name="Escalation Workflows",
            description="Agent escalation procedures and decision trees",
            mimeType="application/json"
        ),
        Resource(
            uri="agent://prompting-strategy/prompting-examples",
            name="Prompting Examples",
            description="Example prompts and responses for different scenarios",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read specific resources"""
    if uri == "agent://prompting-strategy/tier-capabilities":
        capabilities = {}
        for tier in AgentTier:
            result = prompting_mcp.get_agent_capabilities(tier.value)
            if result["success"]:
                capabilities[tier.value] = result["capabilities"]
        
        return json.dumps(capabilities, indent=2)
    
    elif uri == "agent://prompting-strategy/quality-metrics":
        metrics = prompting_mcp.prompting_engine.get_quality_metrics(AgentTier.TIER_1)
        return json.dumps(metrics, indent=2)
    
    elif uri == "agent://prompting-strategy/escalation-workflows":
        workflows = {
            "tier_1_to_tier_2": {
                "trigger": "Complex issue beyond Tier 1 capabilities",
                "process": [
                    "Agent identifies escalation need",
                    "Agent documents current status", 
                    "Agent transfers case to Tier 2",
                    "Tier 2 agent takes over with full context"
                ]
            },
            "tier_2_to_tier_3": {
                "trigger": "Highly complex technical issues",
                "process": [
                    "Tier 2 agent escalates to Tier 3",
                    "Full case documentation provided",
                    "Tier 3 agent provides expert resolution",
                    "Knowledge transfer back to lower tiers"
                ]
            }
        }
        return json.dumps(workflows, indent=2)
    
    elif uri == "agent://prompting-strategy/prompting-examples":
        examples = {
            "tier_1_basic_inquiry": {
                "input": "Customer: Hi, I need help with my account password",
                "output": "Hello! I'd be happy to help you with your password issue. Let me assist you with resetting your password. First, I'll need to verify your account for security purposes. Can you please provide your account email address or username?"
            },
            "tier_1_escalation": {
                "input": "Customer: I'm having a complex technical issue with your API integration",
                "output": "I understand you're experiencing a complex technical issue with our API integration. This type of technical problem requires specialized expertise. Let me escalate this to our technical support team who can provide you with the detailed assistance you need. I'll transfer you to a Tier 2 technical specialist right away."
            }
        }
        return json.dumps(examples, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="generate_agent_prompt",
            description="Generate a comprehensive prompt for an AI agent based on tier, interaction type, and customer message",
            inputSchema={
                "type": "object",
                "properties": {
                    "tier": {
                        "type": "string",
                        "enum": ["tier_1", "tier_2", "tier_3", "supervisor", "floor_manager"],
                        "description": "Agent tier level"
                    },
                    "interaction_type": {
                        "type": "string", 
                        "enum": ["basic_inquiry", "technical_support", "billing_issue", "complaint", "escalation", "vip_support"],
                        "description": "Type of customer interaction"
                    },
                    "customer_message": {
                        "type": "string",
                        "description": "The customer's message or inquiry"
                    },
                    "additional_context": {
                        "type": "object",
                        "description": "Additional context for the interaction",
                        "properties": {
                            "customer_type": {"type": "string"},
                            "priority": {"type": "string"},
                            "previous_interactions": {"type": "array", "items": {"type": "string"}},
                            "escalation_history": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "required": ["tier", "interaction_type", "customer_message"]
            }
        ),
        Tool(
            name="check_escalation_need",
            description="Determine if a customer interaction needs to be escalated to a higher tier",
            inputSchema={
                "type": "object",
                "properties": {
                    "tier": {
                        "type": "string",
                        "enum": ["tier_1", "tier_2", "tier_3", "supervisor", "floor_manager"],
                        "description": "Current agent tier"
                    },
                    "customer_message": {
                        "type": "string",
                        "description": "The customer's message or inquiry"
                    },
                    "interaction_context": {
                        "type": "object",
                        "description": "Context about the interaction",
                        "properties": {
                            "customer_type": {"type": "string"},
                            "issue_complexity": {"type": "string"},
                            "previous_attempts": {"type": "number"},
                            "customer_satisfaction": {"type": "string"}
                        }
                    }
                },
                "required": ["tier", "customer_message"]
            }
        ),
        Tool(
            name="get_agent_capabilities",
            description="Get the capabilities and responsibilities for a specific agent tier",
            inputSchema={
                "type": "object",
                "properties": {
                    "tier": {
                        "type": "string",
                        "enum": ["tier_1", "tier_2", "tier_3", "supervisor", "floor_manager"],
                        "description": "Agent tier level"
                    }
                },
                "required": ["tier"]
            }
        ),
        Tool(
            name="evaluate_response_quality",
            description="Evaluate the quality of an agent response based on QA criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "tier": {
                        "type": "string",
                        "enum": ["tier_1", "tier_2", "tier_3", "supervisor", "floor_manager"],
                        "description": "Agent tier level"
                    },
                    "customer_message": {
                        "type": "string",
                        "description": "Original customer message"
                    },
                    "agent_response": {
                        "type": "string",
                        "description": "Agent's response to evaluate"
                    },
                    "interaction_type": {
                        "type": "string",
                        "enum": ["basic_inquiry", "technical_support", "billing_issue", "complaint", "escalation", "vip_support"],
                        "description": "Type of interaction"
                    }
                },
                "required": ["tier", "customer_message", "agent_response", "interaction_type"]
            }
        ),
        Tool(
            name="suggest_improvements",
            description="Suggest improvements for agent responses based on best practices",
            inputSchema={
                "type": "object",
                "properties": {
                    "tier": {
                        "type": "string",
                        "enum": ["tier_1", "tier_2", "tier_3", "supervisor", "floor_manager"],
                        "description": "Agent tier level"
                    },
                    "current_response": {
                        "type": "string",
                        "description": "Current agent response"
                    },
                    "evaluation_feedback": {
                        "type": "object",
                        "description": "Quality evaluation feedback",
                        "properties": {
                            "score": {"type": "number"},
                            "areas_for_improvement": {"type": "array", "items": {"type": "string"}},
                            "strengths": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "required": ["tier", "current_response"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "generate_agent_prompt":
        tier = arguments.get("tier")
        interaction_type = arguments.get("interaction_type")
        customer_message = arguments.get("customer_message")
        additional_context = arguments.get("additional_context")
        
        result = prompting_mcp.generate_prompt(
            tier, interaction_type, customer_message, additional_context
        )
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "check_escalation_need":
        tier = arguments.get("tier")
        customer_message = arguments.get("customer_message")
        interaction_context = arguments.get("interaction_context", {})
        
        result = prompting_mcp.check_escalation(
            tier, customer_message, interaction_context
        )
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_agent_capabilities":
        tier = arguments.get("tier")
        
        result = prompting_mcp.get_agent_capabilities(tier)
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "evaluate_response_quality":
        tier = arguments.get("tier")
        customer_message = arguments.get("customer_message")
        agent_response = arguments.get("agent_response")
        interaction_type = arguments.get("interaction_type")
        
        # Get quality metrics for the tier
        quality_metrics = prompting_mcp.prompting_engine.get_quality_metrics(
            AgentTier(tier)
        )
        
        # Simple evaluation logic (in a real system, this would be more sophisticated)
        evaluation = {
            "tier": tier,
            "interaction_type": interaction_type,
            "evaluation_criteria": quality_metrics["evaluation_criteria"],
            "scores": {
                "greeting_quality": 4 if "hello" in agent_response.lower() else 2,
                "problem_identification": 4 if len(agent_response) > 50 else 2,
                "solution_provision": 4 if "help" in agent_response.lower() else 2,
                "professional_tone": 4 if "please" in agent_response.lower() else 3,
                "documentation_quality": 3
            },
            "overall_score": 3.4,
            "recommendations": [
                "Ensure proper greeting and acknowledgment",
                "Provide clear solution steps",
                "Maintain professional tone throughout"
            ]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(evaluation, indent=2)
        )]
    
    elif name == "suggest_improvements":
        tier = arguments.get("tier")
        current_response = arguments.get("current_response")
        evaluation_feedback = arguments.get("evaluation_feedback", {})
        
        # Generate improvement suggestions based on tier and current response
        suggestions = {
            "tier": tier,
            "current_response_analysis": {
                "length": len(current_response),
                "tone_indicators": ["professional" if "please" in current_response.lower() else "informal"],
                "solution_indicators": ["helpful" if "help" in current_response.lower() else "unclear"]
            },
            "improvement_suggestions": [
                "Add a warm greeting to establish rapport",
                "Acknowledge the customer's specific concern",
                "Provide step-by-step solution guidance",
                "End with confirmation and follow-up offer"
            ],
            "best_practices": [
                "Use customer's name when available",
                "Provide specific timeframes for resolution",
                "Offer multiple solution options when possible",
                "Document the interaction thoroughly"
            ]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(suggestions, indent=2)
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main server function"""
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="agent-prompting-strategy",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
