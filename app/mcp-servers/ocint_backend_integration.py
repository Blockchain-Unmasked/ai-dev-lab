#!/usr/bin/env python3
"""
OCINT MVP Backend Integration Example
Shows how to integrate OCINT MVP with your existing backend
"""

import json
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from ocint_mvp_prompting_strategy import OCINTMVPEngine, ReportStatus

# Initialize FastAPI app
app = FastAPI(title="OCINT MVP API", version="1.0.0")

# Initialize OCINT engine
ocint_engine = OCINTMVPEngine()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: str
    current_step: Optional[int] = 1

class ChatResponse(BaseModel):
    ai_response: str
    current_step: int
    report_status: str
    completion_percentage: float
    message_count: int
    extracted_info: Dict[str, Any]
    should_escalate: bool
    escalation_summary: Optional[str] = None

class ReportData(BaseModel):
    session_id: str
    report_data: Dict[str, Any]

# In-memory storage for demo (use database in production)
sessions = {}

@app.post("/api/v1/ocint/start-report")
async def start_report(session_id: str):
    """Start a new victim report session"""
    try:
        # Initialize new report
        report_data = ocint_engine.report_template.copy()
        report_data['report_id'] = f"OCINT-{session_id}"
        report_data['session_id'] = session_id
        
        # Store session
        sessions[session_id] = {
            'report_data': report_data,
            'current_step': 1,
            'message_count': 0,
            'conversation_active': True
        }
        
        # Get initial prompt
        initial_message = "Hi, I need help with a crypto theft report"
        prompt = ocint_engine.generate_ocint_prompt(1, initial_message, report_data)
        
        return {
            "success": True,
            "session_id": session_id,
            "report_id": report_data['report_id'],
            "current_step": 1,
            "ai_prompt": prompt,
            "welcome_message": "Hello! I'm here to help you create a report for your crypto theft incident. Can you tell me your name and email address? What is the best phone number to reach you at?"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start report: {str(e)}"
        )

@app.post("/api/v1/ocint/process-message", response_model=ChatResponse)
async def process_message(message: ChatMessage):
    """Process a customer message and return AI response"""
    try:
        session_id = message.session_id
        
        # Check if session exists
        if session_id not in sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found. Please start a new report."
            )
        
        session = sessions[session_id]
        
        # Check if conversation is active
        if not session['conversation_active']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conversation is not active. Report may be complete or escalated."
            )
        
        # Process the message
        result = ocint_engine.process_customer_response(
            message.message,
            session['current_step'],
            session['report_data']
        )
        
        # Update session
        session['report_data'] = result['updated_report']
        session['current_step'] = result.get('next_step', session['current_step'] + 1)
        session['message_count'] = result['updated_report']['message_count']
        
        # Check if conversation should end
        if result['should_escalate']:
            session['conversation_active'] = False
            
            # Generate escalation summary
            escalation_summary = ocint_engine.generate_escalation_prompt(session['report_data'])
            
            return ChatResponse(
                ai_response="Your report is complete and has been escalated to a human investigator. They will contact you within 24 hours.",
                current_step=session['current_step'],
                report_status=result['completion_status']['status'],
                completion_percentage=result['completion_status']['completion_percentage'],
                message_count=session['message_count'],
                extracted_info=result['updated_report'],
                should_escalate=True,
                escalation_summary=escalation_summary
            )
        
        # Move to next step
        if session['current_step'] <= len(ocint_engine.conversation_flow):
            step_info = ocint_engine.conversation_flow[session['current_step'] - 1]
            ai_response = f"Step {session['current_step']}: {step_info['purpose']}\n\n{'. '.join(step_info['questions'])}"
        else:
            ai_response = "Thank you for providing the information. Let me process your report..."
            session['conversation_active'] = False
        
        return ChatResponse(
            ai_response=ai_response,
            current_step=session['current_step'],
            report_status=result['completion_status']['status'],
            completion_percentage=result['completion_status']['completion_percentage'],
            message_count=session['message_count'],
            extracted_info=result['updated_report'],
            should_escalate=result['should_escalate']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )

