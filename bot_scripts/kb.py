from aiogram import types

start_keyboard = types.InlineKeyboardMarkup()
start_keyboard.add(types.InlineKeyboardButton('Помощь', callback_data='help'))
start_keyboard.add(types.InlineKeyboardButton('Подробная информация о плагинах', callback_data='support'))
start_keyboard.add(types.InlineKeyboardButton('Задать вопрос ИИ-консультанту', callback_data='questions'))
#start_keyboard.add(types.InlineKeyboardButton('Оформить лицензию', callback_data='license'))

question_keyboard = types.InlineKeyboardMarkup()
question_keyboard.add(types.InlineKeyboardButton('Задать вопрос ещё раз', callback_data='questions'))
question_keyboard.add(types.InlineKeyboardButton('Назад', callback_data='start'))

file_send_keyboard = types.InlineKeyboardMarkup()
file_send_keyboard.add(types.InlineKeyboardButton('Отправить файл', callback_data='file_sending'))
file_send_keyboard.add(types.InlineKeyboardButton('Не отправлять файл', callback_data='file_not_sending'))

help_keyboard = types.InlineKeyboardMarkup()
help_keyboard.add(types.InlineKeyboardButton('Хочу задать вопрос касаемо работы плагина', callback_data='plugin_work_help'))
help_keyboard.add(types.InlineKeyboardButton('Хочу сообщить об ошибке', callback_data='issue_help'))
help_keyboard.add(types.InlineKeyboardButton('Нужна помощь при установке/активации', callback_data='install_help'))
help_keyboard.add(types.InlineKeyboardButton('Назад', callback_data='start'))

renga_help_keyboard = types.InlineKeyboardMarkup()
renga_help_keyboard.add(types.InlineKeyboardButton('Хочу задать вопрос касаемо работы плагина', callback_data='renga_work_help'))
renga_help_keyboard.add(types.InlineKeyboardButton('Хочу сообщить об ошибке', callback_data='renga_issue_help'))
renga_help_keyboard.add(types.InlineKeyboardButton('Назад', callback_data='start'))

back_to_start_keyboard = types.InlineKeyboardMarkup()
back_to_start_keyboard.add(types.InlineKeyboardButton('Назад', callback_data='start'))

install_help_keyboard = types.InlineKeyboardMarkup()
install_help_keyboard.add(types.InlineKeyboardButton('Ошибка при установке сборки', callback_data='install_error'))
install_help_keyboard.add(types.InlineKeyboardButton('Не получается зарегистрироваться', callback_data='registration_error'))
install_help_keyboard.add(types.InlineKeyboardButton('Не получается ввести ключ активации', callback_data='activation_error'))
install_help_keyboard.add(types.InlineKeyboardButton('Назад', callback_data='help'))

revit_keyboard = types.InlineKeyboardMarkup()
revit_keyboard.row(types.InlineKeyboardButton('Revit 2019', callback_data='revit_2019'),
                   types.InlineKeyboardButton('Revit 2020', callback_data='revit_2020'))
revit_keyboard.row(types.InlineKeyboardButton('Revit 2021', callback_data='revit_2021'),
                   types.InlineKeyboardButton('Revit 2022', callback_data='revit_2022'))
revit_keyboard.row(types.InlineKeyboardButton('Revit 2023', callback_data='revit_2023'),
                   types.InlineKeyboardButton('Revit 2024', callback_data='revit_2024'))
revit_keyboard.row(types.InlineKeyboardButton('Revit 2025', callback_data='revit_2025'),
                   types.InlineKeyboardButton('Назад', callback_data='start'))

plugin_categories_keyboard = types.InlineKeyboardMarkup()
plugin_categories_keyboard.row(types.InlineKeyboardButton('Концепция', callback_data='conception'),
                               types.InlineKeyboardButton('Архитектура', callback_data='architecture'))
plugin_categories_keyboard.row(types.InlineKeyboardButton('Конструктив', callback_data='constructive'),
                               types.InlineKeyboardButton('ОВ и ВК', callback_data='ov_vk'))
plugin_categories_keyboard.row(types.InlineKeyboardButton('Боксы и отверстия', callback_data='boxes'),
                               types.InlineKeyboardButton('Общие', callback_data='general'))
