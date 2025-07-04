# 🎬 Hindi YouTube Shorts Script Generator Bot

A sophisticated multi-user Telegram AI bot that generates high-retention, fact-based YouTube Shorts scripts in Hindi following the style of "Vigyan Mitra" channel.

## ✨ Features

- **🤖 AI-Powered Script Generation**: Uses Google Gemini AI to create engaging 130-160 word Hindi scripts
- **📱 Multi-User Support**: Handles multiple users simultaneously without blocking
- **⚡ Streaming Responses**: Real-time sentence-by-sentence script delivery with typing indicators
- **🔑 API Key Rotation**: Seamless switching between multiple API keys for reliability
- **👑 Admin Panel**: Complete bot management with user statistics and controls
- **🎥 Video Clip Finder**: Suggests relevant stock footage from Pexels API
- **📚 Training System**: Admin can add custom scripts to improve AI performance
- **🗄️ Persistent Storage**: SQLite database for user sessions and script history

## 🚀 Quick Start

### Prerequisites

1. **Telegram Bot Token**: Create a bot with [@BotFather](https://t.me/botfather)
2. **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Pexels API Key** (Optional): Get from [Pexels API](https://www.pexels.com/api/)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hindi-youtube-shorts-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Initialize training data**:
   ```bash
   python add_training_scripts.py
   ```

5. **Start the bot**:
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ | Telegram bot token from BotFather |
| `ADMIN_USER_ID` | ✅ | Telegram user ID for admin access (default: 5482745712) |
| `GEMINI_API_KEY` | ⚠️ | Initial Gemini API key (can be added via admin commands) |
| `PEXELS_API_KEY` | ❌ | Pexels API key for video suggestions |
| `DATABASE_PATH` | ❌ | SQLite database file path (default: bot_data.db) |
| `MAX_CONCURRENT_USERS` | ❌ | Maximum concurrent users (default: 100) |
| `STREAMING_DELAY` | ❌ | Delay between sentences in seconds (default: 1.5) |
| `SCRIPT_MIN_WORDS` | ❌ | Minimum script words (default: 130) |
| `SCRIPT_MAX_WORDS` | ❌ | Maximum script words (default: 160) |

## 📱 Bot Commands

### User Commands
- `/start` - Start the bot and show main menu
- `/help` - Show help information
- `/generate` - Generate a new script
- `/mystats` - View your statistics

### Admin Commands
- `/admin` - Access admin control panel
- `/addkey [API_KEY]` - Add new Gemini API key
- `/removekey [API_KEY]` - Remove API key
- `/keys` - List all active API keys
- `/addscript [SCRIPT]` - Add training script
- `/trainscripts` - View training scripts
- `/stats` - View bot statistics
- `/help_admin` - Show admin help

## 🎯 Script Style

The bot generates scripts following the "Vigyan Mitra" style with:

1. **Hook**: Surprising or shocking opening line
2. **Body**: Step-by-step explanation with analogies
3. **Ending**: Reflective question or thought-provoking statement
4. **Language**: Hindi with naturally mixed English terms
5. **Length**: 130-160 words for 40-60 second videos
6. **Topics**: Real science facts with storytelling

### Example Output
```
क्या आप जानते हैं कि स्पेस में एक छोटा सा नाखून... किसी की जान भी ले सकता है?
ज़ीरो ग्रैविटी में कटे हुए नाखून हवा में तैरते हैं। अगर ये किसी मशीन में चले जाएं, तो बड़ा नुकसान कर सकते हैं। NASA इस समस्या से बचने के लिए हाथों को बैग में रखकर नाखून कटवाता है।
अब सोचिए, जो चीज़ हमें रोज़ बेड के किनारे काटनी होती है... वही स्पेस में इतनी बड़ी मुसीबत बन सकती है!
```

## 🏗️ Architecture

### Core Components

1. **Bot Core** (`main.py`): Entry point and initialization
2. **Configuration** (`config.py`): Environment-based settings
3. **Database Layer** (`bot/database.py`): SQLite operations
4. **AI Integration** (`bot/gemini_client.py`): Gemini AI with streaming
5. **User Handlers** (`bot/handlers.py`): Main user interactions
6. **Admin Panel** (`bot/admin.py`): Bot management
7. **Video Finder** (`bot/video_finder.py`): Stock media suggestions
8. **Utilities** (`bot/utils.py`): Helper functions

### Database Schema

- **api_keys**: API key management with usage tracking
- **user_sessions**: User profiles and activity
- **generated_scripts**: Script history and analytics
- **training_scripts**: Custom training data for AI

## 🔄 API Key Rotation

The bot supports multiple API keys for reliability:

1. **Automatic Rotation**: Keys are used in round-robin fashion
2. **Usage Tracking**: Monitors API key usage and performance
3. **Fallback Handling**: Switches keys on rate limits or errors
4. **Admin Management**: Add/remove keys via Telegram commands

## 🎥 Video Integration

Integration with Pexels API for stock footage:

1. **Keyword Extraction**: Analyzes script content
2. **Smart Search**: Finds relevant videos and images
3. **Quality Filtering**: Prioritizes HD content
4. **Format Optimization**: Suggests portrait videos for Shorts

## 🐳 Docker Deployment

Build and run with Docker:

```bash
# Build image
docker build -t hindi-shorts-bot .

# Run container
docker run -d \
  --name shorts-bot \
  -e BOT_TOKEN=your_token \
  -e GEMINI_API_KEY=your_key \
  -e ADMIN_USER_ID=your_id \
  -v $(pwd)/data:/app/data \
  hindi-shorts-bot
```

## 📊 Monitoring

### Bot Statistics
- Total users and scripts generated
- API key usage and performance
- Top users and script topics
- System health and errors

### Logs
- Structured logging with timestamps
- Error tracking and debugging
- Performance monitoring
- User activity tracking

## 🧪 Testing

Run the test suite:

```bash
# Test bot components
python test_bot.py

# Test specific features
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if needed
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the admin via Telegram
- Check the troubleshooting guide

## 🙏 Acknowledgments

- **Vigyan Mitra** YouTube channel for script style inspiration
- **Google Gemini AI** for powerful language generation
- **Pexels** for stock video and image resources
- **aiogram** for excellent Telegram bot framework

---

Made with ❤️ for creating engaging Hindi science content