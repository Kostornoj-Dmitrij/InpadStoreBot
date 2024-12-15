from main import bot, user_data
from database import cursor, conn, plugin_short_descriptions, project_dir
import kb
import os
import uuid
from config import GPT_SECRET_KEY, B24_WEBHOOK
from gigachat import GigaChat
import requests
from airtable_utils import create_record, update_record
from datetime import datetime
import pytz
from airtable_utils import save_trace

async def show_help_options(user_id):
    keyboard = kb.help_keyboard
    await bot.send_message(user_id, "Выберите пункт, по которому вам нужна помощь", reply_markup=keyboard)

async def show_support_options(user_id):
    keyboard = kb.plugin_categories_keyboard
    await bot.send_message(user_id, "Выберите категорию, в которой находится плагин:", reply_markup=keyboard)

async def show_questions_options(user_id):
    user_data[user_id].state = "asking_question"

    keyboard = kb.back_to_start_keyboard
    await bot.send_message(user_id, "Задайте ваш вопрос", reply_markup=keyboard)

async def show_license_options(user_id):
    keyboard = kb.license_keyboard_options
    await bot.send_message(user_id, "Выберите одну из кнопок", reply_markup=keyboard)

async def get_links(plugin):
    cursor.execute("SELECT video_link, guide_link, plugin_link FROM Plugins WHERE name = ?", (plugin, ))
    links = cursor.fetchone()
    if links[2] == "plugin_link" and links[1] == "guide_link":
        return "Страница плагина: " + links[2]
    if links[2] == "plugin_link":
        return "Текстовая инструкция: " + links[1] + "\nВидео-инструкция: " + links[0]
    if links[1] == "guide_link":
        return "Страница плагина: " + links[2] + "\nВидео-инструкция: " + links[0]
    return "Страница плагина: " + links[2] + "\nТекстовая инструкция: " + links[1] + "\nВидео-инструкция: " + links[0]

async def plugin_choice(chat_id, keyboard):
    if user_data[chat_id].choice == "support":
        await bot.send_message(chat_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)
    elif user_data[chat_id].plugin_category == "renga":
        await bot.send_message(chat_id, "С каким плагином у вас возникла проблема?", reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)

async def user_clear(message):
    user_data[message.chat.id].state = "chat_start"
    user_data[message.chat.id].revit_choice = "chat_start"
    user_data[message.chat.id].feedback_text = ""
    user_data[message.chat.id].license_key = ""
    user_data[message.chat.id].build_version = ""
    user_data[message.chat.id].revit_version = ""
    user_data[message.chat.id].choice = "chat_start"
    user_data[message.chat.id].file_path = ""
    user_data[message.chat.id].photo_path = ""
    user_data[message.chat.id].renga_version = ""
    user_data[message.chat.id].plugin_id = ""
    user_data[message.chat.id].plugin_category = "chat_start"
    user_data[message.chat.id].plugins_build = ""
    user_data[message.chat.id].fio = ""

async def file_saving(message):
    if message.document:
        if message.document.file_size <= 100 * 1024 * 1024:
            file = await bot.get_file(message.document.file_id)
            file_path = os.path.join(project_dir, "data", "files", f"{uuid.uuid4()}_{message.document.file_name}")
            await bot.download_file(file.file_path, file_path)
            user_data[message.chat.id].file_path = os.path.basename(file_path)

            if user_data[message.chat.id].choice == "issue" or user_data[message.chat.id].choice == "install":
                await bot.send_message(message.chat.id, "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист")
            elif user_data[message.chat.id].choice == "renga_issue" or user_data[message.chat.id].choice == "full_issue":
                await bot.send_message(message.chat.id, "Данный вопрос был передан отделу разработок, в ближайшее время с вами свяжется специалист")

            await save_feedback(message)

        else:
            await bot.send_message(message.chat.id, "Файл превышает допустимый размер")
    else:
        await bot.send_message(message.chat.id, "Отправьте файл, пожалуйста!")

    await show_help_options(message.chat.id)

