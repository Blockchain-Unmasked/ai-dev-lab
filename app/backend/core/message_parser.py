#!/usr/bin/env python3
"""
Message Parser using Super Auto Prompt (SAP) structure
Parses user messages into comprehensive JSON format for optimal chat guidance
"""

import json
import re
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class MessageParser:
    """Parser for user messages using SAP structure"""
    
    def __init__(self, sap_config_path: str = "agents/message-structure-sap.json"):
        self.sap_config = self._load_sap_config(sap_config_path)
        self.parsing_rules = self.sap_config.get('parsing_rules', {})
        self.workflow_mapping = self.sap_config.get('workflow_mapping', {})
        
    def _load_sap_config(self, config_path: str) -> Dict[str, Any]:
        """Load SAP configuration"""
        try:
            # Try multiple possible paths
            possible_paths = [
                config_path,
                f"app/{config_path}",
                f"../{config_path}",
                f"../../{config_path}"
            ]
            
            for path in possible_paths:
                try:
                    with open(path, 'r') as f:
                        logger.info(f"✅ Loaded SAP config from: {path}")
                        return json.load(f)
                except FileNotFoundError:
                    continue
            
            # If none of the paths work, try the original
            with open(config_path, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Failed to load SAP config from any path: {e}")
            return {}
    
    def parse_message(self, user_message: str) -> Dict[str, Any]:
        """Parse user message into structured JSON format"""
        start_time = datetime.now()
        
        # Generate unique message ID
        message_id = f"msg_{int(datetime.now().timestamp() * 1000)}"
        
        # Extract entities
        entities = self._extract_entities(user_message)
        
        # Analyze intent
        intent_analysis = self._analyze_intent(user_message, entities)
        
        # Determine message type
        message_type = self._classify_message_type(user_message, entities)
        
        # Determine urgency level
        urgency_level = self._determine_urgency(user_message)
        
        # Analyze context requirements
        context_requirements = self._analyze_context_requirements(user_message, message_type, entities)
        
        # Generate response guidance
        response_guidance = self._generate_response_guidance(message_type, intent_analysis, urgency_level)
        
        # Three-tier analysis for crypto theft
        three_tier_analysis = self._analyze_three_tier(user_message, message_type, entities)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Build structured message
        structured_message = {
            "user_message": user_message,
            "message_id": message_id,
            "timestamp": datetime.now().isoformat() + "Z",
            "message_type": message_type,
            "urgency_level": urgency_level,
            "extracted_entities": entities,
            "intent_analysis": intent_analysis,
            "context_requirements": context_requirements,
            "response_guidance": response_guidance,
            "three_tier_analysis": three_tier_analysis,
            "metadata": {
                "processing_time_ms": round(processing_time, 2),
                "confidence_scores": {
                    "message_classification": intent_analysis.get("confidence_level", 0.8),
                    "entity_extraction": self._calculate_entity_confidence(entities),
                    "intent_analysis": intent_analysis.get("confidence_level", 0.8)
                },
                "version": "1.0.0"
            }
        }
        
        return structured_message
    
    def _extract_entities(self, message: str) -> Dict[str, List[str]]:
        """Extract entities from the message"""
        message_lower = message.lower()
        
        # Extract service providers
        service_providers = []
        provider_indicators = self.parsing_rules.get('service_provider_indicators', [])
        for provider in provider_indicators:
            if provider in message_lower:
                service_providers.append(provider.title())
        
        # Extract crypto types
        crypto_types = []
        crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'litecoin', 'ltc', 'dogecoin', 'doge', 'cardano', 'ada']
        for crypto in crypto_keywords:
            if crypto in message_lower:
                crypto_types.append(crypto.upper())
        
        # Extract amounts (simple regex for numbers)
        amounts = re.findall(r'\$?[\d,]+\.?\d*\s*(?:btc|eth|usd|dollars?|coins?)?', message_lower)
        
        # Extract time references
        time_references = re.findall(r'(?:yesterday|today|tomorrow|last week|this week|last month|this month|\d{1,2}:\d{2}|\d{1,2}/\d{1,2}/\d{2,4})', message_lower)
        
        # Extract wallet addresses (basic pattern)
        wallet_addresses = re.findall(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40}', message)
        
        # Extract transaction IDs (basic pattern)
        transaction_ids = re.findall(r'[a-fA-F0-9]{64}', message)
        
        return {
            "service_providers": service_providers,
            "crypto_types": crypto_types,
            "amounts": amounts,
            "time_references": time_references,
            "wallet_addresses": wallet_addresses,
            "transaction_ids": transaction_ids
        }
    
    def _analyze_intent(self, message: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyze user intent"""
        message_lower = message.lower()
        
        # Determine primary intent
        primary_intent = "ask_question"  # default
        if any(word in message_lower for word in ['theft', 'stolen', 'hacked', 'breach']):
            primary_intent = "report_theft"
        elif any(word in message_lower for word in ['help', 'support', 'assistance']):
            primary_intent = "get_help"
        elif any(word in message_lower for word in ['issue', 'problem', 'not working']):
            primary_intent = "request_support"
        
        # Determine secondary intents
        secondary_intents = []
        if 'urgent' in message_lower or 'asap' in message_lower:
            secondary_intents.append("escalate_issue")
        if '?' in message:
            secondary_intents.append("ask_question")
        
        # Determine emotional state
        emotional_state = "calm"  # default
        emotional_indicators = self.parsing_rules.get('emotional_indicators', {})
        for emotion, indicators in emotional_indicators.items():
            if any(indicator in message_lower for indicator in indicators):
                emotional_state = emotion
                break
        
        # Calculate confidence
        confidence = 0.8
        if primary_intent == "report_theft" and entities.get("service_providers"):
            confidence = 0.95
        elif primary_intent == "get_help" and len(entities.get("service_providers", [])) > 0:
            confidence = 0.85
        
        return {
            "primary_intent": primary_intent,
            "secondary_intents": secondary_intents,
            "emotional_state": emotional_state,
            "confidence_level": confidence
        }
    
    def _classify_message_type(self, message: str, entities: Dict[str, List[str]]) -> str:
        """Classify the message type"""
        message_lower = message.lower()
        
        # Check for crypto theft indicators
        theft_indicators = self.parsing_rules.get('crypto_theft_indicators', [])
        if any(indicator in message_lower for indicator in theft_indicators):
            return "crypto_theft"
        
        # Additional crypto theft detection
        crypto_theft_phrases = [
            "stole my", "hacked", "theft", "stolen", "breach", "unauthorized",
            "someone took", "lost my", "drained", "compromised"
        ]
        crypto_terms = ["bitcoin", "btc", "ethereum", "eth", "crypto", "wallet"]
        
        if (any(phrase in message_lower for phrase in crypto_theft_phrases) and 
            any(crypto in message_lower for crypto in crypto_terms)):
            return "crypto_theft"
        
        # Check for technical issues
        if any(word in message_lower for word in ['not working', 'error', 'bug', 'issue', 'problem']):
            return "technical_issue"
        
        # Check for account help
        if any(word in message_lower for word in ['account', 'login', 'password', 'access']):
            return "account_help"
        
        # Check for billing
        if any(word in message_lower for word in ['billing', 'payment', 'charge', 'fee', 'cost']):
            return "billing"
        
        # Default to general support
        return "general_support"
    
    def _determine_urgency(self, message: str) -> str:
        """Determine urgency level"""
        message_lower = message.lower()
        
        urgency_indicators = self.parsing_rules.get('urgency_indicators', {})
        
        for level, indicators in urgency_indicators.items():
            if any(indicator in message_lower for indicator in indicators):
                return level
        
        return "medium"  # default
    
    def _analyze_context_requirements(self, message: str, message_type: str, entities: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Analyze what additional context is needed"""
        missing_information = []
        clarification_questions = []
        required_workflows = []
        
        if message_type == "crypto_theft":
            if not entities.get("amounts"):
                missing_information.append("amount_stolen")
                clarification_questions.append("What amount was stolen?")
            
            if not entities.get("time_references"):
                missing_information.append("when_theft_occurred")
                clarification_questions.append("When did this happen?")
            
            if not entities.get("transaction_ids"):
                missing_information.append("transaction_details")
                clarification_questions.append("Do you have transaction IDs or wallet addresses?")
            
            required_workflows = ["security_first", "evidence_gathering", "three_tier_reporting"]
        
        elif message_type == "technical_issue":
            clarification_questions.append("Can you describe the specific error or issue you're experiencing?")
            required_workflows = ["troubleshooting", "technical_support"]
        
        elif message_type == "general_support":
            clarification_questions.append("What specific help do you need?")
            required_workflows = ["information_gathering", "standard_support"]
        
        return {
            "missing_information": missing_information,
            "clarification_questions": clarification_questions,
            "required_workflows": required_workflows
        }
    
    def _generate_response_guidance(self, message_type: str, intent_analysis: Dict[str, Any], urgency_level: str) -> Dict[str, Any]:
        """Generate guidance for the response"""
        workflow_config = self.workflow_mapping.get(message_type, {})
        
        response_type = "information_gathering"  # default
        if message_type == "crypto_theft":
            response_type = "structured_guidance"
        elif urgency_level == "critical":
            response_type = "immediate_help"
        
        tone_guidance = workflow_config.get("tone", "professional")
        if intent_analysis.get("emotional_state") == "distressed":
            tone_guidance = "empathetic"
        elif urgency_level == "critical":
            tone_guidance = "urgent"
        
        length_guidance = workflow_config.get("length", "moderate")
        if message_type == "crypto_theft":
            length_guidance = "detailed"
        elif urgency_level == "critical":
            length_guidance = "brief"
        
        return {
            "response_type": response_type,
            "required_components": workflow_config.get("response_components", ["acknowledgment", "guidance"]),
            "tone_guidance": tone_guidance,
            "length_guidance": length_guidance
        }
    
    def _analyze_three_tier(self, message: str, message_type: str, entities: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
        """Analyze three-tier reporting requirements"""
        if message_type != "crypto_theft":
            return None
        
        service_providers = entities.get("service_providers", [])
        service_provider = service_providers[0] if service_providers else "unknown"
        
        evidence_status = "none"
        if entities.get("transaction_ids") or entities.get("wallet_addresses"):
            evidence_status = "partial"
        if entities.get("amounts") and entities.get("time_references"):
            evidence_status = "complete"
        
        return {
            "is_crypto_theft": True,
            "tier_1_leo_required": True,
            "tier_2_service_provider": service_provider,
            "tier_3_ocint_required": True,
            "evidence_status": evidence_status
        }
    
    def _calculate_entity_confidence(self, entities: Dict[str, List[str]]) -> float:
        """Calculate confidence in entity extraction"""
        total_entities = sum(len(entity_list) for entity_list in entities.values())
        if total_entities == 0:
            return 0.5
        elif total_entities >= 3:
            return 0.9
        elif total_entities >= 2:
            return 0.8
        else:
            return 0.7

# Global message parser instance
message_parser = None

def initialize_message_parser(config_path: str = "agents/message-structure-sap.json"):
    """Initialize the global message parser"""
    global message_parser
    message_parser = MessageParser(config_path)
    return message_parser

def get_message_parser() -> Optional[MessageParser]:
    """Get the global message parser instance"""
    return message_parser
