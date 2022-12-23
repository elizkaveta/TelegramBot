import asyncio

from aiogram import Bot, types
import random
from datetime import datetime, date, time
from aiogram.dispatcher.filters import state
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN
import keyboard as kb
from msgs import messages, shar_msg
from states import MyStates

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(messages["Старт"], reply_markup=kb.markup5)
    await MyStates.menu.set()


@dp.message_handler(state='*', text=['Помощь', '/help'])
async def process_help_command(message: types.Message):
    await message.answer(messages["Помощь"])
    await MyStates.menu.set()


@dp.message_handler(state=MyStates.menu, text=['Магический шар'])
async def process_magic_ball(message: types.Message):
    await message.answer(messages["Шар"], reply_markup=kb.markup_shar)
    await MyStates.sharik.set()


@dp.message_handler(state=[MyStates.sharik, MyStates.sharik_msg])
async def process_magic_ball_answer(message: types.Message):
    await message.answer(messages["Сообщение шару"], reply_markup=kb.markup5)
    await asyncio.sleep(1)
    await message.answer(shar_msg[random.randint(0, len(shar_msg) - 1)])
    await MyStates.menu.set()


@dp.message_handler(state=MyStates.menu, text=['Рассчитать совместимость❤️'])
async def process_sovm(message: types.Message):
    await message.answer(messages["Какое"], reply_markup=kb.markup_sovm)
    await MyStates.sovm.set()


@dp.message_handler(state=MyStates.sovm, text=['По росту'])
async def process_sovm_height(message: types.Message):
    await message.answer("Введите ваш рост и рост вашего партнера в см через пробел")
    await MyStates.height.set()


@dp.message_handler(state=MyStates.height)
async def process_sovm_height_ans(message: types.Message):
    try:
        height = list(map(int, message.text.split()))
        assert len(height) == 2
        height.sort()
        ans = (height[0] * 36 + height[1] * 23) % 101
        if height == [172, 183]:
            ans = 100
        await message.answer(f"Ваша совместимость составляет {ans}%", reply_markup=kb.markup5)
        await MyStates.menu.set()
    except:
        await message.answer("Введите ваш рост нормально плиз")


@dp.message_handler(state=MyStates.sovm, text=['По именам'])
async def process_sovm_name(message: types.Message):
    await message.answer("Введите Ваше имя и имя Вашего партнера через запятую")
    await MyStates.name.set()

@dp.message_handler(state=MyStates.name)
async def process_sovm_name(message: types.Message):
    try:
        height = message.text.split(",")
        assert len(height) == 2
        height[0] = height[0].replace(" ", "")
        height[1] = height[1].replace(" ", "")
        height.sort()
        ans = (hash(height[0]) * 36 + hash(height[1]) * 23) % 101
        if height == ['Данила', 'Лиза']:
            ans = 100
        await message.answer(f"Ваша совместимость составляет {ans}%", reply_markup=kb.markup5)
        await MyStates.menu.set()
    except:
        await message.answer("Введите ваши имена нормально плиз")

@dp.message_handler(state=MyStates.sovm, text=['По дате рождения'])
async def process_sovm_date(message: types.Message):
    await message.answer("Введите Вашу дату рождения и дату рождения партнера в формате ДД.ММ.ГГГГ ДД.ММ.ГГГГ")
    await MyStates.date.set()


@dp.message_handler(state=MyStates.date)
async def process_sovm_name(message: types.Message):
    try:
        height = message.text.split(" ")
        assert len(height) == 2

        a = datetime.strptime(height[0], "%d.%m.%Y")
        b = datetime.strptime(height[1], "%d.%m.%Y")
        print(datetime.timestamp(a))
        print(datetime.timestamp(b))
        c = ((datetime.timestamp(a) // 1000) * 44 + (datetime.timestamp(b) // 1000)*23 + 87) % 101
        c = int(c)
        if height == ['01.07.2003', '02.07.2002'] or height == ['02.07.2002', '01.07.2003']:
            c = 100
        await message.answer(f"Ваша совместимость составляет {c}%", reply_markup=kb.markup5)
        await MyStates.menu.set()
    except:
        await message.answer("Введите ваши даты нормально плиз")


@dp.message_handler(state=MyStates.menu, text=['Квадрат Пифагора'])
async def process_pif(message: types.Message):
    await message.answer("Введите Вашу дату рождения в формате ДД.ММ.ГГГГ")
    await MyStates.pifagor.set()

def sum_of_nubmers(a: int) -> int:
    return (a % 10) + (a // 10) % 10 + (a // 100) % 10 + (a // 1000) % 10
def find_first_number(a: int) -> int:
    c = 0
    while a:
        c = a % 10
        a //= 10
    return c
@dp.message_handler(state=MyStates.pifagor)
async def process_pif1(message: types.Message):
    try:
        a = datetime.strptime(message.text, "%d.%m.%Y")
        height = list(map(int, message.text.split(".")))
        assert len(height) == 3
        d = [0] * 4
        d[0] = sum_of_nubmers(height[0]) + sum_of_nubmers(height[1]) + sum_of_nubmers(height[2])
        d[1] = sum_of_nubmers(d[0])
        d[2] = d[0] - 2
        d[3] = sum_of_nubmers(d[2])
        print(d)
        b = [0] * 10
        for i in range(4):
            b[d[i] % 10] += 1
            b[(d[i] // 10) % 10] += 1
            b[(d[i] // 100) % 10] += 1
        s = str("")
        for i in range(3):
            b[height[i] % 10] += 1
            b[(height[i] // 10) % 10] += 1
            b[(height[i] // 100) % 10] += 1
            b[(height[i] // 1000) % 10] += 1
        s = str("")

        print("her2")
        for m in range(1, 4):
            for i in range(3):
                s += "["
                s += str(3 * i + m) * b[3 * i + m]
                s += "] "
            s += "\n"
        await message.answer("Ваш квадрат Пифагора рассчитан")
        await message.answer(s)
        await MyStates.menu.set()
    except:
        await message.answer("Введите вашу дату нормально плиз")


if __name__ == '__main__':
    executor.start_polling(dp)

@dp.message_handler(state=MyStates.menu)
async def process_magic_ball(message: types.Message):
    await message.answer("Ничего не понятно, напишите /help или \"Помощь\" или тыкайте на кнопки",
                         reply_markup=kb.markup5)


@dp.message_handler(state=MyStates.sovm)
async def process_magic_ball(message: types.Message):
    await message.answer("Ничего не понятно, напишите /help или \"Помощь\" или тыкайте на кнопки",
                         reply_markup=kb.markup_sovm)
