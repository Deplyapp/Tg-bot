"""
Database operations for the Telegram bot
"""

import sqlite3
import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class Database:
    """Database manager for bot data"""
    
    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
    
    async def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # API Keys table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS api_keys (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key_value TEXT UNIQUE NOT NULL,
                        key_type TEXT DEFAULT 'gemini',
                        is_active BOOLEAN DEFAULT 1,
                        usage_count INTEGER DEFAULT 0,
                        last_used TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # User sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        language_preference TEXT DEFAULT 'hindi',
                        script_count INTEGER DEFAULT 0,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Generated scripts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS generated_scripts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        topic TEXT,
                        script_content TEXT,
                        word_count INTEGER,
                        api_key_used TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES user_sessions (user_id)
                    )
                ''')
                
                # Training scripts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS training_scripts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        script_content TEXT NOT NULL,
                        added_by INTEGER,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    async def add_api_key(self, key_value: str, key_type: str = "gemini") -> bool:
        """Add a new API key"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO api_keys (key_value, key_type) VALUES (?, ?)",
                    (key_value, key_type)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            logger.warning(f"API key already exists: {key_value[:10]}...")
            return False
        except Exception as e:
            logger.error(f"Error adding API key: {e}")
            return False
    
    async def remove_api_key(self, key_value: str) -> bool:
        """Remove an API key"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM api_keys WHERE key_value = ?", (key_value,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error removing API key: {e}")
            return False
    
    async def get_active_api_keys(self, key_type: str = "gemini") -> List[Dict[str, Any]]:
        """Get all active API keys"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM api_keys WHERE is_active = 1 AND key_type = ? ORDER BY usage_count ASC",
                    (key_type,)
                )
                keys = cursor.fetchall()
                
                # Convert to dict format
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, key)) for key in keys]
        except Exception as e:
            logger.error(f"Error getting API keys: {e}")
            return []
    
    async def update_key_usage(self, key_value: str) -> bool:
        """Update API key usage count"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE api_keys SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP WHERE key_value = ?",
                    (key_value,)
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating key usage: {e}")
            return False
    
    async def create_user_session(self, user_id: int, username: str = None, 
                                 first_name: str = None, last_name: str = None) -> bool:
        """Create or update user session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO user_sessions 
                    (user_id, username, first_name, last_name, last_activity)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (user_id, username, first_name, last_name))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error creating user session: {e}")
            return False
    
    async def save_generated_script(self, user_id: int, topic: str, 
                                   script_content: str, word_count: int, 
                                   api_key_used: str) -> bool:
        """Save generated script to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO generated_scripts 
                    (user_id, topic, script_content, word_count, api_key_used)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, topic, script_content, word_count, api_key_used))
                
                # Update user script count
                cursor.execute(
                    "UPDATE user_sessions SET script_count = script_count + 1 WHERE user_id = ?",
                    (user_id,)
                )
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving generated script: {e}")
            return False
    
    async def add_training_script(self, script_content: str, added_by: int) -> bool:
        """Add a training script"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO training_scripts (script_content, added_by) VALUES (?, ?)",
                    (script_content, added_by)
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding training script: {e}")
            return False
    
    async def get_training_scripts(self) -> List[str]:
        """Get all active training scripts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT script_content FROM training_scripts WHERE is_active = 1"
                )
                scripts = cursor.fetchall()
                return [script[0] for script in scripts]
        except Exception as e:
            logger.error(f"Error getting training scripts: {e}")
            return []
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM user_sessions WHERE user_id = ?",
                    (user_id,)
                )
                user_data = cursor.fetchone()
                
                if user_data:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, user_data))
                return {}
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}


# Global database instance
db = Database()

async def init_database():
    """Initialize database"""
    await db.init_database()
