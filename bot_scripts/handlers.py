from config import TOKEN, YOOTOKEN, sub_info, api_id, api_hash, GPT_SECRET_KEY
from user import User
from database import cursor, conn
from main import bot, dp, user_data
import utils
import kb
import asyncio
from aiogram import types

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    user_id = message.chat.id

    user = User(user_id)
    user_data[user_id] = user
    await utils.user_clear(message)
    keyboard = kb.start_keyboard
    await bot.send_message(user_id, "Привет! Добро пожаловать в бота.", reply_markup=keyboard)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'asking_question')
async def asking_question(message):
    await utils.answer_generation(message)

    keyboard = kb.question_keyboard
    await bot.send_message(message.chat.id, "Вам помог ответ?", reply_markup=keyboard)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'license_key_input')
async def license_key_input(message):
    user_data[message.chat.id].license_key = message.text

    if user_data[message.chat.id].plugin_category == 'renga':
        user_data[message.chat.id].state = 'renga_version_input'
        await bot.send_message(message.chat.id, "Напишите версию Renga, в которой вы работаете")
    else:
        user_data[message.chat.id].state = 'build_version_input'
        await bot.send_message(message.chat.id, "Напишите, пожалуйста, номер сборки, которую вы установили")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'build_version_input')
async def build_version_input(message):
    user_data[message.chat.id].build_version = message.text

    if user_data[message.chat.id].choise == 'full_issue':
        user_data[message.chat.id].state = 'plugin_question_input'
        await bot.send_message(message.chat.id, "Опишите ваш вопрос")

    elif user_data[message.chat.id].choise == 'issue':
        user_data[message.chat.id].state = 'screen_sending'
        user_data[message.chat.id].feedback_text = 'error_report'
        await bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот ошибки")

    elif user_data[message.chat.id].choise == 'install':
        user_data[message.chat.id].state = 'install_question_input'
        await bot.send_message(message.chat.id, "Опишите вашу проблему")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'renga_version_input')
async def renga_version_input(message):
    user_data[message.chat.id].renga_version = message.text
    user_data[message.chat.id].state = 'plugins_build'

    await bot.send_message(message.chat.id, "Напишите номер сборки плагинов, которую вы использовали")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'plugins_build')
async def plugins_build(message):
    user_data[message.chat.id].plugins_build = message.text
    keyboard = kb.renga_help_keyboard
    await bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=keyboard)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'plugin_question_input')
async def plugin_question_input(message):
    user_data[message.chat.id].feedback_text = message.text

    keyboard = kb.file_send_keyboard
    await bot.send_message(message.chat.id, "Отправьте, пожалуйста, файл на котором у вас возник вопрос", reply_markup=keyboard)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'install_question_input')
async def install_question_input(message):
    user_data[message.chat.id].feedback_text = message.text
    user_data[message.chat.id].state = 'screen_sending'

    await bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот проблемы")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'renga_question_input')
async def renga_question_input(message):
    user_data[message.chat.id].feedback_text = message.text
    user_data[message.chat.id].state = 'screen_sending'

    await bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот")

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'file_sending', content_types=['document'])
async def file_sending(message):
    await utils.file_saving(message)

@dp.message_handler(lambda message: user_data[message.chat.id].state == 'screen_sending', content_types=['photo'])
async def screen_sending(message):
    await utils.screen_saving(message)

@dp.message_handler(lambda message: True)
async def handle_text(message):
    user_id = message.chat.id
    if message.text == '/help':
        await utils.show_help_options(user_id)
    elif message.text == '/support':
        await utils.show_support_options(user_id)
    elif message.text == '/questions':
        await utils.show_questions_options(user_id)
    elif message.text == '/license':
        await utils.show_license_options(user_id)

