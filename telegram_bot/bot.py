import requests
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import os

TOKEN = os.getenv("BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

NAME, INTEREST = range(2)


def start(update, context):
    update.message.reply_text("سلام دوست عزیز. لطفا نام خود را وارد کنید: ",)
    return NAME


def name(update, context):
    user = update.message.from_user
    logger.info("Name of %s: %s", user.id, update.message.text)
    update.message.reply_text(
        "لطفا زمینه ی کاری مورد علاقه ی خود را وارد کنید تا از جدید ترین موقعیت های شغلی موجود در بازار باخبر شوید. "
    )

    return INTEREST


def interest(update, context):
    user = update.message.from_user
    logger.info("interest of %s: %s", user.id, update.message.text)
    results = requests.post(
        "http://jobinja:5000/query-jobinja",
        json={"job_title": update.message.text},
        headers={"Content-Type": "application/json"},
    )
    for result in results.json()["results"]:
        update.message.reply_text("\n\n".join(result.values()))

    results = requests.post(
        "http://jobvision:5000/query-jobvision",
        json={"job_title": update.message.text},
        headers={"Content-Type": "application/json"},
    )
    print(">>>>>>> ", results)
    for result in results.json()["results"]:
        update.message.reply_text("\n\n".join(result.values()))
    return INTEREST


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.regex(".*"), name)],
            INTEREST: [MessageHandler(Filters.regex(".*"), interest),],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
