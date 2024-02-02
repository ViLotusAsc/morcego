import discord
import pygame
import threading
from random import randint
import json
import os
import asyncio 
from discord import app_commands
from discord.ext import commands, tasks
import ctypes
from ctypes import wintypes 
from random import choice



variavel_global = ""

lockar = threading.Lock()

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


with open("tsukaLife_share.json", 'r') as file:
    data_life = json.load(file)

class DataChange:
    def __init__(self) -> None:
        pass

    def change_life(self, value):
        data_life['player1']['vida'] = value
        with open("tsukaLife_share.json", "w") as file:
            json.dump(data_life, file, indent=4)


def game():
    pygame.init()

    screen = pygame.display.set_mode((348, 520), pygame.RESIZABLE)
    pygame.display.set_caption("79")
    pygame.display.set_icon(pygame.image.load("sprites/79AC/refriart.png"))

    hwnd = pygame.display.get_wm_info()['window']
        
    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
    user32.SetWindowPos(hwnd, -1, 600, 300, 0, 0, 0x0001)

    background_foto = pygame.image.load("sprites/79AC/menuplay.jpg")
    background_foto = pygame.transform.scale(background_foto, (348, 520))

    gameplay_area = pygame.image.load("sprites/79AC/image_inventory_gameplay.jpg")
    gameplay_area = pygame.transform.scale(gameplay_area, (348, 520))

    area = [(19, 236), (93, 236), (17, 323), (19, 420)]


    running = True

    inventory = data_life["player1"]["inventory"]
    itens_listt = ["faca", "lata", "lupa", "caixa"]

    lockar = threading.Lock()

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

    counter_embaralho = 0

    buttonPlay = Button(122, 242, 238, 270)
    buttonPlay.createButton()

    buttonCredit = Button(521, 279, 859, 335)
    buttonCredit.createButton()

    local = "menu"

    locais_esq = [(351, 427), (468, 427),  (298, 503), (421, 503)]
    locais_dir = [(813, 421), (945, 421), (873, 496), (1023, 497)]

    class Itens:
        def __init__(self):

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
            self.locais_esq = [(19, 236), (93, 236), (24, 426), (88, 427)]
            self.locais_dir = [(813, 421), (945, 421), (873, 496), (1023, 497)]
            self.locais_dir = [(17, 323), (19, 420), (215, 427), (282, 427)]

            self.itens_list = ["faca", "lata", "lupa", "caixa"]

            self.inventario = []

            self.itemEscolhido = ""

        def changeItens(self, lado, item, lugar):
            if lado == "dir":
                self.ladodir[f"lugar{lugar}"] = item
            if lado == "esq":
                self.ladoesq[f"lugar{lugar}"] = item

        def drawSprites(self, obj, lado, num, f=counter_embaralho):
            if obj != "none":
                if lado == "esq":
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
                    self.faca_x = -100
                    self.refri_x = -100
                    self.caixa_x = -100
                    self.lupa_x = -100
            else:
                self.faca_x = -100
                self.refri_x = -100
                self.caixa_x = -100
                self.lupa_x = -99999


    class DisplayText:
        def __init__(self, texto, tamanho, lugar, fonte="Arial"):
            self.texto = texto
            self.tamanho = tamanho
            self.lugar = lugar
            self.fonte = pygame.font.SysFont(fonte, self.tamanho)
            self.text_form = (self.fonte).render(self.texto, True, (0, 0, 0))
        
        def writeText(self):
            screen.blit(self.text_form, self.lugar)

        def change_life(self, value):
            data_life['player1']['vida'] = value
            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)

    changeData = DataChange()


    if True:
        itens = Itens()
        item1 = Itens()
        item2 = Itens()
        item3 = Itens()
        item4 = Itens()
        item5 = Itens()
        item6 = Itens()
        item7 = Itens()


    allitens = [itens, item1, item2, item3, item4, item5, item6, item7]
    itens_esq = [item4, item5, item6, item7]
    itens_dir = [itens, item1, item2, item3]
    def blitAll():
        for item in allitens:
            screen.blit(item.faca_sprite, (item.faca_x, item.faca_y))
            screen.blit(item.refri_sprite, (item.refri_x, item.refri_y))
            screen.blit(item.caixa_sprite, (item.caixa_x, item.caixa_y))
            screen.blit(item.lupa_sprite, (item.lupa_x, item.lupa_y))


    def chooseItens_Right():
        for i in range(0, 2):
            inventory[i] = choice(itens_listt)

    def chooseItens_Left():
        for i in range(2, 4):
            inventory[i] = choice(itens_listt)


    while running:
        inventory = data_life["player1"]["inventory"]
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
                    darPlay = buttonPlay.isButtonPressed(event.pos)
                    if darPlay:
                        local = "jogo"
            screen.blit(background_foto, (0, 0))
            pygame.display.update()

        if local == "jogo":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        itens.drawSprites("lata", "exit", 3)
                        item2.drawSprites("faca", "dir", 1)
                    if event.key == pygame.K_q:
                        print(f"Inventário: {inventory}")
                        changeData.change_life(10)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(inventory)
                    print(event.pos)

            screen.blit(gameplay_area, (0, 0))
            life_text = DisplayText(str(data_life['player1']['vida']), 20, (241, 249))
            money_text = DisplayText(str(data_life['player1']['money']), 20, (50, 191))

            if data_life["player1"]["shuffle"] == True:
                chooseItens_Right()
                chooseItens_Left()
                itens.drawSprites(inventory[0], "exit", 1)
                item1.drawSprites(inventory[1], "exit", 2)
                item4.drawSprites(inventory[2], "exit", 1)
                item5.drawSprites(inventory[3], "exit", 2)

                data_life["player1"]["shuffle"] = False
                with open("tsukaLife_share.json", "w") as file:
                    json.dump(data_life, file, indent=4)


            itens.drawSprites(inventory[0], "esq", 1)
            item1.drawSprites(inventory[1], "esq", 2)
            item4.drawSprites(inventory[2], "dir", 1)
            item5.drawSprites(inventory[3], "dir", 2)
            blitAll()
            life_text.writeText()
            money_text.writeText()
            pygame.display.update()

