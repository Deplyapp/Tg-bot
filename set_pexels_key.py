#!/usr/bin/env python3
"""
Script to add Pexels API key to environment
"""

import os

def set_pexels_key():
    """Set Pexels API key in environment file"""
    
    print("🔑 Pexels API Key Setup")
    print("=" * 50)
    print("To get a Pexels API key:")
    print("1. Go to https://www.pexels.com/api/")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print("4. Copy the key below")
    print()
    
    # Get API key from user
    api_key = input("Enter your Pexels API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⏭️ Skipped Pexels setup. Video suggestions will be disabled.")
        return
    
    # Read current .env file
    env_path = ".env"
    try:
        with open(env_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ .env file not found")
        return
    
    # Update PEXELS_API_KEY line
    updated_lines = []
    key_found = False
    
    for line in lines:
        if line.startswith("PEXELS_API_KEY="):
            updated_lines.append(f"PEXELS_API_KEY={api_key}\n")
            key_found = True
        else:
            updated_lines.append(line)
    
    if not key_found:
        updated_lines.append(f"PEXELS_API_KEY={api_key}\n")
    
    # Write back to file
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"✅ Pexels API key added successfully!")
    print("🔄 Please restart the bot for changes to take effect.")
    print()
    print("To test video suggestions:")
    print("1. Generate a script in the bot")
    print("2. Click '🎥 Find Videos' button")
    print("3. Bot should show relevant stock videos")

if __name__ == "__main__":
    set_pexels_key()