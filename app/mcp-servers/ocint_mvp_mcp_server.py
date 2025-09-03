#!/usr/bin/env python3
"""
OCINT MVP MCP Server - Crypto Theft Victim Report Creation
Focused MCP server for OCINT's MVP workflow
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

from ocint_mvp_prompting_strategy import OCINTMVPEngine, ReportStatus, ReportSection

# Initialize the MCP server
app = Server("ocint-mvp-agent")

# Initialize the OCINT MVP engine
ocint_engine = OCINTMVPEngine()

@app.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="ocint://mvp/agent-capabilities",
            name="OCINT Agent Capabilities",
            description="Tier 1 agent capabilities and scope for crypto theft victim reports",
            mimeType="application/json"
        ),
        Resource(
            uri="ocint://mvp/report-template",
            name="Victim Report Template",
            description="Template structure for crypto theft victim reports",
            mimeType="application/json"
        ),
        Resource(
            uri="ocint://mvp/conversation-flow",
            name="Conversation Flow",
            description="Step-by-step conversation flow for efficient report creation",
            mimeType="application/json"
        ),
        Resource(
            uri="ocint://mvp/escalation-criteria",
            name="Escalation Criteria",
            description="Criteria for escalating reports to human investigators",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read specific resources"""
    if uri == "ocint://mvp/agent-capabilities":
        capabilities = {
            "primary_function": ocint_engine.agent_capabilities.primary_function,
            "scope": ocint_engine.agent_capabilities.scope,
            "boundaries": ocint_engine.agent_capabilities.boundaries,
            "max_messages": ocint_engine.agent_capabilities.max_messages,
            "escalation_triggers": ocint_engine.agent_capabilities.escalation_triggers,
            "required_fields": ocint_engine.agent_capabilities.required_fields
        }
        return json.dumps(capabilities, indent=2)
    
    elif uri == "ocint://mvp/report-template":
        return json.dumps(ocint_engine.report_template, indent=2)
    
    elif uri == "ocint://mvp/conversation-flow":
        return json.dumps(ocint_engine.conversation_flow, indent=2)
    
    elif uri == "ocint://mvp/escalation-criteria":
        criteria = {
            "completion_threshold": 0.8,
            "max_messages": ocint_engine.agent_capabilities.max_messages,
            "escalation_triggers": ocint_engine.agent_capabilities.escalation_triggers,
            "required_fields": ocint_engine.agent_capabilities.required_fields
        }
        return json.dumps(criteria, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="generate_ocint_prompt",
            description="Generate a focused prompt for OCINT Tier 1 agent based on conversation step and customer message",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_step": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Current conversation step (1-5)"
                    },
                    "customer_message": {
                        "type": "string",
                        "description": "The customer's message"
                    },
                    "report_data": {
                        "type": "object",
                        "description": "Current report data",
                        "properties": {
                            "victim_info": {"type": "object"},
                            "incident_details": {"type": "object"},
                            "transaction_info": {"type": "object"},
                            "evidence": {"type": "object"},
                            "status": {"type": "string"},
                            "message_count": {"type": "integer"}
                        }
                    }
                },
                "required": ["current_step", "customer_message", "report_data"]
            }
        ),
        Tool(
            name="process_customer_response",
            description="Process customer response and extract information for the victim report",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_message": {
                        "type": "string",
                        "description": "Customer's response message"
                    },
                    "current_step": {
                        "type": "integer",
                        "description": "Current conversation step"
                    },
                    "report_data": {
                        "type": "object",
                        "description": "Current report data"
                    }
                },
                "required": ["customer_message", "current_step", "report_data"]
            }
        ),
        Tool(
            name="check_report_completion",
            description="Check if the victim report is complete enough for human review",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_data": {
                        "type": "object",
                        "description": "Current report data to check"
                    }
                },
                "required": ["report_data"]
            }
        ),
        Tool(
            name="generate_escalation_summary",
            description="Generate summary for escalating report to human investigator",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_data": {
                        "type": "object",
                        "description": "Complete report data"
                    }
                },
                "required": ["report_data"]
            }
        ),
        Tool(
            name="validate_report_data",
            description="Validate extracted report data for completeness and accuracy",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_data": {
                        "type": "object",
                        "description": "Report data to validate"
                    }
                },
                "required": ["report_data"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "generate_ocint_prompt":
        current_step = arguments.get("current_step")
        customer_message = arguments.get("customer_message")
        report_data = arguments.get("report_data", {})
        
        try:
            prompt = ocint_engine.generate_ocint_prompt(
                current_step, customer_message, report_data
            )
            
            result = {
                "success": True,
                "prompt": prompt,
                "current_step": current_step,
                "prompt_length": len(prompt),
                "estimated_tokens": len(prompt.split()) * 1.3
            }
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "current_step": current_step
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "process_customer_response":
        customer_message = arguments.get("customer_message")
        current_step = arguments.get("current_step")
        report_data = arguments.get("report_data", {})
        
        try:
            result = ocint_engine.process_customer_response(
                customer_message, current_step, report_data
            )
            
            result["success"] = True
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "customer_message": customer_message,
                "current_step": current_step
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "check_report_completion":
        report_data = arguments.get("report_data", {})
        
        try:
            completion_status = ocint_engine._check_report_completion(report_data)
            
            result = {
                "success": True,
                "completion_status": completion_status,
                "ready_for_escalation": completion_status['ready_for_human_review']
            }
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "generate_escalation_summary":
        report_data = arguments.get("report_data", {})
        
        try:
            escalation_prompt = ocint_engine.generate_escalation_prompt(report_data)
            completion_status = ocint_engine._check_report_completion(report_data)
            
            result = {
                "success": True,
                "escalation_summary": escalation_prompt,
                "completion_status": completion_status,
                "report_id": report_data.get('report_id', 'PENDING'),
                "message_count": report_data.get('message_count', 0)
            }
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "validate_report_data":
        report_data = arguments.get("report_data", {})
        
        try:
            completion_status = ocint_engine._check_report_completion(report_data)
            
            # Additional validation logic
            validation_results = {
                "required_fields_check": {},
                "data_quality_check": {},
                "completeness_check": completion_status
            }
            
            # Check each required field
            for field in ocint_engine.agent_capabilities.required_fields:
                has_value = ocint_engine._field_has_value(report_data, field)
                validation_results["required_fields_check"][field] = {
                    "present": has_value,
                    "status": "valid" if has_value else "missing"
                }
            
            # Data quality checks
            validation_results["data_quality_check"] = {
                "email_format": "valid" if "@" in str(report_data.get('victim_info', {}).get('victim_email', '')) else "invalid",
                "phone_format": "valid" if len(str(report_data.get('victim_info', {}).get('victim_phone', ''))) >= 10 else "invalid",
                "amount_format": "valid" if any(char.isdigit() for char in str(report_data.get('transaction_info', {}).get('amount_stolen', ''))) else "invalid"
            }
            
            result = {
                "success": True,
                "validation_results": validation_results,
                "overall_valid": completion_status['completion_percentage'] >= 0.8
            }
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
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
                server_name="ocint-mvp-agent",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
