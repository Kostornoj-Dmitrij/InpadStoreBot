from main import bot, user_data
from database import cursor, conn, plugin_descriptions, plugin_short_descriptions
from config import TOKEN
import kb
import os
import uuid
from config import GPT_SECRET_KEY

from gigachat import GigaChat

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
    await show_support_options(user_id)

async def get_links(plugin):
    cursor.execute("SELECT video_link, guide_link, plugin_link FROM Plugins WHERE name = ?", (plugin, ))
    links = cursor.fetchone()
    return "Страница плагина: " + links[2] + "\nТекстовая инструкция: " + links[1] + "\nВидео-инструкция: " + links[0]

async def plugin_choice(chat_id, keyboard):
    if user_data[chat_id].choise == 'support':
        await bot.send_message(chat_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)
    elif user_data[chat_id].plugin_category == 'renga':
        await bot.send_message(chat_id, "С каким плагином у вас возникла проблема?", reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)

async def user_clear(message):
    user_data[message.chat.id].state = 'chat_start'
    user_data[message.chat.id].revit_choise = 'chat_start'
    user_data[message.chat.id].feedback_text = ''
    user_data[message.chat.id].license_key = ''
    user_data[message.chat.id].build_version = ''
    user_data[message.chat.id].revit_version = ''
    user_data[message.chat.id].choise = 'chat_start'
    user_data[message.chat.id].file_path = ''
    user_data[message.chat.id].photo_path = ''
    user_data[message.chat.id].renga_version = ''
    user_data[message.chat.id].plugin_id = ''
    user_data[message.chat.id].plugin_category = 'chat_start'
    user_data[message.chat.id].plugins_build = ''

async def file_saving(message):
    if message.document:
        if message.document.file_size <= 5 * 1024 * 1024:
            file = await bot.get_file(message.document.file_id)
            file_path = f'data/files/{uuid.uuid4()}_{message.document.file_name}'
            await bot.download_file(file.file_path, file_path)
            user_data[message.chat.id].file_path = os.path.basename(file_path)
            
            if user_data[message.chat.id].choise == 'issue' or user_data[message.chat.id].choise == 'install':
                await bot.send_message(message.chat.id, "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист")
            elif user_data[message.chat.id].choise == 'renga_issue' or user_data[message.chat.id].choise == 'full_issue':
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
        if photo.file_size <= 5 * 1024 * 1024:
            file = await bot.get_file(photo.file_id)
            file_path = f'data/files/{uuid.uuid4()}_{photo.file_id}.jpg'
            await bot.download_file(file.file_path, file_path)
            user_data[message.chat.id].photo_path = os.path.basename(file_path)
        else:
            await bot.send_message(message.chat.id, "Файл превышает допустимый размер")
    else:
        await bot.send_message(message.chat.id, "Отправьте изображение, пожалуйста!")
    
    keyboard = kb.file_send_keyboard

    if user_data[message.chat.id].choise == 'issue' or user_data[message.chat.id].choise == 'renga_issue':
        await bot.send_message(message.chat.id, "Отправьте, пожалуйста, файл на котором вышла данная ошибка, чтобы мы смогли изучить данную проблему", reply_markup=keyboard)
    else:
        await save_feedback(message)
        
        await bot.send_message(message.chat.id, "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист.")
        await show_help_options(message.chat.id)

async def save_feedback(message):
    cursor.execute("INSERT INTO Feedback (user_id, feedback_text, license_key, build_version, revit_version, file_path, photo_path, created_at, " \
                   "renga_version, plugin_id, plugins_build) VALUES (?, ?, ?, ?, ?, ?, ?, DATETIME('now'), ?, ?, ?)", 
                   (message.chat.id, user_data[message.chat.id].feedback_text, user_data[message.chat.id].license_key,  
                    user_data[message.chat.id].build_version, user_data[message.chat.id].revit_version, user_data[message.chat.id].file_path, 
                    user_data[message.chat.id].photo_path, user_data[message.chat.id].renga_version, user_data[message.chat.id].plugin_id, user_data[message.chat.id].plugins_build,))
    conn.commit()
    await user_clear(message)

async def get_chatgpt_response(user_message):
    user_message = f'У вас есть информация о следующих плагинах:\n{plugin_short_descriptions}\n Пользователь спрашивает: {user_message}?\n Дай ответ информативно и без лишней воды:'
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

    cursor.execute("INSERT INTO Questions (user_id, question, answer, created_at) VALUES (?, ?, ?, DATETIME('now'))", (message.chat.id, user_query[:100] + '...', chatgpt_response[:100] + '...',))
    conn.commit()
    await send_long_message(message.chat.id, chatgpt_response)