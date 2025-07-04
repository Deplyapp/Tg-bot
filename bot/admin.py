"""
Admin handlers for bot management
"""

import logging
from typing import List, Dict, Any

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database import db
from bot.utils import is_admin, validate_api_key, format_timestamp, create_admin_help

logger = logging.getLogger(__name__)
admin_router = Router()


def create_admin_keyboard() -> InlineKeyboardMarkup:
    """Create admin control keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔑 API Keys", callback_data="admin_keys"),
        InlineKeyboardButton(text="📊 Bot Stats", callback_data="admin_stats")
    )
    builder.row(
        InlineKeyboardButton(text="📚 Training Scripts", callback_data="admin_training"),
        InlineKeyboardButton(text="👥 User Management", callback_data="admin_users")
    )
    builder.row(
        InlineKeyboardButton(text="➕ Add API Key", callback_data="add_api_key"),
        InlineKeyboardButton(text="✍️ Add Training Script", callback_data="add_training_script")
    )
    builder.row(
        InlineKeyboardButton(text="🗑️ Remove API Key", callback_data="remove_api_key"),
        InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")
    )
    
    return builder.as_markup()


@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    """Admin panel command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    admin_text = f"""
🔧 <b>Admin Control Panel</b>

👋 Welcome, Admin {message.from_user.first_name}!

🎛️ Use the buttons below to manage the bot:
"""
    
    await message.answer(
        admin_text,
        reply_markup=create_admin_keyboard(),
        parse_mode="HTML"
    )


@admin_router.message(Command("addkey"))
async def add_api_key(message: Message):
    """Add API key command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "❌ <b>Usage:</b> <code>/addkey [API_KEY]</code>\n\n"
            "Example: <code>/addkey AIzaSyD...</code>",
            parse_mode="HTML"
        )
        return
    
    api_key = args[1].strip()
    
    # Validate API key
    if not validate_api_key(api_key, "gemini"):
        await message.answer("❌ Invalid API key format. Gemini keys should start with 'AIza'.")
        return
    
    # Add to database
    success = await db.add_api_key(api_key, "gemini")
    
    if success:
        await message.answer(f"✅ API key added successfully!\n\nKey: {api_key[:10]}...")
    else:
        await message.answer("❌ API key already exists or error occurred.")


@admin_router.message(Command("removekey"))
async def remove_api_key(message: Message):
    """Remove API key command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "❌ <b>Usage:</b> <code>/removekey [API_KEY]</code>\n\n"
            "Example: <code>/removekey AIzaSyD...</code>",
            parse_mode="HTML"
        )
        return
    
    api_key = args[1].strip()
    
    # Remove from database
    success = await db.remove_api_key(api_key)
    
    if success:
        await message.answer(f"✅ API key removed successfully!\n\nKey: {api_key[:10]}...")
    else:
        await message.answer("❌ API key not found or error occurred.")


@admin_router.message(Command("keys"))
async def list_api_keys(message: Message):
    """List API keys command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    keys = await db.get_active_api_keys("gemini")
    
    if not keys:
        await message.answer("❌ No API keys found.")
        return
    
    response = "🔑 <b>Active API Keys:</b>\n\n"
    
    for i, key in enumerate(keys, 1):
        key_preview = f"{key['key_value'][:10]}...{key['key_value'][-4:]}"
        usage_count = key['usage_count']
        last_used = key['last_used'] or "Never"
        
        response += f"{i}. <code>{key_preview}</code>\n"
        response += f"   📊 Usage: {usage_count}\n"
        response += f"   🕒 Last used: {format_timestamp(last_used)}\n\n"
    
    await message.answer(response, parse_mode="HTML")


@admin_router.message(Command("addscript"))
async def add_training_script(message: Message):
    """Add training script command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "❌ <b>Usage:</b> <code>/addscript [SCRIPT_CONTENT]</code>\n\n"
            "Example: <code>/addscript क्या आप जानते हैं...</code>",
            parse_mode="HTML"
        )
        return
    
    script_content = args[1].strip()
    
    if len(script_content) < 50:
        await message.answer("❌ Script too short. Minimum 50 characters required.")
        return
    
    # Add to database
    success = await db.add_training_script(script_content, message.from_user.id)
    
    if success:
        await message.answer(f"✅ Training script added successfully!\n\nLength: {len(script_content)} characters")
    else:
        await message.answer("❌ Error adding training script.")


