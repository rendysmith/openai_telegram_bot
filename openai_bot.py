import openai
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import configparser
import os

config = configparser.ConfigParser()
path_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.ini"))
config.read(path_db)

token_bot = config.get('bot', 'token_bot')
name_bot = config.get('bot', 'name_bot')

bot = Bot(token=token_bot)
dp = Dispatcher(bot)

async def get_txt(prompt: str):
    token = config.get('bot', 'token')
    openai.api_key = token
    model = config.get('bot', 'model')
    max_tokens = int(config.get('bot', 'max_tokens'))
    temperature = float(config.get('bot', 'temperature'))

    completion = await openai.Completion.acreate(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    txt = completion.choices[0].text
    return txt



# async def get_txt(prompt: str):
#     openai.api_key = token
#     model = 'text-davinci-003'
#     max_tokens = 3000
#
#     async with openai.AsyncClient() as client:
#         completion = await client.Completion.create(
#             engine=model,
#             prompt=prompt,
#             max_tokens=max_tokens,
#             temperature=0
#         )
#         txt = completion.choices[0].text
#         return txt



@dp.message_handler(commands="start")
async def start(message: types.Message):
    user = message.chat.first_name
    txt = f'''Привет, {user}!
Этот бот создан для большой и дружной семьи.
Задавай умные вопросы, получай умные ответы.'''
    await message.answer(txt)

@dp.message_handler()
async def echo_message(message: types.Message):
    answer = await get_txt(message.text)
    # В переменной msg.text
    # содержится текст сообщения
    await message.answer(answer)

if __name__ == "__main__":
    #Запуск бота
    executor.start_polling(dp, skip_updates=True)
