import logging
from aiogram import Bot, types, executor, Dispatcher
from aiogram.dispatcher.filters import Command
from calc_complex import calc_complex_main
from calc_fraction import calc_fraction_main
from calc_log_reader import log_reader
from config import TOKEN_API
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from lexicon.lexicon_ru import LEXICON_RU

logging.basicConfig(level=logging.INFO)

bot: Bot = Bot(TOKEN_API)
dp: Dispatcher = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.reply("Привет!\nЯ пока что умею вычислять комплексные и вещественные числа!\n"
                        "Для вывода списка команд введите /help",
                        reply_markup=keyboard)


# Создаем объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()

# Создаем объекты инлайн-кнопок
button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='комплексные вычисления',
    callback_data='big_button_1_pressed')

button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='рациональные вычисления',
    callback_data='big_button_2_pressed')


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed'
@dp.callback_query_handler(text='big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    await callback.message.edit_text(text='Введите /complex далее что нужно подсчитать',
                                     reply_markup=callback.message.reply_markup)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@dp.callback_query_handler(text='big_button_2_pressed')
async def process_button_2_press(callback: CallbackQuery):
    await callback.message.edit_text(text='Введите /fraction далее что нужно подсчитать',
                                     reply_markup=callback.message.reply_markup, )
    await callback.answer()
    # await message.reply(f" {calc_fraction_main(command.args)}")


# Добавляем кнопки в клавиатуру методом add
keyboard.add(button_1).add(button_2)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply('''Калькулятор: /calculate\n ''')


@dp.message_handler(commands=['calculate'])
async def calc_command(message: types.Message):
    await message.answer(text=LEXICON_RU['/calculate'])


@dp.message_handler(commands=['complex'])
async def complex_command(message: types.Message, command: Command):
    await message.reply(f" {calc_complex_main(command.args)}")


@dp.message_handler(commands=['fraction'])
async def fraction_command(message: types.Message, command: Command):
    await message.reply(f" {calc_fraction_main(command.args)}")


@dp.message_handler(commands=['calc_log'])
async def log_command(message: types.Message):
    await message.reply(log_reader())


@dp.message_handler(commands=['contact'])
async def process_contact(message: Message):
    await message.answer(text=LEXICON_RU['/contact'])


# Создаем асинхронную функцию
async def set_main_menu(dp: Dispatcher):
    # Создаем список с командами для кнопки menu
    main_menu_commands = [
        types.BotCommand(command='/help', description='Справка по работе калькулятора'),
        types.BotCommand(command='/contact', description='Способы связи'),
        types.BotCommand(command='/calculate', description='Калькулятор')

    ]
    await dp.bot.set_my_commands(main_menu_commands)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_main_menu)
