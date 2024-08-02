"""Задача "Цепочка вопросов":
Необходимо сделать цепочку обработки состояний для нахождения нормы калорий для человека.
Группа состояний:
Импортируйте классы State и StateGroup из aiogram.dispatcher.filters.state.
Создайте класс UserState наследованный от StateGroup.
Внутри этого класса опишите 3 объекта класса State: age, growth, weight (возраст, рост, вес).
Эта группа(класс) будет использоваться в цепочке вызовов message_handler'ов.
Напишите следующие функции для обработки состояний:
Функцию set_age(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Calories'.
Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
После ожидать ввода возраста в атрибут UserState.age при помощи метода set.
Функцию set_growth(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.age.
Эта функция должна обновлять данные в состоянии age на message.text (написанное пользователем сообщение).
Используйте метод update_data.
Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
После ожидать ввода роста в атрибут UserState.growth при помощи метода set.
Функцию set_weight(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
Эта функция должна обновлять данные в состоянии growth на message.text (написанное пользователем сообщение).
Используйте метод update_data.
Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
После ожидать ввода роста в атрибут UserState.weight при помощи метода set.
Функцию send_calories(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
Эта функция должна обновлять данные в состоянии weight на message.text (написанное пользователем сообщение).
Используйте метод update_data.
Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
Используйте упрощённую формулу Миффлина-Сан Жеора для подсчёта нормы калорий.
Данные для формулы берите из ранее объявленной переменной data по ключам age, growth и weight соответственно.
Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
Финишируйте машину состояний методом finish().
В течение написания этих функций помните,
что они асинхронны и все функции и методы должны запускаться с оператором await.

Задача "Меньше текста, больше кликов":
Необходимо дополнить код предыдущей задачи, чтобы вопросы о параметрах тела
для расчёта калорий выдавались по нажатию кнопки.
Измените massage_handler для функции set_age.
Теперь этот хэндлер будет реагировать на текст 'Рассчитать', а не на 'Calories'.
Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton на ней со следующим текстом:
'Рассчитать' и 'Информация'. Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса устройства
при помощи параметра resize_keyboard.
Используйте ранее созданную клавиатуру в ответе функции start, используя параметр reply_markup.
В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками.
При нажатии на кнопку с надписью 'Рассчитать' срабатывает функция set_age
с которой начинается работа машины состояний для age, growth и weight.

Цель: научится создавать Inline клавиатуры и кнопки на них в Telegram-bot.

Задача "Ещё больше выбора":
Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку 'Рассчитать' присылалась Inline-клавиатруа.
Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
С текстом 'Рассчитать норму калорий' и callback_data='calories'
С текстом 'Формулы расчёта' и callback_data='formulas'
Создайте новую функцию main_menu(message), которая:
Будет обёрнута в декоратор message_handler, срабатывающий при передаче текста 'Рассчитать'.
Сама функция будет присылать ранее созданное Inline меню и текст 'Выберите опцию:'
Создайте новую функцию get_formulas(call), которая:
Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
Будет присылать сообщение с формулой Миффлина-Сан Жеора.
Измените функцию set_age и декоратор для неё:
Декоратор смените на callback_query_handler, который будет реагировать на текст 'calories'.
Теперь функция принимает не message, а call. Доступ к сообщению будет следующим - call.message.
По итогу получится следующий алгоритм:
Вводится команда /start
На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
В ответ на кнопку 'Рассчитать' присылается Inline меню: 'Рассчитать норму калорий' и 'Формулы расчёта'
По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
По Inline кнопке 'Рассчитать норму калорий' начинает работать машина состояний по цепочке.
"""

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = '72*****************************************'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(button1, button2)
inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button1= InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2= InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_button1, inline_button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Информация')
async def set_info(message):
    await message.answer('Бот подсчёта суточной нормы калорий по упрощённой формуле Миффлина-Сан Жеора')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Упрощенная формула Миффлина-Сан Жеора для подсчёта суточной нормы калорий для мужчин: '
                              '10 х вес (кг) + 6.25 * рост (см) - 5 х возраст (лет) + 5' '\n' '\n'
                              'Упрощенная формула Миффлина-Сан Жеора для подсчёта суточной нормы калорий для женщин: '
                              '10 х вес (кг) + 6.25 * рост (см) - 5 х возраст (лет) - 161')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_sex(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол: F - для женщин или M - для мужчин ')
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def set_calories(message, state):
    await state.update_data(sex=message.text)
    data = await state.get_data()
    if message.text == "M" or message.text == "m":
        # (weight * 10) + (6.25 * growth) - (5 * age) + 5 формулу Миффлина-Сан Жеора для подсчёта нормы калорий для
        # мужчин
        result = (float(data['weight']) * 10) + (float(data['growth']) * 6.25) - (float(data['age']) * 5) + 5
    elif message.text == "F" or message.text == "f":
        # (weight * 10) + (6.25 * growth) - (5 * age) + 5 формулу Миффлина-Сан Жеора для подсчёта нормы калорий для
        # женщин
        result = (float(data['weight']) * 10) + (float(data['growth']) * 6.25) - (float(data['age']) * 5) - 161
    await message.answer(f'Ваша норма калорий {result}')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
