import json, os

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.common import bot, dp, Dispatcher
from app.db.bot_db import bot_db
from app.config import admin_ids, ROOT_DIR, DEBUG_functions
from app.keyboards import *
import app.keyboards as kb
from app.strings import data_strings, data_polls


class admin_cmd_states(StatesGroup):
    adm_settings = State()
    ch_start_msg = State()
    ch_start_msg2 = State()
    ch_help_msg = State()
    ch_help_msg2 = State()
    ch_about_msg = State()
    ch_about_msg2 = State()
    ch_tasks_msg = State()
    ch_tasks_msg2 = State()
    clear_map_poll = State()
    ch_name_map_poll = State()
    ch_name_map_poll2 = State()
    ch_descr_map_poll = State()
    ch_descr_map_poll2 = State()
    
adm_settings_names = ['ch_start_msg', 'ch_help_msg', 'ch_tasks_msg', 'ch_about_msg']
adm_settings_lbls = [data_strings['cmd'][i]['lbl'] for i in adm_settings_names]

adm_settings_states = [admin_cmd_states.ch_start_msg,
                       admin_cmd_states.ch_help_msg,
                       admin_cmd_states.ch_about_msg,
                       admin_cmd_states.ch_tasks_msg]   

adm_settings_states2 = [admin_cmd_states.ch_start_msg2,
                       admin_cmd_states.ch_help_msg2,
                       admin_cmd_states.ch_about_msg2,
                       admin_cmd_states.ch_tasks_msg2]   

# отобразить id
async def cmd_id(message: Message, state: FSMContext):
    # await message.delete()
    await state.finish()
    await bot.send_message(message.from_user.id, data_strings['cmd']['id']['answer'].format(message.from_user.id, message.from_user.first_name), reply_markup=kb_admin)

# смена названия кнопки голосования
async def cmd_ch_name_map_poll_start(message: Message, state: FSMContext):
    await admin_cmd_states.ch_name_map_poll.set()
    await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_name']['answer'].format(data_polls['map_poll']['lbl']), reply_markup=kb_cancel)

async def cmd_ch_name_map_poll_finish(message: Message, state: FSMContext):

    # переименовываем кнопку
    for row in kb_admin.__dict__['_values']['keyboard']:
        for btn in row:
            if btn['text'] == data_polls['map_poll']['lbl']:
                btn['text'] = message.text
    
    
    data_polls['map_poll']['lbl'] = message.text
    
    # записываем в файл
    str_path = os.path.join(ROOT_DIR, 'polls', 'map_poll', 'poll_strings.json')
    with open(str_path, 'w', encoding='utf-8') as f:
        json.dump(data_polls['map_poll'], f, indent=2, ensure_ascii=False)
    
    if await state.get_state()=='admin_cmd_states:ch_name_map_poll':
        await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_name']['answer2'], reply_markup=kb_yn_cancel)
        await admin_cmd_states.next()
    else:
        await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_name']['answer3'], reply_markup=kb_admin)
        await state.finish()
        
    
async def cmd_ch_name_map_poll_finish_yes(message: Message, state: FSMContext):    
    await state.finish()
    message.text = data_polls['map_poll']['lbl']
    await cmd_ch_descr_map_poll_finish(message=message, state=state)
    # await bot.send_message(message.from_user.id, 'описание голосования также изменено', reply_markup=kb_admin)
    
async def cmd_ch_name_map_poll_finish_no(message: Message, state: FSMContext):    
    await state.finish()
    await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_name']['answer4'], reply_markup=kb_admin)
    
        
# смена названия голосования в базе
async def cmd_ch_descr_map_poll_start(message: Message, state: FSMContext):
    await admin_cmd_states.ch_descr_map_poll.set()
    await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_descr']['answer'].format(data_polls['map_poll']['descr']), reply_markup=kb_cancel)

async def cmd_ch_descr_map_poll_finish(message: Message, state: FSMContext):
    data_polls['map_poll']['descr'] = message.text
    
    # записываем в файл
    str_path = os.path.join(ROOT_DIR, 'polls', 'map_poll', 'poll_strings.json')
    with open(str_path, 'w', encoding='utf-8') as f:
        json.dump(data_polls['map_poll'], f, indent=2, ensure_ascii=False)
    
    bot_db.update_poll_names()
    
    if await state.get_state()=='admin_cmd_states:ch_descr_map_poll':
        await admin_cmd_states.next()
        await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_descr']['answer2'], reply_markup=kb_yn_cancel)
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_descr']['answer3'], reply_markup=kb_admin)
    

