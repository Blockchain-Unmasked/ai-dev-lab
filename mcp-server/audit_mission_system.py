#!/usr/bin/env python3
"""
Mission System Audit Script
Comprehensive audit of all mission system components including:
- Enhanced mission system functionality
- Tool loadout management
- Context management
- Logging systems
- Prompt engine
- Mission lifecycle management
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from enhanced_mission_system import MissionSystem, ToolLoadout, MissionContext

def setup_logging():
    """Setup comprehensive logging for audit"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('mission_system_audit.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def audit_mission_system(repository_root: Path):
    """Comprehensive audit of mission system"""
    logger = setup_logging()
    logger.info("🚀 Starting Mission System Audit")
    
    audit_results = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "PENDING",
        "components": {},
        "issues": [],
        "recommendations": []
    }
    
    try:
        # Initialize mission system
        logger.info("📋 Initializing Mission System")
        mission_system = MissionSystem(repository_root)
        
        # Test basic functionality
        audit_results["components"]["basic_functionality"] = test_basic_functionality(mission_system, logger)
        
        # Test tool loadout management
        audit_results["components"]["tool_loadouts"] = test_tool_loadouts(mission_system, logger)
        
        # Test context management
        audit_results["components"]["context_management"] = test_context_management(mission_system, logger)
        
        # Test mission lifecycle
        audit_results["components"]["mission_lifecycle"] = test_mission_lifecycle(mission_system, logger)
        
        # Test logging systems
        audit_results["components"]["logging_systems"] = test_logging_systems(mission_system, logger)
        
        # Test prompt engine
        audit_results["components"]["prompt_engine"] = test_prompt_engine(mission_system, logger)
        
        # Test error handling
        audit_results["components"]["error_handling"] = test_error_handling(mission_system, logger)
        
        # Test performance
        audit_results["components"]["performance"] = test_performance(mission_system, logger)
        
        # Determine overall status
        overall_status = determine_overall_status(audit_results["components"])
        audit_results["overall_status"] = overall_status
        
        # Generate recommendations
        audit_results["recommendations"] = generate_recommendations(audit_results["components"])
        
        logger.info(f"✅ Mission System Audit Complete - Overall Status: {overall_status}")
        
    except Exception as e:
        logger.error(f"❌ Mission System Audit Failed: {e}")
        audit_results["overall_status"] = "FAILED"
        audit_results["issues"].append(f"Critical error: {str(e)}")
    
    # Save audit results
    save_audit_results(audit_results, repository_root)
    
    return audit_results

