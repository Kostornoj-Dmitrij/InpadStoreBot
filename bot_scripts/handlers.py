from config import TOKEN, YOOTOKEN, sub_info, api_id, api_hash, GPT_SECRET_KEY, BITRIX_WEBHOOK_URL
from user import User
from database import cursor, conn
from main import bot, dp, user_data
import utils
import kb
import asyncio
from aiogram import types
import requests
from airtable_utils import create_record, create_trace_data, save_trace
from datetime import datetime
import pytz

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.chat.id

    user = User(user_id)
    user_data[user_id] = user
    await utils.user_clear(message)


    cursor.execute("SELECT COUNT(*) FROM Users WHERE t_user_chat_id = ?", (user_id,))

    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Users (username, t_user_chat_id, created_at) "
                       "VALUES (?, ?, DATETIME('now'))",
                       (message.from_user.username, user_id))
        conn.commit()
        data = {
            "records": [
                {
                    "fields": {
                        "username": message.from_user.username,
                        "t_user_chat_id": user_id,
                        "created_at": datetime.now(pytz.timezone("Europe/Moscow")).isoformat()
                    }
                }
            ]
        }
        await create_record("Users", data)

    await save_trace(user_id, "command", "/start")

    keyboard = kb.start_keyboard
    await bot.send_message(user_id, "Привет! Добро пожаловать в бота.", reply_markup=keyboard)


@dp.message_handler(lambda message: user_data[message.chat.id].state == "asking_question")
async def asking_question(message):
    await save_trace(message.chat.id, "question_input", message.text)
    await utils.send_data_to_bitrix(message, user_data[message.chat.id].build_version)
    await utils.answer_generation(message)

    keyboard = kb.question_keyboard
    await bot.send_message(message.chat.id, "Вам помог ответ?", reply_markup=keyboard)


@dp.message_handler(lambda message: user_data[message.chat.id].state == "license_key_input")
async def license_key_input(message):
    await save_trace(message.chat.id, "license_key_input", message.text)
    user_data[message.chat.id].license_key = message.text

    if user_data[message.chat.id].plugin_category == "renga":
        user_data[message.chat.id].state = "renga_version_input"
        await bot.send_message(message.chat.id, "Напишите версию Renga, в которой вы работаете")
    else:
        user_data[message.chat.id].state = "build_version_input"
        await bot.send_message(message.chat.id, "Напишите, пожалуйста, номер сборки, которую вы установили")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "build_version_input")
async def build_version_input(message):
    await save_trace(message.chat.id, "build_version_input", message.text)
    user_data[message.chat.id].build_version = message.text

    if user_data[message.chat.id].choice == "full_issue":
        user_data[message.chat.id].state = "plugin_question_input"
        await bot.send_message(message.chat.id, "Опишите ваш вопрос")

    elif user_data[message.chat.id].choice == "issue":
        user_data[message.chat.id].state = "screen_sending"
        user_data[message.chat.id].feedback_text = "error_report"
        await bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот ошибки")

    elif user_data[message.chat.id].choice == "install":
        user_data[message.chat.id].state = "install_question_input"
        await bot.send_message(message.chat.id, "Опишите вашу проблему")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "renga_version_input")
async def renga_version_input(message):
    await save_trace(message.chat.id, "renga_version_input", message.text)
    user_data[message.chat.id].renga_version = message.text
    user_data[message.chat.id].state = "plugins_build"

    await bot.send_message(message.chat.id, "Напишите номер сборки плагинов, которую вы использовали")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "plugins_build")
async def plugins_build(message):
    await save_trace(message.chat.id, "plugins_build_input", message.text)
    user_data[message.chat.id].plugins_build = message.text
    keyboard = kb.renga_help_keyboard
    await bot.send_message(message.chat.id, "Выберите один из вариантов", reply_markup=keyboard)


@dp.message_handler(lambda message: user_data[message.chat.id].state == "plugin_question_input")
async def plugin_question_input(message):
    await save_trace(message.chat.id, "plugin_question_input", message.text)
    user_data[message.chat.id].feedback_text = message.text

    keyboard = kb.file_send_keyboard
    await bot.send_message(message.chat.id, "Отправьте, пожалуйста, файл на котором у вас возник вопрос",
                           reply_markup=keyboard)


@dp.message_handler(lambda message: user_data[message.chat.id].state == "install_question_input")
async def install_question_input(message):
    await save_trace(message.chat.id, "install_question_input", message.text)
    user_data[message.chat.id].feedback_text = message.text
    user_data[message.chat.id].state = "screen_sending"

    await bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот проблемы")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "renga_question_input")
