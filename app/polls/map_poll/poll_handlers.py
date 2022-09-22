import re

from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.common import dp, bot, Dispatcher, registered_users
from app.db.bot_db import bot_db
from app.keyboards import kb_client, kb_cancel, kb_loc_poll, kb_yn_cancel, kb_registered, kb_admin, kb_poll_map_cancel, kb_loc_map_poll
from app.strings import data_polls, data_strings
from app.map_api import *
from app.config import admin_ids, DEBUG_functions
import aiogram.utils.markdown as fmt


class map_poll_states(StatesGroup):
    state0 = State()
    state1 = State()
    state2 = State()

           
# начало диалога вопрос и state0 / state1 poll_start / 'проголосовать повторно'  'посмотреть карту'
async def map_poll_start_check(message: Message, state: FSMContext):
    if DEBUG_functions: print('map_poll_start_check')
    
    r = bot_db.check_user_poll(user_id=message.from_user.id, poll_id=data_polls['map_poll']['id'])
    if r:
        await map_poll_states.state0.set()
        await bot.send_message(message.from_user.id, data_polls['map_poll']['steps']['00'], reply_markup=kb_poll_map_cancel)
    else:
        await map_poll_start(message, state)
        
# старт голосования state1
async def map_poll_start(message: Message, state: FSMContext):
    if DEBUG_functions: print('map_poll_start')
    await map_poll_states.state1.set()
    
    if bot_db.poll_data_exist(poll_id=data_polls['map_poll']['id']):
        kb = kb_loc_map_poll
    else:
        kb = kb_loc_poll
    await bot.send_message(message.from_user.id, data_polls['map_poll']['steps']['01'], reply_markup=kb)
    
# получен текст state1, repeat / state2
async def map_poll_text(message: Message, state: FSMContext):
    if DEBUG_functions: print('map_poll_text')
    # если в ответе только координаты
    pattern = r'^\d\d[.]\d\d\d\d\d\d[,]\d\d[.]\d\d\d\d\d\d$'
    if re.match(pattern, message.text):
        # print('its coords')
        answer, success, coords = get_address_from_coords(message.text)
    else:
        # print('its text')    
        answer, success, coords = get_address_from_coords(data_polls['map_poll']['city']+', ' + message.text)
    
    
    # print(coords)
    # адрес корректно написан текстом
    if success and str(answer[:19]) == data_polls['map_poll']['country']+', '+data_polls['map_poll']['city']:
        # print(answer)
        async with state.proxy() as data:
            data['coord'] = coords
            data['address'] = answer
            await bot.send_message(message.from_user.id, data_polls['map_poll']['steps']['02'].format(str(data['address'])), reply_markup=kb_yn_cancel)
        await map_poll_states.state2.set()
    else:
        await bot.send_message(message.from_user.id, data_polls['map_poll']['repeat']['1'], reply_markup=kb_loc_poll)

# получена локация state1, repeate / state2
async def map_poll_loc(message: Message, state: FSMContext):
    if DEBUG_functions: print('map_poll_loc')
    #вытаскиваем из него долготу и ширину
    current_position = (message.location.longitude, message.location.latitude)
    #создаем строку в виде ДОЛГОТА,ШИРИНА
    coords = f"{current_position[0]},{current_position[1]}"
    # print(coords)
    # bot.send_message(message.chat.id, coords)
    # #отправляем координаты в нашу функцию получения адреса
    answer, success, coords = get_address_from_coords(coords)
    # print(coords)
    if success:
        async with state.proxy() as data:
            data['coord'] = coords
            data['address'] = answer
        await map_poll_states.state2.set()
        await bot.send_message(message.from_user.id, data_polls['map_poll']['steps']['02'].format(str(data['address'])), reply_markup=kb_yn_cancel)
    else:
        await bot.send_message(message.from_user.id, data_polls['map_poll']['repeat']['1'], reply_markup=kb_loc_poll)

# финиш
async def map_poll_finish(message: Message, state: FSMContext):
    if DEBUG_functions: print('map_poll_finish')
    if message.from_user.id in admin_ids:kb = kb_admin
    elif message.from_user.id in registered_users: kb=kb_registered
    else: kb=kb_client
    async with state.proxy() as data:
        bot_db.set_poll_result(data=data['coord'], description=data['address'], user_id=message.from_user.id, poll_id=data_polls['map_poll']['id'])
        # await bot.send_message(message.from_user.id, f"адрес {data['address']} сохранен, спасибо за голосование")
        img = get_static_map_img(data['coord'])
        coords = data['coord']
        # img.save('map_point.png')
        # await message.answer_photo(img, reply_markup=kb)
        # long = data['coord'].split(',')[0]
        # lat = data['coord'].split(',')[1]
        
        # await message.answer_location(latitude=lat, longitude=long)
        
        url = get_url_complete_dynamic_map(poll_id=data_polls['map_poll']['id'])
        # print(url)
        # https://static-maps.yandex.ru/1.x/?l=map&ll={coords}&pt={coords},pm2rdm&spn=0.004,0.004
        caption = data_polls['map_poll']['steps']['03'].format(str(url))
        
        await bot.send_photo(message.from_user.id, img, caption = caption,
                        parse_mode="HTML", reply_markup=kb)
    await state.finish()
 
# показать карту
async def map_poll_show_map(message: Message, state: FSMContext):
    if DEBUG_functions: print('map_poll_show_map')
    if message.from_user.id in admin_ids:kb = kb_admin
    elif message.from_user.id in registered_users: kb=kb_registered
    else: kb=kb_client
    url = get_url_complete_dynamic_map(poll_id=data_polls['map_poll']['id'])
    await bot.send_message(message.from_user.id, data_polls['map_poll']['steps']['04'].format(str(url)), reply_markup=kb )
    await state.finish()
 
 
def register_handlers(dp: Dispatcher):
    
    dp.register_message_handler(map_poll_start_check, commands=data_polls['map_poll']['cmd'], state='*')
    dp.register_message_handler(map_poll_start_check, Text(equals=data_polls['map_poll']['lbl']), state='*')
    
    dp.register_message_handler(map_poll_start, commands=data_polls['map_poll']['cmd'], state=map_poll_states.state0)
    dp.register_message_handler(map_poll_start, Text(equals=data_strings['cmd']['poll']['lbl']), state=map_poll_states.state0)
    dp.register_message_handler(map_poll_start, Text(equals=data_strings['cmd']['no']['lbl']), state=map_poll_states.state2)
    
    dp.register_message_handler(map_poll_show_map, Text(equals=data_strings['cmd']['map']['lbl']), state=map_poll_states.state0)
    
    dp.register_message_handler(map_poll_text, state=map_poll_states.state1, content_types='text')
    dp.register_message_handler(map_poll_loc, state=map_poll_states.state1, content_types='location')

    dp.register_message_handler(map_poll_finish, Text(equals=data_strings['cmd']['yes']['lbl']), state=map_poll_states.state2)
    