#!/usr/bin/env python3
"""
OCINT MVP - Crypto Theft Investigation Onboarding Agent
Focused Tier 1 agent for victim report creation and validation
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class ReportStatus(Enum):
    """Status of victim report creation"""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    VALIDATED = "validated"
    ESCALATED = "escalated"

class ReportSection(Enum):
    """Sections of the victim report"""
    VICTIM_INFO = "victim_info"
    INCIDENT_DETAILS = "incident_details"
    TRANSACTION_INFO = "transaction_info"
    EVIDENCE = "evidence"
    TIMELINE = "timeline"

@dataclass
class VictimReport:
    """Victim report data structure"""
    report_id: str
    victim_info: Dict[str, Any]
    incident_details: Dict[str, Any]
    transaction_info: Dict[str, Any]
    evidence: Dict[str, Any]
    timeline: Dict[str, Any]
    status: ReportStatus
    message_count: int
    created_at: str

@dataclass
class OCINTAgentCapabilities:
    """OCINT Tier 1 agent capabilities"""
    primary_function: str
    scope: List[str]
    boundaries: List[str]
    max_messages: int
    escalation_triggers: List[str]
    required_fields: List[str]

class OCINTMVPEngine:
    """
    OCINT MVP Agent Engine - Focused on crypto theft victim report creation
    """
    
    def __init__(self):
        self.agent_capabilities = self._build_ocint_capabilities()
        self.report_template = self._build_report_template()
        self.conversation_flow = self._build_conversation_flow()
    
    def _build_ocint_capabilities(self) -> OCINTAgentCapabilities:
        """Build OCINT-specific agent capabilities"""
        return OCINTAgentCapabilities(
            primary_function="Crypto theft victim report creation and validation",
            scope=[
                "Collect victim personal information",
                "Gather incident details and timeline",
                "Collect transaction information",
                "Document evidence provided",
                "Validate report completeness",
                "Escalate complete reports to human review"
            ],
            boundaries=[
                "DO NOT attempt to trace transactions",
                "DO NOT provide legal advice",
                "DO NOT investigate the crime",
                "DO NOT contact exchanges or services",
                "DO NOT provide recovery estimates",
                "DO NOT handle payment or billing",
                "ONLY focus on report creation"
            ],
            max_messages=8,  # Keep interactions minimal
            escalation_triggers=[
                "Report is complete and validated",
                "Victim requests human assistance",
                "Complex legal questions arise",
                "Technical issues beyond report creation",
                "Maximum message limit reached"
            ],
            required_fields=[
                "victim_name",
                "victim_email", 
                "victim_phone",
                "incident_date",
                "incident_description",
                "crypto_type",
                "amount_stolen",
                "wallet_addresses",
                "transaction_hashes",
                "evidence_files"
            ]
        )
    
    def _build_report_template(self) -> Dict[str, Any]:
        """Build victim report template"""
        return {
            "report_id": "",
            "victim_info": {
                "name": "",
                "email": "",
                "phone": "",
                "country": "",
                "timezone": ""
            },
            "incident_details": {
                "date": "",
                "time": "",
                "description": "",
                "how_discovered": "",
                "suspected_method": ""
            },
            "transaction_info": {
                "crypto_type": "",
                "amount_stolen": "",
                "wallet_addresses": [],
                "transaction_hashes": [],
                "exchange_used": "",
                "exchange_account": ""
            },
            "evidence": {
                "screenshots": [],
                "transaction_records": [],
                "communication_logs": [],
                "other_documents": []
            },
            "timeline": {
                "discovery_time": "",
                "report_time": "",
                "key_events": []
            },
            "status": "incomplete",
            "message_count": 0,
            "created_at": ""
        }
    
    def _build_conversation_flow(self) -> List[Dict[str, Any]]:
        """Build efficient conversation flow to minimize interactions"""
        return [
            {
                "step": 1,
                "purpose": "Initial greeting and report initiation",
                "questions": [
                    "Hello, I'm here to help you create a report for your crypto theft incident. Can you tell me your name and email address?",
                    "What is the best phone number to reach you at?"
                ],
                "collects": ["victim_name", "victim_email", "victim_phone"]
            },
            {
                "step": 2,
                "purpose": "Incident details collection",
                "questions": [
                    "When did the theft occur? Please provide the date and approximate time.",
                    "Can you briefly describe what happened? How did you discover the theft?"
                ],
                "collects": ["incident_date", "incident_time", "incident_description", "how_discovered"]
            },
            {
                "step": 3,
                "purpose": "Transaction information",
                "questions": [
                    "What type of cryptocurrency was stolen and approximately how much?",
                    "Do you have the wallet addresses involved? Please provide them.",
                    "Do you have any transaction hash IDs from the theft?"
                ],
                "collects": ["crypto_type", "amount_stolen", "wallet_addresses", "transaction_hashes"]
            },
            {
                "step": 4,
                "purpose": "Evidence and validation",
                "questions": [
                    "Do you have any screenshots, transaction records, or other evidence you can share?",
                    "Is there anything else important about this incident I should know?"
                ],
                "collects": ["evidence_files", "additional_details"]
            },
            {
                "step": 5,
                "purpose": "Report completion and escalation",
                "questions": [
                    "I have all the information needed for your report. A human investigator will review this within 24 hours and contact you directly. Is there anything else you'd like to add?"
                ],
                "collects": ["final_confirmation"]
            }
        ]
    
    def generate_ocint_prompt(self, current_step: int, customer_message: str, 
                            report_data: Dict[str, Any]) -> str:
        """Generate focused OCINT agent prompt"""
        
        step_info = self.conversation_flow[current_step - 1] if current_step <= len(self.conversation_flow) else self.conversation_flow[-1]
        
        # Build system prompt
        system_prompt = f"""You are an AI agent specialized in crypto theft victim report creation for OCINT (Crypto Investigation Services). Your ONLY job is to help victims create comprehensive reports for human investigators to review.

