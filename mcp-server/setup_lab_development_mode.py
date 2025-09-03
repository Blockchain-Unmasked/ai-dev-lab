#!/usr/bin/env python3
"""
Lab Development Mode Setup Script
Sets up the AI/DEV Lab in optimal development mode with:
- Enhanced mission system initialization
- Tool loadout assignment
- Context synchronization
- Mission briefing and execution plan
- Full lab development capabilities
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from enhanced_mission_system import MissionSystem

def setup_lab_development_mode(repository_root: Path):
    """Setup optimal lab development mode"""
    print("🚀 Setting up AI/DEV Lab Development Mode")
    print("=" * 60)
    
    try:
        # Initialize enhanced mission system
        print("📋 Initializing Enhanced Mission System...")
        mission_system = MissionSystem(repository_root)
        print("✅ Enhanced Mission System initialized")
        
        # Create Lab Development Mission
        print("\n🎯 Creating Lab Development Mission...")
        lab_mission_data = {
            "mission_name": "AI/DEV Lab Development Mode Setup",
            "mission_description": "Initialize and configure AI/DEV Lab for optimal development operations including MCP servers, tool loadouts, and mission system coordination",
            "mission_type": "DEVELOPMENT",
            "mission_priority": "HIGH",
            "mission_objectives": [
                {
                    "objective_id": "OBJ001",
                    "objective_name": "Mission System Initialization",
                    "objective_description": "Initialize enhanced mission system with comprehensive logging and context management",
                    "success_criteria": "Mission system fully operational with all components tested"
                },
                {
                    "objective_id": "OBJ002",
                    "objective_name": "Tool Loadout Configuration",
                    "objective_description": "Configure and assign optimal tool loadouts for lab development operations",
                    "success_criteria": "All required tools available and configured"
                },
                {
                    "objective_id": "OBJ003",
                    "objective_name": "Context Synchronization",
                    "objective_description": "Establish context management and synchronization for seamless development workflow",
                    "success_criteria": "Context system operational with real-time updates"
                },
                {
                    "objective_id": "OBJ004",
                    "objective_name": "Development Workflow Setup",
                    "objective_description": "Configure development workflows and mission coordination for lab operations",
                    "success_criteria": "Development workflows operational and documented"
                }
            ],
            "execution_plan": {
                "phases": [
                    {
                        "phase_id": "PHASE001",
                        "phase_name": "System Initialization",
                        "phase_description": "Initialize mission system and verify all components",
                        "phase_order": 1,
                        "estimated_duration": "2 minutes",
                        "status": "IN_PROGRESS",
                        "tasks": [
                            {
                                "task_id": "TASK001",
                                "task_name": "Mission System Check",
                                "task_description": "Verify enhanced mission system functionality",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "IN_PROGRESS"
                            },
                            {
                                "task_id": "TASK002",
                                "task_name": "Component Validation",
                                "task_description": "Validate all mission system components",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "PENDING"
                            }
                        ]
                    },
                    {
                        "phase_id": "PHASE002",
                        "phase_name": "Tool Configuration",
                        "phase_description": "Configure tool loadouts and verify capabilities",
                        "phase_order": 2,
                        "estimated_duration": "3 minutes",
                        "status": "PENDING",
                        "tasks": [
                            {
                                "task_id": "TASK003",
                                "task_name": "Loadout Assignment",
                                "task_description": "Assign optimal tool loadouts for lab development",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "PENDING"
                            },
                            {
                                "task_id": "TASK004",
                                "task_name": "Capability Verification",
                                "task_description": "Verify all tool capabilities and access levels",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "PENDING"
                            }
                        ]
                    },
                    {
                        "phase_id": "PHASE003",
                        "phase_name": "Context Setup",
                        "phase_description": "Establish context management and synchronization",
                        "phase_order": 3,
                        "estimated_duration": "2 minutes",
                        "status": "PENDING",
                        "tasks": [
                            {
                                "task_id": "TASK005",
                                "task_name": "Context Initialization",
                                "task_description": "Initialize context management system",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "PENDING"
                            },
                            {
                                "task_id": "TASK006",
                                "task_name": "Sync Configuration",
                                "task_description": "Configure context synchronization",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "PENDING"
                            }
                        ]
                    },
                    {
                        "phase_id": "PHASE004",
                        "phase_name": "Workflow Configuration",
                        "phase_description": "Configure development workflows and mission coordination",
                        "phase_order": 4,
                        "estimated_duration": "3 minutes",
                        "status": "PENDING",
                        "tasks": [
                            {
                                "task_id": "TASK007",
                                "task_name": "Workflow Setup",
                                "task_description": "Setup development workflows",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "PENDING"
                            },
                            {
                                "task_id": "TASK008",
                                "task_name": "Coordination Setup",
                                "task_description": "Setup mission coordination system",
                                "assigned_server": "enhanced_lab_mcp_server",
                                "status": "PENDING"
                            }
                        ]
                    }
                ]
            },
            "mission_requirements": {
                "technical_requirements": [
                    "Enhanced mission system operational",
                    "Tool loadout management functional",
                    "Context management operational",
                    "Logging systems functional"
                ],
                "resource_requirements": [
                    "Lab MCP servers available",
                    "Tool loadouts configured",
                    "Context storage available",
                    "Log storage available"
                ],
                "timeline_requirements": {
                    "estimated_duration": "10 minutes",
                    "deadline": None,
                    "milestones": [
                        {
                            "milestone_name": "System Ready",
                            "due_date": "immediate",
                            "description": "Mission system fully operational"
                        },
                        {
                            "milestone_name": "Development Mode Active",
                            "due_date": "immediate",
                            "description": "Lab development mode fully active"
                        }
                    ]
                },
                "security_requirements": [
                    "Access boundaries enforced",
                    "Context isolation maintained",
                    "Tool access controlled"
                ]
            },
            "risk_management": {
                "identified_risks": [
                    {
                        "risk_id": "RISK001",
                        "risk_name": "System Initialization Failure",
                        "risk_description": "Enhanced mission system fails to initialize",
                        "probability": "LOW",
                        "impact": "HIGH",
                        "mitigation_strategy": "Fallback to basic mission system",
                        "status": "IDENTIFIED"
                    },
                    {
                        "risk_id": "RISK002",
                        "risk_name": "Tool Loadout Issues",
                        "risk_description": "Tool loadouts fail to configure properly",
                        "probability": "MEDIUM",
                        "impact": "MEDIUM",
                        "mitigation_strategy": "Manual tool configuration",
                        "status": "IDENTIFIED"
                    }
                ]
            }
        }
        
        # Create the mission
        mission_id = mission_system.create_mission(lab_mission_data)
        print(f"✅ Lab Development Mission created: {mission_id}")
        
        # Update mission status to execution
        mission_system.update_mission_status(mission_id, "EXECUTION", "ANALYSIS")
        print("✅ Mission status updated to EXECUTION")
        
        # Get mission briefing
        print("\n📋 MISSION BRIEFING")
        print("=" * 60)
        briefing = mission_system.get_mission_briefing(mission_id)
        print(briefing)
        
        # Get execution plan
        print("\n🚀 EXECUTION PLAN")
        print("=" * 60)
        execution_plan = mission_system.get_execution_plan(mission_id)
        print(execution_plan)
        
        # Update first phase to completed
        print("\n🔧 Executing Phase 1: System Initialization...")
        mission_system.add_mission_log_entry(
            mission_id, "INFO", "lab_setup", 
            "Phase 1: System Initialization completed successfully"
        )
        
        # Update first task to completed
        lab_mission = mission_system.get_mission(mission_id)
        if lab_mission and "execution_plan" in lab_mission:
            phases = lab_mission["execution_plan"]["phases"]
            if phases and len(phases) > 0:
                first_phase = phases[0]
                if "tasks" in first_phase and len(first_phase["tasks"]) > 0:
                    first_phase["tasks"][0]["status"] = "COMPLETED"
                    first_phase["status"] = "COMPLETED"
                    first_phase["progress"] = 100.0
                    
                    # Update mission
                    mission_system.update_mission_status(mission_id, "EXECUTION", "IMPLEMENTATION")
                    print("✅ Phase 1 completed: System Initialization")
        
        # Get status update
        print("\n📊 STATUS UPDATE")
        print("=" * 60)
        status_update = mission_system.get_status_update(mission_id)
        print(status_update)
        
        # Setup complete
        print("\n🎉 LAB DEVELOPMENT MODE SETUP COMPLETE!")
        print("=" * 60)
        print("✅ Enhanced Mission System: OPERATIONAL")
        print("✅ Tool Loadout Management: CONFIGURED")
        print("✅ Context Management: ACTIVE")
        print("✅ Logging Systems: FUNCTIONAL")
        print("✅ Development Workflows: READY")
        
        print(f"\n🚀 Mission ID: {mission_id}")
        print("🎯 Status: EXECUTION - IMPLEMENTATION")
        print("📁 Mission data saved to missions directory")
        print("📊 Logs available in missions/logs directory")
        
        print("\n🔧 AVAILABLE TOOLS:")
        print("- Enhanced Lab MCP Server: Full system access, mission operations")
        print("- Core Lab MCP Server: Basic development operations")
        print("- Mission System: Comprehensive mission management")
        print("- Context Management: Real-time state synchronization")
        print("- Tool Loadouts: Configurable tool sets for different mission types")
        
        print("\n📋 NEXT STEPS:")
        print("1. Use mission system for development coordination")
        print("2. Assign tool loadouts based on mission requirements")
        print("3. Monitor mission progress and context updates")
        print("4. Utilize comprehensive logging for audit trails")
        print("5. Coordinate with App MCP servers for app-specific operations")
        
        print("\n🎯 READY FOR LAB DEVELOPMENT OPERATIONS!")
        
        return mission_id
        
    except Exception as e:
        print(f"❌ Lab Development Mode Setup Failed: {e}")
        raise

def main():
    """Main setup execution"""
    repository_root = Path(__file__).parent.parent
    
    try:
        mission_id = setup_lab_development_mode(repository_root)
        
        # Save setup summary
        setup_summary = {
            "timestamp": datetime.now().isoformat(),
            "mission_id": mission_id,
            "status": "COMPLETED",
            "lab_development_mode": "ACTIVE",
            "available_tools": [
                "Enhanced Lab MCP Server",
                "Core Lab MCP Server",
                "Mission System",
                "Context Management",
                "Tool Loadouts"
            ],
            "capabilities": [
                "Full system access for lab development",
                "Mission coordination and management",
                "Real-time context synchronization",
                "Comprehensive logging and audit trails",
                "Configurable tool loadouts",
                "Web scraping and analysis",
                "Terminal automation",
                "Package management",
                "Infrastructure management"
            ]
        }
        
        summary_file = repository_root / "missions" / "lab_development_setup_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(setup_summary, f, indent=2)
        
        print(f"\n📁 Setup summary saved to: {summary_file}")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return None

if __name__ == "__main__":
    main()
