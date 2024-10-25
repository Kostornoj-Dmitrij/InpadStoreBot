from aiogram import Bot, Dispatcher
from config import TOKEN
import os
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)
from transformers import GPT2LMHeadModel, GPT2Tokenizer

user_data = {}


model = GPT2LMHeadModel.from_pretrained("model")
tokenizer = GPT2Tokenizer.from_pretrained("model")