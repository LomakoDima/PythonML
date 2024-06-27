import discord
from config import *
from discord.ext import commands
import re, json, os, random, requests, datetime, calendar

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

USER_DATA_FILE = os.path.join(DATA_DIR, "registered_users.json")

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}


def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


registered_users = load_user_data()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="уничтожение мира)"))
    print(f'We have logged in as {bot.user}')


@bot.command(name='start')
async def start(ctx):
    await ctx.send(f"Привет, {ctx.author.mention}! Добро пожаловать на сервер!")


@bot.command(name='helps')
async def helps(ctx):
    embed = discord.Embed(title="Команды бота", description="Список доступных команд:")
    embed.add_field(name="!register <email> <password>", value="Регистрация нового пользователя.")
    embed.add_field(name="!registered", value="Показать зарегистрированную информацию.")
    embed.add_field(name="!hello", value="Приветствие на сервере.")
    embed.add_field(name="!image", value="Отправить случайное изображение из папки images.")
    embed.add_field(name="!randomimage", value="Отправить случайную гифку c щенятами.")
    embed.add_field(name="!recycle <name>", value="Скажет о том как утилизировать мусор.")
    embed.add_field(name="!clr", value="Покажет календарь на текущий месяц.")
    await ctx.send(embed=embed)

@bot.command(name='recycle')
async def recycle(ctx, *, item: str):
    item = item.lower()
    if item in recycle_info:
        response = recycle_info[item]
    else:
        response = f'Извините, информации об утилизации {item} нет.'
    await ctx.send(response)


@bot.command(name='clr')
async def clr(ctx):
    now = datetime.datetime.now()
    month = now.month
    year = now.year

    cal = calendar.month(year, month)

    await ctx.send(f"Вот календарь на {calendar.month_name[month]} {year}:\n```{cal}```")


@bot.command(name='register')
async def register(ctx, email: str, password: str):
    user_id = str(ctx.author.id)

    if not email_regex.match(email):
        await ctx.send(f"{ctx.author.mention}, пожалуйста, введите корректный email адрес.")
        return

    if user_id in registered_users:
        await ctx.send(f"{ctx.author.mention}, вы уже зарегистрированы с email {registered_users[user_id]['email']}.")
    else:
        registered_users[user_id] = {"email": email, "password": password}
        save_user_data(registered_users)
        await ctx.send(f"{ctx.author.mention}, вы успешно зарегистрированы с email {email}.")


@bot.command(name='registered')
async def registered(ctx):
    user_id = str(ctx.author.id)
    if user_id in registered_users:
        email = registered_users[user_id]["email"]
        await ctx.send(f"{ctx.author.mention}, ваш зарегистрированный email: {email}.")
    else:
        await ctx.send(
            f"{ctx.author.mention}, вы еще не зарегистрированы. Используйте команду !register <email> <password> для "
            f"регистрации.")


def get_duck_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('randomimage')
async def randomimage(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)


@bot.command(name='image')
async def image(ctx):
    if os.path.exists(IMAGES_DIR):
        images = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]
        if images:
            random_image = random.choice(images)
            image_path = os.path.join(IMAGES_DIR, random_image)
            await ctx.send(file=discord.File(image_path))
        else:
            await ctx.send("В папке нет изображений.")
    else:
        await ctx.send("Папка с изображениями не найдена.")


bot.run(botTOKEN)
