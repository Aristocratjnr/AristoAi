import os
from dotenv import load_dotenv
from telebot import TeleBot
import openai
import time

# Load environment variables
load_dotenv()

# Set OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

# Create a reference object to store the chat string and current model
class Reference:
    chat_str = ""

# Initialize bot
TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(token=TOKEN)

# Function to interact with OpenAI API using ChatModal
def ChatModal(prompt):
    global Reference
    try:
        Reference.chat_str += f"Aristo: {prompt}\nUser: "
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Specify gpt-3.5-turbo model
            prompt=Reference.chat_str,
            max_tokens=150,  # Adjust as needed
        )
        Reference.chat_str += f"{response['choices'][0]['text']}"
        return response['choices'][0]['text']
    except openai.error.OpenAIError as e:
        error_message = f"OpenAI Error: {e}"
        print(error_message)
        return error_message

# Command handlers
@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Handler to welcome the user and clear past conversation and context.
    """
    clear_past()
    welcome_message = "👋 Hello! You're welcome, I'm a Student bot created by Aristocrat. How may I help you today? \n\n" \
                
    bot.reply_to(message, welcome_message)

@bot.message_handler(commands=['clear'])
def clear(message):
    """
    Handler to clear the previous conversation and context.
    """
    clear_past()
    bot.reply_to(message, "🗑️ Cleared the past context and chat buddy!")

@bot.message_handler(commands=['help'])
def helper(message):
    """
    Handler to display the help menu.
    """
    help_command = (
        "➡️ Hi there, I'm chatGPT bot created by Aristocrat! Please follow these commands:\n"
        "➡️ /start - to start the conversation\n"
        "➡️ /clear - to clear the past conversation and context\n"
        "➡️ /help - to get this help menu\n"
        "➡️ /menu - to see the menu\n"
        "➡️ /about_developer - to know about the developer\n"
        "➡️ /feedback - to provide feedback\n"
        "➡️ /buycoffee - to buy a coffee for the developer"
    )
    bot.reply_to(message, help_command)

@bot.message_handler(commands=['about'])
def about_bot(message):
    """
    Handler to provide information about the bot and its creator.
    """
    bot_info = (
        "🤖 **About AristoAi Bot**\n\n"
        "Hello! I am AristoAi, a chatbot created by Aristocrat. I am designed to assist students in their research purposes. "
        "Feel free to ask me questions or seek help with your studies!\n\n"
        "👨‍💻 **About the Developer**\n\n" 
        "Aristocrat is a level 300 student pursuing a Bachelor of Science in Information Technology. "
        "I created this bot to aid fellow students in their academic endeavors through my Telegram bot.\n\n"
        "If you have any questions or suggestions, feel free to reach out!"
    )
    bot.reply_to(message, bot_info, parse_mode='Markdown')

@bot.message_handler(commands=['feedback'])
def feedback(message):
    """
    Handler to collect user feedback.
    """
    bot.reply_to(message, "📣 We appreciate your feedback! Please type your feedback, and we'll take it into account.")

@bot.message_handler(commands=['buycoffee'])
def buy_coffee(message):
    """
    Handler to allow users to buy a coffee for the developer.
    """
    coffee_message = "☕️ Thank you so much for considering buying a coffee for the developer! " \
                     "Your support is greatly appreciated. Here's the payment information:\n" \
                     "Momo: 0551784926"
    bot.reply_to(message, coffee_message)

# Add this handler for the /contact command
@bot.message_handler(commands=['contact'])
def contact_handler(message):
    contact_info = (
        "📞 **Contact Developer**:\n"
        "📧 Email: ayimobuobi@gmail.com\n"
        "🔗 GitHub: [github.com/Aristocratjnr](https://github.com/Aristocratjnr)\n"
        "💼 LinkedIn: [linkedin.com/in/obuobi-david-ayim-b40a18241](https://www.linkedin.com/in/obuobi-david-ayim-b40a18241/)\n"
        "💬 Telegram: @aristocratjnr"
    )
    bot.reply_to(message, contact_info, parse_mode='Markdown')

# ChatGPT message handler
@bot.message_handler(func=lambda m: True) 
def chatgpt(message):
    """
    Handler to process the user's input and generate a response using the ChatModal function.
    """
    global Reference

    print(f">>> USER: \n{message.text}")
    
    # Use ChatModal function to interact with OpenAI API
    response = ChatModal(message.text)
    
    Reference.chat_str += message.text + response
    
    print(f">>> chatGPT: \n{Reference.chat_str}")
    
    # Check if the response contains meaningful content
    if response:
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "🤔 I'm sorry, I didn't understand that. Can you please ask in a different way?")

# Function to clear the previous conversation and context
def clear_past():
    Reference.chat_str = ""

if __name__ == '__main__':
    print("Starting AristoAi...")
    bot.polling()
