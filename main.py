import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
from aiogram.filters import Command
import google.generativeai as genai
import asyncio
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация клиента Gemini
genai.configure(api_key="AIzaSyDCZ6cWAss31c5Vo__4KR-pEhn4S104gZw")

# Инициализация бота с использованием DefaultBotProperties
BOT_TOKEN = "7619300974:AAFoHzAQw-9wTU-9I2sY9o3gS0gA9OeWjLY"
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

# Создание роутера
router = Router()

# Инициализация модели и сессии чата
generation_config = {
    "temperature": 1,  # Adjust temperature as needed
    "top_p": 0.95,      # Adjust top_p as needed
    "top_k": 40,       # Adjust top_k as needed
    "max_output_tokens": 8192, # Adjust max_output_tokens as needed
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)
chat_session = model.start_chat()  # Initialize an empty chat session

# Функция старта бота
@router.message(Command("start"))
async def start(message: Message):
    await message.answer('Привет! Я бот, подключенный к Google Gemini. Как я могу помочь?')

# Функция обработки сообщений пользователя
@router.message()
async def handle_message(message: Message):
    user_message = message.text
    gemini_response = chat_session.send_message(user_message)

    try:
        await message.answer(gemini_response.text)
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        await message.answer("Произошла ошибка при отправке сообщения.")

# Основная функция запуска бота
async def main():
    dp = Dispatcher()  # Убедитесь, что Dispatcher инициализирован правильно
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
