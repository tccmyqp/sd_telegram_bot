import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    
DEBAG_db = False
DEBUG_map_api = False
DEBUG_functions = False

token = os.environ.get('telegram_bot_token') # telegram bot token
admin_ids = os.environ.get('telegram_admin_ids') # [111111111, 222222222]
MAP_API_TOKEN = os.environ.get('MAP_API_TOKEN') # yandex map api tiken
db_name = os.environ.get('sqlite_db_name') # 'clear_base.db', 'work_base.db'

WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST') # ngrok, внешний ip
WEBHOOK_PORT = os.environ.get('WEBHOOK_PORT') # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = os.environ.get('WEBHOOK_LISTEN') # 127.0.0.1
WEBHOOK_SSL_CERT = os.environ.get('WEBHOOK_SSL_CERT') # Путь к сертификату
WEBHOOK_SSL_PRIV = os.environ.get('WEBHOOK_SSL_PRIV') # Путь к приватному ключу


dir_path = Path.cwd()

sql_create_name = 'create_db.sql'

# db_path = Path("app", "db", db_name)
# abs_db_path = Path(dir_path, db_path)

sql_create_path = Path( "app", "db", "create_db.sql")
# abs_sql_create_path = Path(dir_path, "app", "db", "create_db.sql")
