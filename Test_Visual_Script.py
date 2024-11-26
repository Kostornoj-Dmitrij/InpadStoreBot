from bot_scripts.config import TOKEN, YOOTOKEN

from aiogram import Bot, Dispatcher, types
import asyncio
from user import User

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)
user_balance = {'user_id': 0}
user_data = {}

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    user_id = message.chat.id
    username = message.chat.username
    if username == None:
        username = 'InpadStore'
    
    user = User(user_id)
    user_data[user_id] = user
    
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('Помощь', callback_data='help'))
    keyboard.add(types.InlineKeyboardButton('Подробная информация о плагинах', callback_data='support'))
    keyboard.add(types.InlineKeyboardButton('Задать вопрос ИИ-консультанту', callback_data='questions'))
    keyboard.add(types.InlineKeyboardButton('Оформить лицензию', callback_data='license'))
                    
    user_data[1390442427].chat_id = 1
    user_data[1390442427].user_id = 1
    user_data[1390442427].keywords_id = 1
    await bot.send_message(user_id, "Привет! Добро пожаловать в бота.", reply_markup=keyboard)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'asking_question') 
async def asking_question(message): 
    await bot.send_message(message.chat.id, "Ответ на вопрос...")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Задать вопрос ещё раз', callback_data='questions'))
    keyboard.add(types.InlineKeyboardButton('Перейти на оператора', callback_data='operator'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='start'))

    await bot.send_message(message.chat.id, "Вам помог ответ?", reply_markup=keyboard)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'license_key_input') 
async def license_key_input(message): 
    user_data[message.chat.id].state = 'build_version_input'

    await bot.send_message(message.chat.id, "Напишите, пожалуйста, номер сборки, которую вы установили")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'build_version_input') 
async def build_version_input(message): 
    
    if user_data[message.chat.id].revit_choice == 'plugin':
        user_data[message.chat.id].state = 'plugin_question_input'
        await bot.send_message(message.chat.id, "Опишите ваш вопрос")
    elif user_data[message.chat.id].revit_choice == 'issue':
        user_data[message.chat.id].state = 'issue_description_input'
        await bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот ошибки и опишите вашу проблему")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'issue_description_input') 
async def issue_description_input(message): 
    await bot.send_message(message.chat.id, "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'plugin_question_input') 
async def plugin_question_input(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Отправить файл', callback_data='file_sending'))
    keyboard.add(types.InlineKeyboardButton('Не отправлять файл', callback_data='file_not_sending'))
    await bot.send_message(message.chat.id, "Отправьте, пожалуйста, файл на котором у вас возник вопрос", reply_markup=keyboard)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'file_sending', content_types=['document', 'photo']) 
async def file_sending(message):
    await bot.send_message(message.chat.id, "Данный вопрос был передан отделу разработок, в ближайшее время с вами свяжется специалист")
    await start(message)

@dp.message_handler(content_types=['photo']) 
async def issue_description_input(message): 
    await bot.send_message(message.chat.id, "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист")
    await start(message)


@dp.message_handler(lambda message: True)
async def handle_text(message):
    user_id = message.chat.id
    if message.text == '/help':
        await show_help_options(user_id)
    elif message.text == '/support':
        await show_support_options(user_id)
    elif message.text == '/questions':
        await show_questions_options(user_id)
    elif message.text == '/license':
        await show_license_options(user_id)

async def show_help_options(user_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Хочу задать вопрос касаемо работы плагина', callback_data='plugin_work_help'))
    keyboard.add(types.InlineKeyboardButton('Хочу сообщить об ошибке', callback_data='issue_help'))
    keyboard.add(types.InlineKeyboardButton('Нужна помощь при установке/активации', callback_data='install_help'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='start'))
    await bot.send_message(user_id, "Выберите пункт, по которому вам нужна помощь", reply_markup=keyboard)

async def show_support_options(user_id):
    if user_data[user_id].revit_choice != 'plugin':
        user_data[user_id].revit_choice = 'support'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton('Концепция', callback_data='conception'),
                types.InlineKeyboardButton('Архитектура', callback_data='architecture'))
    keyboard.row(types.InlineKeyboardButton('Конструктив', callback_data='constructive'),
                types.InlineKeyboardButton('ОВ и ВК', callback_data='ov_vk'))
    keyboard.row(types.InlineKeyboardButton('Боксы и отверстия', callback_data='boxes'),
                types.InlineKeyboardButton('Общие', callback_data='general'))
    keyboard.row(types.InlineKeyboardButton('Renga', callback_data='renga'),
                types.InlineKeyboardButton('Назад', callback_data='start'))

    await bot.send_message(user_id, "Выберите категорию, в которой находится плагин:", reply_markup=keyboard)

async def show_questions_options(user_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='start'))
    user_data[user_id].state = 'asking_question'
    await bot.send_message(user_id, "Задайте ваш вопрос", reply_markup=keyboard)

