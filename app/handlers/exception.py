from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked, MessageNotModified

from app.common import logger
from app.strings import data_strings

# обработка исключения
# @dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    logger.error(data_strings['lbl']['expt_bot_blocked'].format(update, exception))

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


def register_handlers_exception(dp: Dispatcher):
    dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)
