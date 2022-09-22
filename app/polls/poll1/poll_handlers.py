from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.common import bot, dp, Dispatcher
from app.keyboards import kb_client, kb_cancel
from app.strings import data_polls


class poll1_states(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()

# начало диалога
async def poll1_start(message: Message):
    # await message.delete()
    await poll1_states.state1.set()
    await bot.send_message(message.from_user.id, data_polls['poll1']['steps']['0'], reply_markup=kb_cancel)

# первый ответ
async def poll1_1(message: Message, state: FSMContext):
    if message.text=='1':
        async with state.proxy() as data:
            data['state1'] = message.text
        await poll1_states.next()
        await bot.send_message(message.from_user.id, data_polls['poll1']['steps']['1'], reply_markup=kb_cancel)
    else:
        await bot.send_message(message.from_user.id, data_polls['poll1']['repeat']['1'], reply_markup=kb_cancel)

# второй ответ
async def poll1_2(message: Message, state: FSMContext):
    if message.text=='1':
        async with state.proxy() as data:
            data['state2'] = message.text
        await poll1_states.next()
        await bot.send_message(message.from_user.id, data_polls['poll1']['steps']['2'], reply_markup=kb_cancel)
    else:
        await bot.send_message(message.from_user.id, data_polls['poll1']['repeat']['2'], reply_markup=kb_cancel)

# последний ответ
async def poll1_3(message: Message, state: FSMContext):
    if message.text=='1':
        async with state.proxy() as data:
            data['state3'] = message.text
        await bot.send_message(message.from_user.id, data_polls['poll1']['steps']['3'].format(str(data)), reply_markup=kb_client)
        await state.finish()  # выход из состояния и очистка данных
    else:
        await bot.send_message(message.from_user.id, data_polls['poll1']['repeat']['3'], reply_markup=kb_cancel)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(poll1_start, commands=data_polls['poll1']['cmd'], state="*")
    dp.register_message_handler(poll1_start, Text(equals=data_polls['poll1']['lbl']), state="*")
    
    dp.register_message_handler(poll1_1, state=poll1_states.state1)
    dp.register_message_handler(poll1_2, state=poll1_states.state2)
    dp.register_message_handler(poll1_3, state=poll1_states.state3)