async def renga_question_input(message):
    await save_trace(message.chat.id, "renga_version_input", message.text)
    user_data[message.chat.id].feedback_text = message.text
    user_data[message.chat.id].state = "screen_sending"

    await bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "fio_input")
async def fio_input(message):
    await save_trace(message.chat.id, "fio_input", message.text)
    user_data[message.chat.id].fio = message.text

    keyboard = kb.fiz_or_ur_face
    await bot.send_message(message.chat.id, "Вы Юр.Лицо или Физ.Лицо?",
                           reply_markup=keyboard)


@dp.message_handler(lambda message: user_data[message.chat.id].state == "company_input")
async def company_input(message):
    await save_trace(message.chat.id, "company_input", message.text)
    user_data[message.chat.id].company_name = message.text
    user_data[message.chat.id].state = "city_input"
    await bot.send_message(message.chat.id, "Укажите город, в котором вы находитесь")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "city_input")
async def city_input(message):
    await save_trace(message.chat.id, "city_input", message.text)
    user_data[message.chat.id].city = message.text
    user_data[message.chat.id].state = "email_input"
    await bot.send_message(message.chat.id, "Укажите вашу почту")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "email_input")
async def email_input(message):
    await save_trace(message.chat.id, "email_input", message.text)
    user_data[message.chat.id].email = message.text
    user_data[message.chat.id].state = "phone_number_input"
    await bot.send_message(message.chat.id, "Укажите ваш номер телефона")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "phone_number_input")
async def phone_number_input(message):
    await save_trace(message.chat.id, "phone_number_input", message.text)
    user_data[message.chat.id].phone_number = message.text
    await bot.send_message(message.chat.id, "---Данная информация поможет нам с вами связаться---")
    if user_data[message.chat.id].choice == "buy_plugin":
        user_data[message.chat.id].state = "plugins_for_buy_input"
        await bot.send_message(message.chat.id, "Напишите плагины, которые вы хотите приобрести")
    elif user_data[message.chat.id].choice == "test_plugin":
        user_data[message.chat.id].state = "plugins_for_test_input"
        await bot.send_message(message.chat.id, "Напишите плагины, которые вы хотите протестировать")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "plugins_for_buy_input")
async def plugins_for_buy_input(message):
    await save_trace(message.chat.id, "plugins_for_buy_input", message.text)
    user_data[message.chat.id].plugins_for_buy = message.text
    keyboard = kb.plugin_demonstration
    await bot.send_message(message.chat.id, "Нужна ли вам демонстрация плагина?",
                           reply_markup=keyboard)


@dp.message_handler(lambda message: user_data[message.chat.id].state == "plugins_for_test_input")
async def plugins_for_test_input(message):
    await save_trace(message.chat.id, "plugins_for_test_input", message.text)
    user_data[message.chat.id].plugins_for_buy = message.text
    user_data[message.chat.id].state = "license_count_input"
    await bot.send_message(message.chat.id, "Укажите количество лицензий, которые вы хотите получить")


@dp.message_handler(lambda message: user_data[message.chat.id].state == "license_count_input")
async def license_count_input(message):
    await save_trace(message.chat.id, "license_count_input", message.text)
    user_data[message.chat.id].license_count = message.text
    await utils.save_license_feedback(message)
    await bot.send_message(message.chat.id, "Ваша информация была передана менеджеру")
    await start(message)

@dp.message_handler(lambda message: user_data[message.chat.id].state == "file_sending", content_types=["document"])
async def file_sending(message):
    await save_trace(message.chat.id, "file_sending", "document")
    await utils.file_saving(message)


@dp.message_handler(lambda message: user_data[message.chat.id].state == "screen_sending", content_types=["photo"])
async def screen_sending(message):
    await save_trace(message.chat.id, "file_sending", "photo")
    await utils.screen_saving(message)


@dp.message_handler(lambda message: True)
async def handle_text(message):
    user_id = message.chat.id
    if message.text == "/help":
        await save_trace(message.chat.id, "command", "/help")
        await utils.show_help_options(user_id)
    elif message.text == "/support":
        await save_trace(message.chat.id, "command", "/support")
        await utils.show_support_options(user_id)
    elif message.text == "/questions":
        await save_trace(message.chat.id, "command", "/questions")
        await utils.show_questions_options(user_id)
    elif message.text == "/license":
        await save_trace(message.chat.id, "command", "/license")
        await utils.show_license_options(user_id)


