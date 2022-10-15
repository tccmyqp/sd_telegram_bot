import os
import re
import sqlite3
import sys

from app.common import logger
from app.config import DEBAG_db, db_name, sql_create_name
# from app.config import db_name, sql_create_path
from app.strings import data_polls

logger.add(sys.stderr, level="ERROR")

if not DEBAG_db:
    logger.disable("app.db.bot_db")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(ROOT_DIR, db_name)  # type: ignore
sql_create_path = os.path.join(ROOT_DIR, sql_create_name)

class BotDB:

    def __init__(self, db_path):
        try:
            self.db_path = db_path
            # проверяем наличие таблиц
            self.connect = sqlite3.connect(self.db_path)
            logger.info(f'connect: {self.connect}')
            self.cursor = self.connect.cursor()
            logger.info(f'cursor: {self.cursor}')
            self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users'")
            res1 = self.cursor.fetchone()
            self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='poll_names'")
            res2 = self.cursor.fetchone()
            self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='poll_results'")
            res3 = self.cursor.fetchone()
            
            # if self.connect: self.connect.close()
            
            if not res1 or not res2 or not res2 :
                logger.warning(f'нет таблицы:, {res1}, {res2}, {res3}')
                self.create_new()   
        except:
            e = sys.exc_info()[1]
            logger.exception(f'init: {e.args[0]}')# type: ignore
        finally:
            self.db_stop()        
        
    def str_clear(self, table_name):
        return ''.join( chr for chr in table_name if chr.isalnum() or chr=='_')
        
    def db_start(self):
        pass
        # self.connect = sqlite3.connect(self.db_path)
        # self.cursor = self.connect.cursor()
    
    def db_stop(self):
        pass
        # if self.connect: self.connect.close()
    
    # обновляем названия голосований в базе
    def update_poll_names(self):
        logger.info('DB')  
        try:
            self.db_start()   
            for key in data_polls.keys():
                poll_id = data_polls[key]['id']
                poll_name = data_polls[key]['name']
                poll_description = data_polls[key]['descr']
                info_msg = f'poll_id: {poll_id}'
                # если есть такой poll_id обновляем
                if self.cursor.execute("SELECT `poll_id` FROM `poll_names` WHERE `poll_id` = ? ", (poll_id,)).fetchone():
                    logger.info(info_msg + ' обновить')
                    self.cursor.execute("UPDATE `poll_names` SET `name` = ?, `description` = ? WHERE `poll_id` = ?", (poll_name, poll_description, poll_id,))
                    self.connect.commit()
                # если такой записи нет, вставляем новую
                else:
                    logger.info(info_msg + ' вставить')
                    self.cursor.execute("INSERT INTO `poll_names` (`poll_id`, `name`) VALUES (?, ?)", (poll_id, poll_name,))
                    self.connect.commit()
                    
            self.db_stop()
            self.print_table('poll_names')
            
        except:
            e = sys.exc_info()[1]
            logger.exception(f'update_poll_names: {e.args[0]}')# type: ignore
              
        finally:
            self.db_stop()            
                
    # обновляем названия голосований в базе
    def get_poll_ids(self):   
        if DEBAG_db:
            logger.info('DB')  
        try:
            self.db_start()
            res = self.cursor.execute("SELECT `poll_id` FROM `poll_names` ").fetchall()
            self.db_stop()
            ret = [i[0] for i in res]
        except:
            e = sys.exc_info()[1]
            logger.exception(f'get_poll_ids: {e.args[0]}')# type: ignore
        else:
            return ret
        finally:
            self.db_stop()
                                                     
    def create_new(self):
        logger.info('DB')  
        try:
            self.db_start()
            logger.info('создаем новые таблицы')
            with open(sql_create_path, "r") as f:
                sql = f.read()
            logger.info(f'sql_script len: {len(sql)}')    
            self.cursor.executescript(sql)
            self.connect.commit()
            logger.info(self.get_table('users'))
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'create_new: {e.args[0]}')# type: ignore
        finally:
            self.db_stop()
    
    def clear_poll_results(self, poll_id):
        logger.info('DB')  
        try:
            self.db_start()
            result = self.cursor.execute("DELETE from `poll_results` WHERE `poll_id` = ?", (poll_id,))
            self.connect.commit()
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'clear_poll_results: {e.args[0]}')# type: ignore
        finally:
            self.db_stop()        
        
    def user_exists(self, user_id):
        logger.info('DB')  
        try:
            self.db_start()
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ?", (user_id,))
            ret = bool(len(result.fetchall()))
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'user_exists: {e.args[0]}')# type: ignore
        else:    
            return ret
        finally:
            self.db_stop()
                    
    def poll_data_exist(self, poll_id):
        logger.info('DB')  
        try:
            self.db_start()
            result = self.cursor.execute("SELECT `data` FROM `poll_results` WHERE `poll_id` = ?", (poll_id,))
            ret = bool(len(result.fetchall()))
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'poll_data_exist: {e.args[0]}')# type: ignore
        else:    
            return ret
        finally:
            self.db_stop()
            
    def check_user_poll(self, user_id, poll_id):
        logger.info('DB')  
        try:
            self.db_start()
            result = self.cursor.execute("SELECT `data` FROM `poll_results` WHERE `user_id` = ? AND `poll_id` = ?", (user_id, poll_id,)).fetchone()
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'check_user_poll: {e.args[0]}')# type: ignore
        else:    
            return result
        finally:
            self.db_stop()
     
    def set_poll_result(self, data, description, user_id, poll_id):
        logger.info('DB')  
        try:
            self.db_start()
            result = self.cursor.execute("SELECT * FROM `poll_results` WHERE `user_id` = ? AND `poll_id` = ?", (user_id, poll_id,)).fetchone()
            if result:
                #update
                self.cursor.execute("UPDATE `poll_results` SET `data` = ?, `description` = ? WHERE `user_id` = ? AND `poll_id` = ?", (data, description, user_id, poll_id,) ) 
            else:
                #insert
                self.cursor.execute("INSERT INTO `poll_results` (`data`, `description`, `user_id`, `poll_id`) VALUES (?, ?, ?, ?)", (data, description, user_id, poll_id,))
            self.connect.commit()
            # self.print_table('poll_results')
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'set_poll_result: {e.args[0]}')# type: ignore
        finally:
            self.db_stop()  
              
    def add_user(self, user_id, first_name, username, language_code):
        logger.info('DB')  
        try:
            if not self.user_exists(user_id):
                self.db_start()
                self.cursor.execute("INSERT INTO `users` (`user_id`, `first_name`,  `username`, `language_code`) VALUES (?, ?, ?, ?)", (user_id, first_name, username, language_code,))
                self.connect.commit()
                self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'add_user: {e.args[0]}')# type: ignore
        finally:
            self.db_stop()
            
    def del_user(self, user_id):
        logger.info('DB')  
        try:
            if self.user_exists(user_id):
                self.db_start()
                self.cursor.execute("DELETE FROM `users` WHERE `user_id` = ?", (user_id,))
                self.connect.commit()
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'del_user: {e.args[0]}')# type: ignore
        finally:
            self.db_stop()
            
    def change_fmt_state(self, user_id, fsm_state):
        logger.info('DB')  
        try:
            self.db_start()
            self.cursor.execute("UPDATE users SET `fsm_state` = ? WHERE `user_id` = ?", (fsm_state, user_id,))
            self.connect.commit()
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'change_fmt_state: {e.args[0]}')          # type: ignore
        finally:
            self.db_stop()
            
    def set_phone(self, user_id, phone):
        logger.info('DB')  
        try:
            self.db_start()
            self.cursor.execute("UPDATE `users` SET `phone` = ? where `user_id` = ?", (phone, user_id,))
            self.connect.commit()
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'set_phone: {e.args[0]}')           # type: ignore
        finally:
            self.db_stop()
            
    def get_table(self, table_name):
        logger.info('DB')  
        try:
            self.db_start()
            res = self.cursor.execute(f"SELECT * FROM {self.str_clear(table_name)}").fetchall()
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'get_table: {e.args[0]}')# type: ignore
        else:    
            return res       
        finally:
            self.db_stop()
                
    def print_table(self, table_name):
        logger.info('DB')  
        try:
            res = self.get_table(table_name)
            print(f'таблица {table_name}:')
            for item in res: # type: ignore
                print(item)
            print()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'print_table: {e.args[0]}')           # type: ignore
                     
    def registered_user(self, user_id):
        logger.info('DB')  
        try:
            self.db_start()
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ? AND `phone` IS NOT NULL", (user_id,))
            ret = bool(len(result.fetchall()))
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'registered_user: {e.args[0]}')# type: ignore
        else:    
            return ret
        finally:
            self.db_stop()
            
    def get_registered_users(self):
        logger.info('DB')  
        try:
            self.db_start()
            res = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `phone` IS NOT NULL").fetchall()
            ret = [i[0] for i in res]
        except:
            e = sys.exc_info()[1]
            logger.exception(f'get_registered_users: {e.args[0]}')# type: ignore
        else:    
            return ret
        finally:
            self.db_stop() 
               
    def get_poll_results_data(self, poll_id):
        logger.info('DB')  
        try:
            self.db_start()
            res = self.cursor.execute("SELECT `data` FROM `poll_results` WHERE `poll_id` = ?", (poll_id,)).fetchall()
            ret = [i[0] for i in res]
            self.db_stop()
        except:
            e = sys.exc_info()[1]
            logger.exception(f'get_poll_results_data: {e.args[0]}')# type: ignore
        else:    
            return ret
        finally:
            self.db_stop()            
        
bot_db = BotDB(db_path)
