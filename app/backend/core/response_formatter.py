#!/usr/bin/env python3
"""
Response Formatter for AI Chat
Converts structured JSON responses into user-friendly format
"""

import json
import re
import logging
from typing import Dict, Any, Optional
from .chat_flow_manager import get_chat_flow_manager

logger = logging.getLogger(__name__)

class ResponseFormatter:
    """Formats AI responses for user-friendly display"""
    
    def __init__(self):
        self.supported_formats = ['structured_response', 'natural_conversational', 'json']
    
    def format_response(self, ai_response: str) -> str:
        """Format AI response for user display"""
        try:
            # Try to detect if response contains structured JSON
            if self._is_structured_response(ai_response):
                return self._format_structured_response(ai_response)
            else:
                return self._clean_natural_response(ai_response)
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return ai_response  # Return original if formatting fails
    
    def _is_structured_response(self, response: str) -> bool:
        """Check if response contains structured JSON"""
        # Look for common structured response patterns
        structured_patterns = [
            r'```structured_response',
            r'```json',
            r'{\s*"greeting"',
            r'{\s*"acknowledgment"',
            r'{\s*"immediate_security_steps"',
            r'{\s*"reporting_structure"'
        ]
        
        for pattern in structured_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return True
        return False
    
    def _format_structured_response(self, response: str) -> str:
        """Format structured JSON response into user-friendly text"""
        try:
            # Extract JSON from response
            json_match = re.search(r'```(?:structured_response|json)\s*\n?(.*?)\n?```', response, re.DOTALL | re.IGNORECASE)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                # Try to find JSON object in the response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    return self._clean_natural_response(response)
            
            # Parse JSON
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                return self._clean_natural_response(response)
            
            # Format the structured data
            return self._convert_json_to_natural_text(data)
            
        except Exception as e:
            logger.error(f"Error parsing structured response: {e}")
            return self._clean_natural_response(response)
    
    def _convert_json_to_natural_text(self, data: Dict[str, Any]) -> str:
        """Convert structured JSON to natural text"""
        formatted_parts = []
        
        # Handle greeting/acknowledgment
        if 'greeting' in data:
            formatted_parts.append(data['greeting'])
        elif 'acknowledgment' in data:
            formatted_parts.append(data['acknowledgment'])
        
        # Handle immediate security steps
        if 'immediate_security_steps' in data:
            security_data = data['immediate_security_steps']
            formatted_parts.append("\n**Immediate Security Steps:**")
            
            if isinstance(security_data, dict):
                if 'steps' in security_data:
                    for i, step in enumerate(security_data['steps'], 1):
                        if isinstance(step, dict):
                            action = step.get('action', f'Step {i}')
                            details = step.get('details', '')
                            formatted_parts.append(f"\n{i}. **{action}**")
                            if details:
                                formatted_parts.append(f"   {details}")
                        else:
                            formatted_parts.append(f"\n{i}. {step}")
                elif 'description' in security_data:
                    formatted_parts.append(f"\n{security_data['description']}")
        
        # Handle reporting structure
        if 'reporting_structure' in data or 'reporting_structure_explanation' in data:
            reporting_data = data.get('reporting_structure') or data.get('reporting_structure_explanation')
            formatted_parts.append("\n**Three-Tier Reporting Structure:**")
            
            if isinstance(reporting_data, dict):
                if 'introduction' in reporting_data:
                    formatted_parts.append(f"\n{reporting_data['introduction']}")
                
                if 'tiers' in reporting_data:
                    for tier in reporting_data['tiers']:
                        if isinstance(tier, dict):
                            name = tier.get('name', 'Unknown Tier')
                            description = tier.get('description', '')
                            formatted_parts.append(f"\n**{name}**")
                            if description:
                                formatted_parts.append(f"{description}")
        
        # Handle evidence gathering
        if 'evidence_gathering_guidance' in data:
            evidence_data = data['evidence_gathering_guidance']
            formatted_parts.append("\n**Evidence Gathering:**")
            
            if isinstance(evidence_data, dict):
                if 'details' in evidence_data:
                    formatted_parts.append(f"\n{evidence_data['details']}")
        
        # Handle realistic guidance
        if 'realistic_guidance' in data:
            formatted_parts.append(f"\n**Important Note:** {data['realistic_guidance']}")
        
        # Handle next steps
        if 'next_steps' in data:
            formatted_parts.append(f"\n**Next Steps:** {data['next_steps']}")
        
        # Join all parts
        formatted_text = '\n'.join(formatted_parts)
        
        # Clean up formatting
        formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)  # Remove excessive newlines
        formatted_text = formatted_text.strip()
        
        return formatted_text
    
    def _clean_natural_response(self, response: str) -> str:
        """Clean up natural response by removing technical formatting"""
        # Remove code blocks
        response = re.sub(r'```[^`]*```', '', response, flags=re.DOTALL)
        
        # Remove JSON objects
        response = re.sub(r'\{[^{}]*\}', '', response)
        
        # Clean up excessive whitespace
        response = re.sub(r'\n{3,}', '\n\n', response)
        response = re.sub(r'[ \t]+', ' ', response)
        
        return response.strip()
    
    def format_for_frontend(self, ai_response: str, structured_message: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format response for frontend consumption while preserving structured data"""
        # Check if we should use step-by-step flow
        if self._should_use_step_flow(structured_message):
            return self._format_step_by_step(structured_message)
        
        formatted_text = self.format_response(ai_response)
        is_structured = self._is_structured_response(ai_response)
        
        # Extract structured data if present
        structured_data = None
        if is_structured:
            structured_data = self._extract_structured_data(ai_response)
        
        return {
            "formatted_response": formatted_text,
            "original_response": ai_response,
            "is_structured": is_structured,
            "structured_data": structured_data,
            "message_context": structured_message,
            "system_metadata": self._generate_system_metadata(ai_response, structured_data, structured_message)
        }
    
    def _should_use_step_flow(self, structured_message: Optional[Dict[str, Any]]) -> bool:
        """Determine if we should use step-by-step flow"""
        if not structured_message:
            return False
        
        message_type = structured_message.get("message_type")
        return message_type in ["crypto_theft", "general_support"]
    
    def _format_step_by_step(self, structured_message: Dict[str, Any]) -> Dict[str, Any]:
        """Format response using step-by-step flow"""
        chat_flow_manager = get_chat_flow_manager()
        if not chat_flow_manager:
            # Fallback to regular formatting without recursion
            formatted_text = self.format_response("")
            return {
                "formatted_response": formatted_text,
                "original_response": "",
                "is_structured": False,
                "structured_data": None,
                "message_context": structured_message,
                "system_metadata": self._generate_system_metadata("", None, structured_message)
            }
        
        message_type = structured_message.get("message_type", "general_support")
        user_message = structured_message.get("user_message", "")
        
        # Check if user is continuing a flow
        current_step = self._get_current_step(user_message, message_type)
        
        # Get the appropriate step response
        step_data = chat_flow_manager.get_step_response(message_type, current_step, user_message)
        formatted_response = chat_flow_manager.format_step_response(step_data)
        
        return {
            "formatted_response": formatted_response,
            "original_response": "",
            "is_structured": False,
            "structured_data": step_data,
            "message_context": structured_message,
            "system_metadata": {
                "response_type": "step_by_step",
                "step_number": step_data.get("step_number", 0),
                "total_steps": step_data.get("total_steps", 0),
                "is_complete": step_data.get("is_complete", False),
                "flow_type": step_data.get("flow_type", "unknown")
            }
        }
    
    def _get_current_step(self, user_message: str, message_type: str) -> int:
        """Determine the current step based on user message"""
        chat_flow_manager = get_chat_flow_manager()
        if not chat_flow_manager:
            return 1
        
        # Check for specific step indicators
        user_lower = user_message.lower().strip()
        
        # Check for step 3 indicators first (more specific)
        if any(indicator in user_lower for indicator in [
            "transaction details", "evidence", "information ready", "have the details"
        ]):
            return 3
        
        # Check for step 2 indicators
        if any(indicator in user_lower for indicator in [
            "secured", "changed password", "enabled 2fa", "done", "finished", "ready"
        ]):
            return 2
        
        # Check for continuation/explanation requests (stay at current step)
        if any(phrase in user_lower for phrase in ["go through", "walk through", "explain", "tell me about", "each step"]):
            return 3  # Stay at final step for explanations
        
        # Check if user is continuing a flow
        if chat_flow_manager.should_continue_flow(user_message, 1, message_type):
            return 2  # Move to next step
        
        # Default to first step for new conversations
        return 1
    
    def _extract_structured_data(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract structured data from response for system use"""
        try:
            # Extract JSON from response
            json_match = re.search(r'```(?:structured_response|json)\s*\n?(.*?)\n?```', response, re.DOTALL | re.IGNORECASE)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                # Try to find JSON object in the response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    return None
            
            # Parse JSON
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
                
        except Exception as e:
            logger.error(f"Error extracting structured data: {e}")
            return None
    
    def _generate_system_metadata(self, ai_response: str, structured_data: Optional[Dict[str, Any]], structured_message: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate metadata for system use"""
        metadata = {
            "response_type": "structured" if structured_data else "natural",
            "processing_timestamp": "2025-01-26T12:00:00Z",
            "has_security_steps": False,
            "has_reporting_structure": False,
            "has_evidence_guidance": False,
            "urgency_level": "medium",
            "service_providers": [],
            "crypto_types": [],
            "workflows_triggered": []
        }
        
        # Analyze structured data for system metadata
        if structured_data:
            if 'immediate_security_steps' in structured_data:
                metadata["has_security_steps"] = True
                metadata["workflows_triggered"].append("security_first")
            
            if 'reporting_structure' in structured_data or 'reporting_structure_explanation' in structured_data:
                metadata["has_reporting_structure"] = True
                metadata["workflows_triggered"].append("three_tier_reporting")
            
            if 'evidence_gathering_guidance' in structured_data:
                metadata["has_evidence_guidance"] = True
                metadata["workflows_triggered"].append("evidence_gathering")
        
        # Extract information from structured message context
        if structured_message:
            metadata["urgency_level"] = structured_message.get("urgency_level", "medium")
            
            entities = structured_message.get("extracted_entities", {})
            metadata["service_providers"] = entities.get("service_providers", [])
            metadata["crypto_types"] = entities.get("crypto_types", [])
            
            # Add workflows from context requirements
            context_requirements = structured_message.get("context_requirements", {})
            required_workflows = context_requirements.get("required_workflows", [])
            metadata["workflows_triggered"].extend(required_workflows)
            metadata["workflows_triggered"] = list(set(metadata["workflows_triggered"]))  # Remove duplicates
        
        return metadata

# Global response formatter instance
response_formatter = None

def initialize_response_formatter():
    """Initialize the global response formatter"""
    global response_formatter
    response_formatter = ResponseFormatter()
    return response_formatter

def get_response_formatter() -> Optional[ResponseFormatter]:
    """Get the global response formatter instance"""
    return response_formatter
