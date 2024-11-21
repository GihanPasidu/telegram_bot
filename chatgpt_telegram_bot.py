import logging
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Set your OpenAI API Key and Telegram Bot Token
OPENAI_API_KEY = "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"
TELEGRAM_BOT_TOKEN = "7816276179:AAHqO3aSGAXEB_o-HD37Mq4KkVvFwZY7Y20"

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your ChatGPT-powered bot. Ask me anything.")

# Function to handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Generate a response using OpenAI ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
       )
        reply = response['choices'][0]['message']['content'].strip()

        # Send the response back to the user
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Error while processing message: {e}")
        await update.message.reply_text("Sorry, I couldn't process that. Please try again later.")

# Function to log errors
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Main function to run the bot
def main():
    # Set up the bot application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
