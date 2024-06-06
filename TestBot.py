import discord
import calendar
from config import *
from datetime import datetime
import string
import secrets
import random

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    activity = discord.Game(name="programming")
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)

    if message.content.startswith('!start'):
        await message.channel.send("Приветствуем тебя! Чтобы использовать бота в дальнейшим, тебе надо "
                                   "зарегистрироваться. Чтобы зарегистрироваться воспользуйся командой !signup")
    if message.content.startswith('!register'):
        try:
            _, username, email, password = message.content.split()
            register_user(username, email, password)
            await message.channel.send(f'User {username} registered successfully!')
        except ValueError:
            await message.channel.send('Usage: !register <username> <email> <password>')
    elif message.content.startswith('!smile'):
        await message.channel.send(gen_emoji())
    elif message.content.startswith('!coin'):
        await message.channel.send(flip_coin())
    elif message.content.startswith('!pass'):
        await message.channel.send(gen_pass(10))
    elif message.content.startswith(('!users', '!calendar', '!generatepassword', '!smile')):
        if not is_registered(username):
            await message.channel.send(
                'You must be registered to use this command. Use !register <username> <email> <password> to register.')
            return
    elif message.content.startswith('!bye'):
        await message.channel.send("Bye!")
    elif message.content == '!users':
        try:
            with open('users.txt', 'r') as file:
                users = file.read()
            if users:
                await message.channel.send(f'Registered users:\n{users}')
            else:
                await message.channel.send('No registered users.')
        except FileNotFoundError:
            await message.channel.send('No registered users.')
    elif message.content == '!calendar':
        calendar_text = get_current_month_calendar()
        await message.channel.send(f'```\n{calendar_text}\n```')

    else:
        await message.channel.send(message.content)


def register_user(username, email, password):
    with open('users.txt', 'a') as file:
        file.write('\nТут хранятся ваши данные.\n')
        file.write(f'Имя: {username}\n')
        file.write(f'Почта: {email}\n')
        file.write(f'Пароль: {password}\n')


def is_registered(username):
    return username in registered_users


#def generate_password(length=12):
#    alphabet = string.ascii_letters + string.digits + string.punctuation
#    password = ''.join(secrets.choice(alphabet) for _ in range(length))
#    return password




client.run(botTOKEN)
