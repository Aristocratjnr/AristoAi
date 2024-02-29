import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor

API_TOKEN = '6832344311:AAGRC5sj8LSnWkw8QuPvmqFhTY7_7VQrkl0'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Command message handler
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when the user sends "/start" or "/help" command
    """
    await message.reply("Hi!\n I'm AristoAi!\nPowered by aiogram.")

# Echo message handler
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
