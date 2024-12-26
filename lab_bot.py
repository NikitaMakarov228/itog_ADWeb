from aiogram.utils import executor
from create_bot import dp
from funcs.middleware import ThrottlingMiddleware


async def on_sturtup(_):
    print("Бот вышел в онлайн!")


from handler import register_handlers_client

register_handlers_client(dp)
dp.middleware.setup(ThrottlingMiddleware())
executor.start_polling(dp, skip_updates=True, on_startup=on_sturtup)