plugin_categories_keyboard.row(types.InlineKeyboardButton('Renga', callback_data='renga'),
                               types.InlineKeyboardButton('Назад', callback_data='start'))

conception_keyboard = types.InlineKeyboardMarkup()
conception_keyboard.row(types.InlineKeyboardButton('Инсоляция', callback_data='plugin_Инсоляция'),
                        types.InlineKeyboardButton('КЕО', callback_data='plugin_КЕО'))
conception_keyboard.row(types.InlineKeyboardButton('Генерация парков', callback_data='plugin_Генерация парков'),
                        types.InlineKeyboardButton('Генерация деревьев', callback_data='plugin_Генерация деревьев'))
conception_keyboard.row(types.InlineKeyboardButton('Разлиновка модели', callback_data='plugin_Разлиновка модели'),
                        types.InlineKeyboardButton('3D сетки', callback_data='plugin_3D сетки'))
conception_keyboard.row(types.InlineKeyboardButton('БыстроТЭПы', callback_data='plugin_БыстроТЭПы'),
                        types.InlineKeyboardButton('Подсчет площадей', callback_data='plugin_Подсчет площадейКонц'))
conception_keyboard.row(types.InlineKeyboardButton('Назад', callback_data='start'))

architecture_keyboard = types.InlineKeyboardMarkup()
architecture_keyboard.row(types.InlineKeyboardButton('Определить помещение', callback_data='plugin_Определить помещение'),
                          types.InlineKeyboardButton('Расчет плинтуса', callback_data='plugin_Расчет плинтуса'))
architecture_keyboard.row(types.InlineKeyboardButton('Отделка', callback_data='plugin_Отделка'),
                          types.InlineKeyboardButton('Копировать отделку', callback_data='plugin_Копировать отделку'))
architecture_keyboard.row(types.InlineKeyboardButton('Проемы по дверям/окнам из связи', callback_data='plugin_Проемы по дверям/окнам из связи'),
                          types.InlineKeyboardButton('Соединение полов', callback_data='plugin_Соединение полов'))
architecture_keyboard.row(types.InlineKeyboardButton('Подсчет площадей', callback_data='plugin_Подсчет площадейАрх'),
                          types.InlineKeyboardButton('Планировка', callback_data='plugin_Планировка'))
architecture_keyboard.row(types.InlineKeyboardButton('Округление площади', callback_data='plugin_Округление площади'),
                          types.InlineKeyboardButton('Нумерация квартир', callback_data='plugin_Нумерация квартир'))
architecture_keyboard.row(types.InlineKeyboardButton('Назад', callback_data='start'))

constructive_keyboard = types.InlineKeyboardMarkup()
constructive_keyboard.row(types.InlineKeyboardButton('Сборка арматуры', callback_data='plugin_Сборка арматуры'),
                          types.InlineKeyboardButton('Создать разрезы и сечения', callback_data='plugin_Создать разрезы и сечения'))
constructive_keyboard.row(types.InlineKeyboardButton('Создание планов', callback_data='plugin_Создание планов'),
                          types.InlineKeyboardButton('Создание контура', callback_data='plugin_Создание контура'))
constructive_keyboard.row(types.InlineKeyboardButton('Редактирование контура', callback_data='plugin_Редактирование контура'),
                          types.InlineKeyboardButton('Расчет продавливания', callback_data='plugin_Расчет продавливания'))
constructive_keyboard.row(types.InlineKeyboardButton('Создание каркасов', callback_data='plugin_Создание каркасов'),
                          types.InlineKeyboardButton('Создание видов каркасов', callback_data='plugin_Создание видов каркасов'))
constructive_keyboard.row(types.InlineKeyboardButton('Назад', callback_data='start'))

ov_vk_keyboard = types.InlineKeyboardMarkup()
ov_vk_keyboard.row(types.InlineKeyboardButton('Муфты/гильзы', callback_data='plugin_Муфты/гильзы'),
                   types.InlineKeyboardButton('Аэродинамика', callback_data='plugin_Аэродинамика'))
ov_vk_keyboard.row(types.InlineKeyboardButton('Создать виды систем', callback_data='plugin_Создать виды систем'),
                   types.InlineKeyboardButton('Спецификации систем', callback_data='plugin_Спецификации систем'))
