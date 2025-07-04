#!/usr/bin/env python3
"""
Sophisticated Multi-User Telegram AI Bot for Hindi YouTube Shorts Scripts
Author: AI Assistant
"""

import asyncio
import logging
import os
from typing import Dict, Any

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import register_handlers
from bot.admin import register_admin_handlers
from bot.database import init_database
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Initialize configuration
    config = Config()
    
    # Initialize database
    await init_database()
    
    # Add initial API key if provided in environment
    if config.GEMINI_API_KEY:
        from bot.database import db
        await db.add_api_key(config.GEMINI_API_KEY, "gemini")
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Register handlers
    register_handlers(dp)
    register_admin_handlers(dp)
    
    # Store config in bot data for access in handlers
    dp["config"] = config
    
    logger.info("Bot starting...")
    
    try:
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