## YOUR MISSION
- **Primary Function**: {self.agent_capabilities.primary_function}
- **Goal**: Create complete victim reports in {self.agent_capabilities.max_messages} messages or less
- **Current Step**: {current_step} of {len(self.conversation_flow)}

## YOUR SCOPE - ONLY DO THESE THINGS:
{self._format_list(self.agent_capabilities.scope)}

## STRICT BOUNDARIES - NEVER DO THESE:
{self._format_list(self.agent_capabilities.boundaries)}

## CURRENT CONVERSATION STEP
**Purpose**: {step_info['purpose']}
**Questions to Ask**: {', '.join(step_info['questions'])}
**Information to Collect**: {', '.join(step_info['collects'])}

## REPORT STATUS
**Current Status**: {report_data.get('status', 'incomplete')}
**Fields Completed**: {len([k for k, v in report_data.items() if v and k != 'status'])}/{len(self.agent_capabilities.required_fields)}
**Message Count**: {report_data.get('message_count', 0)}/{self.agent_capabilities.max_messages}

## RESPONSE GUIDELINES
1. **Be Direct**: Ask only the questions needed for this step
2. **Be Efficient**: Collect multiple pieces of information in one response
3. **Be Clear**: Explain why you need each piece of information
4. **Stay Focused**: Only discuss report creation, nothing else
5. **Be Empathetic**: Acknowledge this is a difficult situation

## ESCALATION TRIGGERS
Escalate to human investigator when:
{self._format_list(self.agent_capabilities.escalation_triggers)}

## CURRENT INTERACTION
**Customer Message**: {customer_message}

