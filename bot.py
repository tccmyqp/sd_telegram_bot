# import sys
# import unittest

import asyncio
from random import randint

from app.common import (bot, dp, logger, register_handlers_polls,
                        registered_users, set_start_commands)
from app.db.bot_db import bot_db
from app.handlers.admin_cmd import register_handlers_admin_cmd
from app.handlers.common_cmd import register_handlers_common_cmd
from app.handlers.exception import register_handlers_exception

logger.disable('__main__')
# from logging import StreamHandler
# logger.add(StreamHandler(sys.stderr), format="{message}")

# from loguru import logger 
# fmt = "{time} - {name} - {level} - {message}"
# logger.add(level="INFO", format=fmt)


# class TestBotDB(unittest.TestCase):
    
#     def test_equals(self):
#         self.assertEqual("one string", "one string")
        
#     print('добавим пользователя 0')
#     bot_db.add_user(user_id='0', user_name='test_user')

#     print('таблица users:', bot_db.get_records())

#     print('изменим fsm_state')
#     bot_db.change_fmt_state(user_id=555, fsm_state=randint(0,100))

#     print('таблица users:', bot_db.get_records())   

# выполняется при запуске бота
async def on_startup():
    try:
        logger.info("on_startup") # вывод инфо
        
        bot_db.update_poll_names()
        
        if bot_db.user_exists(user_id=0):
            logger.info("user 0 exist")
            bot_db.del_user(user_id=0)
            logger.info("user 0 deleted")
            bot_db.print_table(table_name='users')
        else:
            logger.info("user 0 not exist")
            bot_db.add_user(user_id=0, first_name='test_first_name', username='test_username', language_code='ru')
            logger.info("'user 0 added")
            bot_db.print_table(table_name='users')        
            
        # print('registered:', registered_users)
        register_handlers_exception(dp)  # регистрация хендлеров
        register_handlers_common_cmd(dp)  # регистрация хендлеров
        register_handlers_admin_cmd(dp)  # регистрация хендлеров    
        register_handlers_polls()
                
        await set_start_commands(bot)  # Установка команд бота
        await dp.skip_updates() # пропуск обновлений
        await dp.start_polling() # старт полинга
    except asyncio.TimeoutError:
        print('asyncio timeout!')
    

if __name__ == '__main__':
    # unittest.main()
    asyncio.run(on_startup())