def bot():

    changeable = DataChange()
    intents = discord.Intents.default()
    intents.message_content = True 

    client=commands.Bot(command_prefix=".", intents=discord.Intents.all())
    default_channel = 0

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='Filme'))

    
    embed_tut_1 = discord.Embed(title="Tutorial", color=0xFF5733, description="**A mecânica do jogo:**\nInicialmente se tem uma carga de 6 munições em uma arma, podendo cada bala ser verdadeira ou falsa. Inicialmente falaremos quantas balas falsas e verdadeiras se tem no jogo.")
    embed_tut_1.set_image(url="https://media1.tenor.com/m/ehctjEyMI9MAAAAC/anime-gun.gif")
    embed_tutorial = discord.Embed(title="Quer começar o tutorial?", colour=0xFF5733, description="Se deseja começar o tutorial para entender o funcionamento do jogo, clique no botão verde.")
    embed_tutorial.set_image(url="https://media1.tenor.com/m/irauQe8qvU0AAAAC/anime-study.gif")
    embed_mecanica = discord.Embed(title="Rodadas", color=0xFF5733,description="""*Você e seu oponente devem digitar a ação correspondente nos devidos turnos. Cada um terá sua vez e poderá fazer três escolhas:* \n\n**1 -** *Usar itens*\n**2 -** *Atirar em si mesmo*\n**3 -** *Atirar no oponente*""")
    embed_mecanica.set_image(url="https://media1.tenor.com/m/ANfWGCi3gV0AAAAC/majima-lycoris-recoil.gif")
    embed_atir_sims = discord.Embed(title="**Atirando em Si Mesmo**", color=0xFF5733, description="""**comando:** dSelf / sSelf\n\n*Ao fazer isso, você coloca a sua cabeça à probabilidade da bala ser ou não verdadeira. Caso seja verdadeira, você perde uma vida, caso contrário, você ganha uma rodada e pode jogar novamente*""")
    embed_atir_sims.set_image(url="https://media1.tenor.com/m/20YFPIkutx0AAAAC/anime.gif")
    embed_atir_outr = discord.Embed(title="Atirando no Outro", color=0xFF5733, description="""\n\n**comando:** dShoot / sShoot\n\n*Ao escolher atirar no oponente, você possui a chance de tirar uma vida dele. Simples.*""")
    embed_atir_outr.set_image(url="https://media1.tenor.com/m/te4hePHUrV4AAAAC/anime-gun.gif")
    embed_useitem = discord.Embed(title="**Usando Item**", color=0xFF5733,description="""**comando:** *dUse item / sUse item*\n\n*Nesta situação você pode utilizar diversos itens para ajudar sua estratégia. Cada item possui um efeito diferente e pode ser utilizado a qualquer momento em uma rodada livre (utilizar itens não consome nenhuma rodada)*\n*Possui-se um total de 4 itens disponíveis que serão dispostos aleatoriamente no seu inventário, com um total de 8 slots. Itens não utilizados serão descartados no final da partida, até que as balas acabem, portanto saiba bem quando utilizar*""")
    embed_useitem.set_image(url="https://media1.tenor.com/m/3H6df2G66bAAAAAC/noted-taking-notes.gif")
    embed_caixa_tutorial = discord.Embed(title="**Caixa**", description="""**comando:** *dUse caixa / sUse caixa*\n\n*Este item tem a capacidade de recarregar uma vida de quem o usa. Ainda não se sabe seu conteúdo.*""")
    embed_caixa_tutorial.set_image(url="https://media1.tenor.com/m/MgJOhGDW7sgAAAAC/cigarette-smoke.gif")
    embed_lupa_tutorial = discord.Embed(title="**Lupa**", color=0xFF5733,description="""**comando:** *dUse lupa / sUse lupa*\n\n*Este item tem a capacidade de permitir quem o use de saber magicamente a natureza da bala atual, se causa danos ou não.*""")
    embed_lupa_tutorial.set_image(url="https://media1.tenor.com/m/MM5rhweEpn8AAAAd/anya-forger-detective.gif")
    embed_lata_tutorial = discord.Embed(title="**Lata**", color=0xFF5733, description="""**comando:** *dUse lata / sUse lata*\n\n*Este item tem a capacidade de permitir quem o use de remover a atual bala, sem dar tiros a ninguém*""")
    embed_lata_tutorial.set_image(url="https://media1.tenor.com/m/WuIg2JD8nOcAAAAd/anime-burp-cartoon.gif")
    embed_faca_tutorial = discord.Embed(title="**Faca**", color=0xFF5733, description="""**comando:** *dUse faca / sUse faca*\n\n*Este item tem a capacidade de permitir quem o use de serrar a boca da arma e causar o dobro de dano, sendo o máximo que ela pode causar como 2 vidas. Após isso, a arma será trocada e as alterações feitas pela faca na arma serão descartadas*""")
    embed_faca_tutorial.set_image(url="https://media1.tenor.com/m/rZwlMEQsQrUAAAAC/knife-anime.gif")
    loading_gun_message = discord.Embed(title="Começando o Jogo...", colour=0xFF5733, description="Rodada começa com 3 balas verdadeiras e duas falsas.")
    loading_gun_message.set_image(url="https://media1.tenor.com/m/fDakhj-iKdEAAAAC/aesthetic-anime.gif")
    embeds_tutorial_list = [embed_tutorial, embed_tut_1, embed_mecanica,embed_atir_sims, embed_atir_outr, embed_useitem, embed_caixa_tutorial, embed_lupa_tutorial, embed_lata_tutorial, embed_faca_tutorial]
    embeds_tutorial_counter = data_life["player1"]["tutorial_page"]


    class Buttons(discord.ui.View):
        embeds_tutorial_counter = 1
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="Button",style=discord.ButtonStyle.gray)
        async def blurple_button(self,button:discord.ui.Button,interaction:discord.Interaction):
            button.style=discord.ButtonStyle.green
            await interaction.response.edit_message(content=f"This is an edited button response!",view=self)

    class Tutorial(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="Anterior", style=discord.ButtonStyle.green)
        async def initTutorial(self, interaction:discord.Interaction, button:discord.ui.Button):
            data_life["player1"]["tutorial_page"] -= 1
            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)
            await interaction.response.edit_message(embed=embeds_tutorial_list[data_life["player1"]["tutorial_page"]], view=self)

        @discord.ui.button(label="Próximo", style=discord.ButtonStyle.green)
        async def avance(self, interaction:discord.Interaction, button:discord.ui.Button):
            data_life["player1"]["tutorial_page"] += 1

            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)
            await interaction.response.edit_message(embed=embeds_tutorial_list[data_life["player1"]["tutorial_page"]], view=self)

        @discord.ui.button(label="Start Game", style=discord.ButtonStyle.green)
        async def startgame(self, interaction:discord.Interaction, button:discord.ui.Button):
            possible_ammo = [True, False]
            data_life["player1"]["tutorial_page"] = 0
            data_life["ammo"] = []
            data_life["player1"]["shuffle"] = True
            data_life["player2"]["shuffle"] = True
            data_life["player1"]["vida"] = 3
            data_life["player2"]["vida"] = 3
            data_life["player1"]["doubler"] = False
            data_life["player2"]["doubler"] = False
            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)

            for c in range(0, 6):
                data_life["ammo"].append(choice(possible_ammo))
            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)
            loading_gun_message = discord.Embed(title="Começando o Jogo...", colour=0xFF5733, description=f"Rodada começa com {data_life["ammo"].count(True)} balas verdadeiras e {data_life["ammo"].count(False)} falsas.\n\n**Jogador D começa.**")
            loading_gun_message.set_image(url="https://media1.tenor.com/m/fDakhj-iKdEAAAAC/aesthetic-anime.gif")
            
            await interaction.response.edit_message(embed=loading_gun_message, view=self)

            default_channel = client.get_channel(data_life["channel_set"])

            with open("tsukaLife_share.json", "r") as file:
                data_clone = json.load(file)

            datalife_troc = dict(data_clone)
            datalife_troc["player1"] = data_clone["player2"]
            datalife_troc["player2"] = data_clone["player1"]
            troca_life_pretty = json.dumps(datalife_troc, indent=4)
            await default_channel.send(f"{data_clone["player2"]["command_set"]}datachange ```{troca_life_pretty}```")

    @client.event
    async def on_message(message):
        if message.content.startswith("comname"):                                           # set the command prefix
            await message.channel.send("Ok, command ajusted!")
            data_life["player1"]["command_set"] = str(message.content.split()[-1])
            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)

            default_channel = client.get_channel(data_life["channel_set"])
            mensagem = message.content.split()

            with open("tsukaLife_share.json", "r") as file:
                data_clone = json.load(file)

            datalife_troc = dict(data_clone)
            datalife_troc["player1"] = data_clone["player2"]
            datalife_troc["player2"] = data_clone["player1"]
            troca_life_pretty = json.dumps(datalife_troc, indent=4)
            await default_channel.send(f"{data_clone["player2"]["command_set"]}datachange ```{troca_life_pretty}```")

        if message.content.startswith(f"set_channel"):         # set the channel 
            default_channel = int((message.content.split())[-1])
            await message.channel.send(default_channel)
            data_life["channel_set"] = default_channel
            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file)
            
            default_channel = client.get_channel(data_life["channel_set"])
            mensagem = message.content.split()

            with open("tsukaLife_share.json", "r") as file:
                data_clone = json.load(file)
                
            datalife_troc = dict(data_clone)
            datalife_troc["player1"] = data_clone["player2"]
            datalife_troc["player2"] = data_clone["player1"]
            troca_life_pretty = json.dumps(datalife_troc, indent=4)
            await default_channel.send(f"{data_clone["player2"]["command_set"]}datachange ```{troca_life_pretty}```")

        if message.content.startswith(f"{data_life["player1"]["command_set"]}Start"):
            embed_tutorial = discord.Embed(title="Quer começar o tutorial?", colour=0xFF5733, description="Se deseja começar o tutorial para entender o funcionamento do jogo, clique no botão verde.")
            embed_tutorial.set_image(url="https://media1.tenor.com/m/irauQe8qvU0AAAAC/anime-study.gif")
            await message.channel.send(embed=embed_tutorial, view=Tutorial())

        if message.content.startswith(f"{data_life["player1"]["command_set"]}Use"):
            embed_zoando = discord.Embed(title="Tentou usar um item que não tem", description="Um mano tentou usar um item que não possui. Olha teu inventário aí mano", colour=0xFF5733)
            embed_zoando.set_image(url="https://media1.tenor.com/m/XdutV_U-btkAAAAC/confused-anime.gif")
            if message.content.split()[-1] == "lata":
                if "lata" in data_life["player1"]["inventory"]:
                    if data_life["player1"]["command_set"] == "d":
                        name = "Dealer"
                    else:
                        name = "Quick"
                    bala_removida = choice(data_life["ammo"])
                    data_life["ammo"].remove(bala_removida)
                    lata_place = data_life["player1"]["inventory"].index("lata")
                    data_life["player1"]["inventory"][lata_place] = "none"
                    with open("tsukaLife_share.json", "w") as file:
                        json.dump(data_life, file, indent=4)
                    if bala_removida == True:
                        bala_nature = "Verdadeira"
                    else:
                        bala_nature = "Falsa"
                    embed_lata = discord.Embed(title=f"{name} usou a lata e retirou uma bala **{bala_nature}**", colour=0xFF5733)
                    embed_lata.set_image(url="https://media1.tenor.com/m/apC_-ceSVEQAAAAC/glock-gun.gif")
                    await message.channel.send(embed=embed_lata)
                else:
                    embed_zoando = discord.Embed(title="Tentou usar um item que não tem", description="Um mano tentou usar um item que não possui. Olha teu inventário aí mano", colour=0xFF5733)
                    embed_zoando.set_image(url="https://media1.tenor.com/m/XdutV_U-btkAAAAC/confused-anime.gif")
                    await message.channel.send(embed=embed_zoando)
            if message.content.split()[-1] == "caixa":
                if "caixa" in data_life["player1"]["inventory"]:
                    if data_life["player1"]["command_set"] == "d":
                        name = "Dealer"
                    else:
                        name = "Quick"
                    data_life["player1"]["vida"] += 1
                    caixa_place = data_life["player1"]["inventory"].index("caixa")
                    data_life["player1"]["inventory"][caixa_place] = "none"
                    with open("tsukaLife_share.json", "w") as file:
                        json.dump(data_life, file, indent=4)
                    
                    caixa_embed = discord.Embed(title=f"{name} usou a Caixa e ganhou uma vida extra!", description=f"Ele agora possui {data_life["player1"]["vida"]} vidas!", colour=0xFF5733)
                    caixa_embed.set_image(url="https://media1.tenor.com/m/zBSZER_aGuQAAAAC/cowboy-bebop-scifi.gif")
                    await message.channel.send(embed=caixa_embed)
                else:
                    await message.channel.send(embed=embed_zoando)
                    
            if message.content.split()[-1] == "faca":
                if "faca" in data_life["player1"]["inventory"]:
                    if data_life["player1"]["command_set"] == "d":
                        nome = "Dealer"
                    else:
                        nome = "Quick"

                    if data_life["player1"]["doubler"] == False:
                        faca_embed = discord.Embed(title=f"{nome} usou a Faca e agora seu próximo tiro terá o dobro de dano!", description="Lembre-se que só se pode usar este item uma vez por rodada e ele não é acumulativo!", colour=0xFF5733)
                        faca_embed.set_image(url="https://media1.tenor.com/m/HCfxAi_T6-kAAAAC/l%C3%A2mina-katana.gif")
                    else:
                        faca_embed = discord.Embed(title=f"{nome} tentou usar a faca duas vezes (wtf)", description="Irmão tu não pode usar a faca duas vezes na mesma rodada.", colour=0xFF5733)
                        faca_embed.set_image(url="https://media1.tenor.com/m/5eO4er6KlmUAAAAC/question-mark-gif-anime-boy.gif")
                    data_life["player1"]["doubler"] = True
                    faca_index = data_life["player1"]["inventory"].index("faca")
                    data_life["player1"]["inventory"][faca_index] = "none"
                    with open("tsukaLife_share.json", "w") as file:
                        json.dump(data_life, file, indent=4)
                    
                    await message.channel.send(embed=faca_embed)

                
                else:
                    await message.channel.send(embed=embed_zoando)

            if message.content.split()[-1] == "lupa":
                if data_life["player1"]["command_set"] == "d":
                    nome = "Dealer"
                else:
                    nome = "Quick"

                if "lupa" in data_life["player1"]["inventory"]:
                    lupa_embed = discord.Embed(title=f"{nome} usou a Lupa e agora sabe a natureza da bala!", description="Ela apareceu em seu inventário e sumirá após realizar o tiro.", colour=0xFF5733)
                    lupa_embed.set_image(url="https://media1.tenor.com/m/7Ie8LtlHcwEAAAAd/anime-william-t-spears.gif")

                    if data_life["ammo"][0] == True:
                        data_life["player1"]["money"] = f"A natureza da bala é Verdadeira (True)"
                    else:
                        data_life["player1"]["money"] = f"A natureza da bala é Falsa (False)"
                    
                    lupa_place = data_life["player1"]["inventory"].index("lupa")
                    data_life["player1"]["inventory"][lupa_place] = "none"

                    with open("tsukaLife_share.json", "w") as file:
                        json.dump(data_life, file, indent=4)

                    await message.channel.send(embed=lupa_embed) 
                else:
                    await message.channel.send(embed=embed_zoando)
            
            default_channel = client.get_channel(data_life["channel_set"])
            mensagem = message.content.split()
            with open("tsukaLife_share.json", "r") as file:
                data_clone = json.load(file)
            datalife_troc = dict(data_clone)
            datalife_troc["player1"] = data_clone["player2"]
            datalife_troc["player2"] = data_clone["player1"]
            troca_life_pretty = json.dumps(datalife_troc, indent=4)
            await default_channel.send(f"{data_clone["player2"]["command_set"]}datachange ```{troca_life_pretty}```")

        if message.content.startswith(f"{data_life["player1"]["command_set"]}Self"):
            if data_life["player1"]["command_set"] == "d":
                nome = "Dealer"
            else:
                nome = "Quick"
            if data_life["ammo"][0] == True:
                if data_life["player1"]["doubler"] == True:
                    data_life["player1"]["vida"] -= 2
                    self_embed = discord.Embed(title=f"{nome} atirou em si mesmo e tomou 2 de dano!", description=f"Possui agora {data_life["player1"]["vida"]} de vida!", colour=0xFF5733)
                    self_embed.set_image(url="https://media1.tenor.com/m/4p2gwNLsxBEAAAAC/whizzy-imposterfox.gif")
                    data_life["player1"]["doubler"] = False
                else:
                    data_life["player1"]["vida"] -= 1
                    self_embed = discord.Embed(title=f"{nome} atirou em si mesmo e tomou 1 de dano!", description=f"Possui agora {data_life["player1"]["vida"]} de vida!", colour=0xFF5733)
                    self_embed.set_image(url="https://media1.tenor.com/m/4p2gwNLsxBEAAAAC/whizzy-imposterfox.gif")
            else:
                if data_life["player1"]["doubler"] == True:
                    data_life["player1"]["doubler"] = False
                self_embed = discord.Embed(title=f"{nome} atirou em si mesmo e não tomou dano!", description=f"Continua com {data_life["player1"]["vida"]} de vida!", colour=0xFF5733)
                self_embed.set_image(url="https://media1.tenor.com/m/0EgQgZWi8WoAAAAC/sigh-yamadakun-and-the-seven-witches.gif")

            bala_atirada = data_life["ammo"][0]
            data_life["ammo"].remove(bala_atirada)

            if data_life["player1"]["money"] != "":
                data_life["player1"]["money"] = ""

            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)

            await message.channel.send(embed=self_embed)

            default_channel = client.get_channel(data_life["channel_set"])
            mensagem = message.content.split()
            with open("tsukaLife_share.json", "r") as file:
                data_clone = json.load(file)
            datalife_troc = dict(data_clone)
            datalife_troc["player1"] = data_clone["player2"]
            datalife_troc["player2"] = data_clone["player1"]
            troca_life_pretty = json.dumps(datalife_troc, indent=4)
            await default_channel.send(f"{data_clone["player2"]["command_set"]}datachange ```{troca_life_pretty}```")

        if message.content.startswith(f"{data_life["player1"]["command_set"]}Shoot"):
            if data_life["player1"]["command_set"] == "d":
                nome = "Dealer"
            else:
                nome = "Quick"
            
            if data_life["ammo"][0] == True:
                if data_life["player1"]["doubler"] == True:
                    data_life["player2"]["vida"] -= 2
                    tiro_embed = discord.Embed(title=f"{nome} atirou no adversário e tirou 2 de vida!", description=f"Agora o adveresário possui {data_life["player2"]["vida"]} de vida!", colour=0xFF5733)
                    tiro_embed.set_image(url="https://media1.tenor.com/m/XrtlNAjPlMgAAAAC/kokichi-double-pistol.gif")
                    data_life["player1"]["doubler"] = False
                else:
                    data_life["player2"]["vida"] -= 1
                    tiro_embed = discord.Embed(title=f"{nome} atirou no adversário e tirou 1 de vida!", description=f"Agora o adveresário possui {data_life["player2"]["vida"]} de vida!", colour=0xFF5733)
                    tiro_embed.set_image(url="https://media1.tenor.com/m/XrtlNAjPlMgAAAAC/kokichi-double-pistol.gif")

            else:
                tiro_embed = discord.Embed(title=f"{nome} atirou no adversário e não tirou vida!", description=f"A bala era falsa, e agora o adveresário continua com {data_life["player2"]["vida"]} de vida!", colour=0xFF5733)
                tiro_embed.set_image(url="https://media1.tenor.com/m/NiK2MFhuLa0AAAAC/anime-confused.gif")


            bala_atirada = data_life["ammo"][0]
            data_life["ammo"].remove(bala_atirada)

            if data_life["player1"]["money"] != "":
                data_life["player1"]["money"] = ""

            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_life, file, indent=4)

            await message.channel.send(embed=tiro_embed)

            default_channel = client.get_channel(data_life["channel_set"])
            mensagem = message.content.split()
            with open("tsukaLife_share.json", "r") as file:
                data_clone = json.load(file)
            datalife_troc = dict(data_clone)
            datalife_troc["player1"] = data_clone["player2"]
            datalife_troc["player2"] = data_clone["player1"]
            troca_life_pretty = json.dumps(datalife_troc, indent=4)
            await default_channel.send(f"{data_clone["player2"]["command_set"]}datachange ```{troca_life_pretty}```")

        if message.content.startswith("++"):
            mensagem = message.content.split()
            loading_gun_message = discord.Embed(title="Começando o Jogo...", colour=0xFF5733, description="Rodada começa com 3 balas verdadeiras e duas falsas.")
            loading_gun_message.set_image(url="https://media1.tenor.com/m/fDakhj-iKdEAAAAC/aesthetic-anime.gif")
            await message.channel.send(embed=loading_gun_message)


        # send json to another bot
        if message.content.startswith(f"{data_life["player1"]["command_set"]}changeother"):
            default_channel = client.get_channel(data_life["channel_set"])
            mensagem = message.content.split()
            valor = mensagem[1]
            changeable.change_life(valor)
            datalife_troc = dict(data_life)
            datalife_troc["player1"] = data_life["player2"]
            datalife_troc["player2"] = data_life["player1"]
            troca_life_pretty = json.dumps(datalife_troc, indent=4)
            await default_channel.send(f"{data_life["player2"]["command_set"]}datachange ```{troca_life_pretty}```")

        if message.content.startswith(f"{data_life["player1"]["command_set"]}datachange"):
            data_troca_s = message.content.split()
            data_troca_s.remove(f"{data_life["player1"]["command_set"]}datachange")
            data_troca_dict = ""
            for palavra in data_troca_s:
                for letra in palavra:
                    if letra != "`":
                        data_troca_dict += letra
            print(data_troca_dict)
            data_troca_dictionary = json.loads(data_troca_dict)
            with open("tsukaLife_share.json", "w") as file:
                json.dump(data_troca_dictionary, file, indent=4)

            with open("tsukaLife_share.json", "r") as file:
                tsuka_data = json.load(file)

            data_life["player1"] = tsuka_data["player1"]
            data_life["player2"] = tsuka_data["player2"]

        
    token="TOKEN"
    client.run(token)


if __name__ == "__main__":
    t1 = threading.Thread(target=game)
    t2 = threading.Thread(target=bot)
    t2.start()
    t1.start()

    t2.join()
    t1.join()
