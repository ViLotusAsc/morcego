import discord
import threading

import asyncio 
from discord import app_commands
from discord.ext import commands, tasks
import json

variavel_global = ""

lockar = threading.Lock()

with open('client_database.json', 'r') as file:
    data = json.load(file)

def trocar_variavel(texto):
    global variavel_global
    with lockar:
        variavel_global = texto

send_save = False

def sendsave(yorn):
    global send_save
    with lockar:
        send_save = yorn


def bot():
    intents = discord.Intents.default()
    intents.message_content = True

    client=commands.Bot(command_prefix=".", intents=discord.Intents.all())

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='Filme'))


    class Buttons(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="Button SIM",style=discord.ButtonStyle.green)
        async def blurple_button(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.edit_message(content=f"just edit this message..\nDESAFIO ACEITO!",view=self)
            print('Pressionado!')

    @client.event
    async def on_message(message):
        if message.content.startswith("ei"):
            await message.channel.send("Ei")

    @client.command()
    async def battle(ctx, user):
        await ctx.send("Você quer batalhar?",view=Buttons())
        user_profile = await client.fetch_user(user)
        await ctx.send(",battle")

    @client.command()
    async def dm(ctx, person):
        perfil = await client.fetch_user(person)
        print(person)
        print(type(person))
        try:
            await perfil.send(".dm 629071779138240523")
        except Exception as e:
            await ctx.send(e)

    @client.command()
    async def login(ctx, nome):
        await ctx.send(f"Login feito!")
        data["contas"][nome] = {
            "token": "xxxxxx", 
            "dinheiro": 0, 
            "bot": {
                "nome_bot": "Default", 
                "forca": 10, 
                "vida": 100, 
                "ataques": {
                    "ata1": "default1", 
                    "ata2": "default2"
                }
            }
        }
        with open('client_database.json', 'w') as file:
            file = json.dump(data, file, indent=4)
        user = client.get_user("629071779138240523")
        await user.send("uiui")

        
    token="OTAzMDkzOTU2ODIzMzY3Njgw.GyJXAu.DcqK4xsv_7X8QamkdsgLLSgnzd7veJXi5toVhk"
    client.run(token)

def bot2():
    intents = discord.Intents.default()
    intents.message_content = True

    client=commands.Bot(command_prefix=",", intents=discord.Intents.all())

    @client.command()
    async def battle(ctx):
        ctx.send("ayo")


    token="OTAzMDkzOTU2ODIzMzY3Njgw.GHwJ5S.n-CR2hDp7556hitoK22jpaOpuqFGCKFGBJZ7Nw"
    client.run(token)
bot()