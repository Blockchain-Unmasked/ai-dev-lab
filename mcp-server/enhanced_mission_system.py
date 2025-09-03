#!/usr/bin/env python3
"""
Enhanced Mission System Core for AI/DEV Lab
Provides comprehensive mission management with tool loadouts, context management,
and full mission lifecycle support including mid-mission debriefing and rebriefing
"""

import json
import logging
import uuid
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import time

logger = logging.getLogger(__name__)

class MissionStatus(Enum):
    """Mission status enumeration"""
    PLANNING = "PLANNING"
    BRIEFING = "BRIEFING"
    EXECUTION = "EXECUTION"
    DEBRIEFING = "DEBRIEFING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    REBRIEFING = "REBRIEFING"

class MissionStage(Enum):
    """Mission stage enumeration"""
    INITIALIZATION = "INITIALIZATION"
    ANALYSIS = "ANALYSIS"
    IMPLEMENTATION = "IMPLEMENTATION"
    TESTING = "TESTING"
    VALIDATION = "VALIDATION"
    DEPLOYMENT = "DEPLOYMENT"
    MONITORING = "MONITORING"
    ARCHIVAL = "ARCHIVAL"

class ToolCategory(Enum):
    """Tool category enumeration"""
    LAB_MCP_SERVERS = "LAB_MCP_SERVERS"
    APP_MCP_SERVERS = "APP_MCP_SERVERS"
    CURSOR_EXTENSIONS = "CURSOR_EXTENSIONS"
    SYSTEM_TOOLS = "SYSTEM_TOOLS"
    EXTERNAL_APIS = "EXTERNAL_APIS"

@dataclass
class ToolLoadout:
    """Tool loadout configuration for missions"""
    loadout_id: str
    loadout_name: str
    loadout_description: str
    tool_category: ToolCategory
    tools: List[Dict[str, Any]]
    capabilities: List[str]
    access_level: str
    scope: str
    configuration: Dict[str, Any]
    dependencies: List[str]
    estimated_setup_time: str
    validation_required: bool

@dataclass
class MissionContext:
    """Mission context and state management"""
    context_id: str
    mission_id: str
    current_phase: str
    current_task: str
    execution_state: Dict[str, Any]
    tool_states: Dict[str, Any]
    data_context: Dict[str, Any]
    user_context: Dict[str, Any]
    system_context: Dict[str, Any]
    timestamp: str
    version: str

@dataclass
class MissionObjective:
    """Enhanced mission objective with tracking"""
    objective_id: str
    objective_name: str
    objective_description: str
    success_criteria: str
    status: str = "PENDING"
    completion_percentage: float = 0.0
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""
    assigned_agent: str = ""
    dependencies: List[str] = None
    blockers: List[str] = None
    progress_history: List[Dict[str, Any]] = None

@dataclass
class MissionPhase:
    """Enhanced mission phase with detailed tracking"""
    phase_id: str
    phase_name: str
    phase_description: str
    phase_order: int
    estimated_duration: str
    dependencies: List[str] = None
    status: str = "PENDING"
    progress: float = 0.0
    tasks: List[Dict[str, Any]] = None
    start_time: str = ""
    end_time: str = ""
    actual_duration: str = ""
    phase_context: Dict[str, Any] = None
    tool_requirements: List[str] = None
    validation_criteria: List[str] = None

@dataclass
class MissionTask:
    """Enhanced mission task with tool integration"""
    task_id: str
    task_name: str
    task_description: str
    assigned_server: str
    status: str = "PENDING"
    estimated_effort: str = ""
    actual_effort: str = ""
    outputs: List[str] = None
    tool_loadout: str = ""
    start_time: str = ""
    end_time: str = ""
    task_context: Dict[str, Any] = None
    dependencies: List[str] = None
    blockers: List[str] = None
    validation_results: List[Dict[str, Any]] = None

