#!/usr/bin/env python3
"""
Mission System Core for AI/DEV Lab
Provides mission management, prompt engine, and execution coordination
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class MissionObjective:
    """Mission objective data structure"""
    objective_id: str
    objective_name: str
    objective_description: str
    success_criteria: str
    status: str = "PENDING"
    completion_percentage: float = 0.0
    notes: str = ""


@dataclass
class MissionPhase:
    """Mission phase data structure"""
    phase_id: str
    phase_name: str
    phase_description: str
    phase_order: int
    estimated_duration: str
    dependencies: List[str] = None
    status: str = "PENDING"
    progress: float = 0.0
    tasks: List[Dict[str, Any]] = None


@dataclass
class MissionTask:
    """Mission task data structure"""
    task_id: str
    task_name: str
    task_description: str
    assigned_server: str
    status: str = "PENDING"
    estimated_effort: str = ""
    actual_effort: str = ""
    outputs: List[str] = None


class MissionSystem:
    """Core mission system for coordinating development tasks"""
    
    def __init__(self, repository_root: Path):
        self.repository_root = Path(repository_root)
        self.missions_dir = self.repository_root / "missions"
        self.missions_dir.mkdir(exist_ok=True)
        self.active_missions: Dict[str, Dict[str, Any]] = {}
        self.mission_history: List[Dict[str, Any]] = []
        self.prompt_engine = PromptEngine()
        self.load_missions()
    
    def create_mission(self, mission_data: Dict[str, Any]) -> str:
        """Create a new mission"""
        try:
            mission_id = self._generate_mission_id(mission_data.get("mission_type", "DEVELOPMENT"))
            mission_data["mission_id"] = mission_id
            mission_data["metadata"] = {
                "created_at": datetime.now().isoformat(),
                "created_by": "AI/DEV Lab System",
                "version": "1.0.0"
            }
            mission_data["mission_status"] = "PLANNING"
            mission_data["current_stage"] = "INITIALIZATION"
            
            # Save mission to file
            mission_file = self.missions_dir / f"{mission_id}.json"
            with open(mission_file, 'w') as f:
                json.dump(mission_data, f, indent=2)
            
            self.active_missions[mission_id] = mission_data
            logger.info(f"✅ Mission created: {mission_id}")
            return mission_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create mission: {e}")
            raise
    
    def get_mission(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Get mission by ID"""
        if mission_id in self.active_missions:
            return self.active_missions[mission_id]
        
        # Check mission history
        for mission in self.mission_history:
            if mission["mission_id"] == mission_id:
                return mission
        
        return None
    
    def update_mission_status(self, mission_id: str, new_status: str, stage: str = None) -> bool:
        """Update mission status and stage"""
        try:
            if mission_id not in self.active_missions:
                return False
            
            mission = self.active_missions[mission_id]
            mission["mission_status"] = new_status
            if stage:
                mission["current_stage"] = stage
            
            # Update timestamp
            mission["metadata"]["last_modified"] = datetime.now().isoformat()
            mission["metadata"]["modified_by"] = "AI/DEV Lab System"
            
            # Save to file
            mission_file = self.missions_dir / f"{mission_id}.json"
            with open(mission_file, 'w') as f:
                json.dump(mission, f, indent=2)
            
            logger.info(f"✅ Mission {mission_id} status updated to {new_status}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update mission status: {e}")
            return False
    
    def add_mission_log_entry(self, mission_id: str, level: str, source: str, message: str, data: Dict[str, Any] = None) -> bool:
        """Add log entry to mission"""
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
                "data": data or {}
            }
            
            mission["mission_log"]["log_entries"].append(log_entry)
            
            # Save to file
            mission_file = self.missions_dir / f"{mission_id}.json"
            with open(mission_file, 'w') as f:
                json.dump(mission, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add log entry: {e}")
            return False
    
    def complete_mission(self, mission_id: str, completion_data: Dict[str, Any]) -> bool:
        """Complete a mission and move to history"""
        try:
            if mission_id not in self.active_missions:
                return False
            
            mission = self.active_missions[mission_id]
            mission["mission_status"] = "COMPLETED"
            mission["current_stage"] = "MONITORING"
            mission["completion_data"] = completion_data
            mission["metadata"]["last_modified"] = datetime.now().isoformat()
            
            # Move to history
            self.mission_history.append(mission)
            del self.active_missions[mission_id]
            
            # Archive mission file
            mission_file = self.missions_dir / f"{mission_id}.json"
            archive_file = self.missions_dir / "archive" / f"{mission_id}_completed.json"
            archive_file.parent.mkdir(exist_ok=True)
            mission_file.rename(archive_file)
            
            logger.info(f"✅ Mission {mission_id} completed and archived")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to complete mission: {e}")
            return False
    
    def get_mission_briefing(self, mission_id: str) -> str:
        """Generate mission briefing using prompt engine"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        return self.prompt_engine.generate_mission_briefing(mission)
    
    def get_execution_plan(self, mission_id: str, phase_id: str = None) -> str:
        """Generate execution plan for mission or specific phase"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        if phase_id:
            return self.prompt_engine.generate_phase_execution_plan(mission, phase_id)
        else:
            return self.prompt_engine.generate_mission_execution_plan(mission)
    
    def get_status_update(self, mission_id: str) -> str:
        """Generate status update for mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        return self.prompt_engine.generate_status_update(mission)
    
    def get_debriefing(self, mission_id: str) -> str:
        """Generate debriefing report for completed mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return "Mission not found"
        
        return self.prompt_engine.generate_debriefing(mission)
    
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
                if mission_file.name == "archive":
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

class PromptEngine:
    """Prompt generation engine for mission communication"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def generate_mission_briefing(self, mission: Dict[str, Any]) -> str:
        """Generate mission briefing prompt"""
        template = self.templates.get("mission_briefing", {})
        content = template.get("template_content", "")
        
        # Simple variable replacement (in production, use proper templating engine)
        for key, value in mission.items():
            if isinstance(value, str):
                content = content.replace(f"{{{{{key}}}}}", str(value))
            elif isinstance(value, (int, float)):
                content = content.replace(f"{{{{{key}}}}}", str(value))
        
        return content
    
    def generate_phase_execution_plan(self, mission: Dict[str, Any], phase_id: str) -> str:
        """Generate phase execution plan prompt"""
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
        
        return content
    
    def generate_mission_execution_plan(self, mission: Dict[str, Any]) -> str:
        """Generate overall mission execution plan"""
        return f"🚀 **MISSION EXECUTION PLAN**\n\n**Mission**: {mission.get('mission_name')} ({mission.get('mission_id')})\n\n**Phases**:\n" + \
               "\n".join([f"- Phase {p.get('phase_order')}: {p.get('phase_name')} - {p.get('status')}" 
                          for p in mission.get("execution_plan", {}).get("phases", [])])
    
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
    
    def generate_debriefing(self, mission: Dict[str, Any]) -> str:
        """Generate debriefing prompt"""
        template = self.templates.get("debriefing", {})
        content = template.get("template_content", "")
        
        # Replace variables
        content = content.replace("{{mission_name}}", mission.get("mission_name", ""))
        content = content.replace("{{mission_id}}", mission.get("mission_id", ""))
        content = content.replace("{{mission_type}}", mission.get("mission_type", ""))
        
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
