from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, ReplyKeyboardRemove, Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

from app.common import bot, dp, logger
from app.keyboards import kb_client, kb_admin, kb_registered
from app.config import admin_ids
from app.strings import data_strings
from app.db.bot_db import bot_db
from app.common import set_admin_commands, set_client_commands, registered_users

async def cmd_start(message: Message, state: FSMContext):
    await state.finish()   
    #заносим юзера в базу
    # print(message)
    bot_db.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name, 
                    username=message.from_user.username, language_code=message.from_user.language_code)
    # bot_db.get_user_poll(user_id=message.from_user.id, poll_id=1)
    
    if message.from_user.id in admin_ids: # проверка на админа
        # await message.delete()
        await bot.send_message(message.from_user.id, data_strings['cmd']['start']['answer']+' админ', reply_markup=kb_admin)
        await set_admin_commands(bot)  # Установка команд бота
    else:
        # проверка на регистрацию
        # print(bot_db.get_registered_users())
        # print(registered_users)
        # print(message.from_user.id, type(message.from_user.id), registered_users, message.from_user.id in registered_users)
        if message.from_user.id in registered_users: kb=kb_registered
        else: kb=kb_client
        
        # print(message.from_user.id)
        # await message.delete()
        await bot.send_message(message.from_user.id, data_strings['cmd']['start']['answer'], reply_markup=kb)
        await set_client_commands(bot)  # Установка команд бота


async def cmd_help(message: Message, state: FSMContext):
    await state.finish()
    #заносим юзера в базу
    # print(message)
    bot_db.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name, 
                    username=message.from_user.username, language_code=message.from_user.language_code)
    # bot_db.get_user_poll(user_id=message.from_user.id, poll_id=1)
    
    if message.from_user.id in admin_ids:
        # await message.delete()
        await bot.send_message(message.from_user.id, data_strings['cmd']['help']['answer'], reply_markup=kb_admin)
        # await bot.send_message(chat_id, text)(data_strings['cmd']['help']['answer'], reply_markup=kb_admin)
        await set_admin_commands(bot)  # Установка команд бота
    else:
        # проверка на регистрацию
        if message.from_user.id in registered_users: kb=kb_registered
        else: kb=kb_client
        # print(message.from_user.id)
        # await message.delete()
        await bot.send_message(message.from_user.id, data_strings['cmd']['help']['answer'], reply_markup=kb)
        await set_client_commands(bot)  # Установка команд бота


async def cmd_cancel(message: Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in admin_ids:
        await bot.send_message(message.from_user.id, data_strings['cmd']['cancel']['answer'], reply_markup=kb_admin)
    else:
        # проверка на регистрацию
        if message.from_user.id in registered_users: kb=kb_registered
        else: kb=kb_client       
        await bot.send_message(message.from_user.id, data_strings['cmd']['cancel']['answer'], reply_markup=kb)

async def cmd_loc(message: Message, state: FSMContext):
    # print(message)
    answer = data_strings['cmd']['loc']['answer'].format(message['location']['latitude'], message['location']['longitude'])
    if message.from_user.id in admin_ids:
        await bot.send_message(message.from_user.id, answer, reply_markup=kb_admin)
    else:
        # проверка на регистрацию
        if message.from_user.id in registered_users: kb=kb_registered
        else: kb=kb_client        
        await bot.send_message(message.from_user.id, answer, reply_markup=kb)

async def cmd_tasks(message: Message, state: FSMContext):
    # print(message)
    if message.from_user.id in admin_ids:
        await bot.send_message(message.from_user.id, data_strings['cmd']['tasks']['answer'], reply_markup=kb_admin)
    else:
        # проверка на регистрацию
        if message.from_user.id in registered_users: kb=kb_registered
        else: kb=kb_client       
        await bot.send_message(message.from_user.id, data_strings['cmd']['tasks']['answer'], reply_markup=kb)

async def cmd_about(message: Message, state: FSMContext):
    # print(message)
    if message.from_user.id in admin_ids:
        await bot.send_message(message.from_user.id, data_strings['cmd']['about']['answer'], reply_markup=kb_admin)
    else:
        # проверка на регистрацию
        if message.from_user.id in registered_users: kb=kb_registered
        else: kb=kb_client       
        await bot.send_message(message.from_user.id, data_strings['cmd']['about']['answer'], reply_markup=kb)

async def cmd_donat(message: Message, state: FSMContext):
    # print(message)
    if message.from_user.id in admin_ids:
        await bot.send_message(message.from_user.id, data_strings['cmd']['donat']['answer'], reply_markup=kb_admin)
    else:
        # проверка на регистрацию
        if message.from_user.id in registered_users: kb=kb_registered
        else: kb=kb_client      
        await bot.send_message(message.from_user.id, data_strings['cmd']['donat']['answer'], reply_markup=kb)

async def cmd_contact(message: Message, state: FSMContext):
    # print(message['contact']['phone_number'])
    
    # устанавливаем номер телефона
    bot_db.set_phone(message.from_user.id, message['contact']['phone_number'])
    registered_users.append(message.from_user.id)
    # bot_db.print_table('users')
    if message.from_user.id in admin_ids:
        await bot.send_message(message.from_user.id, data_strings['cmd']['contact']['answer'], reply_markup=kb_admin)
    else:
        await bot.send_message(message.from_user.id, data_strings['cmd']['contact']['answer'], reply_markup=kb_registered)


def register_handlers_common_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, Text(equals=data_strings['cmd']['start']['lbl']), state="*")
    dp.register_message_handler(cmd_start, commands=data_strings['cmd']['start']['cmd'], state="*")
    
    dp.register_message_handler(cmd_help, Text(equals=data_strings['cmd']['help']['lbl']), state="*")
    dp.register_message_handler(cmd_help, commands=data_strings['cmd']['help']['cmd'], state="*")
    
    dp.register_message_handler(cmd_tasks, Text(equals=data_strings['cmd']['tasks']['lbl']), state="*")
    dp.register_message_handler(cmd_tasks, commands=data_strings['cmd']['tasks']['cmd'], state="*")
    
    dp.register_message_handler(cmd_about, Text(equals=data_strings['cmd']['about']['lbl']), state="*")
    dp.register_message_handler(cmd_about, commands=data_strings['cmd']['about']['cmd'], state="*")
    
    dp.register_message_handler(cmd_donat, Text(equals=data_strings['cmd']['donat']['lbl']), state="*")
    dp.register_message_handler(cmd_donat, commands=data_strings['cmd']['donat']['cmd'], state="*")
    
    # dp.register_message_handler(cmd_loc, content_types=["location"], state="*")
    
    dp.register_message_handler(cmd_contact, content_types=["contact"], state="*")
    
    dp.register_message_handler(cmd_cancel, Text(equals=data_strings['cmd']['cancel']['lbl'], ignore_case=True), state="*")
    dp.register_message_handler(cmd_cancel, commands=data_strings['cmd']['cancel']['cmd'], state="*")