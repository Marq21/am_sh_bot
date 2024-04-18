import asyncio
import logging

from aiogram import Bot, Dispatcher

log = logging.getLogger(__name__)


async def main():
    log.info("Creating bot")
    bot = Bot(token="TOKEN")
    dp = Dispatcher()

    # dp.include_router(*some_router*)
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        filename="logs.log"
    )
    asyncio.run(main())