ov_vk_keyboard.row(types.InlineKeyboardButton('Высотные отметки', callback_data='plugin_Высотные отметки'),
                   types.InlineKeyboardButton('Толщина стенки', callback_data='plugin_Толщина стенки'))
ov_vk_keyboard.row(types.InlineKeyboardButton('Диаметр изоляции', callback_data='plugin_Диаметр изоляции'),
                   types.InlineKeyboardButton('S изоляции', callback_data='plugin_S изоляции'))
ov_vk_keyboard.row(types.InlineKeyboardButton('Назад', callback_data='start'))

boxes_keyboard = types.InlineKeyboardMarkup()
boxes_keyboard.row(types.InlineKeyboardButton('Создание заданий', callback_data='plugin_Создание заданий'),
                   types.InlineKeyboardButton('Объединение', callback_data='plugin_Объединение'))
boxes_keyboard.row(types.InlineKeyboardButton('Смещение', callback_data='plugin_Смещение'),
                   types.InlineKeyboardButton('Обрезать', callback_data='plugin_Обрезать'))
boxes_keyboard.row(types.InlineKeyboardButton('Нумерация', callback_data='plugin_Нумерация'),
                   types.InlineKeyboardButton('Отметка', callback_data='plugin_Отметка'))
boxes_keyboard.row(types.InlineKeyboardButton('Отверстия', callback_data='plugin_Отверстия'),
                   types.InlineKeyboardButton('Проверка пересечений', callback_data='plugin_Проверка пересечений'))
boxes_keyboard.row(types.InlineKeyboardButton('Проверка пересекающихся заданий', callback_data='plugin_Проверка перес/заданий'),
                   types.InlineKeyboardButton('Статусы заданий', callback_data='plugin_Статусы заданий'))
boxes_keyboard.row(types.InlineKeyboardButton('Обозреватель статусов', callback_data='plugin_Обозреватель статусов'),
                   types.InlineKeyboardButton('Проверка заданий', callback_data='plugin_Проверка заданий'))
boxes_keyboard.row(types.InlineKeyboardButton('Назад', callback_data='start'))

general_plugins_keyboard = types.InlineKeyboardMarkup()
general_plugins_keyboard.row(types.InlineKeyboardButton('Этажи и секции', callback_data='plugin_Этажи и секции'),
                             types.InlineKeyboardButton('Подсчет узлов', callback_data='plugin_Подсчет узлов'))
general_plugins_keyboard.row(types.InlineKeyboardButton('Печать листов', callback_data='plugin_Печать листов'),
                             types.InlineKeyboardButton('Множественная печать', callback_data='plugin_Множественная печать'))
general_plugins_keyboard.row(types.InlineKeyboardButton('Копировать спецификацию', callback_data='plugin_Копировать спецификацию'),
                             types.InlineKeyboardButton('Копировать параметры', callback_data='plugin_Копировать параметры'))
general_plugins_keyboard.row(types.InlineKeyboardButton('Параметры семейств', callback_data='plugin_Параметры семейств'),
                             types.InlineKeyboardButton('Копировать параметры арматуры', callback_data='plugin_Копировать параметры арматуры'))
general_plugins_keyboard.row(types.InlineKeyboardButton('Комбинатор дверей', callback_data='plugin_Комбинатор дверей'),
                             types.InlineKeyboardButton('Огнекороб', callback_data='plugin_Огнекороб'))
general_plugins_keyboard.row(types.InlineKeyboardButton('Просмотр пересечения', callback_data='plugin_Просмотр пересечения'),
                             types.InlineKeyboardButton('Менеджер узлов', callback_data='plugin_Менеджер узлов'))
general_plugins_keyboard.row(types.InlineKeyboardButton('Проверка модели', callback_data='plugin_Проверка модели'),
                             types.InlineKeyboardButton('Назад', callback_data='start'))

renga_keyboard = types.InlineKeyboardMarkup()
renga_keyboard.row(types.InlineKeyboardButton('Подсчет площадей', callback_data='renga_Подсчет площадейРенг'),
                   types.InlineKeyboardButton('Активация', callback_data='plugin_Подсчет площадей'))
renga_keyboard.row(types.InlineKeyboardButton('Назад', callback_data='start'))