# Hindi YouTube Shorts Script Generator Bot

## Overview

This is a sophisticated multi-user Telegram bot designed to generate Hindi YouTube Shorts scripts using AI. The bot leverages Google's Gemini AI to create engaging, fact-based scripts in Hindi that follow specific formatting and storytelling patterns. It includes features for video clip suggestions, user management, and admin controls.

## System Architecture

### Backend Architecture
- **Framework**: Python with aiogram (Telegram Bot API library)
- **AI Integration**: Google Gemini AI for script generation
- **Database**: SQLite for local data storage
- **Async Processing**: Full asynchronous architecture using asyncio
- **Configuration**: Environment-based configuration management

### Key Components

#### 1. Bot Core (`main.py`)
- Entry point for the application
- Initializes bot, dispatcher, and database
- Registers handlers for user and admin interactions

#### 2. Configuration Management (`config.py`)
- Centralized configuration using environment variables
- Validates required API keys and settings
- Manages bot parameters like concurrent users, script word limits

#### 3. Database Layer (`bot/database.py`)
- SQLite database for persistent storage
- Tables for API keys, user sessions, generated scripts, and training data
- Async database operations with proper connection management

#### 4. AI Integration (`bot/gemini_client.py`)
- Google Gemini AI client with API key rotation
- Streaming response support for real-time script generation
- Built-in system prompt optimized for Hindi YouTube Shorts
- Reference scripts for consistent style and tone

#### 5. User Handlers (`bot/handlers.py`)
- Main user interaction flow
- State management for script generation process
- Topic suggestions and user statistics
- Script formatting and display optimization

#### 6. Admin Panel (`bot/admin.py`)
- Admin-only commands and controls
- API key management
- User statistics and system monitoring
- Broadcast messaging capabilities

#### 7. Video Integration (`bot/video_finder.py`)
- Pexels API integration for stock video suggestions
- Keyword extraction from generated scripts
- Video and image search functionality

#### 8. Utilities (`bot/utils.py`)
- Helper functions for text formatting
- Hindi word counting
- API key validation
- User permission checks

## Data Flow

1. **User Input**: User sends topic or uses suggestion
2. **Processing**: Bot validates input and checks user permissions
3. **AI Generation**: Gemini AI generates script using system prompt
4. **Formatting**: Script is formatted for Telegram display
5. **Storage**: Generated script is stored in database
6. **Response**: Formatted script is sent to user with options
7. **Video Suggestions**: Optional video clips are suggested based on script content

## External Dependencies

### Required APIs
- **Telegram Bot API**: For bot communication
- **Google Gemini AI**: For script generation
- **Pexels API**: For stock video/image suggestions (optional)

### Python Libraries
- `aiogram`: Telegram bot framework
- `google-genai`: Google Gemini AI client
- `aiohttp`: Async HTTP client
- `sqlite3`: Database operations
- `python-dotenv`: Environment variable management

## Deployment Strategy

### Environment Variables Required
- `BOT_TOKEN`: Telegram bot token
- `GEMINI_API_KEY`: Google Gemini AI API key
- `ADMIN_USER_ID`: Telegram user ID for admin access
- `PEXELS_API_KEY`: Pexels API key (optional)
- `DATABASE_PATH`: SQLite database file path
- `MAX_CONCURRENT_USERS`: Maximum concurrent users
- `SCRIPT_MIN_WORDS`: Minimum words in generated script
- `SCRIPT_MAX_WORDS`: Maximum words in generated script

### Database Setup
- SQLite database auto-initializes on first run
- No external database server required
- Database includes tables for users, scripts, API keys, and training data

### Bot Features
- Multi-user support with session management
- Admin panel for monitoring and control
- API key rotation for reliability
- Streaming responses for better UX
- Hindi script generation with specific formatting
- Video clip suggestions
- User statistics and analytics

## Recent Changes
- July 03, 2025. Complete bot implementation with:
  - Multi-user Telegram bot with streaming responses
  - Google Gemini AI integration with API key rotation
  - SQLite database with user sessions and training scripts
  - Admin panel with comprehensive management features
  - Pexels API integration for video clip suggestions
  - Web status interface running on port 5000
  - 12 default training scripts in Vigyan Mitra style
  - Docker deployment configuration
  - Comprehensive README and documentation

## User Preferences

Preferred communication style: Simple, everyday language.
API Keys provided: BOT_TOKEN and GEMINI_API_KEY configured
Admin User ID: 5482745712