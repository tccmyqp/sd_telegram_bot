from aiogram.types import KeyboardButton, ReplyKeyboardMarkup #, ReplyKeyboardRemove
from app.strings import data_strings, data_polls
import dataclasses


btns = {}
poll_btns = {}

# считываем кнопки общих команд
# STR_d = dataclasses.asdict(STR)
for key in data_strings['cmd'].keys():
    btns[key] = KeyboardButton(data_strings['cmd'][key]['lbl'])

btns['contact'] = KeyboardButton(data_strings['cmd']['contact']['lbl'], request_contact=True)
btns['loc'] = KeyboardButton(data_strings['cmd']['loc']['lbl'], request_location=True)

# считываем кнопки голосовалок
# STR_POLLS_d = dataclasses.asdict(STR_POLLS)
for key in data_polls.keys():
    poll_btns[key] = KeyboardButton(data_polls[key]['lbl'])
        

# создаем клавиатуры
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_registered = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_loc_poll = ReplyKeyboardMarkup(resize_keyboard=True)
kb_loc_map_poll = ReplyKeyboardMarkup(resize_keyboard=True)
kb_yn_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_poll_map_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_clmap_chid_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_settings = ReplyKeyboardMarkup(resize_keyboard=True)

kb_poll_map_cancel.row(btns['poll'], btns['map'], btns['cancel'])

kb_clmap_chid_cancel.row(btns['clear_map_poll'], btns['change_map_poll_id'], btns['cancel'])

kb_client.row(
            btns['start'], btns['help'], btns['about'], btns['contact']).row(
            poll_btns['map_poll'], btns['tasks']
            # btns['donat']
            )

kb_registered.row(
            btns['start'], btns['help'], btns['about']).row(
            poll_btns['map_poll'], btns['tasks']
            # btns['donat']
            )

kb_admin.row(
            btns['start'], btns['help'], btns['tasks'], btns['about']).row(
            poll_btns['map_poll'], btns['rst_map_poll'], btns['ch_poll_name'], btns['ch_poll_descr']).row(
            btns['adm_settings'], btns['contact'], btns['id'], btns['donat'])
            

kb_cancel.row(btns['cancel'])

kb_loc_poll.row(btns['loc'], btns['cancel'])
kb_loc_map_poll.row(btns['loc'], btns['map'], btns['cancel'])
kb_yn_cancel.row(btns['yes'], btns['no'], btns['cancel'])

kb_admin_settings.row(
                    btns['ch_start_msg'], btns['ch_help_msg']).row(
                    btns['ch_about_msg'], btns['ch_tasks_msg'], btns['cancel'])

# kb_test = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# kb_test.row(KeyboardButton(msg.btn_online),KeyboardButton(msg.btn_config))
