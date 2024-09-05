# bot.py
import logging
from telegram.ext import Application, CommandHandler
from handlers import start, get_email, view_emails, reset_email, help_command
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_email", get_email))
    application.add_handler(CommandHandler("view_emails", view_emails))
    application.add_handler(CommandHandler("reset_email", reset_email))
    application.add_handler(CommandHandler("help", help_command))

    logger.info("Bot started")
    application.run_polling()

if __name__ == "__main__":
    main()
