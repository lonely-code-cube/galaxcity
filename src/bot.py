from dis import disco
import time

import random
import colorlog, logging

import discord
from discord.ext import commands, tasks

from database.database import Database, Utils
from config.config import BOT_LOG_LEVEL as BOTL, LOG_LEVEL, _MONGO_URI, TOKEN

logging.addLevelName(BOTL, "BOT")
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s(%(name)s) %(levelname)s:%(reset)s%(cyan)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "BOT": "purple",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
    )
)
logger = colorlog.getLogger()
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)

cogs = ["story", "controls", "info", "credits", "help", "guild"]
loaded_cogs = []
bot = commands.Bot(
    command_prefix="g!", intents=discord.Intents.all(), status=discord.Status.online
)
bot.remove_command("help")


def connect_db():
    bot.database = Database(_MONGO_URI)
    logger.log(BOTL, "Connected with database")


def set_theme():
    bot.primary_theme = 0xD82CE8
    bot.fail = 0xE8452C
    bot.success = 0x1FDD48
    logger.log(BOTL, "Configured bot themes")


bot.starttime = int(time.time())
for i in cogs:
    bot.load_extension(f"cogs.{i}")
    loaded_cogs.append(i)


@bot.event
async def on_ready():
    logger.log(BOTL, "Logged in as: {0}".format(bot.user))
    connect_db()
    set_theme()
    for i in loaded_cogs:
        logger.log(BOTL, f"{i}.py is Loaded!")
    await change_activity.start()

@bot.event
async def on_message(message: discord.Message):
    if bot.user.mentioned_in(message):
        await message.channel.send("The prefix is g!")
    await bot.process_commands(message)

def is_owner():
    def predicate(ctx):
        if ctx.author.id in (823588482273902672, 748053138354864229):
            return True
        return False

    return commands.check(predicate)


@bot.check
async def check_user_in_db(ctx):
    user = await bot.database.fetch_user(ctx.author.id)
    if not user:
        await bot.database.init_user(Utils.create_user(ctx.author.id))
    return True


@bot.command(name="ping", help="Return's Bot Latency.")
async def ping(ctx):
    await ctx.reply(
        embed=discord.Embed(
            title="Pong!",
            description=f"{round(bot.latency * 1000)}ms",
            color=bot.primary_theme,
        )
    )


@bot.group(name="cog", help="Cog Based Commands", invoke_without_command=True)
@is_owner()
async def cog(ctx):
    await ctx.reply(
        embed=discord.Embed(color=discord.Color.green(), description=loaded_cogs)
    )


@cog.command(aliases=["ul"], name="unload", help="Unload cogs")
@is_owner()
async def unload(ctx, *, cogss: str = None):
    if not cogss:
        for i in cogs:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Unloaded {i}.py", color=discord.Color.green()
                    )
                )
    else:
        cogl = cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Unloaded {i}.py", color=discord.Color.green()
                    )
                )


@cog.command(aliases=["l"], name="load", help="Load cogs")
@is_owner()
async def load(ctx, *, cogss: str = None):
    if not cogss:
        for i in cogs:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Loaded {i}.py", color=discord.Color.green()
                    )
                )
    else:
        cogl = cogss.split(", ")
        for i in cogl:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Loaded {i}.py", color=discord.Color.green()
                    )
                )


@cog.command(aliases=["rl"], name="reload", help="Reload cogs")
@is_owner()
async def reload(ctx, *, cogss: str = None):
    if not cogss:
        for i in loaded_cogs:
            bot.reload_extension(f"cogs.{i}")
            await ctx.send(
                embed=discord.Embed(
                    description=f"Reloaded {i}.py", color=discord.Color.green()
                )
            )
    else:
        cogl = cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.reload_extension(f"cogs.{i}")
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Reloaded {i}.py", color=discord.Color.green()
                    )
                )


@bot.command(name="set")
@is_owner()
async def set(ctx, user: discord.User, level: int):
    user = await bot.database.fetch_user(user.id)
    user.level = level
    await bot.database.update_user(user)
    await ctx.send(embed=discord.Embed(title=f"Set your level to {level}"))


@bot.command(name="uptime", help="Show's bot uptime.", aliases=["ut"])
async def uptime(ctx):
    await ctx.reply(
        embed=discord.Embed(
            description="Bot is online since: <t:{0}:F> (<t:{0}:R>)".format(
                bot.starttime
            ),
            color=discord.Color.green(),
        )
    )


@tasks.loop(minutes=1)
async def change_activity():
    status = [
        "Galaxy",
        "moons",
        "stars",
        "Conch Shell",
        "first prize!!!",
        "my Develpoers",
        "Swastik's girlfriend",
        "ASMR",
        "sunset",
        "sunrise",
        "space",
        "humans at Mars",
        "location of ISS",
        "Martians",
    ]
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=random.choice(status)
        )
    )


def get_token():
    token = TOKEN
    if not token:
        logger.critical("TOKEN environment variable not set")
        exit(1)
    return token


bot.run(get_token())