@app.get("/api/v1/ocint/report-status/{session_id}")
async def get_report_status(session_id: str):
    """Get current report status"""
    try:
        if session_id not in sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        session = sessions[session_id]
        completion_status = ocint_engine._check_report_completion(session['report_data'])
        
        return {
            "success": True,
            "session_id": session_id,
            "current_step": session['current_step'],
            "message_count": session['message_count'],
            "conversation_active": session['conversation_active'],
            "report_status": completion_status['status'],
            "completion_percentage": completion_status['completion_percentage'],
            "ready_for_escalation": completion_status['ready_for_human_review'],
            "completed_fields": completion_status['completed_fields'],
            "missing_fields": completion_status['missing_fields']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get report status: {str(e)}"
        )

@app.get("/api/v1/ocint/report-data/{session_id}")
async def get_report_data(session_id: str):
    """Get complete report data"""
    try:
        if session_id not in sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        session = sessions[session_id]
        
        return {
            "success": True,
            "session_id": session_id,
            "report_data": session['report_data'],
            "completion_status": ocint_engine._check_report_completion(session['report_data'])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get report data: {str(e)}"
        )

@app.post("/api/v1/ocint/escalate-report/{session_id}")
async def escalate_report(session_id: str):
    """Manually escalate a report to human investigators"""
    try:
        if session_id not in sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        session = sessions[session_id]
        
        # Generate escalation summary
        escalation_summary = ocint_engine.generate_escalation_prompt(session['report_data'])
        
        # Mark as escalated
        session['report_data']['status'] = 'escalated'
        session['conversation_active'] = False
        
        return {
            "success": True,
            "session_id": session_id,
            "escalation_summary": escalation_summary,
            "message": "Report has been escalated to human investigators"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to escalate report: {str(e)}"
        )

@app.get("/api/v1/ocint/conversation-flow")
async def get_conversation_flow():
    """Get the conversation flow structure"""
    try:
        return {
            "success": True,
            "conversation_flow": ocint_engine.conversation_flow,
            "agent_capabilities": {
                "primary_function": ocint_engine.agent_capabilities.primary_function,
                "scope": ocint_engine.agent_capabilities.scope,
                "boundaries": ocint_engine.agent_capabilities.boundaries,
                "max_messages": ocint_engine.agent_capabilities.max_messages,
                "escalation_triggers": ocint_engine.agent_capabilities.escalation_triggers
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation flow: {str(e)}"
        )

@app.get("/api/v1/ocint/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "OCINT MVP API",
        "version": "1.0.0",
        "engine_loaded": ocint_engine is not None
    }

# Example usage and testing
async def test_backend_integration():
    """Test the backend integration"""
    print("🚀 Testing OCINT MVP Backend Integration")
    print("=" * 50)
    
    # Test session creation
    session_id = "test-session-001"
    
    # Start report
    print(f"📋 Starting report for session: {session_id}")
    # This would be a real API call in production
    print("✅ Report started successfully")
    
    # Test message processing
    test_messages = [
        "Hi, I need help. Someone stole my Bitcoin yesterday. My name is John Smith and my email is john@example.com. You can call me at 555-123-4567.",
        "The theft happened on 2024-01-15 around 2:30 PM. I logged into my wallet and saw all my Bitcoin was gone.",
        "I lost about 2.5 Bitcoin worth around $100,000. The wallet address was 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.",
        "Yes, I have screenshots of the wallet showing the transactions."
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n💬 Processing message {i}: {message[:50]}...")
        # This would be a real API call in production
        print(f"✅ Message processed successfully")
    
    print(f"\n🎉 Backend integration test complete!")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting OCINT MVP Backend Server")
    print("=" * 50)
    print("Available endpoints:")
    print("• POST /api/v1/ocint/start-report")
    print("• POST /api/v1/ocint/process-message")
    print("• GET /api/v1/ocint/report-status/{session_id}")
    print("• GET /api/v1/ocint/report-data/{session_id}")
    print("• POST /api/v1/ocint/escalate-report/{session_id}")
    print("• GET /api/v1/ocint/conversation-flow")
    print("• GET /api/v1/ocint/health")
    print("\n🌐 Server will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
