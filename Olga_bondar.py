import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
import datetime


"""Токен бота с которым мы работаем"""
TOKEN = "MTE3ODUzMzQyMTE0MDY3NjYwOA.GV-t1K.52NzHuawrxK7yuUW9lR7pMYDRPVhzEmUF8FORM"
PREFIX = "!"
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Бот зашел на сервер как {bot.user.name}")


@bot.command( pass_context = True)
@commands.has_permissions( administrator = True)
async def clear(ctx, ammount = 20):
    if ammount < 100:
        await ctx.channel.purge(limit = ammount + 1)
        print(f"Chat has been cleared by {ctx.message.author} for {ammount} messages")
    else:
        await ctx.channel.send("Слишком большое число")



@bot.command( pass_context = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    author = ctx.message.author
    if not author.guild_permissions.administrator:
        embed = discord.Embed(
            title = 'Kick ❌',
            description = f'Нельзя кикнуть человека без прав администратора',
            colour = discord.Colour.from_rgb(171, 0, 0)
            )
        await ctx.send(embed=embed)

    elif member.mention == author.mention:
        embed = discord.Embed(
            title = 'Kick ❌',
            description = f'Нельзя кикнуть самого себя',
            colour = discord.Colour.from_rgb(171, 0, 0)
            )
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title = 'Kick ✅',
            description = f'**{member.mention}**  успешно  кикнут',
            colour = discord.Colour.from_rgb(0, 189, 0)
            )
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

@bot.command( pass_context = True)
async def ban(ctx, member: discord.Member, *, reason : str = None):
    author = ctx.message.author
    if not author.guild_permissions.administrator:
        embed = discord.Embed(
            title = 'Ban ❌',
            description = f'Нельзя забанить человека без прав администратора',
            colour = discord.Colour.from_rgb(171, 0, 0)
            )
        await ctx.send(embed=embed)

    elif member.mention == author.mention:
        embed = discord.Embed(
            title = 'Ban ❌',
            description = f'Нельзя забанить самого себя',
            colour = discord.Colour.from_rgb(171, 0, 0)
            )
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title = 'Ban ✅',
            description = f'**{member.mention}**  успешно  забанен',
            colour = discord.Colour.from_rgb(0, 189, 0)
            )
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

@bot.command(name='mute', description='Поставить пользователя на таймаут прям сейчас в этом канале')
@commands.has_permissions( administrator = True)
async def mute(ctx, user: discord.Member,  duration: any = 5, reason : str = "Просто мут"):

    if isinstance(duration, int) and isinstance(user, discord.Member):
        time = datetime.timedelta(minutes=duration)
        await ctx.channel.set_permissions(user, send_messages=False, reason=f"Таймаут на {duration} минут")
        await user.timeout(time)
        embed = discord.Embed(
            title = 'Mute ✅',
            description = f'**{user.mention}**  успешно  замучен  на  **{int(duration)} минут** за {reason}',
            colour = discord.Colour.from_rgb(0, 189, 0)
            )
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)

    elif isinstance(user, discord.Member) and not isinstance(duration, int) :
        embed = discord.Embed(
                title = 'Mute ❌',
                description = f'{ctx.message.author.mention}  Напишите только число минут',
                colour = discord.Colour.from_rgb(171, 0, 0)
            )
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)

    elif not isinstance(user, discord.Member) or user is None:
        embed = discord.Embed(
            title = 'Mute ❌',
            description = f'{ctx.message.author.mention}  укажите  кого  нужно  наказать',
            colour = discord.Colour.from_rgb(171, 0, 0)
        )
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)

@bot.command( pass_context = True)
async def top_of_games(ctx, data: any = 1):
    if isinstance(data, int):
        data = int(data)
        if data < 12:
            url = f"https://kuplinov-play.games/top-250/page/{data}/"
            request = requests.get(url)
            html = bs(request.text, "lxml")

            data = html.find_all('article',  class_="short expand-link anim")
            await ctx.channel.send(f"Топ игр с сайта: kuplinov-play.games")
            print(request)
            games = " "
            for z in data:
                game_text = z.find("h3")
                games += f'\n{game_text.text}'
                print(games)
            await ctx.channel.send(games)
        else:
            await ctx.channel.send("Не существует такой страницы")
    else:
        await ctx.channel.send("Это не число")


intents = discord.Intents.default()
intents.message_content = True


bot.run(TOKEN)
