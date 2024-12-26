from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from transformers import pipeline
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
OURTOKEN = "7758746654:AAGx5NA63qKeiLgUSkyQqroflPHA7mdmgog"
bot = Bot(token=OURTOKEN)
dp = Dispatcher(bot, storage=storage)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