class MissionSystem:
    """Enhanced mission system with comprehensive lifecycle management"""
    
    def __init__(self, repository_root: Path):
        self.repository_root = Path(repository_root)
        self.missions_dir = self.repository_root / "missions"
        self.missions_dir.mkdir(exist_ok=True)
        self.context_dir = self.missions_dir / "contexts"
        self.context_dir.mkdir(exist_ok=True)
        self.tool_loadouts_dir = self.missions_dir / "tool_loadouts"
        self.tool_loadouts_dir.mkdir(exist_ok=True)
        
        self.active_missions: Dict[str, Dict[str, Any]] = {}
        self.mission_history: List[Dict[str, Any]] = []
        self.mission_contexts: Dict[str, MissionContext] = {}
        self.tool_loadouts: Dict[str, ToolLoadout] = {}
        
        self.prompt_engine = EnhancedPromptEngine()
        self.context_manager = ContextManager(self.context_dir)
        self.tool_manager = ToolLoadoutManager(self.tool_loadouts_dir)
        
        self.load_missions()
        self.load_tool_loadouts()
        self.initialize_logging()
        
        # Start background context sync
        self.context_sync_thread = threading.Thread(target=self._context_sync_loop, daemon=True)
        self.context_sync_thread.start()
    
    def initialize_logging(self):
        """Initialize comprehensive logging system"""
        log_dir = self.missions_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Mission activity log
        self.mission_logger = logging.getLogger("mission_system")
        mission_handler = logging.FileHandler(log_dir / "mission_activities.log")
        mission_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.mission_logger.addHandler(mission_handler)
        self.mission_logger.setLevel(logging.DEBUG)
        
        # Tool usage log
        self.tool_logger = logging.getLogger("tool_usage")
        tool_handler = logging.FileHandler(log_dir / "tool_usage.log")
        tool_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.tool_logger.addHandler(tool_handler)
        self.tool_logger.setLevel(logging.DEBUG)
        
        # Context change log
        self.context_logger = logging.getLogger("context_changes")
        context_handler = logging.FileHandler(log_dir / "context_changes.log")
        context_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.context_logger.addHandler(context_handler)
        self.context_logger.setLevel(logging.DEBUG)
    
    def create_mission(self, mission_data: Dict[str, Any]) -> str:
        """Create a new mission with comprehensive setup"""
        try:
            mission_id = self._generate_mission_id(mission_data.get("mission_type", "DEVELOPMENT"))
            mission_data["mission_id"] = mission_id
            
            # Initialize comprehensive metadata
            mission_data["metadata"] = {
                "created_at": datetime.now().isoformat(),
                "created_by": "AI/DEV Lab System",
                "version": "2.0.0",
                "last_modified": datetime.now().isoformat(),
                "modified_by": "AI/DEV Lab System"
            }
            
            # Set initial status and stage
            mission_data["mission_status"] = MissionStatus.PLANNING.value
            mission_data["current_stage"] = MissionStage.INITIALIZATION.value
            
            # Initialize mission lifecycle
            mission_data["mission_lifecycle"] = {
                "current_phase": "INITIALIZATION",
                "phase_history": [],
                "status_history": [],
                "context_snapshots": [],
                "tool_usage_log": [],
                "performance_metrics": {}
            }
            
            # Initialize context
            mission_data["mission_context"] = {
                "execution_context": {},
                "tool_context": {},
                "data_context": {},
                "user_context": {},
                "system_context": {}
            }
            
            # Save mission to file
            mission_file = self.missions_dir / f"{mission_id}.json"
            with open(mission_file, 'w') as f:
                json.dump(mission_data, f, indent=2)
            
            self.active_missions[mission_id] = mission_data
            
            # Create initial context
            self._create_mission_context(mission_id, mission_data)
            
            # Log mission creation
            self.mission_logger.info(f"✅ Mission created: {mission_id}")
            self._log_mission_activity(mission_id, "MISSION_CREATED", "Mission created successfully")
            
            return mission_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create mission: {e}")
            raise
    
    def _create_mission_context(self, mission_id: str, mission_data: Dict[str, Any]):
        """Create initial mission context"""
        context = MissionContext(
            context_id=f"{mission_id}_context",
            mission_id=mission_id,
            current_phase="INITIALIZATION",
            current_task="",
            execution_state={},
            tool_states={},
            data_context={},
            user_context={},
            system_context={},
            timestamp=datetime.now().isoformat(),
            version="2.0.0"
        )
        
        self.mission_contexts[mission_id] = context
        self.context_manager.save_context(context)
        self.context_logger.info(f"Context created for mission: {mission_id}")
    
    def update_mission_status(self, mission_id: str, new_status: str, stage: str = None, 
                            context_update: Dict[str, Any] = None) -> bool:
        """Update mission status with comprehensive tracking"""
        try:
            if mission_id not in self.active_missions:
                return False
            
            mission = self.active_missions[mission_id]
            old_status = mission.get("mission_status")
            
            # Update status and stage
            mission["mission_status"] = new_status
            if stage:
                mission["current_stage"] = stage
            
            # Update metadata
            mission["metadata"]["last_modified"] = datetime.now().isoformat()
            mission["metadata"]["modified_by"] = "AI/DEV Lab System"
            
            # Track status history
            if "mission_lifecycle" not in mission:
                mission["mission_lifecycle"] = {}
            if "status_history" not in mission["mission_lifecycle"]:
                mission["mission_lifecycle"]["status_history"] = []
            
            status_entry = {
                "timestamp": datetime.now().isoformat(),
                "old_status": old_status,
                "new_status": new_status,
                "stage": stage,
                "agent": "AI/DEV Lab System"
            }
            mission["mission_lifecycle"]["status_history"].append(status_entry)
            
            # Update context if provided
            if context_update and mission_id in self.mission_contexts:
                context = self.mission_contexts[mission_id]
                context.execution_state.update(context_update.get("execution_state", {}))
                context.tool_states.update(context_update.get("tool_states", {}))
                context.data_context.update(context_update.get("data_context", {}))
                context.timestamp = datetime.now().isoformat()
                
                # Save context snapshot
                self._save_context_snapshot(mission_id, context)
                self.context_manager.save_context(context)
            
            # Save mission to file
            mission_file = self.missions_dir / f"{mission_id}.json"
            with open(mission_file, 'w') as f:
                json.dump(mission, f, indent=2)
            
            # Log status change
            self.mission_logger.info(f"✅ Mission {mission_id} status updated: {old_status} -> {new_status}")
            self._log_mission_activity(mission_id, "STATUS_UPDATED", f"Status changed from {old_status} to {new_status}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update mission status: {e}")
            return False
    
    def _save_context_snapshot(self, mission_id: str, context: MissionContext):
        """Save context snapshot for historical tracking"""
        snapshot = {
            "timestamp": context.timestamp,
            "context_data": asdict(context),
            "version": context.version
        }
        
        if mission_id in self.active_missions:
            mission = self.active_missions[mission_id]
            if "mission_lifecycle" not in mission:
                mission["mission_lifecycle"] = {}
            if "context_snapshots" not in mission["mission_lifecycle"]:
                mission["mission_lifecycle"]["context_snapshots"] = []
            
            mission["mission_lifecycle"]["context_snapshots"].append(snapshot)
    
    def add_mission_log_entry(self, mission_id: str, level: str, source: str, message: str, 
                             data: Dict[str, Any] = None, tool_usage: Dict[str, Any] = None) -> bool:
        """Add comprehensive log entry to mission"""
        try:
            if mission_id not in self.active_missions:
                return False
            
            mission = self.active_missions[mission_id]
            if "mission_log" not in mission:
                mission["mission_log"] = {"log_entries": []}
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "source": source,
                "message": message,
                "data": data or {},
                "tool_usage": tool_usage or {}
            }
            
            mission["mission_log"]["log_entries"].append(log_entry)
            
            # Track tool usage if provided
            if tool_usage and "mission_lifecycle" in mission:
                if "tool_usage_log" not in mission["mission_lifecycle"]:
                    mission["mission_lifecycle"]["tool_usage_log"] = []
                mission["mission_lifecycle"]["tool_usage_log"].append(tool_usage)
                
                # Log tool usage separately
                self.tool_logger.info(f"Tool usage in mission {mission_id}: {tool_usage}")
            
            # Save to file
            mission_file = self.missions_dir / f"{mission_id}.json"
            with open(mission_file, 'w') as f:
                json.dump(mission, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add log entry: {e}")
            return False
    
    def _log_mission_activity(self, mission_id: str, activity_type: str, description: str, 
                             data: Dict[str, Any] = None):
        """Log mission activity for comprehensive tracking"""
        activity = {
            "timestamp": datetime.now().isoformat(),
            "activity_type": activity_type,
            "description": description,
            "data": data or {},
            "mission_id": mission_id
        }
        
        self.mission_logger.info(f"Activity: {activity_type} - {description}")
        
        # Add to mission lifecycle if available
        if mission_id in self.active_missions:
            mission = self.active_missions[mission_id]
            if "mission_lifecycle" not in mission:
                mission["mission_lifecycle"] = {}
            if "activity_log" not in mission["mission_lifecycle"]:
                mission["mission_lifecycle"]["activity_log"] = []
            
            mission["mission_lifecycle"]["activity_log"].append(activity)
    
    def get_mission_briefing(self, mission_id: str, include_tool_loadout: bool = True) -> str:
        """Generate comprehensive mission briefing with tool loadout"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        # Include tool loadout information if requested
        if include_tool_loadout and "tool_loadout" in mission:
            tool_info = self._get_tool_loadout_info(mission["tool_loadout"])
            mission["tool_loadout_details"] = tool_info
        
        return self.prompt_engine.generate_mission_briefing(mission)
    
    def get_execution_plan(self, mission_id: str, phase_id: str = None, 
                          include_tool_requirements: bool = True) -> str:
        """Generate execution plan with tool requirements"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        # Include tool requirements if requested
        if include_tool_requirements:
            mission["tool_requirements"] = self._get_mission_tool_requirements(mission_id)
        
        if phase_id:
            return self.prompt_engine.generate_phase_execution_plan(mission, phase_id)
        else:
            return self.prompt_engine.generate_mission_execution_plan(mission)
    
    def get_mid_mission_debriefing(self, mission_id: str, phase_id: str = None) -> str:
        """Generate mid-mission debriefing for current progress"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        # Calculate current progress and status
        mission["current_progress"] = self._calculate_mission_progress(mission_id)
        mission["phase_status"] = self._get_phase_status_summary(mission_id)
        mission["tool_usage_summary"] = self._get_tool_usage_summary(mission_id)
        
        return self.prompt_engine.generate_mid_mission_debriefing(mission)
    
    def get_rebriefing(self, mission_id: str, rebriefing_context: Dict[str, Any]) -> str:
        """Generate rebriefing for mission continuation"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        # Include rebriefing context
        mission["rebriefing_context"] = rebriefing_context
        mission["current_state"] = self._get_mission_current_state(mission_id)
        mission["continuation_plan"] = self._generate_continuation_plan(mission_id, rebriefing_context)
        
        return self.prompt_engine.generate_rebriefing(mission)
    
    def get_status_update(self, mission_id: str) -> str:
        """Generate status update for mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        return self.prompt_engine.generate_status_update(mission)
    
    def _calculate_mission_progress(self, mission_id: str) -> Dict[str, Any]:
        """Calculate comprehensive mission progress"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {}
        
        progress = {
            "overall_progress": 0.0,
            "phase_progress": {},
            "objective_progress": {},
            "task_progress": {},
            "tool_utilization": {}
        }
        
        # Calculate phase progress
        phases = mission.get("execution_plan", {}).get("phases", [])
        if phases:
            completed_phases = sum(1 for p in phases if p.get("status") == "COMPLETED")
            progress["overall_progress"] = (completed_phases / len(phases)) * 100
            
            for phase in phases:
                phase_id = phase.get("phase_id")
                progress["phase_progress"][phase_id] = {
                    "name": phase.get("phase_name"),
                    "status": phase.get("status"),
                    "progress": phase.get("progress", 0.0),
                    "tasks_completed": sum(1 for t in phase.get("tasks", []) if t.get("status") == "COMPLETED"),
                    "total_tasks": len(phase.get("tasks", []))
                }
        
        return progress
    
    def _get_phase_status_summary(self, mission_id: str) -> Dict[str, Any]:
        """Get comprehensive phase status summary"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {}
        
        phases = mission.get("execution_plan", {}).get("phases", [])
        summary = {}
        
        for phase in phases:
            phase_id = phase.get("phase_id")
            summary[phase_id] = {
                "name": phase.get("phase_name"),
                "order": phase.get("phase_order"),
                "status": phase.get("status"),
                "progress": phase.get("progress", 0.0),
                "start_time": phase.get("start_time"),
                "estimated_duration": phase.get("estimated_duration"),
                "actual_duration": phase.get("actual_duration"),
                "dependencies": phase.get("dependencies", []),
                "blockers": phase.get("blockers", [])
            }
        
        return summary
    
    def _get_tool_usage_summary(self, mission_id: str) -> Dict[str, Any]:
        """Get tool usage summary for mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {}
        
        tool_log = mission.get("mission_lifecycle", {}).get("tool_usage_log", [])
        summary = {
            "total_tool_usage": len(tool_log),
            "tools_used": {},
            "usage_by_phase": {},
            "performance_metrics": {}
        }
        
        for usage in tool_log:
            tool_name = usage.get("tool_name", "unknown")
            if tool_name not in summary["tools_used"]:
                summary["tools_used"][tool_name] = 0
            summary["tools_used"][tool_name] += 1
        
        return summary
    
    def _get_mission_current_state(self, mission_id: str) -> Dict[str, Any]:
        """Get current mission state for rebriefing"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {}
        
        current_state = {
            "mission_status": mission.get("mission_status"),
            "current_stage": mission.get("current_stage"),
            "current_phase": None,
            "current_task": None,
            "recent_activities": [],
            "active_blockers": [],
            "tool_states": {},
            "data_context": {}
        }
        
        # Get current phase and task
        phases = mission.get("execution_plan", {}).get("phases", [])
        for phase in phases:
            if phase.get("status") == "IN_PROGRESS":
                current_state["current_phase"] = phase
                tasks = phase.get("tasks", [])
                for task in tasks:
                    if task.get("status") == "IN_PROGRESS":
                        current_state["current_task"] = task
                        break
                break
        
        # Get recent activities
        if "mission_lifecycle" in mission:
            activity_log = mission["mission_lifecycle"].get("activity_log", [])
            current_state["recent_activities"] = activity_log[-10:] if len(activity_log) > 10 else activity_log
        
        # Get context information
        if mission_id in self.mission_contexts:
            context = self.mission_contexts[mission_id]
            current_state["tool_states"] = context.tool_states
            current_state["data_context"] = context.data_context
        
        return current_state
    
    def _generate_continuation_plan(self, mission_id: str, rebriefing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate continuation plan for rebriefing"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {}
        
        continuation_plan = {
            "next_actions": [],
            "tool_requirements": [],
            "dependencies": [],
            "estimated_effort": "",
            "success_criteria": [],
            "risk_mitigation": []
        }
        
        # Analyze current state and generate next steps
        current_phase = self._get_current_phase(mission_id)
        if current_phase:
            continuation_plan["next_actions"] = self._generate_next_actions(current_phase, rebriefing_context)
            continuation_plan["tool_requirements"] = self._get_phase_tool_requirements(current_phase)
            continuation_plan["dependencies"] = current_phase.get("dependencies", [])
        
        return continuation_plan
    
    def _get_current_phase(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Get current active phase"""
        mission = self.get_mission(mission_id)
        if not mission:
            return None
        
        phases = mission.get("execution_plan", {}).get("phases", [])
        for phase in phases:
            if phase.get("status") in ["IN_PROGRESS", "PENDING"]:
                return phase
        
        return None
    
    def _generate_next_actions(self, current_phase: Dict[str, Any], 
                              rebriefing_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate next actions based on current phase and context"""
        actions = []
        
        # Generate actions based on phase status and context
        if current_phase.get("status") == "PENDING":
            actions.append({
                "action": "START_PHASE",
                "description": f"Begin execution of {current_phase.get('phase_name')}",
                "priority": "HIGH",
                "estimated_effort": "5 minutes"
            })
        
        # Add context-specific actions
        if rebriefing_context.get("requires_tool_setup"):
            actions.append({
                "action": "SETUP_TOOLS",
                "description": "Configure and validate required tools",
                "priority": "HIGH",
                "estimated_effort": "10 minutes"
            })
        
        return actions
    
    def _get_phase_tool_requirements(self, phase: Dict[str, Any]) -> List[str]:
        """Get tool requirements for a specific phase"""
        return phase.get("tool_requirements", [])
    
    def _get_mission_tool_requirements(self, mission_id: str) -> Dict[str, Any]:
        """Get comprehensive tool requirements for mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {}
        
        requirements = {
            "lab_mcp_servers": [],
            "app_mcp_servers": [],
            "cursor_extensions": [],
            "system_tools": [],
            "external_apis": []
        }
        
        # Extract tool requirements from mission data
        if "tool_loadout" in mission:
            loadout_id = mission["tool_loadout"]
            if loadout_id in self.tool_loadouts:
                loadout = self.tool_loadouts[loadout_id]
                category = loadout.tool_category.value
                if category in requirements:
                    requirements[category].append({
                        "loadout_id": loadout_id,
                        "loadout_name": loadout.loadout_name,
                        "tools": loadout.tools,
                        "capabilities": loadout.capabilities
                    })
        
        return requirements
    
    def _get_tool_loadout_info(self, loadout_id: str) -> Dict[str, Any]:
        """Get detailed tool loadout information"""
        if loadout_id in self.tool_loadouts:
            loadout = self.tool_loadouts[loadout_id]
            return asdict(loadout)
        return {}
    
    def _context_sync_loop(self):
        """Background context synchronization loop"""
        while True:
            try:
                for mission_id in list(self.active_missions.keys()):
                    if mission_id in self.mission_contexts:
                        context = self.mission_contexts[mission_id]
                        self.context_manager.save_context(context)
                
                time.sleep(30)  # Sync every 30 seconds
            except Exception as e:
                logger.error(f"Context sync error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def load_tool_loadouts(self):
        """Load tool loadout configurations"""
        try:
            for loadout_file in self.tool_loadouts_dir.glob("*.json"):
                with open(loadout_file, 'r') as f:
                    loadout_data = json.load(f)
                
                loadout = ToolLoadout(**loadout_data)
                self.tool_loadouts[loadout.loadout_id] = loadout
            
            logger.info(f"✅ Loaded {len(self.tool_loadouts)} tool loadouts")
            
        except Exception as e:
            logger.error(f"❌ Failed to load tool loadouts: {e}")
    
    def get_available_tool_loadouts(self, mission_type: str = None) -> List[Dict[str, Any]]:
        """Get available tool loadouts for mission type"""
        loadouts = []
        
        for loadout in self.tool_loadouts.values():
            if mission_type is None or mission_type in loadout.capabilities:
                loadouts.append(asdict(loadout))
        
        return loadouts
    
    def assign_tool_loadout(self, mission_id: str, loadout_id: str) -> bool:
        """Assign tool loadout to mission"""
        try:
            if mission_id not in self.active_missions:
                return False
            
            if loadout_id not in self.tool_loadouts:
                return False
            
            mission = self.active_missions[mission_id]
            mission["tool_loadout"] = loadout_id
            
            # Update mission context with tool information
            if mission_id in self.mission_contexts:
                context = self.mission_contexts[mission_id]
                loadout = self.tool_loadouts[loadout_id]
                context.tool_states["assigned_loadout"] = {
                    "loadout_id": loadout_id,
                    "loadout_name": loadout.loadout_name,
                    "assigned_at": datetime.now().isoformat()
                }
                self.context_manager.save_context(context)
            
            # Save mission
            mission_file = self.missions_dir / f"{mission_id}.json"
            with open(mission_file, 'w') as f:
                json.dump(mission, f, indent=2)
            
            self._log_mission_activity(mission_id, "TOOL_LOADOUT_ASSIGNED", f"Assigned tool loadout: {loadout_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to assign tool loadout: {e}")
            return False
    
    # Inherit other methods from original MissionSystem
    def get_mission(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Get mission by ID"""
        if mission_id in self.active_missions:
            return self.active_missions[mission_id]
        
        # Check mission history
        for mission in self.mission_history:
            if mission["mission_id"] == mission_id:
                return mission
        
        return None
    
    def list_active_missions(self) -> List[Dict[str, Any]]:
        """List all active missions"""
        return list(self.active_missions.values())
    
    def list_completed_missions(self) -> List[Dict[str, Any]]:
        """List all completed missions"""
        return self.mission_history
    
    def _generate_mission_id(self, mission_type: str) -> str:
        """Generate unique mission ID"""
        year = datetime.now().year
        unique_part = str(uuid.uuid4())[:8].upper()
        type_prefix = mission_type[:3].upper()
        return f"{type_prefix}-{year}-{unique_part}"
    
    def load_missions(self):
        """Load existing missions from files"""
        try:
            for mission_file in self.missions_dir.glob("*.json"):
                if mission_file.name == "archive" or mission_file.name.startswith("context_") or mission_file.name.startswith("tool_loadout_"):
                    continue
                
                with open(mission_file, 'r') as f:
                    mission_data = json.load(f)
                
                mission_id = mission_data.get("mission_id")
                if mission_id:
                    if mission_data.get("mission_status") == "COMPLETED":
                        self.mission_history.append(mission_data)
                    else:
                        self.active_missions[mission_id] = mission_data
            
            logger.info(f"✅ Loaded {len(self.active_missions)} active missions and {len(self.mission_history)} completed missions")
            
        except Exception as e:
            logger.error(f"❌ Failed to load missions: {e}")


class ContextManager:
    """Manages mission context persistence and retrieval"""
    
    def __init__(self, context_dir: Path):
        self.context_dir = context_dir
    
    def save_context(self, context: MissionContext):
        """Save mission context to file"""
        try:
            context_file = self.context_dir / f"context_{context.mission_id}.json"
            with open(context_file, 'w') as f:
                json.dump(asdict(context), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save context: {e}")
    
    def load_context(self, mission_id: str) -> Optional[MissionContext]:
        """Load mission context from file"""
        try:
            context_file = self.context_dir / f"context_{mission_id}.json"
            if context_file.exists():
                with open(context_file, 'r') as f:
                    context_data = json.load(f)
                return MissionContext(**context_data)
        except Exception as e:
            logger.error(f"Failed to load context: {e}")
        
        return None


class ToolLoadoutManager:
    """Manages tool loadout configurations"""
    
    def __init__(self, tool_loadouts_dir: Path):
        self.tool_loadouts_dir = tool_loadouts_dir
    
    def save_loadout(self, loadout: ToolLoadout):
        """Save tool loadout to file"""
        try:
            loadout_file = self.tool_loadouts_dir / f"loadout_{loadout.loadout_id}.json"
            with open(loadout_file, 'w') as f:
                json.dump(asdict(loadout), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save loadout: {e}")
    
    def load_loadout(self, loadout_id: str) -> Optional[ToolLoadout]:
        """Load tool loadout from file"""
        try:
            loadout_file = self.tool_loadouts_dir / f"loadout_{loadout_id}.json"
            if loadout_file.exists():
                with open(loadout_file, 'r') as f:
                    loadout_data = json.load(f)
                return ToolLoadout(**loadout_data)
        except Exception as e:
            logger.error(f"Failed to load loadout: {e}")
        
        return None


class EnhancedPromptEngine:
    """Enhanced prompt engine with tool loadout support"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def generate_mission_briefing(self, mission: Dict[str, Any]) -> str:
        """Generate enhanced mission briefing with tool loadout"""
        template = self.templates.get("mission_briefing", {})
        content = template.get("template_content", "")
        
        # Enhanced variable replacement
        content = self._replace_variables(content, mission)
        
        # Add tool loadout information if available
        if "tool_loadout_details" in mission:
            tool_info = mission["tool_loadout_details"]
            content += f"\n\n🔧 **TOOL LOADOUT ASSIGNED**\n"
            content += f"**Loadout**: {tool_info.get('loadout_name', 'Unknown')}\n"
            content += f"**Category**: {tool_info.get('tool_category', 'Unknown')}\n"
            content += f"**Capabilities**: {', '.join(tool_info.get('capabilities', []))}\n"
            content += f"**Access Level**: {tool_info.get('access_level', 'Unknown')}\n"
            content += f"**Scope**: {tool_info.get('scope', 'Unknown')}\n"
        
        return content
    
    def generate_phase_execution_plan(self, mission: Dict[str, Any], phase_id: str) -> str:
        """Generate enhanced phase execution plan"""
        template = self.templates.get("execution_plan", {})
        content = template.get("template_content", "")
        
        # Find the specific phase
        current_phase = None
        next_phase = None
        
        for phase in mission.get("execution_plan", {}).get("phases", []):
            if phase.get("phase_id") == phase_id:
                current_phase = phase
                # Find next phase
                for next_p in mission.get("execution_plan", {}).get("phases", []):
                    if next_p.get("phase_order") == phase.get("phase_order") + 1:
                        next_phase = next_p
                        break
                break
        
        if not current_phase:
            return f"Phase {phase_id} not found in mission {mission.get('mission_id')}"
        
        # Replace variables
        content = content.replace("{{mission_name}}", mission.get("mission_name", ""))
        content = content.replace("{{mission_id}}", mission.get("mission_id", ""))
        content = content.replace("{{current_phase.phase_name}}", current_phase.get("phase_name", ""))
        content = content.replace("{{current_phase.phase_order}}", str(current_phase.get("phase_order", "")))
        content = content.replace("{{current_phase.status}}", current_phase.get("status", ""))
        
        if next_phase:
            content = content.replace("{{next_phase.phase_name}}", next_phase.get("phase_name", ""))
        else:
            content = content.replace("{{next_phase.phase_name}}", "Final Phase")
        
        # Add tool requirements if available
        if "tool_requirements" in mission:
            content += f"\n\n🔧 **TOOL REQUIREMENTS FOR THIS PHASE**\n"
            for category, tools in mission["tool_requirements"].items():
                if tools:
                    content += f"**{category.replace('_', ' ').title()}**:\n"
                    for tool in tools:
                        content += f"- {tool.get('loadout_name', 'Unknown')}: {', '.join(tool.get('capabilities', []))}\n"
        
        return content
    
    def generate_mission_execution_plan(self, mission: Dict[str, Any]) -> str:
        """Generate enhanced mission execution plan"""
        content = f"🚀 **MISSION EXECUTION PLAN**\n\n**Mission**: {mission.get('mission_name')} ({mission.get('mission_id')})\n\n**Phases**:\n"
        
        phases = mission.get("execution_plan", {}).get("phases", [])
        for phase in phases:
            content += f"- Phase {phase.get('phase_order')}: {phase.get('phase_name')} - {phase.get('status')}\n"
        
        # Add tool requirements if available
        if "tool_requirements" in mission:
            content += f"\n\n🔧 **MISSION TOOL REQUIREMENTS**\n"
            for category, tools in mission["tool_requirements"].items():
                if tools:
                    content += f"**{category.replace('_', ' ').title()}**:\n"
                    for tool in tools:
                        content += f"- {tool.get('loadout_name', 'Unknown')}: {', '.join(tool.get('capabilities', []))}\n"
        
        return content
    
    def generate_mid_mission_debriefing(self, mission: Dict[str, Any]) -> str:
        """Generate mid-mission debriefing"""
        content = f"📋 **MID-MISSION DEBRIEFING**\n\n**Mission**: {mission.get('mission_name')} ({mission.get('mission_id')})\n"
        content += f"**Current Status**: {mission.get('mission_status')}\n"
        content += f"**Current Stage**: {mission.get('current_stage')}\n"
        
        # Add progress information
        if "current_progress" in mission:
            progress = mission["current_progress"]
            content += f"**Overall Progress**: {progress.get('overall_progress', 0):.1f}%\n\n"
            
            content += "**Phase Progress**:\n"
            for phase_id, phase_info in progress.get("phase_progress", {}).items():
                content += f"- {phase_info.get('name', 'Unknown')}: {phase_info.get('progress', 0):.1f}% "
                content += f"({phase_info.get('tasks_completed', 0)}/{phase_info.get('total_tasks', 0)} tasks)\n"
        
        # Add tool usage summary
        if "tool_usage_summary" in mission:
            tool_summary = mission["tool_usage_summary"]
            content += f"\n**Tool Usage Summary**:\n"
            content += f"- Total Tool Usage: {tool_summary.get('total_tool_usage', 0)}\n"
            content += f"- Tools Used: {', '.join(tool_summary.get('tools_used', {}).keys())}\n"
        
        content += "\n**Next Steps**:\n"
        content += "1. Review current progress and identify blockers\n"
        content += "2. Validate tool usage and performance\n"
        content += "3. Plan next phase execution\n"
        content += "4. Update mission status and context\n"
        
        return content
    
    def generate_rebriefing(self, mission: Dict[str, Any]) -> str:
        """Generate rebriefing for mission continuation"""
        content = f"🔄 **MISSION REBRIEFING**\n\n**Mission**: {mission.get('mission_name')} ({mission.get('mission_id')})\n"
        content += f"**Rebriefing Context**: {mission.get('rebriefing_context', {}).get('reason', 'Unknown')}\n"
        
        # Add current state information
        if "current_state" in mission:
            state = mission["current_state"]
            content += f"**Current Status**: {state.get('mission_status', 'Unknown')}\n"
            content += f"**Current Stage**: {state.get('current_stage', 'Unknown')}\n"
            
            if state.get("current_phase"):
                phase = state["current_phase"]
                content += f"**Current Phase**: {phase.get('phase_name', 'Unknown')}\n"
            
            if state.get("current_task"):
                task = state["current_task"]
                content += f"**Current Task**: {task.get('task_name', 'Unknown')}\n"
        
        # Add continuation plan
        if "continuation_plan" in mission:
            plan = mission["continuation_plan"]
            content += f"\n**Continuation Plan**:\n"
            
            content += "**Next Actions**:\n"
            for i, action in enumerate(plan.get("next_actions", []), 1):
                content += f"{i}. {action.get('action', 'Unknown')}: {action.get('description', 'No description')}\n"
                content += f"   Priority: {action.get('priority', 'Unknown')}\n"
                content += f"   Estimated Effort: {action.get('estimated_effort', 'Unknown')}\n"
            
            if plan.get("tool_requirements"):
                content += f"\n**Tool Requirements**:\n"
                for tool in plan["tool_requirements"]:
                    content += f"- {tool}\n"
        
        content += "\n**Ready to continue mission?**\n"
        content += "Respond with 'MISSION CONTINUATION ACKNOWLEDGED' to proceed."
        
        return content
    
    def generate_status_update(self, mission: Dict[str, Any]) -> str:
        """Generate status update prompt"""
        template = self.templates.get("status_update", {})
        content = template.get("template_content", "")
        
        # Calculate overall progress
        total_phases = len(mission.get("execution_plan", {}).get("phases", []))
        completed_phases = sum(1 for p in mission.get("execution_plan", {}).get("phases", []) 
                              if p.get("status") == "COMPLETED")
        overall_progress = (completed_phases / total_phases * 100) if total_phases > 0 else 0
        
        # Replace variables
        content = content.replace("{{mission_name}}", mission.get("mission_name", ""))
        content = content.replace("{{mission_id}}", mission.get("mission_id", ""))
        content = content.replace("{{mission_status}}", mission.get("mission_status", ""))
        content = content.replace("{{current_stage}}", mission.get("current_stage", ""))
        content = content.replace("{{overall_progress}}", f"{overall_progress:.1f}")
        
        return content
    
    def _replace_variables(self, content: str, data: Dict[str, Any]) -> str:
        """Enhanced variable replacement"""
        for key, value in data.items():
            if isinstance(value, str):
                content = content.replace(f"{{{{{key}}}}}", str(value))
            elif isinstance(value, (int, float)):
                content = content.replace(f"{{{{{key}}}}}", str(value))
            elif isinstance(value, list):
                # Handle list variables
                list_content = ""
                for item in value:
                    if isinstance(item, dict):
                        item_str = ", ".join([f"{k}: {v}" for k, v in item.items()])
                        list_content += f"- {item_str}\n"
                    else:
                        list_content += f"- {item}\n"
                content = content.replace(f"{{{{{key}}}}}", list_content)
        
        return content
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load prompt templates"""
        try:
            templates_file = Path(__file__).parent / "meta" / "prompt-engine-templates.json"
            if templates_file.exists():
                with open(templates_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load prompt templates: {e}")
        
        return {}
