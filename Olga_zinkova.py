import datetime
import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
import Bad_words

"""Время бана участника за частое употребление матов"""
delta = datetime.timedelta(days=0,
                           seconds=0,
                           microseconds=0,
                           milliseconds=0,
                           minutes=0,
                           hours=1,
                           weeks=0)

"""Токен бота с которым мы работаем"""
TOKEN = "MTE3ODUzMzUxMjY5ODEzNDYwOQ.GiPZzI.sWgvCKAQUGb75dbKs9cDG0SyihW7Q9eCexVjV0"
kick_list = 0
banword_list = 0
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="")


@bot.event
async def on_ready():
    print(f"Бот зашел на сервер как {bot.user.name}")


@bot.event
async def on_message(message):
    global kick_list, banword_list
    msg = message.content
    print(f"{message.author} написал: {msg}")
    for i in Bad_words.words_list:
        print(fuzz.WRatio(i, msg))
        if fuzz.WRatio(i, msg) >= 90 or fuzz.partial_ratio(i, msg) >= 90 or i in msg:
            kick_list += 1
            print(kick_list)
            print(i)
            await message.delete()

        member = message.author
        if kick_list > 5 and message.author.mention != bot.user.mention and banword_list == 0:
            await message.channel.send(embed = discord.Embed(description=f"{member.mention}, если ты продолжишь писать сообщения с матами, я тебя замьючу на {delta}!"))
            banword_list += 1
            kick_list = 0
        elif kick_list > 5 and message.author.mention != bot.user.mention and banword_list == 1:
            reason = f"Употреблено слишком много сообщений с матами: {kick_list}"
            if message.author.guild_permissions.administrator and message.author != bot.user.name:
                await message.channel.send(embed = discord.Embed(description=f"Не могу замьютить {member.mention}, так как он(а) является администратором"))
                banword_list = 0
                kick_list = 0
                pass
            else:
                await member.timeout(delta)
                await message.channel.send(embed = discord.Embed(description=f"Пользователь {member.mention} был замьючен за: {reason}"))
                banword_list = 0
                kick_list = 0



"""Запуск бота"""
bot.run(TOKEN)