@admin_router.message(Command("trainscripts"))
async def list_training_scripts(message: Message):
    """List training scripts command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    scripts = await db.get_training_scripts()
    
    if not scripts:
        await message.answer("❌ No training scripts found.")
        return
    
    # Send all scripts in chunks to avoid message length limits
    scripts_text = f"📚 <b>Training Scripts ({len(scripts)} total):</b>\n\n"
    
    current_message = scripts_text
    
    for i, script in enumerate(scripts, 1):
        script_line = f"{i}. {script[:150]}{'...' if len(script) > 150 else ''}\n\n"
        
        # Check if adding this script would exceed message limit
        if len(current_message + script_line) > 4000:
            # Send current message and start new one
            await message.answer(current_message, parse_mode="HTML")
            current_message = f"📚 <b>Training Scripts (continued):</b>\n\n{script_line}"
        else:
            current_message += script_line
    
    # Send the last message
    if current_message.strip():
        await message.answer(current_message, parse_mode="HTML")


@admin_router.message(Command("stats"))
async def bot_stats(message: Message):
    """Bot statistics command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    try:
        # Get database statistics
        import sqlite3
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Count users
            cursor.execute("SELECT COUNT(*) FROM user_sessions")
            total_users = cursor.fetchone()[0]
            
            # Count scripts
            cursor.execute("SELECT COUNT(*) FROM generated_scripts")
            total_scripts = cursor.fetchone()[0]
            
            # Count API keys
            cursor.execute("SELECT COUNT(*) FROM api_keys WHERE is_active = 1")
            active_keys = cursor.fetchone()[0]
            
            # Count training scripts
            cursor.execute("SELECT COUNT(*) FROM training_scripts WHERE is_active = 1")
            training_scripts = cursor.fetchone()[0]
            
            # Get top users
            cursor.execute("""
                SELECT username, script_count 
                FROM user_sessions 
                ORDER BY script_count DESC 
                LIMIT 5
            """)
            top_users = cursor.fetchall()
        
        stats_text = f"""
📊 <b>Bot Statistics</b>

👥 <b>Users:</b> {total_users}
📝 <b>Scripts Generated:</b> {total_scripts}
🔑 <b>Active API Keys:</b> {active_keys}
📚 <b>Training Scripts:</b> {training_scripts}

🏆 <b>Top Users:</b>
"""
        
        for i, (username, count) in enumerate(top_users, 1):
            username_display = f"@{username}" if username else "Unknown"
            stats_text += f"{i}. {username_display}: {count} scripts\n"
        
        await message.answer(stats_text, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Error getting bot stats: {e}")
        await message.answer(f"❌ Error retrieving statistics: {str(e)}")


@admin_router.message(Command("help_admin"))
async def admin_help(message: Message):
    """Admin help command"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Access denied. Admin only command.")
        return
    
    await message.answer(create_admin_help(), parse_mode="HTML")


@admin_router.callback_query(F.data == "admin_keys")
async def admin_keys_callback(callback: CallbackQuery):
    """Handle admin keys callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access denied.")
        return
    
    keys = await db.get_active_api_keys("gemini")
    
    if not keys:
        response = "❌ No API keys found."
    else:
        response = "🔑 <b>Active API Keys:</b>\n\n"
        
        for i, key in enumerate(keys, 1):
            key_preview = f"{key['key_value'][:10]}...{key['key_value'][-4:]}"
            usage_count = key['usage_count']
            last_used = key['last_used'] or "Never"
            
            response += f"{i}. <code>{key_preview}</code>\n"
            response += f"   📊 Usage: {usage_count}\n"
            response += f"   🕒 Last used: {format_timestamp(last_used)}\n\n"
    
    await callback.message.edit_text(
        response,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="admin_panel")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@admin_router.callback_query(F.data == "admin_stats")
async def admin_stats_callback(callback: CallbackQuery):
    """Handle admin stats callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access denied.")
        return
    
    try:
        # Get database statistics
        import sqlite3
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Count users
            cursor.execute("SELECT COUNT(*) FROM user_sessions")
            total_users = cursor.fetchone()[0]
            
            # Count scripts
            cursor.execute("SELECT COUNT(*) FROM generated_scripts")
            total_scripts = cursor.fetchone()[0]
            
            # Count API keys
            cursor.execute("SELECT COUNT(*) FROM api_keys WHERE is_active = 1")
            active_keys = cursor.fetchone()[0]
            
            # Count training scripts
            cursor.execute("SELECT COUNT(*) FROM training_scripts WHERE is_active = 1")
            training_scripts = cursor.fetchone()[0]
        
        stats_text = f"""
📊 <b>Bot Statistics</b>

👥 <b>Users:</b> {total_users}
📝 <b>Scripts Generated:</b> {total_scripts}
🔑 <b>Active API Keys:</b> {active_keys}
📚 <b>Training Scripts:</b> {training_scripts}

🔄 <b>Last Updated:</b> Now
"""
        
        await callback.message.edit_text(
            stats_text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Refresh", callback_data="admin_stats")],
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin_panel")]
            ]),
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Error getting admin stats: {e}")
        await callback.message.edit_text(
            f"❌ Error retrieving statistics: {str(e)}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin_panel")]
            ]),
            parse_mode="HTML"
        )
    
    await callback.answer()


@admin_router.callback_query(F.data == "admin_training")
async def admin_training_callback(callback: CallbackQuery):
    """Handle admin training callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access denied.")
        return
    
    scripts = await db.get_training_scripts()
    
    if not scripts:
        response = "❌ No training scripts found.\n\n"
        response += "📝 <b>Add training scripts:</b>\n"
        response += "• Use command: <code>/addscript [SCRIPT_CONTENT]</code>\n"
        response += "• Scripts help AI learn Vigyan Mitra style\n"
        response += "• Minimum 50 characters required"
        
        await callback.message.edit_text(
            response,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin_panel")]
            ]),
            parse_mode="HTML"
        )
    else:
        # Send all training scripts in multiple messages
        await callback.message.edit_text(
            f"📚 <b>Training Scripts ({len(scripts)} total):</b>\n\n"
            "📤 Sending all scripts...",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin_panel")]
            ]),
            parse_mode="HTML"
        )
        
        # Send scripts in chunks
        current_message = f"📚 <b>All Training Scripts ({len(scripts)} total):</b>\n\n"
        
        for i, script in enumerate(scripts, 1):
            script_line = f"{i}. {script[:200]}{'...' if len(script) > 200 else ''}\n\n"
            
            # Check if adding this script would exceed message limit
            if len(current_message + script_line) > 4000:
                # Send current message and start new one
                await callback.message.answer(current_message, parse_mode="HTML")
                current_message = f"📚 <b>Training Scripts (continued):</b>\n\n{script_line}"
            else:
                current_message += script_line
        
        # Send the last message
        if current_message.strip():
            await callback.message.answer(current_message, parse_mode="HTML")
    await callback.answer()