def test_basic_functionality(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test basic mission system functionality"""
    logger.info("🔧 Testing Basic Functionality")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test mission creation
        logger.info("  Testing mission creation")
        mission_data = {
            "mission_name": "Audit Test Mission",
            "mission_description": "Test mission for system audit",
            "mission_type": "AUDIT",
            "mission_priority": "HIGH",
            "mission_objectives": [
                {
                    "objective_id": "OBJ001",
                    "objective_name": "System Validation",
                    "objective_description": "Validate mission system functionality",
                    "success_criteria": "All tests pass"
                }
            ],
            "execution_plan": {
                "phases": [
                    {
                        "phase_id": "PHASE001",
                        "phase_name": "Testing Phase",
                        "phase_description": "Execute system tests",
                        "phase_order": 1,
                        "estimated_duration": "5 minutes",
                        "tasks": [
                            {
                                "task_id": "TASK001",
                                "task_name": "System Test",
                                "task_description": "Test system components",
                                "assigned_server": "enhanced_lab_mcp_server"
                            }
                        ]
                    }
                ]
            }
        }
        
        mission_id = mission_system.create_mission(mission_data)
        results["tests"]["mission_creation"] = "PASSED"
        logger.info(f"    ✅ Mission created: {mission_id}")
        
        # Test mission retrieval
        logger.info("  Testing mission retrieval")
        retrieved_mission = mission_system.get_mission(mission_id)
        if retrieved_mission:
            results["tests"]["mission_retrieval"] = "PASSED"
            logger.info("    ✅ Mission retrieval successful")
        else:
            results["tests"]["mission_retrieval"] = "FAILED"
            results["issues"].append("Mission retrieval failed")
        
        # Test mission listing
        logger.info("  Testing mission listing")
        active_missions = mission_system.list_active_missions()
        if len(active_missions) > 0:
            results["tests"]["mission_listing"] = "PASSED"
            logger.info(f"    ✅ Active missions: {len(active_missions)}")
        else:
            results["tests"]["mission_listing"] = "FAILED"
            results["issues"].append("No active missions found")
        
        # Clean up test mission
        mission_system.update_mission_status(mission_id, "COMPLETED")
        logger.info("    ✅ Test mission completed")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Basic functionality test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Basic functionality error: {str(e)}")
    
    return results

def test_tool_loadouts(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test tool loadout management"""
    logger.info("🔧 Testing Tool Loadout Management")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test loadout availability
        logger.info("  Testing loadout availability")
        available_loadouts = mission_system.get_available_tool_loadouts()
        if available_loadouts:
            results["tests"]["loadout_availability"] = "PASSED"
            logger.info(f"    ✅ Available loadouts: {len(available_loadouts)}")
        else:
            results["tests"]["loadout_availability"] = "FAILED"
            results["issues"].append("No tool loadouts available")
        
        # Test loadout assignment
        if available_loadouts:
            logger.info("  Testing loadout assignment")
            test_mission_data = {
                "mission_name": "Loadout Test Mission",
                "mission_description": "Test tool loadout assignment",
                "mission_type": "DEVELOPMENT"
            }
            
            test_mission_id = mission_system.create_mission(test_mission_data)
            loadout_id = available_loadouts[0]["loadout_id"]
            
            if mission_system.assign_tool_loadout(test_mission_id, loadout_id):
                results["tests"]["loadout_assignment"] = "PASSED"
                logger.info(f"    ✅ Loadout assigned: {loadout_id}")
            else:
                results["tests"]["loadout_assignment"] = "FAILED"
                results["issues"].append("Loadout assignment failed")
            
            # Clean up
            mission_system.update_mission_status(test_mission_id, "COMPLETED")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Tool loadout test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Tool loadout error: {str(e)}")
    
    return results

def test_context_management(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test context management functionality"""
    logger.info("🔧 Testing Context Management")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test context creation
        logger.info("  Testing context creation")
        test_mission_data = {
            "mission_name": "Context Test Mission",
            "mission_description": "Test context management",
            "mission_type": "DEVELOPMENT"
        }
        
        test_mission_id = mission_system.create_mission(test_mission_data)
        
        # Check if context was created
        if test_mission_id in mission_system.mission_contexts:
            results["tests"]["context_creation"] = "PASSED"
            logger.info("    ✅ Mission context created")
        else:
            results["tests"]["context_creation"] = "FAILED"
            results["issues"].append("Mission context not created")
        
        # Test context updates
        logger.info("  Testing context updates")
        context_update = {
            "execution_state": {"current_task": "context_test"},
            "tool_states": {"test_tool": "active"},
            "data_context": {"test_data": "sample"}
        }
        
        if mission_system.update_mission_status(test_mission_id, "EXECUTION", context_update=context_update):
            results["tests"]["context_updates"] = "PASSED"
            logger.info("    ✅ Context updates successful")
        else:
            results["tests"]["context_updates"] = "FAILED"
            results["issues"].append("Context updates failed")
        
        # Clean up
        mission_system.update_mission_status(test_mission_id, "COMPLETED")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Context management test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Context management error: {str(e)}")
    
    return results

def test_mission_lifecycle(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test mission lifecycle management"""
    logger.info("🔧 Testing Mission Lifecycle")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test mission briefing
        logger.info("  Testing mission briefing")
        test_mission_data = {
            "mission_name": "Lifecycle Test Mission",
            "mission_description": "Test mission lifecycle",
            "mission_type": "DEVELOPMENT",
            "tool_loadout": "LAB_DEV_001"
        }
        
        test_mission_id = mission_system.create_mission(test_mission_data)
        
        briefing = mission_system.get_mission_briefing(test_mission_id)
        if briefing and "MISSION BRIEFING" in briefing:
            results["tests"]["mission_briefing"] = "PASSED"
            logger.info("    ✅ Mission briefing generated")
        else:
            results["tests"]["mission_briefing"] = "FAILED"
            results["issues"].append("Mission briefing generation failed")
        
        # Test execution plan
        logger.info("  Testing execution plan")
        execution_plan = mission_system.get_execution_plan(test_mission_id)
        if execution_plan and "MISSION EXECUTION PLAN" in execution_plan:
            results["tests"]["execution_plan"] = "PASSED"
            logger.info("    ✅ Execution plan generated")
        else:
            results["tests"]["execution_plan"] = "FAILED"
            results["issues"].append("Execution plan generation failed")
        
        # Test mid-mission debriefing
        logger.info("  Testing mid-mission debriefing")
        mid_debriefing = mission_system.get_mid_mission_debriefing(test_mission_id)
        if mid_debriefing and "MID-MISSION DEBRIEFING" in mid_debriefing:
            results["tests"]["mid_debriefing"] = "PASSED"
            logger.info("    ✅ Mid-mission debriefing generated")
        else:
            results["tests"]["mid_debriefing"] = "FAILED"
            results["issues"].append("Mid-mission debriefing generation failed")
        
        # Test rebriefing
        logger.info("  Testing rebriefing")
        rebriefing_context = {"reason": "Test rebriefing", "requires_tool_setup": True}
        rebriefing = mission_system.get_rebriefing(test_mission_id, rebriefing_context)
        if rebriefing and "MISSION REBRIEFING" in rebriefing:
            results["tests"]["rebriefing"] = "PASSED"
            logger.info("    ✅ Rebriefing generated")
        else:
            results["tests"]["rebriefing"] = "FAILED"
            results["issues"].append("Rebriefing generation failed")
        
        # Clean up
        mission_system.update_mission_status(test_mission_id, "COMPLETED")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Mission lifecycle test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Mission lifecycle error: {str(e)}")
    
    return results

def test_logging_systems(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test logging systems"""
    logger.info("🔧 Testing Logging Systems")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test mission logging
        logger.info("  Testing mission logging")
        test_mission_data = {
            "mission_name": "Logging Test Mission",
            "mission_description": "Test logging systems",
            "mission_type": "DEVELOPMENT"
        }
        
        test_mission_id = mission_system.create_mission(test_mission_data)
        
        # Add log entries
        log_data = {"test_key": "test_value"}
        tool_usage = {"tool_name": "test_tool", "operation": "test_operation"}
        
        if mission_system.add_mission_log_entry(
            test_mission_id, "INFO", "audit_test", "Test log entry", 
            data=log_data, tool_usage=tool_usage
        ):
            results["tests"]["mission_logging"] = "PASSED"
            logger.info("    ✅ Mission logging successful")
        else:
            results["tests"]["mission_logging"] = "FAILED"
            results["issues"].append("Mission logging failed")
        
        # Check log files exist
        log_dir = mission_system.missions_dir / "logs"
        if log_dir.exists():
            log_files = list(log_dir.glob("*.log"))
            if log_files:
                results["tests"]["log_file_creation"] = "PASSED"
                logger.info(f"    ✅ Log files created: {len(log_files)}")
            else:
                results["tests"]["log_file_creation"] = "FAILED"
                results["issues"].append("No log files created")
        else:
            results["tests"]["log_file_creation"] = "FAILED"
            results["issues"].append("Log directory not created")
        
        # Clean up
        mission_system.update_mission_status(test_mission_id, "COMPLETED")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Logging systems test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Logging systems error: {str(e)}")
    
    return results

def test_prompt_engine(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test prompt engine functionality"""
    logger.info("🔧 Testing Prompt Engine")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test prompt engine initialization
        logger.info("  Testing prompt engine initialization")
        if mission_system.prompt_engine:
            results["tests"]["prompt_engine_init"] = "PASSED"
            logger.info("    ✅ Prompt engine initialized")
        else:
            results["tests"]["prompt_engine_init"] = "FAILED"
            results["issues"].append("Prompt engine not initialized")
        
        # Test template loading
        logger.info("  Testing template loading")
        templates = mission_system.prompt_engine.templates
        if templates:
            results["tests"]["template_loading"] = "PASSED"
            logger.info(f"    ✅ Templates loaded: {len(templates)}")
        else:
            results["tests"]["template_loading"] = "FAILED"
            results["issues"].append("No templates loaded")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Prompt engine test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Prompt engine error: {str(e)}")
    
    return results

def test_error_handling(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test error handling capabilities"""
    logger.info("🔧 Testing Error Handling")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test invalid mission ID handling
        logger.info("  Testing invalid mission ID handling")
        invalid_mission = mission_system.get_mission("INVALID_ID")
        if invalid_mission is None:
            results["tests"]["invalid_mission_handling"] = "PASSED"
            logger.info("    ✅ Invalid mission ID handled gracefully")
        else:
            results["tests"]["invalid_mission_handling"] = "FAILED"
            results["issues"].append("Invalid mission ID not handled properly")
        
        # Test invalid loadout assignment
        logger.info("  Testing invalid loadout assignment")
        test_mission_data = {
            "mission_name": "Error Test Mission",
            "mission_description": "Test error handling",
            "mission_type": "DEVELOPMENT"
        }
        
        test_mission_id = mission_system.create_mission(test_mission_data)
        
        if not mission_system.assign_tool_loadout(test_mission_id, "INVALID_LOADOUT"):
            results["tests"]["invalid_loadout_handling"] = "PASSED"
            logger.info("    ✅ Invalid loadout assignment handled gracefully")
        else:
            results["tests"]["invalid_loadout_handling"] = "FAILED"
            results["issues"].append("Invalid loadout assignment not handled properly")
        
        # Clean up
        mission_system.update_mission_status(test_mission_id, "COMPLETED")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Error handling test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Error handling error: {str(e)}")
    
    return results

def test_performance(mission_system: MissionSystem, logger: logging.Logger) -> dict:
    """Test system performance"""
    logger.info("🔧 Testing Performance")
    
    results = {
        "status": "PENDING",
        "tests": {},
        "issues": []
    }
    
    try:
        # Test mission creation performance
        logger.info("  Testing mission creation performance")
        start_time = datetime.now()
        
        test_mission_data = {
            "mission_name": "Performance Test Mission",
            "mission_description": "Test system performance",
            "mission_type": "DEVELOPMENT"
        }
        
        test_mission_id = mission_system.create_mission(test_mission_data)
        creation_time = (datetime.now() - start_time).total_seconds()
        
        if creation_time < 5.0:  # Should complete within 5 seconds
            results["tests"]["creation_performance"] = "PASSED"
            logger.info(f"    ✅ Mission creation performance: {creation_time:.2f}s")
        else:
            results["tests"]["creation_performance"] = "FAILED"
            results["issues"].append(f"Mission creation too slow: {creation_time:.2f}s")
        
        # Test context sync performance
        logger.info("  Testing context sync performance")
        start_time = datetime.now()
        
        context_update = {
            "execution_state": {"performance_test": "running"},
            "tool_states": {"test_tool": "active"}
        }
        
        mission_system.update_mission_status(test_mission_id, "EXECUTION", context_update=context_update)
        sync_time = (datetime.now() - start_time).total_seconds()
        
        if sync_time < 2.0:  # Should complete within 2 seconds
            results["tests"]["sync_performance"] = "PASSED"
            logger.info(f"    ✅ Context sync performance: {sync_time:.2f}s")
        else:
            results["tests"]["sync_performance"] = "FAILED"
            results["issues"].append(f"Context sync too slow: {sync_time:.2f}s")
        
        # Clean up
        mission_system.update_mission_status(test_mission_id, "COMPLETED")
        
        results["status"] = "PASSED"
        
    except Exception as e:
        logger.error(f"    ❌ Performance test failed: {e}")
        results["status"] = "FAILED"
        results["issues"].append(f"Performance test error: {str(e)}")
    
    return results

def determine_overall_status(components: dict) -> str:
    """Determine overall audit status"""
    failed_components = 0
    total_components = len(components)
    
    for component_name, component_result in components.items():
        if component_result.get("status") == "FAILED":
            failed_components += 1
    
    if failed_components == 0:
        return "PASSED"
    elif failed_components < total_components / 2:
        return "PARTIAL"
    else:
        return "FAILED"

def generate_recommendations(components: dict) -> list:
    """Generate recommendations based on audit results"""
    recommendations = []
    
    for component_name, component_result in components.items():
        if component_result.get("status") == "FAILED":
            issues = component_result.get("issues", [])
            for issue in issues:
                recommendations.append({
                    "component": component_name,
                    "issue": issue,
                    "priority": "HIGH",
                    "recommendation": f"Fix {component_name} issue: {issue}"
                })
        elif component_result.get("status") == "PARTIAL":
            recommendations.append({
                "component": component_name,
                "issue": "Partial functionality",
                "priority": "MEDIUM",
                "recommendation": f"Review and improve {component_name} functionality"
            })
    
    # Add general recommendations
    recommendations.append({
        "component": "general",
        "issue": "System optimization",
        "priority": "LOW",
        "recommendation": "Consider performance optimizations for large-scale operations"
    })
    
    return recommendations

def save_audit_results(audit_results: dict, repository_root: Path):
    """Save audit results to file"""
    try:
        audit_file = repository_root / "missions" / "audit_results.json"
        with open(audit_file, 'w') as f:
            json.dump(audit_results, f, indent=2)
        print(f"✅ Audit results saved to: {audit_file}")
    except Exception as e:
        print(f"❌ Failed to save audit results: {e}")

def main():
    """Main audit execution"""
    repository_root = Path(__file__).parent.parent
    
    print("🚀 Starting Mission System Comprehensive Audit")
    print(f"📁 Repository: {repository_root}")
    print("=" * 60)
    
    audit_results = audit_mission_system(repository_root)
    
    print("\n" + "=" * 60)
    print("📊 AUDIT RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"Overall Status: {audit_results['overall_status']}")
    print(f"Timestamp: {audit_results['timestamp']}")
    
    print("\nComponent Status:")
    for component_name, component_result in audit_results["components"].items():
        status = component_result.get("status", "UNKNOWN")
        status_icon = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "⚠️"
        print(f"  {status_icon} {component_name}: {status}")
    
    if audit_results["issues"]:
        print(f"\nIssues Found: {len(audit_results['issues'])}")
        for issue in audit_results["issues"]:
            print(f"  ❌ {issue}")
    
    if audit_results["recommendations"]:
        print(f"\nRecommendations: {len(audit_results['recommendations'])}")
        for rec in audit_results["recommendations"]:
            priority_icon = "🔴" if rec["priority"] == "HIGH" else "🟡" if rec["priority"] == "MEDIUM" else "🟢"
            print(f"  {priority_icon} {rec['recommendation']}")
    
    print(f"\n🎯 Mission System Audit Complete!")
    print(f"📁 Detailed results saved to: missions/audit_results.json")
    
    return audit_results

if __name__ == "__main__":
    main()
