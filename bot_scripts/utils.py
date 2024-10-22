from main import bot, user_data
from database import cursor, conn
from config import TOKEN
import kb
import re
import requests
import os
import uuid
async def show_help_options(user_id):
    keyboard = kb.help_keyboard
    await bot.send_message(user_id, "Выберите пункт, по которому вам нужна помощь", reply_markup=keyboard)

async def show_support_options(user_id):
    if user_data[user_id].revit_choise != "plugin" and user_data[user_id].revit_choise != 'license':
        user_data[user_id].revit_choise = "support"
    keyboard = kb.plugin_categories_keyboard

    await bot.send_message(user_id, "Выберите категорию, в которой находится плагин:", reply_markup=keyboard)

async def show_questions_options(user_id):
    keyboard = kb.back_to_start_keyboard

    user_data[user_id].state = "asking_question"
    await bot.send_message(user_id, "Задайте ваш вопрос", reply_markup=keyboard)

async def show_license_options(user_id):
    await show_support_options(user_id)

async def get_links(plugin):
    cursor.execute("SELECT video_link, guide_link, plugin_link FROM Plugins WHERE name = ?", (plugin, ))
    links = cursor.fetchone()
    return "Страница плагина: " + links[2] + "\nВидео-инструкция: " + links[0] + "\nТекстовая инструкция: " + links[1]

async def plugin_choice(chat_id, keyboard):
    if user_data[chat_id].revit_choise == 'plugin':
        await bot.send_message(chat_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)


async def file_saving(message):
    if message.document:
        if message.document.file_size <= 5 * 1024 * 1024:
            file = await bot.get_file(message.document.file_id)
            file_path = f'data/files/{uuid.uuid4()}_{message.document.file_name}'
            await bot.download_file(file.file_path, file_path)
            cursor.execute("INSERT INTO Feedback (user_id, feedback_text, license_key, build_version, file_path, created_at) VALUES (?, ?, ?, ?, ?, DATETIME('now'))", (message.chat.id, user_data[message.chat.id].feedback_text, user_data[message.chat.id].license_key,  user_data[message.chat.id].build_version, os.path.basename(file_path),))
            conn.commit()
            await bot.send_message(message.chat.id, "Данный вопрос был передан отделу разработок, в ближайшее время с вами свяжется специалист")
        else:
            await bot.send_message(message.chat.id, "Файл превышает допустимый размер")
    elif message.photo:
        photo = message.photo[-1]
        if photo.file_size <= 5 * 1024 * 1024:
            file = await bot.get_file(photo.file_id)
            file_path = f'data/files/{uuid.uuid4()}_{photo.file_id}.jpg'
            await bot.download_file(file.file_path, file_path)
            cursor.execute("INSERT INTO Feedback (user_id, feedback_text, license_key, build_version, file_path, created_at) VALUES (?, ?, ?, ?, ?, DATETIME('now'))", (message.chat.id, user_data[message.chat.id].feedback_text, user_data[message.chat.id].license_key,  user_data[message.chat.id].build_version, os.path.basename(file_path),))
            conn.commit()
            await bot.send_message(message.chat.id, "Данный вопрос был передан отделу разработок, в ближайшее время с вами свяжется специалист")
        else:
            await bot.send_message(message.chat.id, "Файл превышает допустимый размер")
    
    await show_help_options(message.chat.id)