async def show_license_options(user_id):
    await show_support_options(user_id)

@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
    user_id = call.message.chat.id
    
    if call.data == 'start':
        await start(call.message)
    
    elif call.data == 'help':
        await show_help_options(call.message.chat.id)

    elif call.data == 'support':
        await show_support_options(call.message.chat.id)

    elif call.data == 'questions':
        await show_questions_options(call.message.chat.id)
    
    elif call.data == 'license':
        prices = [types.LabeledPrice(label='Руб', amount = 500000)]
        await bot.send_invoice(call.message.chat.id, title="Модуль 'Планировка'",
                         description='payment',
                         provider_token=YOOTOKEN, currency='RUB',
                         start_parameter='test_bot', prices=prices, payload='test-invoice-payload')
        
        await show_license_options(call.message.chat.id)

    elif call.data == 'plugin_work_help':
        user_data[call.message.chat.id].revit_choice = 'plugin'
        await show_support_options(call.message.chat.id)

    elif call.data == 'issue_help':
        user_data[call.message.chat.id].revit_choice = 'plugin'
        await show_support_options(call.message.chat.id)

    elif call.data == 'install_help':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Ошибка при установке сборки', callback_data='install_error'))
        keyboard.add(types.InlineKeyboardButton('Не получается зарегистрироваться', callback_data='registration_error'))
        keyboard.add(types.InlineKeyboardButton('Не получается ввести ключ активации', callback_data='activation_error'))
        keyboard.add(types.InlineKeyboardButton('Назад', callback_data='help'))

        await bot.send_message(call.message.chat.id, "Выберите категорию, по которой вам нужна помощь.", reply_markup=keyboard)
    
    elif call.data in ["install_error", "registration_error", "activation_error"]:
        user_data[call.message.chat.id].revit_choice = 'issue'
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('Revit 2019', callback_data='revit'),
                    types.InlineKeyboardButton('Revit 2020', callback_data='revit'))
        keyboard.row(types.InlineKeyboardButton('Revit 2021', callback_data='revit'),
                    types.InlineKeyboardButton('Revit 2022', callback_data='revit'))
        keyboard.row(types.InlineKeyboardButton('Revit 2023', callback_data='revit'),
                    types.InlineKeyboardButton('Revit 2024', callback_data='revit'))
        keyboard.row(types.InlineKeyboardButton('Revit 2025', callback_data='revit'),
                    types.InlineKeyboardButton('Назад', callback_data='install_help'))
        await bot.send_message(call.message.chat.id, "Выберите версию Revit, в котором запускали плагин", reply_markup=keyboard)
    
    elif call.data == "revit":
        user_data[call.message.chat.id].state = 'license_key_input'
        await bot.send_message(call.message.chat.id, "Введите, пожалуйста, ваш лицензионный ключ, который вы использовали")
    
    elif call.data == 'conception':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('Инсоляция', callback_data='plugin'),
                    types.InlineKeyboardButton('КЕО', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Генерация парков', callback_data='plugin'),
                    types.InlineKeyboardButton('Генерация деревьев', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Разлиновка модели', callback_data='plugin'),
                    types.InlineKeyboardButton('3D сетки', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('БыстроТЭПы', callback_data='plugin'),
                    types.InlineKeyboardButton('Подсчет площадей', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Назад', callback_data='support'))
        if user_data[call.message.chat.id].revit_choice == 'plugin':
            await bot.send_message(user_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)
        else:
            await bot.send_message(user_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)
    
    elif call.data == 'architecture':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('Определить помещение', callback_data='plugin'),
                    types.InlineKeyboardButton('Расчет плинтуса', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Отделка', callback_data='plugin'),
                    types.InlineKeyboardButton('Копировать отделку', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Проемы по дверям/окнам из связи', callback_data='plugin'),
                    types.InlineKeyboardButton('Соединение полов', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Подсчет площадей', callback_data='plugin'),
                    types.InlineKeyboardButton('Планировка', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Округление площади', callback_data='plugin'),
                    types.InlineKeyboardButton('Нумерация квартир', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Назад', callback_data='support'))

        if user_data[call.message.chat.id].revit_choice == 'plugin':
            await bot.send_message(user_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)
        else:
            await bot.send_message(user_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)
    
    elif call.data == 'constructive':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('Сборка арматуры', callback_data='plugin'),
                    types.InlineKeyboardButton('Создать разрезы и сечения', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Создание планов', callback_data='plugin'),
                    types.InlineKeyboardButton('Создание контура', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Редактирование контура', callback_data='plugin'),
                    types.InlineKeyboardButton('Расчет продавливания', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Создание каркасов', callback_data='plugin'),
                    types.InlineKeyboardButton('Создание видов каркасов', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Назад', callback_data='support'))

        if user_data[call.message.chat.id].revit_choice == 'plugin':
            await bot.send_message(user_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)
        else:
            await bot.send_message(user_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)
    
    elif call.data == 'ov_vk':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('Муфты/гильзы', callback_data='plugin'),
                    types.InlineKeyboardButton('Аэродинамика', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Создать виды систем', callback_data='plugin'),
                    types.InlineKeyboardButton('Спецификации систем', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Высотные отметки', callback_data='plugin'),
                    types.InlineKeyboardButton('Толщина стенки', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Диаметр изоляции', callback_data='plugin'),
                    types.InlineKeyboardButton('S изоляции', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Назад', callback_data='support'))

        if user_data[call.message.chat.id].revit_choice == 'plugin':
            await bot.send_message(user_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)
        else:
            await bot.send_message(user_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)
    
    elif call.data == 'boxes':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('Создание заданий', callback_data='plugin'),
                    types.InlineKeyboardButton('Объединение', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Смещение', callback_data='plugin'),
                    types.InlineKeyboardButton('Обрезать', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Нумерация', callback_data='plugin'),
                    types.InlineKeyboardButton('Отметка', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Отверстия', callback_data='plugin'),
                    types.InlineKeyboardButton('Проверка пересечений', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Проверка пересекающихся заданий', callback_data='plugin'),
                    types.InlineKeyboardButton('Статусы заданий', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Обозреватель статусов', callback_data='plugin'),
                    types.InlineKeyboardButton('Проверка заданий', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Назад', callback_data='support'))

        if user_data[call.message.chat.id].revit_choice == 'plugin':
            await bot.send_message(user_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)
        else:
            await bot.send_message(user_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)

    elif call.data == 'general':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('Этажи и секции', callback_data='plugin'),
                    types.InlineKeyboardButton('Подсчет узлов', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Печать листов', callback_data='plugin'),
                    types.InlineKeyboardButton('Множественная печать', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Копировать спецификацию', callback_data='plugin'),
                    types.InlineKeyboardButton('Копировать параметры', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Параметры семейств', callback_data='plugin'),
                    types.InlineKeyboardButton('Копировать параметры арматуры', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Комбинатор дверей', callback_data='plugin'),
                    types.InlineKeyboardButton('Огнекороб', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Просмотр пересечения', callback_data='plugin'),
                    types.InlineKeyboardButton('Менеджер узлов', callback_data='plugin'))
        keyboard.row(types.InlineKeyboardButton('Проверка модели', callback_data='plugin'),
                    types.InlineKeyboardButton('Назад', callback_data='support'))

        if user_data[call.message.chat.id].revit_choice == 'plugin':
            await bot.send_message(user_id, "Выберите каким плагином вы пользовались:", reply_markup=keyboard)
        else:
            await bot.send_message(user_id, "Выберите на какой плагин вам нужна информация:", reply_markup=keyboard)

    elif call.data == 'plugin':
        if user_data[call.message.chat.id].revit_choice == 'plugin':
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(types.InlineKeyboardButton('Revit 2019', callback_data='revit'),
                        types.InlineKeyboardButton('Revit 2020', callback_data='revit'))
            keyboard.row(types.InlineKeyboardButton('Revit 2021', callback_data='revit'),
                        types.InlineKeyboardButton('Revit 2022', callback_data='revit'))
            keyboard.row(types.InlineKeyboardButton('Revit 2023', callback_data='revit'),
                        types.InlineKeyboardButton('Revit 2024', callback_data='revit'))
            keyboard.row(types.InlineKeyboardButton('Revit 2025', callback_data='revit'),
                        types.InlineKeyboardButton('Назад', callback_data='support'))
            await bot.send_message(call.message.chat.id, "Выберите версию Revit, в котором запускали плагин", reply_markup=keyboard)
        else:
            await bot.send_message(call.message.chat.id, "Ссылки на vk видео и pdf инструкции (файлы)")
            await start(call.message)
    elif call.data == 'file_sending':
        user_data[call.message.chat.id].state = 'file_sending'
        await bot.send_message(call.message.chat.id, "Отправьте, пожалуйста, файл на котором у вас возник вопрос")
    elif call.data == 'file_not_sending':
        await bot.send_message(call.message.chat.id, "Данный вопрос был передан отделу разработок, в ближайшее время с вами свяжется специалист")
        await start(call.message)
    else:
        await bot.answer_callback_query(call.id, text="Ошибка!")


async def main():
    bot_polling_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(bot_polling_task)

asyncio.run(main())