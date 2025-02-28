import io
import os
import logging
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)

logging.basicConfig(level=logging.INFO)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = "deepseek-reasoner"

if not BOT_TOKEN or not DEEPSEEK_API_KEY:
    logging.error("Missing BOT_TOKEN or DEEPSEEK_API_KEY in environment variables.")
    exit(1)

AUTHORIZED_ACCOUNTS = os.getenv("AUTHORIZED_ACCOUNTS", "")
authorized_accounts = [int(acc) for acc in AUTHORIZED_ACCOUNTS.split(",") if acc.strip().isdigit()]

def read_system_prompt():
    try:
        with open('prompt.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        logging.warning("prompt.txt not found. Using default system prompt.")
        return "You are a helpful assistant."

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

async def set_commands(app: Application) -> None:
    commands = [
        BotCommand("start", "Start conversation and initialize history"),
        BotCommand("help", "Show help message"),
        BotCommand("model", "Display current model"),
        BotCommand("clear", "Clear conversation history")
    ]
    await app.bot.set_my_commands(commands)
    logging.info("Bot commands set successfully.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user.id not in authorized_accounts:
        await update.message.reply_text("Unauthorized account.")
        return

    context.user_data["history"] = [{"role": "system", "content": context.bot_data['system_prompt']}]
    
    welcome_text = (
        "Welcome! How can I help you today?\n\n"
        "Available commands:\n"
        "/help - Show this help message\n"
        "/model - Show current model\n"
        "/clear - Clear conversation history\n\n"
        "Type '/' in the input field to see available commands."
    )
    await update.message.reply_text(welcome_text)
    logging.info(f"User {user.id} ({user.username or 'no username'}) sent /start")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are the available commands:\n"
        "/start - Start the conversation and initialize history\n"
        "/help - Show this help message\n"
        "/model - Display the current model in use\n"
        "/clear - Clear the conversation history"
    )
    await update.message.reply_text(help_text)

async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Current model: {MODEL}")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history"] = [{"role": "system", "content": context.bot_data['system_prompt']}]
    await update.message.reply_text("Conversation history cleared.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user.id not in authorized_accounts:
        await update.message.reply_text("Unauthorized account.")
        return

    user_input = update.message.text.strip()
    logging.info(f"User {user.id} ({user.username or 'no username'}) wrote: {user_input}")

    if "history" not in context.user_data:
        context.user_data["history"] = [{"role": "system", "content": context.bot_data['system_prompt']}]

    conversation = context.user_data["history"]

    conversation.append({"role": "user", "content": user_input})

    await update.message.chat.send_action(action="typing")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=conversation,
            temperature=0.0,
            stream=False
        )

        if response.choices and hasattr(response.choices[0].message, 'content'):
            assistant_reply = response.choices[0].message.content
        else:
            logging.error("Unexpected response structure from API.")
            await update.message.reply_text("❌ Unexpected API response format.")
            return

        conversation.append({"role": "assistant", "content": assistant_reply})

        if len(assistant_reply) > 4000:
            text_buffer = io.BytesIO(assistant_reply.encode('utf-8'))
            text_buffer.name = "response.txt"
            await update.message.reply_document(text_buffer)
            await update.message.reply_text("📄 Response was too long, sent as file!")
        else:
            await update.message.reply_text(assistant_reply)

    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        await update.message.reply_text("❌ Sorry, I encountered an error. Please try again!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.bot_data['system_prompt'] = read_system_prompt()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('model', model_command))
    app.add_handler(CommandHandler('clear', clear_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands(app))

    logging.info("Bot started. Polling for messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
