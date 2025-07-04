"""
Main bot handlers for user interactions
"""

import asyncio
import logging
from typing import Dict, Any

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database import db
from bot.gemini_client import gemini_client
from bot.video_finder import VideoFinder
from bot.utils import (
    format_script_for_display, extract_topic_from_script, count_words_hindi,
    create_topic_suggestions, create_help_text, generate_user_report
)

logger = logging.getLogger(__name__)
router = Router()


class GenerationStates(StatesGroup):
    """States for script generation flow"""
    waiting_for_topic = State()
    generating = State()
    showing_result = State()


# Topic suggestions
TOPIC_SUGGESTIONS = create_topic_suggestions()


def create_main_menu() -> InlineKeyboardMarkup:
    """Create main menu keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎬 Generate Script", callback_data="generate_script"),
        InlineKeyboardButton(text="📊 My Stats", callback_data="user_stats")
    )
    builder.row(
        InlineKeyboardButton(text="🎯 Topic Suggestions", callback_data="topic_suggestions"),
        InlineKeyboardButton(text="🎥 Video Clips", callback_data="video_clips")
    )
    builder.row(
        InlineKeyboardButton(text="❓ Help", callback_data="help"),
        InlineKeyboardButton(text="🔄 Regenerate", callback_data="regenerate")
    )
    
    return builder.as_markup()


def create_topic_keyboard() -> InlineKeyboardMarkup:
    """Create topic selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    # Add topic suggestions
    for topic in TOPIC_SUGGESTIONS[:8]:  # Show first 8
        builder.row(
            InlineKeyboardButton(text=topic, callback_data=f"topic_{topic}")
        )
    
    builder.row(
        InlineKeyboardButton(text="✍️ Custom Topic", callback_data="custom_topic"),
        InlineKeyboardButton(text="🎲 Random Topic", callback_data="random_topic")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")
    )
    
    return builder.as_markup()


