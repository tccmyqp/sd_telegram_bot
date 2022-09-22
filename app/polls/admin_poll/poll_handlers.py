from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.common import bot, dp, Dispatcher
from app.config import admin_ids
from app.keyboards import kb_client, kb_admin, kb_cancel
from app.strings import data_polls


class admin_poll_states(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    
# начало диалога
async def admin_poll_start(message: Message):
    # await message.delete()
    await admin_poll_states.state1.set()
    await bot.send_message(message.from_user.id, data_polls['admin_poll']['steps']['0'], reply_markup=kb_cancel)
    
# первый ответ
async def admin_poll_step_1(message: Message, state: FSMContext):
    if message.text=='1':
        async with state.proxy() as data:
            data['state1'] = message.text
        await admin_poll_states.next()
        await bot.send_message(message.from_user.id, data_polls['admin_poll']['steps']['1'], reply_markup=kb_cancel)
    else:
        await bot.send_message(message.from_user.id, data_polls['admin_poll']['repeat']['1'], reply_markup=kb_cancel)
    
# второй ответ
async def admin_poll_step_2(message: Message, state: FSMContext):
    if message.text=='1':
        async with state.proxy() as data:
            data['state2'] = message.text
        await admin_poll_states.next()
        await bot.send_message(message.from_user.id, data_polls['admin_poll']['steps']['2'], reply_markup=kb_cancel)
    else:
        await bot.send_message(message.from_user.id, data_polls['admin_poll']['repeat']['2'], reply_markup=kb_cancel)
# последний ответ
async def admin_poll_step_3(message: Message, state: FSMContext):
    if message.text=='1':
        async with state.proxy() as data:
            data['state3'] = message.text
            print(data._data)
            await bot.send_message(message.from_user.id, data_polls['admin_poll']['steps']['3'].format(str(data._data)), reply_markup=kb_admin)
        await state.finish()# выход из состояния и очистка данных
    else:
        await bot.send_message(message.from_user.id, data_polls['admin_poll']['repeat']['3'], reply_markup=kb_cancel)
 

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_poll_start, IDFilter(user_id=admin_ids), commands=data_polls['admin_poll']['cmd'], state="*")
    dp.register_message_handler(admin_poll_start, IDFilter(user_id=admin_ids), Text(equals=data_polls['admin_poll']['lbl']), state="*")
    dp.register_message_handler(admin_poll_step_1, state=admin_poll_states.state1)
    dp.register_message_handler(admin_poll_step_2, state=admin_poll_states.state2)
    dp.register_message_handler(admin_poll_step_3, state=admin_poll_states.state3)
