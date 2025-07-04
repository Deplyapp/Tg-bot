"""
Utility functions for the bot
"""

import re
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def format_script_for_display(script: str) -> str:
    """Format script for better display in Telegram"""
    # Add line breaks for better readability
    formatted = script.replace('. ', '.\n\n')
    formatted = formatted.replace('? ', '?\n\n')
    formatted = formatted.replace('! ', '!\n\n')
    formatted = formatted.replace('। ', '।\n\n')
    
    return formatted.strip()


def extract_topic_from_script(script: str) -> str:
    """Extract topic from script for better organization"""
    # Try to extract from first sentence
    sentences = script.split('.')
    if sentences:
        first_sentence = sentences[0].strip()
        # Remove common question starters
        topic = re.sub(r'^(क्या आप जानते हैं|क्या आप|क्या)', '', first_sentence).strip()
        return topic[:50] + "..." if len(topic) > 50 else topic
    
    return "Science Topic"


def count_words_hindi(text: str) -> int:
    """Count words in Hindi/English mixed text"""
    # Split by spaces and count non-empty tokens
    words = text.split()
    return len([word for word in words if word.strip()])


def validate_api_key(key: str, key_type: str = "gemini") -> bool:
    """Validate API key format"""
    if key_type == "gemini":
        # Gemini API keys usually start with 'AIza'
        return key.startswith('AIza') and len(key) > 30
    elif key_type == "pexels":
        # Pexels API keys are typically 563492ad6f9170000100000112345678 format
        return len(key) >= 32 and key.replace('-', '').isalnum()
    
    return len(key) > 10  # Basic validation


def format_media_info(media_list: List[Dict[str, Any]]) -> str:
    """Format media information for display"""
    if not media_list:
        return "No media found"
    
    formatted = []
    for i, media in enumerate(media_list, 1):
        media_type = media.get('type', 'unknown')
        title = media.get('title', 'Untitled')
        keyword = media.get('keyword', '')
        
        formatted.append(f"{i}. {title} ({media_type})")
        if keyword:
            formatted.append(f"   Keyword: {keyword}")
    
    return '\n'.join(formatted)


def create_progress_bar(current: int, total: int, length: int = 10) -> str:
    """Create a simple progress bar"""
    filled = int(length * current / total)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {current}/{total}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe saving"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    return filename[:100]


def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp


def create_topic_suggestions() -> List[str]:
    """Create topic suggestions for users"""
    return [
        "स्पेस में जीवन",
        "समुंदर के रहस्य",
        "दिमाग की शक्ति",
        "भविष्य की तकनीक",
        "जापानी साइंस",
        "NASA के प्रयोग",
        "इंसानी शरीर",
        "अंतरिक्ष यान",
        "वैज्ञानिक खोज",
        "टेक्नोलॉजी के चमत्कार"
    ]


def is_admin(user_id: int, admin_id: int = 5482745712) -> bool:
    """Check if user is admin"""
    return user_id == admin_id


def generate_user_report(user_stats: Dict[str, Any]) -> str:
    """Generate user activity report"""
    if not user_stats:
        return "No user data available"
    
    report = f"📊 User Statistics\n\n"
    report += f"User ID: {user_stats.get('user_id', 'N/A')}\n"
    report += f"Username: @{user_stats.get('username', 'N/A')}\n"
    report += f"Scripts Generated: {user_stats.get('script_count', 0)}\n"
    report += f"Language: {user_stats.get('language_preference', 'Hindi')}\n"
    report += f"Member Since: {format_timestamp(user_stats.get('created_at', ''))}\n"
    report += f"Last Activity: {format_timestamp(user_stats.get('last_activity', ''))}\n"
    
    return report


def create_help_text() -> str:
    """Create help text for users"""
    return """
🤖 <b>Hindi YouTube Shorts Script Generator</b>

📝 <b>Available Commands:</b>
• <code>/start</code> - Start the bot
• <code>/help</code> - Show this help message
• <code>/generate</code> - Generate a new script
• <code>/mystats</code> - View your statistics

🎯 <b>Features:</b>
• Generate 130-160 word Hindi scripts
• Streaming sentence-by-sentence delivery
• Topic suggestions and custom topics
• Video clip recommendations
• Multiple language support

🚀 <b>How to use:</b>
1. Click "Generate Script" button
2. Choose a topic or enter custom topic
3. Watch as script is generated live
4. Get video clip suggestions
5. Regenerate if needed

📞 <b>Need help?</b> Contact admin for support.
"""


def create_admin_help() -> str:
    """Create admin help text"""
    return """
🔧 <b>Admin Commands</b>

🔑 <b>API Key Management:</b>
• <code>/addkey [API_KEY]</code> - Add new Gemini API key
• <code>/removekey [API_KEY]</code> - Remove API key
• <code>/keys</code> - List all active keys

📚 <b>Training Management:</b>
• <code>/addscript [SCRIPT]</code> - Add training script
• <code>/trainscripts</code> - View training scripts

📊 <b>Statistics:</b>
• <code>/stats</code> - Bot usage statistics
• <code>/users</code> - Active users count

⚙️ <b>Bot Control:</b>
• <code>/broadcast [MESSAGE]</code> - Send message to all users
• <code>/maintenance</code> - Toggle maintenance mode
"""
