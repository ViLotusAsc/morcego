import discord
import pygame
import threading
from random import randint
import json
import os
import asyncio 
import discord
import asyncio 
from discord import app_commands
from discord.ext import commands, tasks



variavel_global = ""

lockar = threading.Lock()

with open('client_database.json', 'r') as file:
    data = json.load(file)

def trocar_variavel(texto):
    global variavel_global
    with lockar:
        variavel_global = texto

addorno = False
item_information = []
def willAdd(vaiounao, name, position, number):
    global addorno
    global item_information
    if name == "":
        with lockar:
            item_information = []
    else:
        with lockar:
            addorno = vaiounao
            item_information.append(name)
            item_information.append(position)
            item_information.append(number)


print(data)

def game():
    pygame.init()

    screen = pygame.display.set_mode((348, 520), pygame.RESIZABLE)

    background_foto = pygame.image.load("sprites/79AC/sem título.jpg")
    background_foto = pygame.transform.scale(background_foto, (1180, 620))

    gameplay_area = pygame.image.load("sprites/79AC/gameplay.jpg")
    gameplay_area = pygame.transform.scale(gameplay_area, (348, 520))

    mesa_foto = pygame.image.load("sprites/79AC/mesa.jpg")
    mesa_foto = pygame.transform.scale(mesa_foto, (1180, 620))

    running = True

    inventory = []

    lockar = threading.Lock()
    with open('tsukaDatabase_local.json', 'r') as file:
        data = json.load(file)

    class Button:
        def __init__(self, x, y, x_final, y_final):
            self.x = x
            self.y = y
            self.x_final = x_final
            self.y_final = y_final
            self.ButtonCollision = pygame.Rect((self.x, self.y) ,((self.x_final-self.x), (self.y_final- self.y)))

        def createButton(self):
            self.ButtonCollision = pygame.Rect((self.x, self.y) ,((self.x_final-self.x), (self.y_final- self.y)))

        def printButton(self, color=(0, 0, 0)):
            pygame.draw.rect(screen, (color), self.ButtonCollision)

        def isButtonPressed(self, point):
            if pygame.Rect.collidepoint(self.ButtonCollision, point):
                return True
            else:
                return False

    buttonPlay = Button(521, 209, 859, 265)
    buttonPlay.createButton()

    buttonCredit = Button(521, 279, 859, 335)
    buttonCredit.createButton()

    local = "menu"

    locais_esq = [(351, 427), (468, 427),  (298, 503), (421, 503)]
    locais_dir = [(813, 421), (945, 421), (873, 496), (1023, 497)]

    class Itens:
        def __init__(self):
            self.ladoesq = data["mesaIndivEsq"]
            self.ladodir = data["mesaIndivDir"]

            self.faca_sprite = pygame.image.load("sprites/79AC/knife_artt.png")
            self.faca_sprite = pygame.transform.scale(self.faca_sprite, (45, 45))
            self.faca_x = -100
            self.faca_y = 0

            self.refri_sprite = pygame.image.load("sprites/79AC/cokeartt.png")
            self.refri_sprite = pygame.transform.scale(self.refri_sprite, (50, 50))
            self.refri_x = -100
            self.refri_y = 0

            self.caixa_sprite = pygame.image.load("sprites/79AC/caixinhaart.png")
            self.caixa_sprite = pygame.transform.scale(self.caixa_sprite, (50, 50))
            self.caixa_x = -100
            self.caixa_y = 0

            self.lupa_sprite = pygame.image.load("sprites/79AC/lupaart.png")
            self.lupa_sprite = pygame.transform.scale(self.lupa_sprite, (50, 50))
            self.lupa_x = -100
            self.lupa_y = 0

            self.locais_esq = [(351, 427), (468, 427),  (298, 503), (421, 503)]
            self.locais_esq = [(23, 309), (89, 311), (24, 426), (88, 427)]
            self.locais_dir = [(813, 421), (945, 421), (873, 496), (1023, 497)]
            self.locais_dir = [(215, 310), (282, 307), (215, 427), (282, 427)]

            self.itens_list = ["faca", "lata", "lupa", "caixa"]

            self.inventario = []

            self.itemEscolhido = ""

        def changeItens(self, lado, item, lugar):
            if lado == "dir":
                self.ladodir[f"lugar{lugar}"] = item
            if lado == "esq":
                self.ladoesq[f"lugar{lugar}"] = item

        def saveInformations(self):
            with open("tsukaDatabase_local.json", "w") as file:
                file = json.dump(data, file, indent=4)

        def drawSprites(self, obj, lado, num):
            if len(inventory) < 9:
                if lado == "esq":
                    inventory.append(obj)
                    if obj == "faca":
                        self.itemEscolhido = "faca"
                        self.faca_x = self.locais_esq[num-1][0]
                        self.faca_y = self.locais_esq[num-1][1]
                    if obj == "lata":
                        self.itemEscolhido = "lata"
                        self.refri_x = self.locais_esq[num-1][0]
                        self.refri_y = self.locais_esq[num-1][1]
                    if obj == "caixa":
                        self.caixa_x = self.locais_esq[num-1][0]
                        self.caixa_y = self.locais_esq[num-1][1]
                    if obj == "lupa":
                        self.lupa_x = self.locais_esq[num-1][0]
                        self.lupa_y = self.locais_esq[num-1][1]
                if lado == "dir":
                    inventory.append(obj)
                    if obj == "faca":
                        self.itemEscolhido = "faca"
                        self.faca_x = self.locais_dir[num-1][0]
                        self.faca_y = self.locais_dir[num-1][1]
                    if obj == "lata":
                        self.itemEscolhido = "lata"
                        self.refri_x = self.locais_dir[num-1][0]
                        self.refri_y = self.locais_dir[num-1][1]
                    if obj == "caixa":
                        self.caixa_x = self.locais_dir[num-1][0]
                        self.caixa_y = self.locais_dir[num-1][1]
                    if obj == "lupa":
                        self.lupa_x = self.locais_dir[num-1][0]
                        self.lupa_y = self.locais_dir[num-1][1]
                if lado == "exit":
                    try:
                        inventory.remove(obj)
                    except:
                        pass
                    if obj == "faca":
                        self.faca_x = -100
                    if obj == "lata":
                        self.refri_x = -100
                    if obj == "caixa":
                        self.caixa_x = -100
                    if obj == "lupa":
                        self.lupa_x = -100


    itens = Itens()
    item1 = Itens()
    item2 = Itens()
    item3 = Itens()
    item4 = Itens()
    item5 = Itens()
    item6 = Itens()
    item7 = Itens()

    allitens = [itens, item1, item2, item3, item4, item5, item6, item7]
    def blitAll():
        for item in allitens:
            screen.blit(item.faca_sprite, (item.faca_x, item.faca_y))
            screen.blit(item.refri_sprite, (item.refri_x, item.refri_y))
            screen.blit(item.caixa_sprite, (item.caixa_x, item.caixa_y))
            screen.blit(item.lupa_sprite, (item.lupa_x, item.lupa_y))

    while running:
        if local == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        print(background_foto.get_size())
                    if event.type == pygame.K_a:
                            pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                    darPlay = buttonPlay.isButtonPressed
                    if darPlay:
                        local = "jogo"
            screen.blit(background_foto, (100, 20))
            pygame.display.update()

        if local == "jogo":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        itens.drawSprites("lata", "exit", 3)
                    if event.key == pygame.K_q:
                        print(f"Inventário: {inventory}")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                    print(f"--- X: {itens.faca_x}\n--- Y: {itens.faca_y}")
                    print(gameplay_area.get_size())
            

            screen.blit(mesa_foto, (100, 20))
            screen.blit(gameplay_area, (0, 0))
            blitAll()
            #screen.blit(gameplay_area, (0, 0))
            pygame.display.update()


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
        if message.content.startswith("++"):
            mensagem = message.content.split()
            name = mensagem[1]
            posic = mensagem[2]
            nnumber = mensagem[3]
            loading_gun_message = discord.Embed(title="Começando o Jogo...", colour=0xFF5733, description="https://media1.tenor.com/m/fDakhj-iKdEAAAAC/aesthetic-anime.gif")
            await message.channel.send(embed=loading_gun_message)

            

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

    @client.event
    async def on_message(message):
        if message.content.startswith(",battle"):
            mensagem = (message.content).split()
            conta = mensagem[-1]
            await message.channel.send("Ei")
            conta1 = await client.fetch_user(conta)
            await conta1.send("ayo")

    @client.command()
    async def battle(ctx):
        await ctx.send("ayo")


    token="OTAzMDkzOTU2ODIzMzY3Njgw.GHwJ5S.n-CR2hDp7556hitoK22jpaOpuqFGCKFGBJZ7Nw"
    client.run(token)


if __name__ == "__main__":
    t1 = threading.Thread(target=game)
    t2 = threading.Thread(target=bot)
    t3 = threading.Thread(target=bot2)
    t2.start()
    #sleep(20)
    t1.start()
    t3.start()

    t2.join()
    t1.join()
    #t3.join()