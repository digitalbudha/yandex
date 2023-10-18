import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares import LoggingMiddleware
from aiogram.utils import executor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Инициализация
load_dotenv()
logging.basicConfig(filename="error.log", level=logging.ERROR)
bot = Bot(token=os.environ['TELEGRAM_API_TOKEN'])
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Инициализация Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_API_CREDENTIALS'], scope)
gc = gspread.authorize(creds)
worksheet = gc.open_by_key(os.environ['SPREADSHEET_ID']).sheet1

# Обработчик входящих сообщений
@dp.message_handler()
async def on_message(message: types.Message):
    try:
        username = message.from_user.username
        timestamp = message.date
        text = message.text
        row = [str(timestamp), username, text]
        worksheet.append_row(row)
    except Exception as e:
        logging.error(f"Error: {e}")
    await message.answer("Сообщение записано в Google Sheets.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)