async def screen_saving(message):
    if message.photo:
        photo = message.photo[-1]
        if photo.file_size <= 20 * 1024 * 1024:
            file = await bot.get_file(photo.file_id)
            file_path = os.path.join(project_dir, "data", "files", f"{uuid.uuid4()}_{photo.file_id}.jpg")
            await bot.download_file(file.file_path, file_path)
            user_data[message.chat.id].photo_path = os.path.basename(file_path)
        else:
            await bot.send_message(message.chat.id, "Файл превышает допустимый размер")
    else:
        await bot.send_message(message.chat.id, "Отправьте изображение, пожалуйста!")

    keyboard = kb.file_send_keyboard

    if user_data[message.chat.id].choice == "issue" or user_data[message.chat.id].choice == "renga_issue":
        await bot.send_message(message.chat.id, "Отправьте, пожалуйста, файл на котором вышла данная ошибка, чтобы мы смогли изучить данную проблему", reply_markup=keyboard)
    else:
        await save_feedback(message)

        await bot.send_message(message.chat.id, "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист.")
        await show_help_options(message.chat.id)

async def save_feedback(message):
    cursor.execute("SELECT user_id FROM Users WHERE t_user_chat_id = ?", (message.chat.id, ))
    user_id = cursor.fetchone()[0]
    if user_data[message.chat.id].plugin_category == "renga":
        cursor.execute("INSERT INTO Renga_Feedback (user_id, feedback_text, license_key, renga_version, plugins_build, plugin_id, file_path, photo_path, created_at"
                       ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATETIME('now'))",
                       (user_id, user_data[message.chat.id].feedback_text, user_data[message.chat.id].license_key,
                        user_data[message.chat.id].renga_version, user_data[message.chat.id].plugins_build, user_data[message.chat.id].plugin_id, user_data[message.chat.id].file_path,
                        user_data[message.chat.id].photo_path, ))
        data = {
            "records": [
                {
                    "fields": {
                        "user_id": user_id,
                        "feedback_text": user_data[message.chat.id].feedback_text,
                        "license_key": user_data[message.chat.id].license_key,
                        "renga_version": user_data[message.chat.id].renga_version,
                        "plugins_build": user_data[message.chat.id].plugins_build,
                        "plugin_id": user_data[message.chat.id].plugin_id,
                        "file_path": user_data[message.chat.id].file_path,
                        "photo_path": user_data[message.chat.id].photo_path,
                        "created_at": datetime.now(pytz.timezone("Europe/Moscow")).isoformat()
                    }
                }
            ]
        }
        await create_record("Renga_Feedback", data)

    else:
        cursor.execute("INSERT INTO Revit_Feedback (user_id, feedback_text, license_key, revit_version, build_version, plugin_id, file_path, photo_path, created_at"
                       ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATETIME('now'))",
                       (user_id, user_data[message.chat.id].feedback_text, user_data[message.chat.id].license_key,
                        user_data[message.chat.id].revit_version, user_data[message.chat.id].build_version, user_data[message.chat.id].plugin_id,
                        user_data[message.chat.id].file_path, user_data[message.chat.id].photo_path,))
        data = {
            "records": [
                {
                    "fields": {
                        "user_id": user_id,
                        "feedback_text": user_data[message.chat.id].feedback_text,
                        "license_key": user_data[message.chat.id].license_key,
                        "revit_version": user_data[message.chat.id].revit_version,
                        "build_version": user_data[message.chat.id].build_version,
                        "plugin_id": user_data[message.chat.id].plugin_id,
                        "file_path": user_data[message.chat.id].file_path,
                        "photo_path": user_data[message.chat.id].photo_path,
                        "created_at": datetime.now(pytz.timezone("Europe/Moscow")).isoformat()
                    }
                }
            ]
        }
        await create_record("Revit_Feedback", data)

    conn.commit()
    await user_clear(message)

