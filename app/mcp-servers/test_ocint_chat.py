#!/usr/bin/env python3
"""
OCINT MVP Chat Testing Script
Interactive testing for the OCINT victim report creation chat
"""

import json
import asyncio
from pathlib import Path
from ocint_mvp_prompting_strategy import OCINTMVPEngine, ReportStatus, ReportSection

class OCINTChatTester:
    """Interactive chat tester for OCINT MVP"""
    
    def __init__(self):
        self.engine = OCINTMVPEngine()
        self.report_data = self.engine.report_template.copy()
        self.current_step = 1
        self.conversation_active = True
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("🚀 OCINT MVP - Crypto Theft Victim Report Chat Tester")
        print("=" * 60)
        print("This is an interactive test of the OCINT victim report creation chat.")
        print("You'll play the role of a crypto theft victim.")
        print("\n📋 Instructions:")
        print("- Type your responses as if you're a victim reporting a crypto theft")
        print("- The AI agent will guide you through the report creation process")
        print("- Type 'quit' to exit, 'reset' to start over, 'status' to see report status")
        print("- Type 'help' for more commands")
        print("\n🎯 Goal: Create a complete victim report in 8 messages or less")
        print("=" * 60)
    
    def display_help(self):
        """Display help information"""
        print("\n📚 Available Commands:")
        print("- 'quit' or 'exit' - Exit the chat tester")
        print("- 'reset' - Start a new report")
        print("- 'status' - Show current report status")
        print("- 'step' - Show current conversation step")
        print("- 'help' - Show this help message")
        print("- 'prompt' - Show the current AI prompt")
        print("- 'data' - Show extracted report data")
        print("\n💬 Just type normally to respond to the AI agent")
    
    def display_status(self):
        """Display current report status"""
        completion = self.engine._check_report_completion(self.report_data)
        
        print(f"\n📊 Report Status:")
        print(f"   Step: {self.current_step}/5")
        print(f"   Messages: {self.report_data.get('message_count', 0)}/8")
        print(f"   Status: {completion['status']}")
        print(f"   Completion: {completion['completion_percentage']:.1%}")
        print(f"   Ready for Escalation: {completion['ready_for_human_review']}")
        
        if completion['completed_fields']:
            print(f"   ✅ Completed: {', '.join(completion['completed_fields'])}")
        if completion['missing_fields']:
            print(f"   ❌ Missing: {', '.join(completion['missing_fields'])}")
    
    def display_step_info(self):
        """Display current step information"""
        if self.current_step <= len(self.engine.conversation_flow):
            step_info = self.engine.conversation_flow[self.current_step - 1]
            print(f"\n📋 Current Step {self.current_step}: {step_info['purpose']}")
            print(f"   Questions: {', '.join(step_info['questions'])}")
            print(f"   Collects: {', '.join(step_info['collects'])}")
        else:
            print(f"\n📋 Step {self.current_step}: Report completion and escalation")
    
    def display_prompt(self):
        """Display the current AI prompt"""
        if self.current_step <= len(self.engine.conversation_flow):
            step_info = self.engine.conversation_flow[self.current_step - 1]
            sample_message = "Hi, I need help with a crypto theft report"
            prompt = self.engine.generate_ocint_prompt(
                self.current_step, sample_message, self.report_data
            )
            print(f"\n🤖 AI Prompt (Step {self.current_step}):")
            print("-" * 40)
            print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
            print("-" * 40)
    
    def display_report_data(self):
        """Display extracted report data"""
        print(f"\n📄 Extracted Report Data:")
        print(json.dumps(self.report_data, indent=2))
    
    def reset_conversation(self):
        """Reset the conversation to start over"""
        self.report_data = self.engine.report_template.copy()
        self.current_step = 1
        self.conversation_active = True
        print("\n🔄 Conversation reset! Starting fresh...")
        self.display_status()
    
    def process_user_input(self, user_input: str):
        """Process user input and generate AI response"""
        
        # Handle special commands
        if user_input.lower() in ['quit', 'exit']:
            self.conversation_active = False
            print("\n👋 Goodbye! Thanks for testing OCINT MVP chat.")
            return
        
        elif user_input.lower() == 'reset':
            self.reset_conversation()
            return
        
        elif user_input.lower() == 'status':
            self.display_status()
            return
        
        elif user_input.lower() == 'step':
            self.display_step_info()
            return
        
        elif user_input.lower() == 'help':
            self.display_help()
            return
        
        elif user_input.lower() == 'prompt':
            self.display_prompt()
            return
        
        elif user_input.lower() == 'data':
            self.display_report_data()
            return
        
        # Process normal conversation
        if not self.conversation_active:
            print("❌ Conversation is not active. Type 'reset' to start over.")
            return
        
        # Generate AI prompt
        prompt = self.engine.generate_ocint_prompt(
            self.current_step, user_input, self.report_data
        )
        
        # Process the response
        result = self.engine.process_customer_response(
            user_input, self.current_step, self.report_data
        )
        
        # Update report data
        self.report_data = result['updated_report']
        
        # Display AI response (simulated)
        print(f"\n🤖 AI Agent Response:")
        print(f"   Step {self.current_step}: {result['completion_status']['status']}")
        print(f"   Completion: {result['completion_status']['completion_percentage']:.1%}")
        
        # Show what was extracted
        if self.current_step == 1 and self.report_data.get('victim_info'):
            print(f"   ✅ Extracted: {self.report_data['victim_info']}")
        elif self.current_step == 2 and self.report_data.get('incident_details'):
            print(f"   ✅ Extracted: {self.report_data['incident_details']}")
        elif self.current_step == 3 and self.report_data.get('transaction_info'):
            print(f"   ✅ Extracted: {self.report_data['transaction_info']}")
        elif self.current_step == 4 and self.report_data.get('evidence'):
            print(f"   ✅ Extracted: {self.report_data['evidence']}")
        
        # Check if escalation is needed
        if result['should_escalate']:
            print(f"\n🚨 ESCALATION TRIGGERED!")
            print(f"   Status: {result['completion_status']['status']}")
            print(f"   Ready for Human Review: {result['completion_status']['ready_for_human_review']}")
            
            if result['completion_status']['ready_for_human_review']:
                escalation_summary = self.engine.generate_escalation_prompt(self.report_data)
                print(f"\n📋 Escalation Summary:")
                print(escalation_summary[:300] + "..." if len(escalation_summary) > 300 else escalation_summary)
            
            self.conversation_active = False
            print(f"\n🎉 Report creation complete! Ready for human investigator review.")
            return
        
        # Move to next step
        self.current_step += 1
        if self.current_step > len(self.engine.conversation_flow):
            print(f"\n⚠️  Reached maximum conversation steps")
            self.conversation_active = False
            return
        
        # Show next step info
        if self.current_step <= len(self.engine.conversation_flow):
            step_info = self.engine.conversation_flow[self.current_step - 1]
            print(f"\n📋 Next Step {self.current_step}: {step_info['purpose']}")
            print(f"   Questions: {', '.join(step_info['questions'])}")
    
    def run_interactive_test(self):
        """Run the interactive chat test"""
        self.display_welcome()
        
        # Show initial step
        self.display_step_info()
        
        while self.conversation_active:
            try:
                # Get user input
                user_input = input(f"\n💬 You (Step {self.current_step}): ").strip()
                
                if not user_input:
                    print("❌ Please enter a response or command.")
                    continue
                
                # Process the input
                self.process_user_input(user_input)
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Type 'help' for available commands or 'reset' to start over.")

