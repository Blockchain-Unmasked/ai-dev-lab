#!/usr/bin/env python3
"""
AI/DEV Lab App - Secrets Management Module
Handles API keys, secrets, and sensitive configuration
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class SecretsManager:
    """Manages application secrets and sensitive data"""
    
    def __init__(self, secrets_file: str = "app/secrets/secrets.json"):
        self.secrets_file = Path(secrets_file)
        self.secrets_dir = self.secrets_file.parent
        self.secrets: Dict[str, Any] = {}
        self._ensure_secrets_directory()
        self._load_secrets()
        
    def _ensure_secrets_directory(self):
        """Ensure secrets directory exists"""
        self.secrets_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_secrets(self):
        """Load secrets from file"""
        if self.secrets_file.exists():
            try:
                with open(self.secrets_file, 'r') as f:
                    self.secrets = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load secrets file: {e}")
                self.secrets = {}
        else:
            self.secrets = {}
            
    def _save_secrets(self):
        """Save secrets to file"""
        try:
            with open(self.secrets_file, 'w') as f:
                json.dump(self.secrets, f, indent=2)
        except Exception as e:
            print(f"Error saving secrets: {e}")
            
    def get_secret(self, key: str, default: Any = None) -> Any:
        """Get a secret value"""
        return self.secrets.get(key, default)
        
    def set_secret(self, key: str, value: Any):
        """Set a secret value"""
        self.secrets[key] = value
        self._save_secrets()
        
    def delete_secret(self, key: str):
        """Delete a secret"""
        if key in self.secrets:
            del self.secrets[key]
            self._save_secrets()
            
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service"""
        return self.get_secret(f"{service}_api_key")
        
    def set_api_key(self, service: str, api_key: str):
        """Set API key for a specific service"""
        self.set_secret(f"{service}_api_key", api_key)
        
    def list_secrets(self) -> list:
        """List all secret keys"""
        return list(self.secrets.keys())
        
    def export_secrets(self, filepath: str):
        """Export secrets to a file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.secrets, f, indent=2)
            print(f"Secrets exported to {filepath}")
        except Exception as e:
            print(f"Error exporting secrets: {e}")
            
    def import_secrets(self, filepath: str):
        """Import secrets from a file"""
        try:
            with open(filepath, 'r') as f:
                imported_secrets = json.load(f)
            self.secrets.update(imported_secrets)
            self._save_secrets()
            print(f"Secrets imported from {filepath}")
        except Exception as e:
            print(f"Error importing secrets: {e}")

# Global secrets manager instance
secrets_manager = SecretsManager()

def get_secret(key: str, default: Any = None) -> Any:
    """Get a secret value"""
    return secrets_manager.get_secret(key, default)
    
def set_secret(key: str, value: Any):
    """Set a secret value"""
    secrets_manager.set_secret(key, value)
    
def get_api_key(service: str) -> Optional[str]:
    """Get API key for a specific service"""
    return secrets_manager.get_api_key(service)
    
def set_api_key(service: str, api_key: str):
    """Set API key for a specific service"""
    secrets_manager.set_api_key(service, api_key)
