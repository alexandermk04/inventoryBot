import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, PollAnswerHandler, filters, ApplicationBuilder
import logging

from messages.base import start, add_category_from_user, get_categories_message, handle_receipt, handle_expiration_update, \
    handle_category_poll, CategoryProductGetter

from data.repository import get_categories

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your bot token here
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('category', add_category_from_user))
    app.add_handler(CommandHandler('categories', get_categories_message))

    categories = get_categories()

    for category in categories:
        app.add_handler(CommandHandler(category.name, CategoryProductGetter(category.name).get_category_products))

    app.add_handler(MessageHandler(filters.PHOTO, handle_receipt))
    app.add_handler(MessageHandler(filters.REPLY, handle_expiration_update))
    app.add_handler(PollAnswerHandler(handle_category_poll))
    app.add_error_handler(error)

    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()
