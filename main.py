from telebot import TeleBot
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize bot
TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(token=TOKEN)

# Initialize MistralAI Mixtral model and tokenizer
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map={"cuda": 0})

# Create a reference object to store the chat string
class Reference:
    chat_str = ""

# Function to interact with MistralAI Mixtral model using ChatModal
def ChatModal(prompt):
    global Reference
    try:
        Reference.chat_str += f"Aristo: {prompt}\nUser: "
        
        # Encode messages using the MistralAI Mixtral tokenizer
        inputs = tokenizer(Reference.chat_str, return_tensors="pt", max_length=1024, truncation=True)
        
        # Generate a response from the MistralAI Mixtral model
        outputs = model.generate(**inputs, max_length=300, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
        
        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        Reference.chat_str += response
        return response
    except Exception as e:
        error_message = f"MistralAI Mixtral Error: {e}"
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
        "➡️ Hi there, I'm AristoAi! Please follow these commands:\n"
        "➡️ /start - to start the conversation\n"
        "➡️ /clear - to clear the past conversation and context\n"
        "➡️ /help - to get this help menu\n"
        "➡️ /about - to know about the bot and developer\n"
        "➡️ /feedback - to provide feedback\n"
        "➡️ /buycoffee - to buy a coffee for the developer\n"
        "➡️ /contact - to contact the developer"
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
def feedback_handler(message):
    """
    Handler to collect user feedback.
    """
    bot.reply_to(message, "📣 We appreciate your feedback! Please type your feedback, and we'll take it into account.")

@bot.message_handler(commands=['buycoffee'])
def buy_coffee_handler(message):
    """
    Handler to allow users to buy a coffee for the developer.
    """
    coffee_message = "☕️ Thank you so much for considering buying a coffee for the developer! " \
                     "Your support is greatly appreciated. Here's the payment information:\n" \
                     "Momo: 0551784926"
    bot.reply_to(message, coffee_message)

@bot.message_handler(commands=['contact'])
def contact_handler(message):
    """
    Handler to provide contact information for the developer.
    """
    contact_info = (
        "📞 **Contact Developer**:\n"
        "📧 Email: ayimobuobi@gmail.com\n"
        "🔗 GitHub: [github.com/Aristocratjnr](https://github.com/Aristocratjnr)\n"
        "💼 LinkedIn: [linkedin.com/in/obuobi-david-ayim-b40a18241](https://www.linkedin.com/in/obuobi-david-ayim-b40a18241/)\n"
        "💬 Telegram: @aristocratjnr"
    )
    bot.reply_to(message, contact_info, parse_mode='Markdown')

# Remaining handlers remain the same

# ...

# ChatGPT message handler
@bot.message_handler(func=lambda m: True) 
def chatgpt(message):
    """
    Handler to process the user's input and generate a response using the ChatModal function.
    """
    global Reference

    print(f">>> USER: \n{message.text}")
    
    # Use ChatModal function to interact with MistralAI Mixtral model
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
