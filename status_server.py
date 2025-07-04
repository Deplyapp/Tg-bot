#!/usr/bin/env python3
"""
Simple web status server to show bot information
"""

import asyncio
import sqlite3
from datetime import datetime
from aiohttp import web, ClientSession
import json

async def get_bot_stats():
    """Get bot statistics from database"""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            
            # Get basic stats
            cursor.execute("SELECT COUNT(*) FROM user_sessions")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM generated_scripts")
            total_scripts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM api_keys WHERE is_active = 1")
            active_keys = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM training_scripts WHERE is_active = 1")
            training_scripts = cursor.fetchone()[0]
            
            return {
                "users": total_users,
                "scripts": total_scripts,
                "api_keys": active_keys,
                "training_scripts": training_scripts,
                "last_updated": datetime.now().isoformat()
            }
    except Exception as e:
        return {"error": str(e)}

async def index(request):
    """Main status page"""
    stats = await get_bot_stats()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hindi YouTube Shorts Bot - Status</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
                padding: 20px;
            }}
            .container {{ 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            h1 {{ 
                text-align: center; 
                margin-bottom: 30px; 
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .status {{ 
                display: inline-block; 
                background: #4CAF50; 
                color: white; 
                padding: 8px 16px; 
                border-radius: 25px; 
                font-size: 14px;
                font-weight: bold;
                margin-left: 10px;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
            .stats {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin: 30px 0; 
            }}
            .stat-card {{ 
                background: rgba(255,255,255,0.2); 
                padding: 20px; 
                border-radius: 15px; 
                text-align: center;
                transition: transform 0.3s ease;
            }}
            .stat-card:hover {{ transform: translateY(-5px); }}
            .stat-number {{ 
                font-size: 2.5em; 
                font-weight: bold; 
                margin-bottom: 10px;
                color: #FFD700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .stat-label {{ 
                font-size: 1.1em; 
                opacity: 0.9; 
            }}
            .features {{ 
                margin-top: 40px; 
            }}
            .feature-grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 15px; 
                margin-top: 20px; 
            }}
            .feature {{ 
                background: rgba(255,255,255,0.1); 
                padding: 15px; 
                border-radius: 10px; 
                border-left: 4px solid #FFD700;
            }}
            .footer {{ 
                text-align: center; 
                margin-top: 40px; 
                opacity: 0.8; 
                font-size: 0.9em;
            }}
            .telegram-link {{
                display: inline-block;
                background: #0088cc;
                color: white;
                padding: 12px 24px;
                border-radius: 25px;
                text-decoration: none;
                margin: 20px 10px;
                font-weight: bold;
                transition: background 0.3s ease;
            }}
            .telegram-link:hover {{
                background: #006699;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 Hindi YouTube Shorts Bot <span class="status">● ONLINE</span></h1>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{stats.get('users', 0)}</div>
                    <div class="stat-label">👥 Total Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('scripts', 0)}</div>
                    <div class="stat-label">📝 Scripts Generated</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('api_keys', 0)}</div>
                    <div class="stat-label">🔑 Active API Keys</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('training_scripts', 0)}</div>
                    <div class="stat-label">📚 Training Scripts</div>
                </div>
            </div>
            
            <div class="features">
                <h2>✨ Bot Features</h2>
                <div class="feature-grid">
                    <div class="feature">
                        <strong>🤖 AI-Powered Scripts</strong><br>
                        Generates 130-160 word Hindi scripts using Google Gemini AI
                    </div>
                    <div class="feature">
                        <strong>⚡ Streaming Responses</strong><br>
                        Real-time sentence-by-sentence delivery with typing indicators
                    </div>
                    <div class="feature">
                        <strong>📱 Multi-User Support</strong><br>
                        Handles multiple users simultaneously without blocking
                    </div>
                    <div class="feature">
                        <strong>🔑 API Key Rotation</strong><br>
                        Seamless switching between multiple API keys for reliability
                    </div>
                    <div class="feature">
                        <strong>👑 Admin Panel</strong><br>
                        Complete bot management with statistics and controls
                    </div>
                    <div class="feature">
                        <strong>🎥 Video Suggestions</strong><br>
                        Finds relevant stock footage using Pexels API
                    </div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="https://t.me/your_all_ai_bot" class="telegram-link">🚀 Start Using Bot</a>
                <a href="/api/stats" class="telegram-link">📊 API Stats</a>
            </div>
            
            <div class="footer">
                <p>Last updated: {stats.get('last_updated', 'Unknown')}</p>
                <p>Made with ❤️ for creating engaging Hindi science content</p>
            </div>
        </div>
        
        <script>
            // Auto refresh every 30 seconds
            setTimeout(() => location.reload(), 30000);
        </script>
    </body>
    </html>
    """
    
    return web.Response(text=html, content_type='text/html')

async def api_stats(request):
    """API endpoint for stats"""
    stats = await get_bot_stats()
    return web.json_response(stats)

async def init_app():
    """Initialize web application"""
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/api/stats', api_stats)
    return app

if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='0.0.0.0', port=5000)