import logging
from aiogram import Bot, Dispatcher, executor, types
from transformers import AutoModelForCausalLM, AutoTokenizer

API_TOKEN = '6832344311:AAFfQGEJS1ttkPPMXv2sy4s3fj4rbGWIyGY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Load MistralAI Mixtral model and tokenizer
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map={"cuda": 0})

# Command message handler
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when the user sends "/start" or "/help" command
    """
    welcome_message = "Hi!\nI'm AristoAi!\nPowered by MistralAI Mixtral."
    await message.reply(welcome_message)

# Echo message handler
@dp.message_handler()
async def chat_with_mistral(message: types.Message):
    """
    Handler to chat with the MistralAI Mixtral model
    """
    user_input = message.text

    # Prepare input for MistralAI Mixtral model
    chat_history = [
        {"role": "user", "content": user_input},
    ]

    inputs = tokenizer.apply_chat_template(chat_history, return_tensors="pt").to("cuda")

    # Generate response from MistralAI Mixtral model
    outputs = model.generate(inputs, max_new_tokens=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Send the response to the user
    await message.answer(response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