def run_quick_test():
    """Run a quick automated test"""
    print("🚀 OCINT MVP - Quick Automated Test")
    print("=" * 50)
    
    engine = OCINTMVPEngine()
    report_data = engine.report_template.copy()
    current_step = 1
    
    # Test messages
    test_messages = [
        "Hi, I need help. Someone stole my Bitcoin yesterday. My name is John Smith and my email is john@example.com. You can call me at 555-123-4567.",
        "The theft happened on 2024-01-15 around 2:30 PM. I logged into my wallet and saw all my Bitcoin was gone. I think someone hacked my computer.",
        "I lost about 2.5 Bitcoin worth around $100,000. The wallet address was 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and the transaction hash is abc123def456789...",
        "Yes, I have screenshots of the wallet showing the transactions and some emails from the exchange. I can provide those."
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n💬 Test Message {i}: {message[:60]}...")
        
        # Generate prompt
        prompt = engine.generate_ocint_prompt(current_step, message, report_data)
        
        # Process response
        result = engine.process_customer_response(message, current_step, report_data)
        report_data = result['updated_report']
        
        print(f"🤖 AI Response:")
        print(f"   Step {current_step}: {result['completion_status']['status']}")
        print(f"   Completion: {result['completion_status']['completion_percentage']:.1%}")
        print(f"   Messages: {report_data['message_count']}/8")
        
        # Show extracted info
        if current_step == 1:
            print(f"   👤 Victim Info: {report_data.get('victim_info', {})}")
        elif current_step == 2:
            print(f"   📅 Incident: {report_data.get('incident_details', {})}")
        elif current_step == 3:
            print(f"   💰 Transaction: {report_data.get('transaction_info', {})}")
        elif current_step == 4:
            print(f"   📎 Evidence: {report_data.get('evidence', {})}")
        
        # Check escalation
        if result['should_escalate']:
            print(f"\n🚨 ESCALATION TRIGGERED!")
            escalation_summary = engine.generate_escalation_prompt(report_data)
            print(f"📋 Summary: {escalation_summary[:200]}...")
            break
        
        current_step += 1
        if current_step > len(engine.conversation_flow):
            break
    
    print(f"\n🎉 Quick test complete!")
    print(f"✅ Final status: {result['completion_status']['status']}")
    print(f"✅ Completion: {result['completion_status']['completion_percentage']:.1%}")
    print(f"✅ Messages used: {report_data['message_count']}")

def main():
    """Main function"""
    print("Choose test mode:")
    print("1. Interactive chat test (recommended)")
    print("2. Quick automated test")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        tester = OCINTChatTester()
        tester.run_interactive_test()
    elif choice == "2":
        run_quick_test()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run again and select 1, 2, or 3.")

if __name__ == "__main__":
    main()
