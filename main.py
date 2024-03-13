from telebot import TeleBot
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Initialize bot
TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(token=TOKEN)

# Function to interact with Gemini API
def get_gemini_response(prompt):
    try:
        # Make a request to the Gemini API
        response = requests.get('AIzaSyCj91hAkWdcvwe_71NiJmFAORFLa2KfBOA', params={'prompt': prompt})
        data = response.json()
        return data['response'] if 'response' in data else None
    except Exception as e:
        print(f"Error accessing Gemini API: {e}")
        return None

# Chat message handler
@bot.message_handler(func=lambda m: True)
def chat_handler(message):
    """
    Handler to process the user's input and generate a response using the Gemini API.
    """
    if message.text.startswith('/start'):
        welcome_message = "👋 Hello! I'm your bot. How can I assist you today?"
        bot.reply_to(message, welcome_message)
    elif message.text.startswith('/help'):
        help_message = (
            "🤖 **Help Menu** 🤖\n\n"
            "Here are the available commands:\n\n"
            "➡️ /start - Start the conversation\n"
            "➡️ /help - Display this help message\n"
            "➡️ /about - Learn more about the bot\n"
            "➡️ /feedback - Provide feedback\n"
            "➡️ /buycoffee - Buy me a coffee ☕️\n"
            "➡️ /contact - Contact the developer"
        )
        bot.reply_to(message, help_message, parse_mode='Markdown')
    elif message.text.startswith('/about'):
        about_message = "🤖 **About This Bot** 🤖\n\n" \
                        "This bot provides assistance using the Gemini API."
        bot.reply_to(message, about_message, parse_mode='Markdown')
    elif message.text.startswith('/feedback'):
        bot.reply_to(message, "📣 We appreciate your feedback! Please type your feedback, and we'll take it into account.")
    elif message.text.startswith('/buycoffee'):
        coffee_message = "☕️ Thank you for considering buying me a coffee! Your support is greatly appreciated."
        bot.reply_to(message, coffee_message)
    elif message.text.startswith('/contact'):
        contact_info = (
            "📞 **Contact Developer**:\n\n"
            "📧 Email: ayimobuobi@gmail.com\n"
            "🔗 GitHub: [github.com/developer](https://github.com/developer)\n"
            "💼 LinkedIn: [linkedin.com/in/developer](https://www.linkedin.com/in/developer/)\n"
            "💬 Telegram: @aristocratjnr"
        )
        bot.reply_to(message, contact_info, parse_mode='Markdown')
    else:
        response = get_gemini_response(message.text)
        if response:
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Sorry, I couldn't process your request at the moment.")

if __name__ == '__main__':
    print("Starting the bot...")
    bot.polling()