@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
    user_id = call.message.chat.id

    if call.data == "start":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))
        await start(call.message)

    elif call.data == "help":
        await save_trace(call.message.chat.id, "command", "/help")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))
        await utils.show_help_options(call.message.chat.id)

    elif call.data == "support":
        await save_trace(call.message.chat.id, "command", "/support")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choice = "support"

        await utils.show_support_options(call.message.chat.id)

    elif call.data == "questions":
        await save_trace(call.message.chat.id, "command", "/questions")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))
        await utils.show_questions_options(call.message.chat.id)

    elif call.data == "license":
        await save_trace(call.message.chat.id, "command", "/license")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choice = "license"

        await utils.show_license_options(call.message.chat.id)

    elif call.data == "plugin_work_help":
        await save_trace(call.message.chat.id, "choice_help_option", "plugin_work_help")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choice = "full_issue"

        await utils.show_support_options(call.message.chat.id)

    elif call.data == "issue_help":
        await save_trace(call.message.chat.id, "choice_help_option", "issue_help")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choice = "issue"

        await utils.show_support_options(call.message.chat.id)

    elif call.data == "install_help":
        await save_trace(call.message.chat.id, "choice_help_option", "install_help")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].choice = "install"

        keyboard = kb.install_help_keyboard
        await bot.send_message(call.message.chat.id, "Выберите категорию, по которой вам нужна помощь.",
                               reply_markup=keyboard)

    elif call.data in ["install_error", "registration_error", "activation_error"]:
        await save_trace(call.message.chat.id, "choice_help_option", call.data)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.revit_keyboard
        await bot.send_message(call.message.chat.id, "Выберите версию Revit, в котором запускали плагин",
                               reply_markup=keyboard)
    elif call.data in ["renga_work_help", "renga_issue_help"]:
        await save_trace(call.message.chat.id, "choice_help_option", call.data)
        user_data[call.message.chat.id].choice = "renga_issue"
        user_data[call.message.chat.id].state = "renga_question_input"
        await bot.send_message(call.message.chat.id, "Опишите проблему")
    elif call.data.startswith("revit_"):
        if user_data[call.message.chat.id].plugin_category != "renga":
            await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].state = "license_key_input"
        user_data[call.message.chat.id].revit_version = call.data[6:]
        await save_trace(call.message.chat.id, "revit_choice", call.data[6:])

        await bot.send_message(call.message.chat.id,
                               "Введите, пожалуйста, ваш лицензионный ключ, который вы использовали")

    elif call.data == "conception":
        await save_trace(call.message.chat.id, "choice_plugin_category", "conception")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.conception_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == "architecture":
        await save_trace(call.message.chat.id, "choice_plugin_category", "architecture")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.architecture_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == "constructive":
        await save_trace(call.message.chat.id, "choice_plugin_category", "constructive")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.constructive_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == "ov_vk":
        await save_trace(call.message.chat.id, "choice_plugin_category", "ov_vk")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.ov_vk_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == "boxes":
        await save_trace(call.message.chat.id, "choice_plugin_category", "boxes")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.boxes_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == "general":
        await save_trace(call.message.chat.id, "choice_plugin_category", "general")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        keyboard = kb.general_plugins_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data == "renga":
        await save_trace(call.message.chat.id, "choice_plugin_category", "renga")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].plugin_category = "renga"

        keyboard = kb.renga_keyboard
        await utils.plugin_choice(call.message.chat.id, keyboard)

    elif call.data.startswith("plugin_"):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        plugin_name = call.data[7:]
        if plugin_name == "Проверка перес/заданий":
            plugin_name = "Проверка пересекающихся заданий"

        await save_trace(call.message.chat.id, "choice_plugin", plugin_name)

        cursor.execute("SELECT plugin_id FROM Plugins WHERE name = ?", (plugin_name,))
        user_data[call.message.chat.id].plugin_id = str(cursor.fetchone()[0])

        if user_data[call.message.chat.id].choice[-5:] == "issue":
            keyboard = kb.revit_keyboard
            await bot.send_message(call.message.chat.id, "Выберите версию Revit, в котором запускали плагин",
                                   reply_markup=keyboard)

        elif user_data[call.message.chat.id].choice == "license":

            prices = [types.LabeledPrice(label="Руб", amount=500000)]
            await bot.send_invoice(call.message.chat.id, title="Плагин" + plugin_name,
                                   description="payment",
                                   provider_token=YOOTOKEN, currency="RUB",
                                   start_parameter="test_bot", prices=prices, payload="test-invoice-payload")

        else:
            links = await utils.get_links(plugin_name)

            await bot.send_message(call.message.chat.id, "Ссылки на vk видео и pdf инструкции (файлы):\n" + links)
            await start(call.message)

    elif call.data.startswith("renga_"):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        plugin_name = call.data[6:]

        await save_trace(call.message.chat.id, "choice_plugin", plugin_name)

        cursor.execute("SELECT plugin_id FROM Plugins WHERE name = ?", (plugin_name,))
        user_data[call.message.chat.id].plugin_id = str(cursor.fetchone()[0])

        if user_data[call.message.chat.id].choice == "support":
            links = await utils.get_links(call.data[6:])

            await bot.send_message(call.message.chat.id, "Ссылки на vk видео и pdf инструкции (файлы):\n" + links)
            await start(call.message)

        elif user_data[call.message.chat.id].choice == "license":

            prices = [types.LabeledPrice(label="Руб", amount=500000)]
            await bot.send_invoice(call.message.chat.id, title="Плагин" + plugin_name,
                                   description="payment",
                                   provider_token=YOOTOKEN, currency="RUB",
                                   start_parameter="test_bot", prices=prices, payload="test-invoice-payload")

        else:
            call.data = "revit_"
            await callback_inline(call)


    elif call.data == "file_sending":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].state = "file_sending"

        await bot.send_message(call.message.chat.id, "Прикрепите файл сюда")

    elif call.data == "file_not_sending":
        await save_trace(call.message.chat.id, "file_command", "file_not_sending")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        await utils.save_feedback(call.message)

        await bot.send_message(call.message.chat.id,
                               "Данный вопрос был передан отделу разработок, в ближайшее время с вами свяжется специалист")
        await start(call.message)

    elif call.data == "buy_plugin":
        await save_trace(call.message.chat.id, "license_option", "plugin_buy")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].state = "fio_input"
        user_data[call.message.chat.id].choice = "buy_plugin"

        await bot.send_message(call.message.chat.id, "Укажите, пожалуйста, информацию о себе:")
        await bot.send_message(call.message.chat.id, "Укажите ваше ФИО")

    elif call.data == "test_plugin":
        await save_trace(call.message.chat.id, "license_option", "plugin_test")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].state = "fio_input"
        user_data[call.message.chat.id].choice = "test_plugin"

        await bot.send_message(call.message.chat.id, "Укажите, пожалуйста, информацию о себе:")
        await bot.send_message(call.message.chat.id, "Укажите ваше ФИО")

    elif call.data == "fiz_face":
        await save_trace(call.message.chat.id, "face_choice", "fiz_face")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].face = "fiz_face"
        user_data[call.message.chat.id].state = "company_input"

        await bot.send_message(call.message.chat.id, "Укажите название вашей компании")

    elif call.data == "ur_face":
        await save_trace(call.message.chat.id, "face_choice", "ur_face")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id))

        user_data[call.message.chat.id].face = "ur_face"
        user_data[call.message.chat.id].state = "company_input"

        await bot.send_message(call.message.chat.id, "Укажите название вашей компании")

    elif call.data == "demonstration_plugin":
        await save_trace(call.message.chat.id, "demonstration_should_input", "yes")
        user_data[call.message.chat.id].demonstration_should = "Да"
        user_data[call.message.chat.id].state = "license_count_input"
        await bot.send_message(call.message.chat.id, "Укажите количество лицензий, которые вы хотите приобрести")
    elif call.data == "no_demonstration_plugin":
        await save_trace(call.message.chat.id, "demonstration_should_input", "no")
        user_data[call.message.chat.id].demonstration_should = "Нет"
        user_data[call.message.chat.id].state = "license_count_input"
        await bot.send_message(call.message.chat.id, "Укажите количество лицензий, которые вы хотите приобрести")
    else:
        await bot.answer_callback_query(call.id, text="Ошибка!")


@dp.shipping_query_handler(lambda query: True)
async def shipping(shipping_query):
    await bot.answer_shipping_query(shipping_query.id, ok=True,
                                    error_message="Произошла ошибка.")


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Произошла ошибка.")


@dp.message_handler(content_types=["successful_payment"])
async def got_payment(message):
    await bot.send_message(message.chat.id,
                           "Ключ вашей лицензии: 189571ghji\nИнструкция по активации ключа: https://google.com\n Обращайтесь по любым вопросам")
    await start(message)


async def main():
    bot_polling_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(bot_polling_task)


asyncio.run(main())