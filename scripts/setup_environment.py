#!/usr/bin/env python3
"""
AI/DEV Lab - Environment Setup Script
Sets up environment configuration, secrets, and dot files
"""

import os
import sys
import json
import shutil
from pathlib import Path

def setup_environment():
    """Main environment setup function"""
    print("🏗️ AI/DEV Lab Environment Setup")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"📁 Project root: {project_root}")
    
    # Create necessary directories
    create_directories(project_root)
    
    # Setup environment files
    setup_env_files(project_root)
    
    # Setup secrets management
    setup_secrets_management(project_root)
    
    # Setup configuration files
    setup_config_files(project_root)
    
    # Validate setup
    validate_setup(project_root)
    
    print("\n✅ Environment setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy app/env.example to app/.env and configure your values")
    print("2. Copy app/frontend/env.example.js to app/frontend/env.js")
    print("3. Set up your API keys and secrets")
    print("4. Run the app: cd app && python3 -m uvicorn backend.main:app --reload")

def create_directories(project_root: Path):
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "app/secrets",
        "app/storage",
        "app/logs",
        "app/backups",
        "app/database/migrations",
        "app/database/schemas",
        "app/database/seeds",
        "app/backend/uploads",
        "app/frontend/assets/images",
        "app/deployment/ssl",
        "logs/audits",
        "logs/missions",
        "logs/development"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created: {directory}")
        
    # Create .gitkeep files in empty directories
    gitkeep_dirs = [
        "app/secrets",
        "app/storage",
        "app/backups",
        "app/database/migrations",
        "app/database/schemas",
        "app/database/seeds",
        "app/backend/uploads",
        "app/frontend/assets/images",
        "app/deployment/ssl"
    ]
    
    for directory in gitkeep_dirs:
        gitkeep_file = project_root / directory / ".gitkeep"
        if not gitkeep_file.exists():
            gitkeep_file.touch()
            print("  📝 Added .gitkeep to: " + directory)

def setup_env_files(project_root: Path):
    """Setup environment configuration files"""
    print("\n🔧 Setting up environment files...")
    
    # Create .env file from example if it doesn't exist
    env_example = project_root / "app" / "env.example"
    env_file = project_root / "app" / ".env"
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print(f"  ✅ Created: app/.env from example")
        
        # Update .env with project-specific values
        update_env_file(env_file, project_root)
    else:
        print(f"  ℹ️  Environment file already exists: app/.env")
    
    # Create frontend env.js from example if it doesn't exist
    frontend_env_example = project_root / "app" / "frontend" / "env.example.js"
    frontend_env_file = project_root / "app" / "frontend" / "env.js"
    
    if not frontend_env_file.exists() and frontend_env_example.exists():
        shutil.copy(frontend_env_example, frontend_env_file)
        print(f"  ✅ Created: app/frontend/env.js from example")
    else:
        print(f"  ℹ️  Frontend environment file already exists: app/frontend/env.js")

def update_env_file(env_file: Path, project_root: Path):
    """Update .env file with project-specific values"""
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update paths to be relative to project root
        content = content.replace(
            "app/database/demo_database.db",
            str(project_root / "app" / "database" / "demo_database.db")
        )
        content = content.replace(
            "app/logs/app.log",
            str(project_root / "app" / "logs" / "app.log")
        )
        content = content.replace(
            "app/storage/",
            str(project_root / "app" / "storage" / "")
        )
        content = content.replace(
            "app/backups/",
            str(project_root / "app" / "backups" / "")
        )
        
        with open(env_file, 'w') as f:
            f.write(content)
            
        print(f"  🔧 Updated .env with project-specific paths")
        
    except Exception as e:
        print(f"  ⚠️  Warning: Could not update .env file: {e}")