@admin_router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery):
    """Handle admin panel callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access denied.")
        return
    
    admin_text = f"""
🔧 <b>Admin Control Panel</b>

👋 Welcome, Admin {callback.from_user.first_name}!

🎛️ Use the buttons below to manage the bot:
"""
    
    await callback.message.edit_text(
        admin_text,
        reply_markup=create_admin_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# Interactive handlers for adding/removing keys and scripts
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_api_key = State()
    waiting_for_training_script = State()
    waiting_for_key_to_remove = State()


@admin_router.callback_query(F.data == "add_api_key")
async def add_api_key_callback(callback: CallbackQuery, state: FSMContext):
    """Handle add API key callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access denied", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🔑 <b>Add New Gemini API Key</b>\n\n"
        "🔗 <b>How to get your API key:</b>\n"
        "1. Go to https://makersuite.google.com/app/apikey\n"
        "2. Sign in with your Google account\n"
        "3. Click 'Create API Key'\n"
        "4. Copy the key and send it to me\n\n"
        "📝 <b>Send your Gemini API key:</b>\n"
        "(It should start with 'AIzaSy...')",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Cancel", callback_data="admin_panel")]
        ])
    )
    await state.set_state(AdminStates.waiting_for_api_key)
    await callback.answer()


@admin_router.callback_query(F.data == "add_training_script")
async def add_training_script_callback(callback: CallbackQuery, state: FSMContext):
    """Handle add training script callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access denied", show_alert=True)
        return
    
    await callback.message.edit_text(
        "✍️ <b>Add New Training Script</b>\n\n"
        "📝 <b>Guidelines for Training Scripts:</b>\n"
        "• Write in Vigyan Mitra style (130-160 words)\n"
        "• Start with surprising question\n"
        "• Include scientific facts in middle\n"
        "• End with thought-provoking question\n"
        "• Use Hindi with natural English terms\n"
        "• Minimum 50 characters required\n\n"
        "📋 <b>Example Format:</b>\n"
        "<i>क्या आप जानते हैं कि... [scientific fact]... अब सोचिए...</i>\n\n"
        "💬 <b>Send your training script:</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Cancel", callback_data="admin_panel")]
        ])
    )
    await state.set_state(AdminStates.waiting_for_training_script)
    await callback.answer()


@admin_router.callback_query(F.data == "remove_api_key")
async def remove_api_key_callback(callback: CallbackQuery, state: FSMContext):
    """Handle remove API key callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Access denied", show_alert=True)
        return
    
    keys = await db.get_active_api_keys()
    
    if not keys:
        await callback.message.edit_text(
            "❌ <b>No API Keys Found</b>\n\n"
            "There are no API keys to remove.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="admin_panel")]
            ])
        )
        await callback.answer()
        return
    
    response = "🗑️ <b>Remove API Key</b>\n\n"
    response += "📋 <b>Current API Keys:</b>\n\n"
    
    for i, key in enumerate(keys, 1):
        key_preview = key.get('key_value', '')[:15] + "..." + key.get('key_value', '')[-8:]
        usage_count = key.get('usage_count', 0)
        response += f"{i}. <code>{key_preview}</code> (Used {usage_count} times)\n"
    
    response += "\n💬 <b>Send the full API key to remove:</b>\n"
    response += "<i>Copy and paste the complete key</i>"
    
    await callback.message.edit_text(
        response,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Cancel", callback_data="admin_panel")]
        ])
    )
    await state.set_state(AdminStates.waiting_for_key_to_remove)
    await callback.answer()