def create_generation_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for generation actions"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔄 Regenerate", callback_data="regenerate"),
        InlineKeyboardButton(text="🎥 Find Videos", callback_data="find_videos")
    )
    builder.row(
        InlineKeyboardButton(text="🎯 New Topic", callback_data="generate_script"),
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu")
    )
    
    return builder.as_markup()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    """Handle /start command"""
    user = message.from_user
    
    # Create user session
    await db.create_user_session(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = f"""
🎬 <b>Welcome to Hindi YouTube Shorts Script Generator!</b>

नमस्ते {user.first_name}! 👋

🚀 मैं आपके लिए <b>high-retention Hindi YouTube Shorts scripts</b> generate करता हूं।

✨ <b>Features:</b>
• 130-160 word Hindi scripts
• Vigyan Mitra style storytelling
• Real-time streaming responses
• Video clip suggestions
• Multiple topic options

📱 <b>Ready to create viral content?</b>
Click "Generate Script" to get started!
"""
    
    await message.answer(
        welcome_text,
        reply_markup=create_main_menu(),
        parse_mode="HTML"
    )
    
    await state.clear()


@router.message(Command("help"))
async def help_command(message: Message):
    """Handle /help command"""
    await message.answer(
        create_help_text(),
        parse_mode="HTML"
    )


@router.message(Command("generate"))
async def generate_command(message: Message, state: FSMContext):
    """Handle /generate command"""
    await message.answer(
        "🎯 <b>Choose a topic for your script:</b>",
        reply_markup=create_topic_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(GenerationStates.waiting_for_topic)


@router.message(Command("mystats"))
async def stats_command(message: Message):
    """Handle /mystats command"""
    user_stats = await db.get_user_stats(message.from_user.id)
    
    if user_stats:
        report = generate_user_report(user_stats)
        await message.answer(report, parse_mode="HTML")
    else:
        await message.answer("❌ No statistics found. Generate a script first!")


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, state: FSMContext):
    """Handle main menu callback"""
    await callback.message.edit_text(
        "🏠 <b>Main Menu</b>\n\nChoose an option:",
        reply_markup=create_main_menu(),
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "generate_script")
async def generate_script_callback(callback: CallbackQuery, state: FSMContext):
    """Handle generate script callback"""
    await callback.message.edit_text(
        "🎯 <b>Choose a topic for your script:</b>",
        reply_markup=create_topic_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(GenerationStates.waiting_for_topic)
    await callback.answer()


@router.callback_query(F.data == "topic_suggestions")
async def topic_suggestions_callback(callback: CallbackQuery):
    """Handle topic suggestions callback"""
    await callback.message.edit_text(
        "🎯 <b>Choose a topic for your script:</b>",
        reply_markup=create_topic_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("topic_"))
async def topic_selected_callback(callback: CallbackQuery, state: FSMContext):
    """Handle topic selection callback"""
    topic = callback.data.replace("topic_", "")
    await state.update_data(topic=topic)
    
    await callback.message.edit_text(
        f"🎬 <b>Generating script for:</b> {topic}\n\n⏳ Please wait...",
        parse_mode="HTML"
    )
    
    await state.set_state(GenerationStates.generating)
    await callback.answer()
    
    # Start script generation
    await generate_script_streaming(callback.message, topic, state)


@router.callback_query(F.data == "custom_topic")
async def custom_topic_callback(callback: CallbackQuery, state: FSMContext):
    """Handle custom topic callback"""
    await callback.message.edit_text(
        "✍️ <b>Enter your custom topic:</b>\n\n"
        "Example: 'स्पेस में खाना कैसे बनता है'\n\n"
        "Type your topic and send it:",
        parse_mode="HTML"
    )
    await state.set_state(GenerationStates.waiting_for_topic)
    await callback.answer()


@router.callback_query(F.data == "random_topic")
async def random_topic_callback(callback: CallbackQuery, state: FSMContext):
    """Handle random topic callback"""
    await callback.message.edit_text(
        "🎲 <b>Generating random science script...</b>\n\n⏳ Please wait...",
        parse_mode="HTML"
    )
    
    await state.set_state(GenerationStates.generating)
    await callback.answer()
    
    # Generate with random topic
    await generate_script_streaming(callback.message, None, state)


@router.callback_query(F.data == "regenerate")
async def regenerate_callback(callback: CallbackQuery, state: FSMContext):
    """Handle regenerate callback"""
    data = await state.get_data()
    topic = data.get("topic")
    
    await callback.message.edit_text(
        f"🔄 <b>Regenerating script...</b>\n\n⏳ Please wait...",
        parse_mode="HTML"
    )
    
    await state.set_state(GenerationStates.generating)
    await callback.answer()
    
    # Regenerate script
    await generate_script_streaming(callback.message, topic, state)


@router.callback_query(F.data == "find_videos")
async def find_videos_callback(callback: CallbackQuery, state: FSMContext):
    """Handle find videos callback"""
    data = await state.get_data()
    script = data.get("script")
    
    if not script:
        await callback.answer("❌ No script found. Generate a script first!")
        return
    
    await callback.message.edit_text(
        "🎥 <b>Finding video clips...</b>\n\n⏳ Please wait...",
        parse_mode="HTML"
    )
    
    # Find videos using Pexels API
    from config import Config
    config = Config()
    pexels_key = config.PEXELS_API_KEY
    if not pexels_key:
        await callback.message.edit_text(
            "❌ <b>Video search not available</b>\n\n"
            "Pexels API key not configured.",
            reply_markup=create_generation_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    try:
        video_finder = VideoFinder(pexels_key)
        result = await video_finder.find_media_for_script(script)
        
        if result["success"]:
            videos = result["videos"]
            images = result["images"]
            
            response_text = f"🎥 <b>Found {len(videos)} videos and {len(images)} images</b>\n\n"
            
            # Show videos
            if videos:
                response_text += "📹 <b>Videos:</b>\n"
                for i, video in enumerate(videos[:3], 1):
                    response_text += f"{i}. {video['title']}\n"
                    response_text += f"   👤 {video.get('user', 'Unknown')}\n"
                    response_text += f"   🔗 {video['url']}\n\n"
            
            # Show images
            if images:
                response_text += "🖼️ <b>Images:</b>\n"
                for i, image in enumerate(images[:3], 1):
                    response_text += f"{i}. {image['title']}\n"
                    response_text += f"   📸 {image.get('photographer', 'Unknown')}\n"
                    response_text += f"   🔗 {image['url']}\n\n"
            
            response_text += f"💡 <b>Keywords used:</b> {', '.join(result['keywords'])}"
            
        else:
            response_text = f"❌ <b>Video search failed</b>\n\n{result['error']}"
        
        await callback.message.edit_text(
            response_text,
            reply_markup=create_generation_keyboard(),
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Error finding videos: {e}")
        await callback.message.edit_text(
            "❌ <b>Error finding videos</b>\n\nPlease try again later.",
            reply_markup=create_generation_keyboard(),
            parse_mode="HTML"
        )
    
    await callback.answer()


@router.callback_query(F.data == "user_stats")
async def user_stats_callback(callback: CallbackQuery):
    """Handle user stats callback"""
    user_stats = await db.get_user_stats(callback.from_user.id)
    
    if user_stats:
        report = generate_user_report(user_stats)
        await callback.message.edit_text(
            report,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            "❌ No statistics found. Generate a script first!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="main_menu")]
            ]),
            parse_mode="HTML"
        )
    
    await callback.answer()


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    """Handle help callback"""
    await callback.message.edit_text(
        create_help_text(),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="main_menu")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery, state: FSMContext):
    """Handle back to menu callback"""
    await callback.message.edit_text(
        "🏠 <b>Main Menu</b>\n\nChoose an option:",
        reply_markup=create_main_menu(),
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()


@router.message(StateFilter(GenerationStates.waiting_for_topic))
async def custom_topic_received(message: Message, state: FSMContext):
    """Handle custom topic input"""
    topic = message.text.strip()
    
    if len(topic) < 5:
        await message.answer("❌ Topic too short. Please enter a longer topic (minimum 5 characters).")
        return
    
    await state.update_data(topic=topic)
    
    # Send generating message
    generating_msg = await message.answer(
        f"🎬 <b>Generating script for:</b> {topic}\n\n⏳ Please wait...",
        parse_mode="HTML"
    )
    
    await state.set_state(GenerationStates.generating)
    
    # Start script generation
    await generate_script_streaming(generating_msg, topic, state)


async def generate_script_streaming(message: Message, topic: str, state: FSMContext):
    """Generate script with streaming response"""
    try:
        user_id = message.chat.id
        
        # Show typing indicator
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        # Generate script using streaming
        script_parts = []
        word_count = 0
        api_key_used = ""
        
        async for chunk in gemini_client.generate_script_streaming(topic):
            if chunk["type"] == "error":
                await message.edit_text(
                    f"❌ <b>Error generating script:</b>\n\n{chunk['content']}",
                    reply_markup=create_generation_keyboard(),
                    parse_mode="HTML"
                )
                return
            
            elif chunk["type"] == "metadata":
                word_count = chunk["word_count"]
                total_sentences = chunk["total_sentences"]
                
                # Update message with progress
                await message.edit_text(
                    f"🎬 <b>Script Topic:</b> {chunk['topic']}\n"
                    f"📝 <b>Expected Length:</b> {word_count} words\n"
                    f"📊 <b>Streaming:</b> {total_sentences} sentences\n\n"
                    f"⏳ <b>Starting generation...</b>",
                    parse_mode="HTML"
                )
            
            elif chunk["type"] == "sentence":
                sentence = chunk["content"]
                script_parts.append(sentence)
                
                # Update message with streaming content
                current_script = " ".join(script_parts)
                progress = f"📝 Sentence {chunk['index'] + 1}"
                
                if not chunk["is_last"]:
                    progress += " ⏳"
                
                await message.edit_text(
                    f"🎬 <b>Live Generation:</b>\n\n{format_script_for_display(current_script)}\n\n{progress}",
                    parse_mode="HTML"
                )
                
                # Show typing action
                if not chunk["is_last"]:
                    await message.bot.send_chat_action(message.chat.id, "typing")
            
            elif chunk["type"] == "complete":
                full_script = chunk["full_script"]
                api_key_used = chunk["api_key_used"]
                
                # Save to database
                await db.save_generated_script(
                    user_id=user_id,
                    topic=topic or "Random Science Topic",
                    script_content=full_script,
                    word_count=count_words_hindi(full_script),
                    api_key_used=api_key_used
                )
                
                # Store in state
                await state.update_data(
                    script=full_script,
                    topic=topic or "Random Science Topic"
                )
                
                # Final message
                final_text = f"✅ <b>Script Generated Successfully!</b>\n\n"
                final_text += f"🎯 <b>Topic:</b> {topic or 'Random Science Topic'}\n"
                final_text += f"📝 <b>Length:</b> {count_words_hindi(full_script)} words\n\n"
                final_text += f"📜 <b>Your Script:</b>\n\n{format_script_for_display(full_script)}"
                
                await message.edit_text(
                    final_text,
                    reply_markup=create_generation_keyboard(),
                    parse_mode="HTML"
                )
                
                await state.set_state(GenerationStates.showing_result)
                break
    
    except Exception as e:
        logger.error(f"Error in streaming generation: {e}")
        await message.edit_text(
            f"❌ <b>Generation Error:</b>\n\n{str(e)}",
            reply_markup=create_generation_keyboard(),
            parse_mode="HTML"
        )


def register_handlers(dp):
    """Register all handlers"""
    dp.include_router(router)