async def cmd_ch_descr_map_poll_finish_yes(message: Message, state: FSMContext):    
    await state.finish()
    message.text = data_polls['map_poll']['descr']
    await cmd_ch_name_map_poll_finish(message=message, state=state)
    # await bot.send_message(message.from_user.id, 'описание голосования также изменено', reply_markup=kb_admin)
    
    # message.text = data_polls['map_poll']['lbl']
    # await cmd_ch_descr_map_poll_finish(message=message, state=state)
    
async def cmd_ch_descr_map_poll_finish_no(message: Message, state: FSMContext):    
    await state.finish()
    await bot.send_message(message.from_user.id, data_strings['cmd']['ch_poll_descr']['answer4'], reply_markup=kb_admin)

# adm_settings
async def cmd_adm_settings(message: Message, state: FSMContext):
    if DEBUG_functions: print('cmd_adm_settings')
    await admin_cmd_states.adm_settings.set()
    await bot.send_message(message.from_user.id, data_strings['cmd']['adm_settings']['answer'], reply_markup=kb_admin_settings)

# начало изменений настроек
async def cmd_adm_settings_start(message: Message, state: FSMContext):
    if DEBUG_functions: print('cmd_adm_settings_start')
    
    if message.text == data_strings['cmd']['ch_start_msg']['lbl']:
        await admin_cmd_states.ch_start_msg.set()
        answer = data_strings['cmd']['start']['answer']  
          
    elif message.text == data_strings['cmd']['ch_help_msg']['lbl']:
        await admin_cmd_states.ch_help_msg.set()
        answer = data_strings['cmd']['help']['answer']
        
    elif message.text == data_strings['cmd']['ch_about_msg']['lbl']:
        await admin_cmd_states.ch_about_msg.set()
        answer = data_strings['cmd']['about']['answer']
        
    elif message.text == data_strings['cmd']['ch_tasks_msg']['lbl']:
        await admin_cmd_states.ch_tasks_msg.set()
        answer = data_strings['cmd']['tasks']['answer']
        
    await bot.send_message(message.from_user.id, data_strings['cmd']['adm_settings']['answer2'].format(answer), reply_markup=kb_cancel)

# подтверждение    
async def cmd_adm_settings_process(message: Message, state: FSMContext):
    st = await state.get_state()
    
    if DEBUG_functions: print('cmd_adm_settings_process', 'message.text:', message.text, ' st:', st)   
    if st in ['admin_cmd_states:ch_start_msg', 'admin_cmd_states:ch_help_msg', 'admin_cmd_states:ch_about_msg', 'admin_cmd_states:ch_tasks_msg']:
        await admin_cmd_states.next()
    async with state.proxy() as data: data['new_msg'] = message.text
    await bot.send_message(message.from_user.id, data_strings['cmd']['adm_settings']['answer3'].format(message.text), reply_markup=kb_yn_cancel)
    
# сохранение изменений
async def cmd_adm_settings_finish(message: Message, state: FSMContext):
    if DEBUG_functions: print('cmd_adm_settings_finish')
    data = await state.get_data()
    st = await state.get_state()
    
    if st == 'admin_cmd_states:ch_start_msg2':
       data_strings['cmd']['start']['answer'] = data['new_msg']
    elif st == 'admin_cmd_states:ch_help_msg2':
        data_strings['cmd']['help']['answer'] = data['new_msg']
    elif st == 'admin_cmd_states:ch_about_msg2':
        data_strings['cmd']['about']['answer'] = data['new_msg']
    elif st == 'admin_cmd_states:ch_tasks_msg2':
        data_strings['cmd']['tasks']['answer'] = data['new_msg']
    
    print(st, data['new_msg'])  
    # сохраняем strings.json
    with open(os.path.join(ROOT_DIR,'strings.json'), 'w', encoding='utf-8') as f:
        json.dump(data_strings, f, indent=2, ensure_ascii=False)
    await bot.send_message(message.from_user.id, data_strings['cmd']['adm_settings']['answer4'].format(data['new_msg']), reply_markup=kb_admin)
    await state.finish()
    
