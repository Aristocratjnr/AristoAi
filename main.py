"""
main.py - Telegram Bot using Gemini API
"""
import os
import logging
from telebot import TeleBot
from dotenv import load_dotenv
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Initialize bot
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logging.error("BOT_TOKEN not found in environment variables. Please set it in your .env file.")
    exit(1)
bot = TeleBot(token=TOKEN)

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"


def get_gemini_response(prompt: str) -> str:
    """
    Send a prompt to the Gemini API and return the response.
    """
    if not GEMINI_API_KEY:
        logging.error("GEMINI_API_KEY not found in environment variables.")
        return "Gemini API key is not configured."
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": GEMINI_API_KEY}
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        # Extract the response text from Gemini API response
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't process your request.")
    except Exception as e:
        logging.error(f"Error accessing Gemini API: {e}")
        return "Sorry, I couldn't process your request at the moment."


@bot.message_handler(func=lambda m: True)
def chat_handler(message):
    """
    Handler to process the user's input and generate a response using the Gemini API.
    """
    text = message.text.strip()
    if text.startswith('/start'):
        welcome_message = "👋 Hello! I'm your bot. How can I assist you today?"
        bot.reply_to(message, welcome_message)
    elif text.startswith('/help'):
        help_message = (
            "🤖 **Help Menu** 🤖\n\n"
            "Here are the available commands:\n\n"
            "➡️ /start - Start the conversation\n"
            "➡️ /help - Display this help message\n"
            "➡️ /about - Learn more about the bot\n"
            "➡️ /feedback - Provide feedback\n"
            "➡️ /buycoffee - Buy me a coffee\n"
            "➡️ /contact - Contact the developer"
        )
        bot.reply_to(message, help_message, parse_mode='Markdown')
    elif text.startswith('/about'):
        about_message = (
            "🤖 **About This Bot** 🤖\n\n"
            "This bot provides assistance using the Gemini API."
        )
        bot.reply_to(message, about_message, parse_mode='Markdown')
    elif text.startswith('/feedback'):
        bot.reply_to(message, "📣 We appreciate your feedback! Please type your feedback, and we'll take it into account.")
    elif text.startswith('/buycoffee'):
        coffee_message = "☕️ Thank you for considering buying me a coffee! Your support is greatly appreciated."
        bot.reply_to(message, coffee_message)
    elif text.startswith('/contact'):
        contact_info = (
            "📞 Contact Developer: 0551784926 \n\n"
            "📧 Email: ayimobuobi@gmail.com\n"
            "🔗 GitHub: [github.com/aristocratjnr](https://github.com/aristocratjnr)\n"
            "💼 LinkedIn: [linkedin.com/in/developer](https://www.linkedin.com/in/developer/)\n"
            "💬 Telegram: @aristocratjnr"
        )
        bot.reply_to(message, contact_info, parse_mode='Markdown')
    else:
        response = get_gemini_response(text)
        bot.reply_to(message, response)


def main():
    logging.info("Starting the bot...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot polling failed: {e}")


if __name__ == '__main__':
    main()
