Бот для музыкальной группы

Задачи:

    отображение:
        - информации о группе
        - расписания

    голосование с просмотром результатов на карте

Функционал:

    пользователь:
    - вывод информации о боте
    - вывод информации о группе
    - вывод расписания выступлений группы
    - вывод ссылки на добровольное пожертвование
    - регистрация пользователя (для будущих фич)
    - голосование за конкретный адрес
    - просмотр карты с отметками все адресов за которые проголосовали
    
    админ:
    - изменение информации, выводимой пользователю во всех пунктах:
    - изменение названия голосования
    - изменение id голосования в базе данных
    - очистка данных голосования

Структура:

    bot.py - точка входа

    app/common.py               общие объекты
    app/config.py               файл конфигурации
    app/keyboards.py            клавиатуры
    app/map_api.py              реализация map api
    app/strings.json            строковые данные
    app/strings.py              загрузка строковых данных из strings.json в соответствующие структуры
    
    app/db/bot_db.py            реализация работы с базой данных
    app/db/clear_base.db        чистая база данных
    app/db/create_db.sql        скрипт создания структуры базы данных

    app/handlers/admin_cmd.py   команды админа и их логика, принимаемые ботом
    app/handlers/common_cmd.py  общие команды и их логика, принимаемые ботом
    app/handlers/exception.py   обработка исключений

    app/polls  содержит папки с настройками голосований, каждая папка соответствует одному голосованию
    app/polls/poll_name по имени папки осуществляется доступ к соответствующим данным

    app/polls/poll_name/poll_handlers.py    команды данного голосования и их логика
    app/polls/poll_name/poll_strings.json   строковые данные данного голосования

Переменные окружения:

    telegram_bot_token = ''
    telegram_admin_ids = '111111111,222222222'
    MAP_API_TOKEN = ''
    sqlite_db_name = 'clear_base.db'