# начало сброса map_poll
async def cmd_rst_map_poll(message: Message, state: FSMContext):    
    # проверяем пустая ли таблица
    if bot_db.poll_data_exist(poll_id=data_polls['map_poll']['id']):
        
        # если нет то выбираем очистить текущую или обновить id
        await admin_cmd_states.clear_map_poll.set()
        await bot.send_message(message.from_user.id, data_strings['cmd']['rst_map_poll']['answer1'], reply_markup=kb_clmap_chid_cancel)
    else:    
        # иначе ничего не делаем
        await bot.send_message(message.from_user.id, data_strings['cmd']['rst_map_poll']['answer1'], reply_markup=kb_admin)

# выбрана очистка таблицы map_poll                           
async def cmd_rst_map_poll_clear(message: Message, state: FSMContext):
    bot_db.clear_poll_results(poll_id=data_polls['map_poll']['id'])
    await state.finish()
    await bot.send_message(message.from_user.id, data_strings['cmd']['clear_map_poll']['answer'], reply_markup=kb_admin)

# выбрана смена id map_poll    
async def cmd_rst_map_poll_change(message: Message, state: FSMContext):
    global data_polls
    
    path = os.path.join(ROOT_DIR,'polls','map_poll','poll_strings.json')
    
    # найдем следующий id
    new_id = max(bot_db.get_poll_ids())+1
    
    # устанавливаем id
    data_polls['map_poll']['id'] = new_id
    
    # сохраним данные в json
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data_polls['map_poll'], f, indent=2, ensure_ascii=False)
                
    await state.finish()
    await bot.send_message(message.from_user.id, data_strings['cmd']['change_map_poll_id']['answer']+str(new_id), reply_markup=kb_admin)


def register_handlers_admin_cmd(dp: Dispatcher):
    
    dp.register_message_handler(cmd_id, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['id']['lbl']), state="*")
    
    # выбор настроек
    dp.register_message_handler(cmd_adm_settings, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['adm_settings']['lbl']), state="*")
    
    # запуск ch_start_msg
    dp.register_message_handler(cmd_adm_settings_start, IDFilter(user_id=admin_ids), Text(equals=adm_settings_lbls), state=admin_cmd_states.adm_settings)
    
    # запрос сообщения
    dp.register_message_handler(cmd_adm_settings_process, IDFilter(user_id=admin_ids), state=adm_settings_states)
    
    # обработка сообщения
    dp.register_message_handler(cmd_adm_settings_finish, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['yes']['lbl']), state=adm_settings_states2)
    dp.register_message_handler(cmd_adm_settings_start, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['no']['lbl']), state=adm_settings_states2)
        
    #ch_name_map_poll
    dp.register_message_handler(cmd_ch_name_map_poll_start, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['ch_poll_name']['lbl']), state="*")
    dp.register_message_handler(cmd_ch_name_map_poll_finish, IDFilter(user_id=admin_ids), state=admin_cmd_states.ch_name_map_poll)
    
    # запрос на соответсвенное изменение описания/названия
    dp.register_message_handler(cmd_ch_name_map_poll_finish_yes, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['yes']['lbl']), state=admin_cmd_states.ch_name_map_poll2)
    dp.register_message_handler(cmd_ch_name_map_poll_finish_no, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['no']['lbl']), state=admin_cmd_states.ch_name_map_poll2)
    dp.register_message_handler(cmd_ch_descr_map_poll_finish_yes, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['yes']['lbl']), state=admin_cmd_states.ch_descr_map_poll2)
    dp.register_message_handler(cmd_ch_descr_map_poll_finish_no, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['no']['lbl']), state=admin_cmd_states.ch_descr_map_poll2)

    #ch_descr_map_poll
    dp.register_message_handler(cmd_ch_descr_map_poll_start, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['ch_poll_descr']['lbl']), state="*")
    dp.register_message_handler(cmd_ch_descr_map_poll_finish, IDFilter(user_id=admin_ids), state=admin_cmd_states.ch_descr_map_poll)
    
    
    dp.register_message_handler(cmd_rst_map_poll, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['rst_map_poll']['lbl']), state="*")
    dp.register_message_handler(cmd_rst_map_poll_clear, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['clear_map_poll']['lbl']), state=admin_cmd_states.clear_map_poll)
    dp.register_message_handler(cmd_rst_map_poll_change, IDFilter(user_id=admin_ids), Text(equals=data_strings['cmd']['change_map_poll_id']['lbl']), state=admin_cmd_states.clear_map_poll)
    
    # dp.register_message_handler(cmd_get_avatar_by_id, IDFilter(user_id=admin_id), commands=data_strings['cmd']['id']['cmd'], state="*")

