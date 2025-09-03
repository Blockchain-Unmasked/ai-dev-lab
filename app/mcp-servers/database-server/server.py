#!/usr/bin/env python3
"""
Database MCP Server for AI Intake/Support Agent Demo
Provides persistent storage for conversations, users, and metrics
"""

import json
import sqlite3
import logging
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseMCPServer:
    """MCP Server for database operations"""
    
    def __init__(self):
        self.server = Server("ai-dev-lab-database")
        self.db_path = "demo_database.db"
        self.setup_database()
        self.setup_capabilities()
        self.setup_handlers()
    
    def setup_database(self):
        """Initialize SQLite database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                name TEXT,
                created_at TIMESTAMP,
                preferences TEXT
            )
        ''')
        
        # A/B Testing metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_testing_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id TEXT,
                variant TEXT,
                metric_name TEXT,
                metric_value REAL,
                timestamp TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Database initialized successfully")
    
    def setup_capabilities(self):
        """Setup server capabilities"""
        self.server.capabilities = {
            "tools": {
                "store_conversation": Tool(
                    name="store_conversation",
                    description="Store a new conversation in the database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "conversation_id": {"type": "string"},
                            "user_id": {"type": "string"},
                            "initial_message": {"type": "string"}
                        },
                        "required": ["conversation_id", "user_id"]
                    }
                ),
                "add_message": Tool(
                    name="add_message",
                    description="Add a message to an existing conversation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "conversation_id": {"type": "string"},
                            "role": {"type": "string"},
                            "content": {"type": "string"},
                            "metadata": {"type": "object"}
                        },
                        "required": ["conversation_id", "role", "content"]
                    }
                ),
                "get_conversation": Tool(
                    name="get_conversation",
                    description="Retrieve a conversation with all messages",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "conversation_id": {"type": "string"}
                        },
                        "required": ["conversation_id"]
                    }
                ),
                "save_user_profile": Tool(
                    name="save_user_profile",
                    description="Save or update user profile information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "email": {"type": "string"},
                            "name": {"type": "string"},
                            "preferences": {"type": "object"}
                        },
                        "required": ["user_id"]
                    }
                ),
                "record_ab_metric": Tool(
                    name="record_ab_metric",
                    description="Record A/B testing metric data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_id": {"type": "string"},
                            "variant": {"type": "string"},
                            "metric_name": {"type": "string"},
                            "metric_value": {"type": "number"},
                            "metadata": {"type": "object"}
                        },
                        "required": ["test_id", "variant", "metric_name", "metric_value"]
                    }
                ),
                "health": Tool(
                    name="health",
                    description="Health check endpoint - always succeeds",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                "export_conversation_data": Tool(
                    name="export_conversation_data",
                    description="Export conversation data in various formats",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "conversation_id": {"type": "string"},
                            "format": {"type": "string", "enum": ["json", "csv", "txt"]}
                        },
                        "required": ["conversation_id", "format"]
                    }
                )
            },
            "resources": {
                "conversations": Resource(
                    uri="db://conversations",
                    name="Conversations Database",
                    description="Access to stored conversations and messages",
                    mimeType="application/json"
                ),
                "users": Resource(
                    uri="db://users",
                    name="Users Database",
                    description="User profiles and preferences",
                    mimeType="application/json"
                ),
                "metrics": Resource(
                    uri="db://metrics",
                    name="Metrics Database",
                    description="A/B testing and performance metrics",
                    mimeType="application/json"
                )
            }
        }
    
    def setup_handlers(self):
        """Setup server event handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return list(self.server.capabilities["tools"].values())
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
            logger.info(f"Tool called: {name} with args: {arguments}")
            
            if name == "store_conversation":
                return await self.store_conversation(arguments)
            elif name == "add_message":
                return await self.add_message(arguments)
            elif name == "get_conversation":
                return await self.get_conversation(arguments)
            elif name == "save_user_profile":
                return await self.save_user_profile(arguments)
            elif name == "record_ab_metric":
                return await self.record_ab_metric(arguments)
            elif name == "export_conversation_data":
                return await self.export_conversation_data(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            return list(self.server.capabilities["resources"].values())
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            if uri == "db://conversations":
                return self.get_conversations_summary()
            elif uri == "db://users":
                return self.get_users_summary()
            elif uri == "db://metrics":
                return self.get_metrics_summary()
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
    async def store_conversation(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Store a new conversation"""
        conversation_id = args["conversation_id"]
        user_id = args["user_id"]
        initial_message = args.get("initial_message", "")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert conversation
            cursor.execute('''
                INSERT INTO conversations (id, user_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (conversation_id, user_id, datetime.now(), datetime.now()))
            
            # Insert initial message if provided
            if initial_message:
                cursor.execute('''
                    INSERT INTO messages (conversation_id, role, content, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (conversation_id, "user", initial_message, datetime.now()))
            
            conn.commit()
            return {"success": True, "conversation_id": conversation_id}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
    
    async def add_message(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a message to a conversation"""
        conversation_id = args["conversation_id"]
        role = args["role"]
        content = args["content"]
        metadata = args.get("metadata", {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert message
            cursor.execute('''
                INSERT INTO messages (conversation_id, role, content, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (conversation_id, role, content, datetime.now(), json.dumps(metadata)))
            
            # Update conversation timestamp
            cursor.execute('''
                UPDATE conversations SET updated_at = ? WHERE id = ?
            ''', (datetime.now(), conversation_id))
            
            conn.commit()
            return {"success": True, "message_added": True}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
    
    async def get_conversation(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve a conversation with all messages"""
        conversation_id = args["conversation_id"]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get conversation details
            cursor.execute('''
                SELECT * FROM conversations WHERE id = ?
            ''', (conversation_id,))
            conversation = cursor.fetchone()
            
            if not conversation:
                return {"success": False, "error": "Conversation not found"}
            
            # Get all messages
            cursor.execute('''
                SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp
            ''', (conversation_id,))
            messages = cursor.fetchall()
            
            return {
                "success": True,
                "conversation": {
                    "id": conversation[0],
                    "user_id": conversation[1],
                    "created_at": conversation[2],
                    "updated_at": conversation[3],
                    "status": conversation[4],
                    "messages": [
                        {
                            "role": msg[2],
                            "content": msg[3],
                            "timestamp": msg[4],
                            "metadata": json.loads(msg[5]) if msg[5] else {}
                        }
                        for msg in messages
                    ]
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
    
    async def save_user_profile(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update user profile"""
        user_id = args["user_id"]
        email = args.get("email")
        name = args.get("name")
        preferences = args.get("preferences", {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO users (id, email, name, created_at, preferences)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, email, name, datetime.now(), json.dumps(preferences)))
            
            conn.commit()
            return {"success": True, "user_id": user_id}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
    
    async def record_ab_metric(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Record A/B testing metric"""
        test_id = args["test_id"]
        variant = args["variant"]
        metric_name = args["metric_name"]
        metric_value = args["metric_value"]
        metadata = args.get("metadata", {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO ab_testing_metrics (test_id, variant, metric_name, metric_value, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (test_id, variant, metric_name, metric_value, datetime.now(), json.dumps(metadata)))
            
            conn.commit()
            return {"success": True, "metric_recorded": True}
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
    
    async def export_conversation_data(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Export conversation data in specified format"""
        conversation_id = args["conversation_id"]
        export_format = args["format"]
        
        # Get conversation data
        conversation_data = await self.get_conversation({"conversation_id": conversation_id})
        
        if not conversation_data["success"]:
            return conversation_data
        
        conversation = conversation_data["conversation"]
        
        if export_format == "json":
            return {"success": True, "data": json.dumps(conversation, indent=2), "format": "json"}
        elif export_format == "csv":
            # Convert to CSV format
            csv_data = "timestamp,role,content\n"
            for message in conversation["messages"]:
                csv_data += f"{message['timestamp']},{message['role']},{message['content']}\n"
            return {"success": True, "data": csv_data, "format": "csv"}
        elif export_format == "txt":
            # Convert to plain text
            txt_data = f"Conversation: {conversation_id}\n"
            txt_data += f"User: {conversation['user_id']}\n"
            txt_data += f"Created: {conversation['created_at']}\n\n"
            
            for message in conversation["messages"]:
                txt_data += f"[{message['timestamp']}] {message['role'].upper()}: {message['content']}\n"
            
            return {"success": True, "data": txt_data, "format": "txt"}
        else:
            return {"success": False, "error": "Unsupported format"}
    
    def get_conversations_summary(self) -> str:
        """Get summary of all conversations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM messages')
        messages = cursor.fetchone()[0]
        
        conn.close()
        
        return json.dumps({
            "total_conversations": total,
            "total_messages": messages,
            "database_path": self.db_path
        }, indent=2)
    
    def get_users_summary(self) -> str:
        """Get summary of all users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return json.dumps({
            "total_users": total,
            "database_path": self.db_path
        }, indent=2)
    
    def get_metrics_summary(self) -> str:
        """Get summary of all metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM ab_testing_metrics')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return json.dumps({
            "total_metrics": total,
            "database_path": self.db_path
        }, indent=2)

async def main():
    """Main server function"""
    db_server = DatabaseMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await db_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-dev-lab-database",
                server_version="1.0.0",
                capabilities=db_server.server.capabilities
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