def setup_secrets_management(project_root: Path):
    """Setup secrets management system"""
    print("\n🔐 Setting up secrets management...")
    
    secrets_dir = project_root / "app" / "secrets"
    secrets_file = secrets_dir / "secrets.json"
    
    if not secrets_file.exists():
        # Create initial secrets structure
        initial_secrets = {
            "app": {
                "secret_key": "dev-secret-key-change-in-production",
                "jwt_secret": "dev-jwt-secret-change-in-production"
            },
            "api_keys": {
                "gemini": "",
                "openai": "",
                "anthropic": ""
            },
            "mcp_servers": {
                "lab_server_api_key": "",
                "app_server_api_key": ""
            },
            "database": {
                "user": "",
                "password": ""
            },
            "external_services": {
                "webhook_url": "",
                "slack_webhook": ""
            }
        }
        
        with open(secrets_file, 'w') as f:
            json.dump(initial_secrets, f, indent=2)
            
        print(f"  ✅ Created: app/secrets/secrets.json")
    else:
        print(f"  ℹ️  Secrets file already exists: app/secrets/secrets.json")
    
    # Create .gitignore for secrets directory
    gitignore_file = secrets_dir / ".gitignore"
    if not gitignore_file.exists():
        with open(gitignore_file, 'w') as f:
            f.write("# Secrets directory - NEVER commit secrets\n")
            f.write("*.json\n")
            f.write("*.key\n")
            f.write("*.pem\n")
            f.write("*.p12\n")
            f.write("*.pfx\n")
            f.write("!example.json\n")
            
        print(f"  ✅ Created: app/secrets/.gitignore")

def setup_config_files(project_root: Path):
    """Setup configuration files"""
    print("\n⚙️  Setting up configuration files...")
    
    # Create app configuration
    config_dir = project_root / "app" / "backend" / "core"
    config_file = config_dir / "config.py"
    
    if not config_file.exists():
        print(f"  ⚠️  Warning: Configuration file not found: {config_file}")
        print(f"     Please ensure the backend core module is properly set up")
    else:
        print(f"  ✅ Configuration file exists: {config_file}")
    
    # Create database configuration
    db_config_file = project_root / "app" / "database" / "config.py"
    if not db_config_file.exists():
        create_database_config(db_config_file)
        print(f"  ✅ Created: app/database/config.py")
    else:
        print(f"  ℹ️  Database config already exists: app/database/config.py")

def create_database_config(db_config_file: Path):
    """Create database configuration file"""
    config_content = '''#!/usr/bin/env python3
"""
AI/DEV Lab App - Database Configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(".env")
if env_path.exists():
    load_dotenv(env_path)

class DatabaseConfig:
    """Database configuration settings"""
    
    def __init__(self):
        self.type = os.getenv("DATABASE_TYPE", "sqlite")
        self.url = os.getenv("DATABASE_URL", "sqlite:///app/database/demo_database.db")
        self.host = os.getenv("DATABASE_HOST", "localhost")
        self.port = int(os.getenv("DATABASE_PORT", "5432"))
        self.name = os.getenv("DATABASE_NAME", "ai_dev_lab_demo")
        self.user = os.getenv("DATABASE_USER", "")
        self.password = os.getenv("DATABASE_PASSWORD", "")
        self.ssl_mode = os.getenv("DATABASE_SSL_MODE", "prefer")
    
    def get_connection_string(self) -> str:
        """Get database connection string"""
        if self.type == "sqlite":
            return self.url
        elif self.type == "postgresql":
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        else:
            raise ValueError(f"Unsupported database type: {self.type}")

# Global database config instance
db_config = DatabaseConfig()
'''
    
    with open(db_config_file, 'w') as f:
        f.write(config_content)

def validate_setup(project_root: Path):
    """Validate the environment setup"""
    print("\n🔍 Validating setup...")
    
    # Check required files
    required_files = [
        "app/.env",
        "app/frontend/env.js",
        "app/secrets/secrets.json",
        "app/secrets/.gitignore"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
    
    # Check required directories
    required_dirs = [
        "app/secrets",
        "app/storage",
        "app/logs",
        "app/backups",
        "app/database/migrations"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not (project_root / dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"  ❌ Missing directories: {missing_dirs}")
        return False
    
    print(f"  ✅ All required files and directories exist")
    
    # Check .gitignore
    gitignore_file = project_root / ".gitignore"
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            content = f.read()
            if ".env" in content and "secrets/" in content:
                print(f"  ✅ .gitignore properly configured")
            else:
                print(f"  ⚠️  Warning: .gitignore may not include all necessary exclusions")
    else:
        print(f"  ❌ .gitignore file not found")
    
    return True

def main():
    """Main function"""
    try:
        setup_environment()
        return 0
    except Exception as e:
        print(f"\n❌ Environment setup failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
