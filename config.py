"""
Configuration settings for the Telegram bot
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for bot settings"""
    
    # Bot configuration
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Admin configuration
    ADMIN_USER_ID: int = int(os.getenv("ADMIN_USER_ID", "5482745712"))
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    PEXELS_API_KEY: str = os.getenv("PEXELS_API_KEY", "")
    
    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "bot_data.db")
    
    # Bot settings
    MAX_CONCURRENT_USERS: int = int(os.getenv("MAX_CONCURRENT_USERS", "100"))
    STREAMING_DELAY: float = float(os.getenv("STREAMING_DELAY", "1.5"))
    
    # Script settings
    SCRIPT_MIN_WORDS: int = int(os.getenv("SCRIPT_MIN_WORDS", "130"))
    SCRIPT_MAX_WORDS: int = int(os.getenv("SCRIPT_MAX_WORDS", "160"))
    
    # Pexels settings
    PEXELS_RESULTS_LIMIT: int = int(os.getenv("PEXELS_RESULTS_LIMIT", "5"))
    
    def __init__(self):
        """Initialize configuration and validate required settings"""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        
        # Gemini API key is optional - will be managed through database
        pass
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        return bool(self.BOT_TOKEN)