@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
    user_id = call.message.chat.id

    if call.data == 'start':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))
        await start(call.message)

    elif call.data == 'help':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))
        await utils.show_help_options(call.message.chat.id)

    elif call.data == 'support':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choise = 'support'

        await utils.show_support_options(call.message.chat.id)

    elif call.data == 'questions':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))
        await utils.show_questions_options(call.message.chat.id)

    elif call.data == 'license':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choise = 'license'

        await utils.show_license_options(call.message.chat.id)

    elif call.data == 'plugin_work_help':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choise = 'full_issue'

        await utils.show_support_options(call.message.chat.id)

    elif call.data == 'issue_help':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choise = 'issue'

        await utils.show_support_options(call.message.chat.id)

    elif call.data == 'install_help':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choise = 'install'

        keyboard = kb.install_help_keyboard
        await bot.send_message(call.message.chat.id, "Выберите категорию, по которой вам нужна помощь.", reply_markup=keyboard)

    elif call.data in ["install_error", "registration_error", "activation_error"]:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.revit_keyboard
        await bot.send_message(call.message.chat.id, "Выберите версию Revit, в котором запускали плагин", reply_markup=keyboard)
    elif call.data in ["renga_work_help", "renga_issue_help"]:
        user_data[call.message.chat.id].choise = 'renga_issue'
        user_data[call.message.chat.id].state = 'renga_question_input'
        await bot.send_message(call.message.chat.id, "Опишите проблему")
    elif call.data.startswith("revit_"):
        if user_data[call.message.chat.id].plugin_category != 'renga':
            await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].state = 'license_key_input'
        user_data[call.message.chat.id].revit_version = call.data[6:]

        await bot.send_message(call.message.chat.id, "Введите, пожалуйста, ваш лицензионный ключ, который вы использовали")

    elif call.data == 'conception':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.conception_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == 'architecture':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.architecture_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == 'constructive':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.constructive_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == 'ov_vk':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.ov_vk_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == 'boxes':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.boxes_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == 'general':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.general_plugins_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == 'renga':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].plugin_category = 'renga'

        keyboard = kb.renga_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data.startswith('plugin_'):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        plugin_name = call.data[7:]
        if plugin_name == 'Проверка перес/заданий':
            plugin_name = 'Проверка пересекающихся заданий'

        cursor.execute("SELECT plugin_id FROM Plugins WHERE name = ?", (plugin_name,))
        user_data[call.message.chat.id].plugin_id = cursor.fetchone()[0]

        if user_data[call.message.chat.id].choise[-5:] == 'issue':
            keyboard = kb.revit_keyboard
            await bot.send_message(call.message.chat.id, "Выберите версию Revit, в котором запускали плагин", reply_markup=keyboard)

        elif user_data[call.message.chat.id].choise == 'license':

            prices = [types.LabeledPrice(label='Руб', amount = 500000)]
            await bot.send_invoice(call.message.chat.id, title='Плагин' + plugin_name,
                                   description='payment',
                                   provider_token=YOOTOKEN, currency='RUB',
                                   start_parameter='test_bot', prices=prices, payload='test-invoice-payload')

        else:
            links = await utils.get_links(plugin_name)

            await bot.send_message(call.message.chat.id, "Ссылки на vk видео и pdf инструкции (файлы):\n" + links)
            await start(call.message)

    elif call.data.startswith('renga_'):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        plugin_name = call.data[6:]
        cursor.execute("SELECT plugin_id FROM Plugins WHERE name = ?", (plugin_name,))
        user_data[call.message.chat.id].plugin_id = cursor.fetchone()[0]

        if user_data[call.message.chat.id].choise == 'support':
            links = await utils.get_links(call.data[6:])

            await bot.send_message(call.message.chat.id, "Ссылки на vk видео и pdf инструкции (файлы):\n" + links)
            await start(call.message)

        elif user_data[call.message.chat.id].choise == 'license':

            prices = [types.LabeledPrice(label='Руб', amount = 500000)]
            await bot.send_invoice(call.message.chat.id, title='Плагин' + plugin_name,
                                   description='payment',
                                   provider_token=YOOTOKEN, currency='RUB',
                                   start_parameter='test_bot', prices=prices, payload='test-invoice-payload')

        else:
            call.data ='revit_'
            await callback_inline(call)


    elif call.data == 'file_sending':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].state = 'file_sending'

        await bot.send_message(call.message.chat.id, "Прикрепите файл сюда")

    elif call.data == 'file_not_sending':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        await utils.save_feedback(call.message)

        await bot.send_message(call.message.chat.id, "Данный вопрос был передан отделу разработок, в ближайшее время с вами свяжется специалист")
        await start(call.message)

    else:
        await bot.answer_callback_query(call.id, text="Ошибка!")

@dp.shipping_query_handler(lambda query: True)
async def shipping(shipping_query):
    await bot.answer_shipping_query(shipping_query.id, ok=True,
                                    error_message='Произошла ошибка.')

@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Произошла ошибка.")

@dp.message_handler(content_types=['successful_payment'])
async def got_payment(message):
    await bot.send_message(message.chat.id, "Ключ вашей лицензии: 189571ghji\nИнструкция по активации ключа: https://google.com\n Обращайтесь по любым вопросам")
    await start(message)

async def main():
    bot_polling_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(bot_polling_task)

asyncio.run(main())