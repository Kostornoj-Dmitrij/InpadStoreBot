from aiogram import Bot, Dispatcher
from config import TOKEN
import os
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

user_data = {}