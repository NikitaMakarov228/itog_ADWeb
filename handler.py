from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from funcs.wiki_get import fetch_wikipedia_article
from funcs.model import summarize_large_text
from funcs.get_groups import search_vk_groups
from funcs.translation import translate_word


class Msg(StatesGroup):
    msg_text = State()


@dp.message_handler(commands=["start"], state=None)
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(
        user_id,
        "Здравствуйте, я бот, который поможет вам получить краткую информацию из статьи на Wikipedia.\nОтправье мне название статьи(на русском или английском), и я отправлю вам необходимую информацию!",
    )
    await Msg.msg_text.set()


@dp.message_handler(commands=["new"], state=None)
async def generate_new(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(
        user_id,
        "Отправь мне тему!",
    )
    await Msg.msg_text.set()


@dp.message_handler(content_types=["msg_text"], state=Msg.msg_text)
async def getMessage(message: types.Message, state: FSMContext):
    msg = await bot.send_message(message.from_user.id, "Получение статьи...")
    user_id = message.from_user.id
    wiki_data = fetch_wikipedia_article(message.text)
    if type(wiki_data) is str:
        await bot.send_message(user_id, wiki_data)
        await state.finish()
    else:

        async def progress_callback(current, total):
            await bot.edit_message_text(
                text=f"Обработка: {round(current*100/total,1)}%",
                chat_id=msg.chat.id,
                message_id=msg.message_id,
            )

        summarized_text = await summarize_large_text(
            wiki_data["text"], progress_callback=progress_callback
        )
        summarized_text = translate_word(summarized_text, src_lang="en", dest_lang="ru")
        title = translate_word(wiki_data["title"], src_lang="en", dest_lang="ru")
        groups = search_vk_groups(title)
        text = f"\t<b>{title}</b>\n\n{summarized_text}\n\n<b>Источник:</b> {wiki_data['link']}\n\n"
        if groups:
            text += "Крупные сообщества по этой теме:\n"
            for group in groups:
                text += f"- {group[0]}: {group[1]}\n"
        await bot.edit_message_text(
            text=text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="HTML"
        )
        await state.finish()


def register_handlers_client(dp):
    dp.register_message_handler(process_start_command, commands=["start"])
    dp.register_message_handler(generate_new, commands=["new"])
    dp.register_message_handler(getMessage, state=Msg.msg_text)
