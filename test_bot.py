#!/usr/bin/env python3
"""
Test script to verify bot functionality
"""

import asyncio
import sqlite3
from bot.database import db
from bot.gemini_client import gemini_client

async def test_bot():
    """Test bot components"""
    print("🔍 Testing bot components...")
    
    # Test database
    print("\n1. Testing database connection...")
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM api_keys WHERE is_active = 1")
            active_keys = cursor.fetchone()[0]
            print(f"   ✅ Active API keys: {active_keys}")
            
            cursor.execute("SELECT COUNT(*) FROM training_scripts WHERE is_active = 1")
            training_scripts = cursor.fetchone()[0]
            print(f"   ✅ Training scripts: {training_scripts}")
            
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    # Test API keys
    print("\n2. Testing API key retrieval...")
    try:
        keys = await db.get_active_api_keys("gemini")
        print(f"   ✅ Found {len(keys)} active Gemini API keys")
        if keys:
            print(f"   ✅ First key preview: {keys[0]['key_value'][:10]}...")
    except Exception as e:
        print(f"   ❌ API key error: {e}")
    
    # Test script generation
    print("\n3. Testing script generation...")
    try:
        result = await gemini_client.generate_script("स्पेस में खाना")
        if result['success']:
            print(f"   ✅ Script generated successfully!")
            print(f"   ✅ Word count: {result['word_count']}")
            print(f"   ✅ Script preview: {result['script'][:100]}...")
        else:
            print(f"   ❌ Script generation failed: {result['error']}")
    except Exception as e:
        print(f"   ❌ Script generation error: {e}")
    
    print("\n🎉 Bot testing complete!")

if __name__ == "__main__":
    asyncio.run(test_bot())