# 🔧 Admin Guide - Hindi YouTube Shorts Bot

This guide explains how to manage your bot as an admin user (ID: 5482745712).

## 🎯 Quick Access

Your bot is running at: `@your_all_ai_bot`

**Admin Commands Summary:**
```
/admin - Access admin panel
/addkey [API_KEY] - Add Gemini API key
/removekey [API_KEY] - Remove API key
/keys - View all API keys
/addscript [SCRIPT] - Add training script
/trainscripts - View training scripts
/stats - Bot statistics
```

## 🔑 Managing API Keys

### Adding a New Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Send to bot: `/addkey AIzaSyD...your_key_here`

### Viewing Current Keys
Send: `/keys`

The bot will show:
- Key preview (first 10 + last 4 characters)
- Usage count
- Last used time

### Removing a Key
Send: `/removekey AIzaSyD...full_key_here`

**Note:** The bot automatically rotates between multiple keys for reliability.

## 📚 Managing Training Scripts

### Adding Training Scripts
Training scripts help the AI learn the Vigyan Mitra style better.

Send: `/addscript [YOUR_SCRIPT]`

**Example:**
```
/addscript क्या आप जानते हैं कि चांद पर पानी कैसे मिला? 
NASA के Lunar Reconnaissance Orbiter ने चांद के दक्षिणी ध्रुव पर बर्फ के रूप में पानी खोजा। ये बर्फ अरबों साल पुराने craters में छुपी हुई है जहां सूरज की रोशनी कभी नहीं पहुंचती।
अब सोचिए, जो पानी धरती पर जीवन देता है वही चांद पर भविष्य के अंतरिक्ष मिशन का आधार बन सकता है!
```

### Viewing Training Scripts
Send: `/trainscripts`

**Current Training Scripts:** 12 default scripts are already loaded.

### Training Script Guidelines
- Minimum 50 characters
- Follow Vigyan Mitra style:
  - Start with surprising question
  - Scientific explanation in middle
  - End with thought-provoking question
- Use Hindi with natural English terms
- Real science facts only

## 🎥 Setting Up Pexels (Video Suggestions)

### Getting Pexels API Key
1. Go to [Pexels API](https://www.pexels.com/api/)
2. Sign up and get your API key
3. Add it to your environment:

**Option 1: Edit .env file**
```bash
PEXELS_API_KEY=your_pexels_key_here
```

**Option 2: Set environment variable**
```bash
export PEXELS_API_KEY=your_pexels_key_here
```

Then restart the bot for changes to take effect.

### Testing Pexels Integration
1. Generate a script using the bot
2. Click "🎥 Find Videos" button
3. Bot should show relevant stock videos and images

## 📊 Bot Statistics

### Viewing Statistics
Send: `/stats`

Shows:
- Total users
- Scripts generated
- Active API keys
- Training scripts count
- Top users by script generation

### Web Dashboard
Visit: `http://your-replit-url.replit.app:5000`

Live dashboard showing:
- Bot status
- Real-time statistics
- Feature overview

## 🛠️ Admin Panel Interface

Send `/admin` to access the interactive admin panel with buttons:

- **🔑 API Keys** - Manage Gemini API keys
- **📊 Bot Stats** - View usage statistics  
- **📚 Training Scripts** - Manage training data
- **👥 User Management** - User statistics
- **🔧 System Info** - Technical information
- **📢 Broadcast** - Send messages to all users

## ⚠️ Troubleshooting

### Common Issues

**1. "No API keys available" error**
- Add at least one Gemini API key using `/addkey`
- Check if keys are valid at Google AI Studio

**2. "Video search not available"**
- Add Pexels API key to environment
- Restart the bot after adding the key

**3. Bot not responding**
- Check if bot is running (look for "● ONLINE" status)
- Verify BOT_TOKEN is correct
- Check logs for error messages

**4. Scripts not in Vigyan Mitra style**
- Add more training scripts using `/addscript`
- Review existing training scripts with `/trainscripts`

### Log Monitoring
Bot logs show:
- User interactions
- API key usage
- Error messages
- Database operations

## 🔄 Maintenance Tasks

### Regular Tasks
1. **Monitor API usage** - Check `/keys` for usage patterns
2. **Add training scripts** - Improve AI with new examples
3. **Review statistics** - Use `/stats` to track growth
4. **Update API keys** - Replace expired or rate-limited keys

### Monthly Tasks
1. **Backup database** - Copy `bot_data.db` file
2. **Review user feedback** - Check for common issues
3. **Update training data** - Add successful script examples
4. **Performance optimization** - Monitor response times

## 📱 User Support

### Common User Questions

**Q: How to generate scripts?**
A: Click "🎬 Generate Script" and choose a topic

**Q: Can I suggest custom topics?**
A: Yes, click "✍️ Custom Topic" and type your idea

**Q: How long are the scripts?**
A: 130-160 words, perfect for 40-60 second YouTube Shorts

**Q: Can I regenerate if I don't like the script?**
A: Yes, click "🔄 Regenerate" button

### Broadcast Messages
Use admin panel to send announcements to all users about:
- New features
- Maintenance schedules
- Usage tips
- Bot improvements

## 🚀 Advanced Features

### API Key Rotation
- Bot automatically switches between keys
- Prevents rate limiting
- Ensures high availability
- Tracks usage per key

### Streaming Responses
- Scripts delivered sentence by sentence
- Real-time typing indicators
- Better user experience
- Prevents timeout issues

### Database Management
All data stored in SQLite:
- User sessions and preferences
- Generated scripts history
- API key management
- Training scripts collection

## 💡 Best Practices

### API Key Management
- Keep 2-3 active keys for redundancy
- Monitor usage with `/keys` command
- Replace keys showing high usage
- Test new keys before removing old ones

### Training Script Quality
- Only add high-quality examples
- Follow exact Vigyan Mitra format
- Use real scientific facts
- Maintain consistent tone and style

### User Engagement
- Monitor popular topics via `/stats`
- Add training scripts for trending topics
- Respond to user feedback quickly
- Update features based on usage patterns

---

## 📞 Support

For technical issues or questions:
1. Check this guide first
2. Review bot logs for errors
3. Test with `/admin` panel
4. Restart bot if needed

**Admin Contact:** User ID 5482745712 has full admin access to all bot functions.