**Your Response**: Provide a focused response that collects the needed information for this step. Be efficient and empathetic."""

        return system_prompt
    
    def process_customer_response(self, customer_message: str, current_step: int, 
                                report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer response and extract information"""
        
        step_info = self.conversation_flow[current_step - 1] if current_step <= len(self.conversation_flow) else self.conversation_flow[-1]
        
        # Extract information based on current step
        extracted_info = {}
        
        if current_step == 1:  # Victim info
            extracted_info.update(self._extract_victim_info(customer_message))
        elif current_step == 2:  # Incident details
            extracted_info.update(self._extract_incident_details(customer_message))
        elif current_step == 3:  # Transaction info
            extracted_info.update(self._extract_transaction_info(customer_message))
        elif current_step == 4:  # Evidence
            extracted_info.update(self._extract_evidence_info(customer_message))
        
        # Update report data
        updated_report = {**report_data, **extracted_info}
        updated_report['message_count'] = report_data.get('message_count', 0) + 1
        
        # Check if report is complete
        completion_status = self._check_report_completion(updated_report)
        updated_report['status'] = completion_status['status']
        
        # Determine next step
        next_step = current_step + 1 if completion_status['status'] == 'incomplete' else None
        
        return {
            'updated_report': updated_report,
            'next_step': next_step,
            'completion_status': completion_status,
            'should_escalate': completion_status['status'] in ['complete', 'escalated']
        }
    
    def _extract_victim_info(self, message: str) -> Dict[str, Any]:
        """Extract victim information from message"""
        info = {}
        
        # Simple extraction (in production, use more sophisticated NLP)
        if '@' in message:
            import re
            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
            if email_match:
                info['victim_email'] = email_match.group(0)
        
        # Look for phone number patterns
        import re
        phone_match = re.search(r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})', message)
        if phone_match:
            info['victim_phone'] = phone_match.group(0)
        
        # Extract name (look for "My name is" or "I'm" patterns)
        import re
        name_patterns = [
            r'my name is ([A-Z][a-z]+ [A-Z][a-z]+)',
            r"i'm ([A-Z][a-z]+ [A-Z][a-z]+)",
            r"i am ([A-Z][a-z]+ [A-Z][a-z]+)",
            r'name is ([A-Z][a-z]+ [A-Z][a-z]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                info['victim_name'] = match.group(1)
                break
        
        return info
    
    def _extract_incident_details(self, message: str) -> Dict[str, Any]:
        """Extract incident details from message"""
        info = {}
        
        # Look for date patterns
        import re
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{1,2}-\d{1,2}',
            r'\d{1,2}-\d{1,2}-\d{4}'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, message)
            if match:
                info['incident_date'] = match.group(0)
                break
        
        # Look for time patterns
        time_match = re.search(r'\d{1,2}:\d{2}\s*(AM|PM|am|pm)?', message)
        if time_match:
            info['incident_time'] = time_match.group(0)
        
        # Extract description (rest of the message)
        info['incident_description'] = message
        
        return info
    
    def _extract_transaction_info(self, message: str) -> Dict[str, Any]:
        """Extract transaction information from message"""
        info = {}
        
        # Look for crypto types
        crypto_types = ['bitcoin', 'btc', 'ethereum', 'eth', 'litecoin', 'ltc', 'dogecoin', 'doge']
        for crypto in crypto_types:
            if crypto.lower() in message.lower():
                info['crypto_type'] = crypto.upper()
                break
        
        # Look for amounts
        import re
        amount_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', message)
        if amount_match:
            info['amount_stolen'] = amount_match.group(1)
        
        # Look for wallet addresses (basic pattern)
        wallet_match = re.search(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40}', message)
        if wallet_match:
            info['wallet_addresses'] = [wallet_match.group(0)]
        
        # Look for transaction hashes
        tx_match = re.search(r'[a-fA-F0-9]{64}', message)
        if tx_match:
            info['transaction_hashes'] = [tx_match.group(0)]
        
        return info
    
    def _extract_evidence_info(self, message: str) -> Dict[str, Any]:
        """Extract evidence information from message"""
        info = {}
        
        # Look for file references
        if any(word in message.lower() for word in ['screenshot', 'image', 'photo', 'picture']):
            info['evidence_files'] = ['screenshots mentioned']
        
        if any(word in message.lower() for word in ['transaction', 'record', 'receipt']):
            info['evidence_files'] = info.get('evidence_files', []) + ['transaction records mentioned']
        
        return info
    
    def _check_report_completion(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if report is complete enough for human review"""
        
        required_fields = self.agent_capabilities.required_fields
        completed_fields = []
        missing_fields = []
        
        for field in required_fields:
            if self._field_has_value(report_data, field):
                completed_fields.append(field)
            else:
                missing_fields.append(field)
        
        completion_percentage = len(completed_fields) / len(required_fields)
        
        # Determine status
        if completion_percentage >= 0.8:  # 80% complete
            status = 'complete'
        elif report_data.get('message_count', 0) >= self.agent_capabilities.max_messages:
            status = 'escalated'  # Force escalation at message limit
        else:
            status = 'incomplete'
        
        return {
            'status': status,
            'completion_percentage': completion_percentage,
            'completed_fields': completed_fields,
            'missing_fields': missing_fields,
            'ready_for_human_review': status in ['complete', 'escalated']
        }
    
    def _field_has_value(self, report_data: Dict[str, Any], field: str) -> bool:
        """Check if a field has a meaningful value"""
        # Navigate nested structure
        if field in ['victim_name', 'victim_email', 'victim_phone']:
            return bool(report_data.get('victim_info', {}).get(field))
        elif field in ['incident_date', 'incident_description']:
            return bool(report_data.get('incident_details', {}).get(field))
        elif field in ['crypto_type', 'amount_stolen', 'wallet_addresses']:
            return bool(report_data.get('transaction_info', {}).get(field))
        elif field in ['evidence_files']:
            return bool(report_data.get('evidence', {}).get(field))
        else:
            return bool(report_data.get(field))
    
    def _format_list(self, items: List[str]) -> str:
        """Format list items for prompt readability"""
        return "\n".join([f"- {item}" for item in items])
    
    def generate_escalation_prompt(self, report_data: Dict[str, Any]) -> str:
        """Generate prompt for escalating to human investigator"""
        
        completion_status = self._check_report_completion(report_data)
        
        return f"""## ESCALATION TO HUMAN INVESTIGATOR

**Report ID**: {report_data.get('report_id', 'PENDING')}
**Status**: {completion_status['status']}
**Completion**: {completion_status['completion_percentage']:.1%}
**Message Count**: {report_data.get('message_count', 0)}/{self.agent_capabilities.max_messages}

## REPORT SUMMARY
**Victim**: {report_data.get('victim_info', {}).get('victim_name', 'Not provided')}
**Email**: {report_data.get('victim_info', {}).get('victim_email', 'Not provided')}
**Phone**: {report_data.get('victim_info', {}).get('victim_phone', 'Not provided')}
**Incident Date**: {report_data.get('incident_details', {}).get('incident_date', 'Not provided')}
**Crypto Type**: {report_data.get('transaction_info', {}).get('crypto_type', 'Not provided')}
**Amount**: {report_data.get('transaction_info', {}).get('amount_stolen', 'Not provided')}

## COMPLETED FIELDS
{self._format_list(completion_status['completed_fields'])}

## MISSING FIELDS
{self._format_list(completion_status['missing_fields'])}

## NEXT STEPS FOR HUMAN INVESTIGATOR
1. Review report completeness
2. Contact victim for missing information if needed
3. Validate the incident details
4. Begin investigation process
5. Provide victim with case number and timeline

**Ready for human review**: {completion_status['ready_for_human_review']}"""

# Example usage and testing
if __name__ == "__main__":
    # Initialize OCINT MVP engine
    engine = OCINTMVPEngine()
    
    # Test scenario
    print("🚀 OCINT MVP - Crypto Theft Victim Report Creation")
    print("=" * 60)
    
    # Simulate conversation
    report_data = engine.report_template.copy()
    current_step = 1
    
    # Step 1: Initial contact
    customer_message = "Hi, I need help. Someone stole my Bitcoin yesterday. My name is John Smith and my email is john@example.com. You can call me at 555-123-4567."
    
    print(f"\n📋 Step {current_step}: Initial Contact")
    print(f"Customer: {customer_message}")
    
    # Generate prompt
    prompt = engine.generate_ocint_prompt(current_step, customer_message, report_data)
    print(f"\n🤖 Agent Prompt Generated ({len(prompt)} characters)")
    
    # Process response
    result = engine.process_customer_response(customer_message, current_step, report_data)
    report_data = result['updated_report']
    
    print(f"✅ Extracted Info: {result['updated_report']['victim_info']}")
    print(f"📊 Report Status: {result['completion_status']['status']}")
    print(f"📈 Completion: {result['completion_status']['completion_percentage']:.1%}")
    
    # Step 2: Incident details
    current_step = 2
    customer_message = "The theft happened on 2024-01-15 around 2:30 PM. I logged into my wallet and saw all my Bitcoin was gone. I think someone hacked my computer."
    
    print(f"\n📋 Step {current_step}: Incident Details")
    print(f"Customer: {customer_message}")
    
    result = engine.process_customer_response(customer_message, current_step, report_data)
    report_data = result['updated_report']
    
    print(f"✅ Extracted Info: {result['updated_report']['incident_details']}")
    print(f"📊 Report Status: {result['completion_status']['status']}")
    print(f"📈 Completion: {result['completion_status']['completion_percentage']:.1%}")
    
    # Step 3: Transaction info
    current_step = 3
    customer_message = "I lost about 2.5 Bitcoin worth around $100,000. The wallet address was 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and the transaction hash is abc123def456..."
    
    print(f"\n📋 Step {current_step}: Transaction Info")
    print(f"Customer: {customer_message}")
    
    result = engine.process_customer_response(customer_message, current_step, report_data)
    report_data = result['updated_report']
    
    print(f"✅ Extracted Info: {result['updated_report']['transaction_info']}")
    print(f"📊 Report Status: {result['completion_status']['status']}")
    print(f"📈 Completion: {result['completion_status']['completion_percentage']:.1%}")
    
    # Check if ready for escalation
    if result['should_escalate']:
        print(f"\n🚨 READY FOR ESCALATION!")
        escalation_prompt = engine.generate_escalation_prompt(report_data)
        print(f"\n📋 Escalation Summary:")
        print(escalation_prompt)
    
    print(f"\n🎉 OCINT MVP Test Complete!")
    print(f"✅ Report created in {report_data['message_count']} messages")
    print(f"✅ Completion rate: {result['completion_status']['completion_percentage']:.1%}")
    print(f"✅ Ready for human review: {result['completion_status']['ready_for_human_review']}")