@admin_router.message(AdminStates.waiting_for_api_key)
async def process_new_api_key(message: Message, state: FSMContext):
    """Process new API key from admin"""
    if not is_admin(message.from_user.id):
        await message.reply("❌ Access denied")
        return
    
    api_key = message.text.strip()
    
    # Validate API key format
    if not api_key.startswith('AIzaSy') or len(api_key) < 35:
        await message.reply(
            "❌ <b>Invalid API Key Format</b>\n\n"
            "API key should:\n"
            "• Start with 'AIzaSy'\n"
            "• Be at least 35 characters long\n\n"
            "Please send a valid Gemini API key.",
            parse_mode="HTML"
        )
        return
    
    # Add to database
    success = await db.add_api_key(api_key)
    
    if success:
        await message.reply(
            "✅ <b>API Key Added Successfully!</b>\n\n"
            f"🔑 Key: {api_key[:10]}...{api_key[-4:]}\n"
            "🔄 Bot will now use this key for API rotation\n\n"
            "Use /admin to return to admin panel",
            parse_mode="HTML"
        )
    else:
        await message.reply(
            "❌ <b>Failed to Add API Key</b>\n\n"
            "Possible reasons:\n"
            "• Key already exists\n"
            "• Database error\n\n"
            "Please try again or check if key is already added.",
            parse_mode="HTML"
        )
    
    await state.clear()


@admin_router.message(AdminStates.waiting_for_training_script)
async def process_new_training_script(message: Message, state: FSMContext):
    """Process new training script from admin"""
    if not is_admin(message.from_user.id):
        await message.reply("❌ Access denied")
        return
    
    script_content = message.text.strip()
    
    # Validate script content
    if len(script_content) < 50:
        await message.reply(
            "❌ <b>Script Too Short</b>\n\n"
            f"Current length: {len(script_content)} characters\n"
            "Minimum required: 50 characters\n\n"
            "Please send a longer training script.",
            parse_mode="HTML"
        )
        return
    
    # Add to database
    success = await db.add_training_script(script_content, message.from_user.id)
    
    if success:
        await message.reply(
            "✅ <b>Training Script Added Successfully!</b>\n\n"
            f"📊 Length: {len(script_content)} characters\n"
            f"📝 Preview: {script_content[:100]}...\n\n"
            "🤖 AI will now learn from this script\n"
            "Use /admin to return to admin panel",
            parse_mode="HTML"
        )
    else:
        await message.reply(
            "❌ <b>Failed to Add Training Script</b>\n\n"
            "Database error occurred. Please try again.",
            parse_mode="HTML"
        )
    
    await state.clear()


@admin_router.message(AdminStates.waiting_for_key_to_remove)
async def process_remove_api_key(message: Message, state: FSMContext):
    """Process API key removal from admin"""
    if not is_admin(message.from_user.id):
        await message.reply("❌ Access denied")
        return
    
    api_key = message.text.strip()
    
    # Remove from database
    success = await db.remove_api_key(api_key)
    
    if success:
        await message.reply(
            "✅ <b>API Key Removed Successfully!</b>\n\n"
            f"🗑️ Removed: {api_key[:10]}...{api_key[-4:]}\n\n"
            "Use /admin to return to admin panel",
            parse_mode="HTML"
        )
    else:
        await message.reply(
            "❌ <b>Failed to Remove API Key</b>\n\n"
            "Possible reasons:\n"
            "• Key not found in database\n"
            "• Key doesn't match exactly\n\n"
            "Please check the key and try again.",
            parse_mode="HTML"
        )
    
    await state.clear()


def register_admin_handlers(dp):
    """Register admin handlers"""
    dp.include_router(admin_router)
