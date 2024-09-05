import logging
import html  # Add the html module to handle escaping
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from temp_mail_api import generate_temp_mail, get_temp_mail_messages
from filter import clean_html
import os

logger = logging.getLogger(__name__)

current_email = None
current_identifier = None

GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

async def start(update: Update, context: CallbackContext):
    logger.info("Received /start command")
    
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    username = update.message.from_user.username or "unknown username"

    start_message = (
        "👋 Welcome to the Temp Mail Bot! 🌐\n"
        "Use /help to see the available commands. 💌"
    )

    keyboard = [
        [
            InlineKeyboardButton("👨‍💻 Code Owner", url="https://github.com/hexguard"),
            InlineKeyboardButton("🤖 Contact Owner", url="https://t.me/maario5c"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(start_message, reply_markup=reply_markup)

    # Send a notification to the specified group chat
    if GROUP_CHAT_ID:
        group_message = (
            f"📢 New user started the bot!\n"
            f"User ID: {user_id}\n"
            f"Name: {first_name}\n"
            f"Username: @{username}"
        )
        try:
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=group_message)
        except Exception as e:
            logger.error(f"Failed to notify group chat: {e}")

async def get_email(update: Update, context: CallbackContext):
    global current_email, current_identifier
    logger.info("Received /getEmail command")
    if current_email:
        await update.message.reply_text(f"✉️ You already have a temporary email: {current_email}. Use /reset_email to generate a new email.")
    else:
        current_email, current_identifier = await generate_temp_mail()
        if current_email:
            logger.info(f"Generated email: {current_email}")
            await update.message.reply_text(f"✅ Your temporary email is: {current_email}")
        else:
            logger.error("Failed to generate a temporary email")
            await update.message.reply_text("❌ Failed to generate a temporary email. Please try again later.")

async def view_emails(update: Update, context: CallbackContext):
    logger.info("Received /view_emails command")
    if current_identifier:
        messages = await get_temp_mail_messages(current_identifier)
        if messages:
            for message in messages:
                logger.info(f"Retrieved message from: {message['from']}")
                
                # Escape any special characters or HTML entities
                clean_sender = html.escape(message['from'])
                clean_text = clean_html(message['body'])
                full_message = f"📧 From: {clean_sender}\n\n{clean_text}"
                await send_long_message(update, full_message)
        else:
            logger.info("No messages found")
            await update.message.reply_text("📭 No messages found, or failed to retrieve messages. Please try again later.")
    else:
        logger.warning("No email generated yet")
        await update.message.reply_text("⚠️ You need to generate an email first using /get_email.")

async def reset_email(update: Update, context: CallbackContext):
    global current_email, current_identifier
    logger.info("Received /resetEmail command")
    current_email, current_identifier = await generate_temp_mail()
    if current_email:
        logger.info(f"Generated new email: {current_email}")
        await update.message.reply_text(f"🔄 Your previous email has been removed. Here is your new temp mail: {current_email}")
    else:
        logger.error("Failed to generate a new temporary email")
        await update.message.reply_text("❌ Failed to generate a new temporary email. Please try again later.")

async def help_command(update: Update, context: CallbackContext):
    logger.info("Received /help command")
    help_text = (
        "📧 Here are the available commands:\n"
        "/get_email - Generate a new temporary email address\n"
        "/view_emails - Retrieve emails for the generated temporary address\n"
        "/reset_email - Reset the current email and get a new one\n"
        "/help - See this list of supported commands and descriptions"
    )
    await update.message.reply_text(help_text)

async def send_long_message(update: Update, text: str):
    """Send a long message by splitting it into chunks."""
    max_length = 4096
    for i in range(0, len(text), max_length):
        await update.message.reply_text(text[i:i + max_length], parse_mode=ParseMode.HTML)
