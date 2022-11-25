
from os import stat
from aiogram import Bot, Dispatcher, executor
from aiogram import types
from contextlib import suppress
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sqlite3

TOKEN = '5594391007:AAHGebNbF9JGlycU-HivOrPp33XLNnji2oU'

# ? Настройка логирования в stdout
logging.basicConfig(
    level=logging.INFO,
    format=u"%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# ? Подключение логгера
logger = logging.getLogger(__name__)


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определяем БД и таблицы ---------------------------------------
# с путём до файла БД сам разберешься. Будем считать, что он лежит рядом
# С полями таблицы тоже можешь оперировать.
conn = sqlite3.connect("fins.db")
cur = conn.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS finsbot(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER,
    username TEXT);
"""
)
conn.commit()
cur.close()

# Функция добавления пользователя в БД, если его там нет
def put_user(user_id: int, username: str = None) -> None:
    cur = conn.cursor()
    cur.execute("SELECT * FROM finsbot WHERE user_id = ?", (user_id,))
    if user_is_exist := cur.fetchone():
        cur.close()
        return

    cur.execute(
        "INSERT INTO finsbot VALUES (NULL, ?,?)",
        (
            user_id,
            username,
        ),
    )
    conn.commit()
    cur.close()


# * Определяем стейты для FSM
class MainStates(StatesGroup):
    antichaos = State()
    crypto = State()


button_1 = types.KeyboardButton('Курсы')
button_2 = types.KeyboardButton('Услуги')
button_3 = types.KeyboardButton('Поддержка 🛠')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_1, button_2, button_3)


ku = types.ReplyKeyboardMarkup(resize_keyboard=True)
b_1 = types.KeyboardButton('Crypto Trip')
b_2 = types.KeyboardButton('Up to Perfection')
ku.add(b_1, b_2)


course_kbd = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1 = types.KeyboardButton('Программа курса')
bt2 = types.KeyboardButton('Тарифы')
bt3 = types.KeyboardButton('Поддержка 🛠')
bt4 = types.KeyboardButton('Назад ↩️')
course_kbd.add(bt1, bt2, bt3, bt4)


pk1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
bk1 = types.KeyboardButton('Тарифы')
bk2 = types.KeyboardButton('Поддержка 🛠')
bk3 = types.KeyboardButton('Назад ↩️')
pk1.add(bk1, bk2, bk3)


op = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Оплата картой 💳')
item2 = types.KeyboardButton('Оплата через кошелёк(крипта)📈')
back = types.KeyboardButton('Назад ↩️')
op.add(item1, item2, back)


# state="*" означает, что этот хэндлер будет работать при любом стэйте
@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish() # Завершение активного стейта
    await message.answer("Привет! Это команда Finesse✨ \n\nFinesse - это команда профессионалов, которая круглосуточно анализирует,"
    "выдают сетапы и делятся торгами, оттачивают стратегии и помогают развиваться другим.", reply_markup=greet_kb)
    put_user(message.from_user.id, message.from_user.username)    

@dp.message_handler(text="Курсы", state="*")
async def courses(message: types.Message):
    with open('ob.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Пожалуйста, выберете курс!", reply_markup=ku)


@dp.message_handler(text="Поддержка 🛠", state="*")
async def support(message: types.Message):
    await message.answer("Оставьте свой вопрос и в ближайшее время с вами свяжется менеджер!\n https://t.me/Manager_Finesse", reply_markup=greet_kb)


@dp.message_handler(text='Crypto Trip', state="*")
async def antishaos(message: types.Message, state: FSMContext):
    await MainStates.antichaos.set() # устанавливаем стейт. теперь будут работать только те хэндлеры, в которых есть state=MainStates.antichaos
    with open('trip.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Информация о курсе!", reply_markup=course_kbd)


@dp.message_handler(text='Up to Perfection', state="*")
async def crypto_x(message: types.Message):
    await MainStates.crypto.set()
    with open('perf.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Информация о курсе!", reply_markup=course_kbd)


# Программа курса антихаос
# state=MainStates.antichaos = этот хендлер будет работать только в этом стейте
@dp.message_handler(text="Программа курса", state=MainStates.antichaos)
async def course_prog_antichaos(message: types.Message, state: FSMContext):
    with open('trr.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Программа курса!", reply_markup=course_kbd)



# Тарифы антихаос
@dp.message_handler(text="Тарифы", state=MainStates.antichaos)
async def tarifs_antichaos(message: types.Message, state: FSMContext):
    with open('tripop.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Выберете способ оплаты!", reply_markup=op)
    

# Программа криптофигни
@dp.message_handler(text="Программа курса", state=MainStates.crypto)
async def course_prog_crypto(message: types.Message, state: FSMContext):
     with open('prr.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
        await message.answer("Программа курса!", reply_markup=course_kbd)



# Тарифы криптофигни
@dp.message_handler(text="Тарифы", state=MainStates.crypto)
async def tarifs_crypto(message: types.Message, state: FSMContext):
    with open('perfop.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Выберете способ оплаты!", reply_markup=op)


@dp.message_handler(text='Оплата картой 💳', state="*")
async def payment_card(message: types.Message):
    await message.answer(
        "Номер карты(Tinkoff): 5536 9141 7128 3959 \n\nПосле оплаты ОБЯЗАТЕЛЬНО отправьте чек в чат https://t.me/Manager_Finesse"
        "\n\nВнимательно проверьте скопированный номер карты!\n\n"
        "С уважением - Finesse", reply_markup=greet_kb)


@dp.message_handler(text='Оплата через кошелёк(крипта)📈', state="*")
async def payment_wallet(message: types.Message):
    with open('kod.jpg', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("BTC (Bitcoin): 1BdoJuPqAPYhwmmJj3v4RKtRkNZu9v12ci\n\nUSDT (TRC20): TKjpkG1YynK9HzBzdigmTZYM7CGb6rq1ur\n\nUSDT (ERC20): 0xd52e0cecac194a5fe09734bafa7e75a481d4c445\n\nПосле оплаты ОБЯЗАТЕЛЬНО отправьте Txid транзакции (либо цифры если внутренний перевод Binance) менеджеру:https://t.me/Manager_Finesse\n\nВнимательно проверьте скопированный номер кошелька!\n\nС уважением - Finesse", reply_markup=greet_kb)


@dp.message_handler(text="Назад ↩️", state="*")
async def go_back(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Главное меню", reply_markup=greet_kb)


@dp.message_handler(text="Услуги", state="*")
async def services(message: types.Message):
    await message.answer("В данном канале предоставлены все услуги от Finesse: https://t.me/FinesseService", reply_markup=greet_kb)


if __name__ == "__main__":

    # * Запуск поллинга
    try:
        logger.warning("Starting bot")
        executor.start_polling(dp)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