async def save_license_feedback(message):
    cursor.execute("SELECT * FROM Users WHERE t_user_chat_id = ?", (message.chat.id, ))
    user_id = cursor.fetchone()[0]
    cursor.execute("UPDATE Users SET fio = ?, face = ?, company_name = ?, city = ?, email = ?, phone_number = ? WHERE user_id = ?",
                   (user_data[message.chat.id].fio, user_data[message.chat.id].face, user_data[message.chat.id].company_name,
                    user_data[message.chat.id].city, user_data[message.chat.id].email, user_data[message.chat.id].phone_number, user_id))
    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id, ))
    selected_data = cursor.fetchone()
    data = {
        "fields": {
            "fio": selected_data[4],
            "face": selected_data[5],
            "company_name": selected_data[6],
            "city": selected_data[7],
            "email": selected_data[8],
            "phone_number": selected_data[9],
        }
    }

    await update_record("Users", data, user_id)
    if user_data[message.chat.id].choice == "buy_plugin":
        cursor.execute("INSERT INTO Licenses_Requests (request_type, user_id, plugins, license_count, created_at, demonstration_should"
                       ") VALUES (?, ?, ?, ?, DATETIME('now'), ?)",
                       ("Покупка плагинов", user_id, user_data[message.chat.id].plugins_for_buy, user_data[message.chat.id].license_count,
                        user_data[message.chat.id].demonstration_should))
        data = {
            "records": [
                {
                    "fields": {
                        "request_type": "Покупка плагинов",
                        "user_id": user_id,
                        "plugins": user_data[message.chat.id].plugins_for_buy,
                        "license_count": user_data[message.chat.id].license_count,
                        "created_at": datetime.now(pytz.timezone("Europe/Moscow")).isoformat(),
                        "demonstration_should": user_data[message.chat.id].demonstration_should
                    }
                }
            ]
        }
        await create_record("Licenses_Requests", data)

    else:
        cursor.execute("INSERT INTO Licenses_Requests (request_type, user_id, plugins, license_count, created_at, demonstration_should"
                       ") VALUES (?, ?, ?, ?, DATETIME('now'), ?)",
                       ("Тестирование плагинов", user_id, user_data[message.chat.id].plugins_for_buy, user_data[message.chat.id].license_count,
                        user_data[message.chat.id].demonstration_should))
        data = {
            "records": [
                {
                    "fields": {
                        "request_type": "Тестирование плагинов",
                        "user_id": user_id,
                        "plugins": user_data[message.chat.id].plugins_for_buy,
                        "license_count": user_data[message.chat.id].license_count,
                        "created_at": datetime.now(pytz.timezone("Europe/Moscow")).isoformat(),
                        "demonstration_should": user_data[message.chat.id].demonstration_should
                    }
                }
            ]
        }
        await create_record("Licenses_Requests", data)

    conn.commit()
    await user_clear(message)

async def get_chatgpt_response(user_message):
    user_message = f"У вас есть информация о следующих плагинах:\n{plugin_short_descriptions}\n Пользователь спрашивает: {user_message}?\n Дай ответ информативно и без лишней воды:"
    try:
        with GigaChat(credentials=GPT_SECRET_KEY, verify_ssl_certs=False) as giga:
            response = giga.chat(user_message)
            return response.choices[0].message.content
    except:
        return "Пожалуйста, сократите ваш вопрос"

async def send_long_message(chat_id, text, chunk_size=4096):
    for i in range(0, len(text), chunk_size):
        await bot.send_message(chat_id, text[i:i + chunk_size])

async def answer_generation(message):
    user_query = message.text
    chatgpt_response = await get_chatgpt_response(user_query)

    cursor.execute("SELECT user_id FROM Users WHERE t_user_chat_id = ?", (message.chat.id, ))
    user_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO Questions (user_id, question, answer, created_at) VALUES (?, ?, ?, DATETIME('now'))", (user_id, user_query[:100] + "...", chatgpt_response[:100] + "...",))
    conn.commit()

    data = {
        "records": [
            {
                "fields": {
                    "user_id": user_id,
                    "question": user_query[:100] + "...",
                    "answer": chatgpt_response[:100] + "...",
                    "created_at": datetime.now(pytz.timezone("Europe/Moscow")).isoformat()
                }
            }
        ]
    }
    await create_record("Questions", data)

    await send_long_message(message.chat.id, chatgpt_response)

async def send_data_to_bitrix(message, data):
    payload = {
        "fields": {
            "TITLE": "Запрос от Telegram-бота",
            "NAME": message.chat.id,
            "DESCRIPTION": f"Пользователь ввел версию сборки: {user_data[message.chat.id].build_version}",
            "RESPONSIBLE_ID": 1
        }
    }

    try:
        response = requests.post(
            f"{B24_WEBHOOK}crm.lead.add.json", json=payload
        )
    except Exception as e:
        print(f"Произошла ошибка при взаимодействии с Битрикс24: {str(e)}")