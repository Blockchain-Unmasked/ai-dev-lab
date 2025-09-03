#!/usr/bin/env python3
"""
App-Specific MCP Server for AI Intake/Support Agent Demo
Provides tools and resources specific to the demo application
"""

import json
import logging
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppMCPServer:
    """MCP Server specifically for the AI Intake/Support Agent Demo"""
    
    def __init__(self):
        self.server = Server("ai-dev-lab-app")
        self.setup_capabilities()
        self.setup_handlers()
        
    def setup_capabilities(self):
        """Setup server capabilities"""
        self.server.capabilities = {
            "tools": {
                "analyze_chat_conversation": Tool(
                    name="analyze_chat_conversation",
                    description="Analyze a chat conversation for sentiment, intent, and key topics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "conversation": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "role": {"type": "string"},
                                        "content": {"type": "string"},
                                        "timestamp": {"type": "string"}
                                    }
                                }
                            }
                        },
                        "required": ["conversation"]
                    }
                ),
                "generate_response_template": Tool(
                    name="generate_response_template",
                    description="Generate a response template based on user intent and context",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_intent": {"type": "string"},
                            "context": {"type": "string"},
                            "response_type": {
                                "type": "string",
                                "enum": ["greeting", "problem_solving", "escalation", "closing"]
                            }
                        },
                        "required": ["user_intent", "context"]
                    }
                ),
                "calculate_response_metrics": Tool(
                    name="calculate_response_metrics",
                    description="Calculate response quality metrics for A/B testing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "responses": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "response_time": {"type": "number"},
                                        "user_satisfaction": {"type": "number"},
                                        "resolution_time": {"type": "number"}
                                    }
                                }
                            }
                        },
                        "required": ["responses"]
                    }
                ),
                "health": Tool(
                    name="health",
                    description="Health check endpoint - always succeeds",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            },
            "resources": {
                "chat_templates": Resource(
                    uri="app://chat-templates",
                    name="Chat Response Templates",
                    description="Predefined response templates for common scenarios",
                    mimeType="application/json"
                ),
                "qa_guidelines": Resource(
                    uri="app://qa-guidelines",
                    name="QA Guidelines",
                    description="Quality assurance guidelines for agent responses",
                    mimeType="text/markdown"
                ),
                "ab_testing_config": Resource(
                    uri="app://ab-testing-config",
                    name="A/B Testing Configuration",
                    description="Configuration for A/B testing scenarios",
                    mimeType="application/json"
                )
            },
            "prompts": {
                "customer_greeting": {
                    "name": "customer_greeting",
                    "description": "Generate a friendly greeting for new customers",
                    "arguments": {
                        "customer_name": "string",
                        "time_of_day": "string"
                    }
                },
                "problem_escalation": {
                    "name": "problem_escalation",
                    "description": "Generate escalation response for complex issues",
                    "arguments": {
                        "issue_type": "string",
                        "urgency_level": "string"
                    }
                }
            }
        }
    
    def setup_handlers(self):
        """Setup server event handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools"""
            return list(self.server.capabilities["tools"].values())
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
            """Handle tool calls"""
            logger.info(f"Tool called: {name} with args: {arguments}")
            
            if name == "analyze_chat_conversation":
                return await self.analyze_conversation(arguments)
            elif name == "generate_response_template":
                return await self.generate_template(arguments)
            elif name == "calculate_response_metrics":
                return await self.calculate_metrics(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources"""
            return list(self.server.capabilities["resources"].values())
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read resource content"""
            logger.info(f"Resource requested: {uri}")
            
            if uri == "app://chat-templates":
                return self.get_chat_templates()
            elif uri == "app://qa-guidelines":
                return self.get_qa_guidelines()
            elif uri == "app://ab-testing-config":
                return self.get_ab_testing_config()
            else:
                raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> List[Dict[str, Any]]:
            """List available prompts"""
            return list(self.server.capabilities["prompts"].values())
    
    async def analyze_conversation(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze chat conversation"""
        conversation = args["conversation"]
        
        # Simple analysis (in production, this could use AI)
        total_messages = len(conversation)
        user_messages = sum(1 for msg in conversation if msg.get("role") == "user")
        agent_messages = total_messages - user_messages
        
        # Basic sentiment analysis
        sentiment = "neutral"
        if any("thank" in msg.get("content", "").lower() for msg in conversation):
            sentiment = "positive"
        elif any("angry" in msg.get("content", "").lower() or "frustrated" in msg.get("content", "").lower() for msg in conversation):
            sentiment = "negative"
        
        return {
            "analysis": {
                "total_messages": total_messages,
                "user_messages": user_messages,
                "agent_messages": agent_messages,
                "sentiment": sentiment,
                "conversation_length": "short" if total_messages < 5 else "medium" if total_messages < 10 else "long"
            }
        }
    
    async def generate_template(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response template"""
        intent = args["user_intent"]
        context = args["context"]
        response_type = args.get("response_type", "problem_solving")
        
        templates = {
            "greeting": f"Hello! I'm here to help you with {context}. How can I assist you today?",
            "problem_solving": f"I understand you're experiencing {context}. Let me help you resolve this issue. Could you provide more details?",
            "escalation": f"This {context} issue requires special attention. I'll escalate this to our specialist team right away.",
            "closing": f"Thank you for bringing this {context} to our attention. Is there anything else I can help you with?"
        }
        
        return {
            "template": templates.get(response_type, templates["problem_solving"]),
            "response_type": response_type,
            "context": context
        }
    
    async def calculate_metrics(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate response metrics"""
        responses = args["responses"]
        
        if not responses:
            return {"metrics": "No responses to analyze"}
        
        avg_response_time = sum(r.get("response_time", 0) for r in responses) / len(responses)
        avg_satisfaction = sum(r.get("user_satisfaction", 0) for r in responses) / len(responses)
        avg_resolution_time = sum(r.get("resolution_time", 0) for r in responses) / len(responses)
        
        return {
            "metrics": {
                "average_response_time": round(avg_response_time, 2),
                "average_satisfaction": round(avg_satisfaction, 2),
                "average_resolution_time": round(avg_resolution_time, 2),
                "total_responses": len(responses)
            }
        }
    
    def get_chat_templates(self) -> str:
        """Get chat response templates"""
        return json.dumps({
            "greetings": [
                "Hello! How can I help you today?",
                "Hi there! I'm here to assist you.",
                "Welcome! What can I do for you?"
            ],
            "problem_acknowledgments": [
                "I understand your concern. Let me help you with that.",
                "I see the issue you're describing. Let me investigate.",
                "Thank you for bringing this to my attention."
            ],
            "closings": [
                "Is there anything else I can help you with?",
                "Thank you for contacting us. Have a great day!",
                "I'm glad I could help. Feel free to reach out again."
            ]
        }, indent=2)
    
    def get_qa_guidelines(self) -> str:
        """Get QA guidelines"""
        return """# Quality Assurance Guidelines

## Response Quality Standards
- **Accuracy**: Ensure all information provided is correct
- **Clarity**: Use clear, simple language
- **Empathy**: Show understanding of customer concerns
- **Efficiency**: Provide solutions in minimal steps

## Escalation Criteria
- Technical issues requiring specialist knowledge
- Customer complaints about service quality
- Requests for management intervention
- Complex billing or account issues

## Response Time Targets
- Initial response: < 30 seconds
- Problem resolution: < 5 minutes
- Escalation: < 2 minutes
"""
    
    def get_ab_testing_config(self) -> str:
        """Get A/B testing configuration"""
        return json.dumps({
            "test_scenarios": [
                {
                    "id": "response_style",
                    "name": "Response Style Testing",
                    "variants": [
                        {"id": "formal", "name": "Formal Professional"},
                        {"id": "casual", "name": "Casual Friendly"}
                    ]
                },
                {
                    "id": "response_length",
                    "name": "Response Length Testing",
                    "variants": [
                        {"id": "concise", "name": "Concise"},
                        {"id": "detailed", "name": "Detailed"}
                    ]
                }
            ],
            "metrics": ["response_time", "user_satisfaction", "resolution_rate"],
            "sample_size": 100
        }, indent=2)

async def main():
    """Main server function"""
    app_server = AppMCPServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await app_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-dev-lab-app",
                server_version="1.0.0",
                capabilities=app_server.server.capabilities
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
