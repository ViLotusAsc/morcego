import pygame
from random import randint
from random import choice
import json
import threading
import ctypes
from ctypes import wintypes 

pygame.init()

screen = pygame.display.set_mode((348, 520), pygame.RESIZABLE)

hwnd = pygame.display.get_wm_info()['window']
    
user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
user32.SetWindowPos(hwnd, -1, 600, 300, 0, 0, 0x0001)

background_foto = pygame.image.load("sprites/79AC/sem título.jpg")
background_foto = pygame.transform.scale(background_foto, (1180, 620))

gameplay_area = pygame.image.load("sprites/79AC/gameplay.jpg")
gameplay_area = pygame.transform.scale(gameplay_area, (348, 520))

#mesa_foto = pygame.image.load("sprites/79AC/mesa.jpg")
#mesa_foto = pygame.transform.scale(mesa_foto, (1180, 620))

running = True

inventory = ["none", "none", "none", "lata", "none", "none", "none", "none"]
inventory_dir = ["none", "none", "none", "none"]
inventory_esq =  ["none",  "none", "none", "none"]
inventory_places_dir = [(23, 309), (89, 311), (24, 426), (88, 427)]
inventory_places_esq = [(215, 310), (282, 307), (215, 427), (282, 427)]

itens_listt = ["faca", "lata", "lupa", "caixa"]

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

counter_embaralho = 0

buttonPlay = Button(521, 209, 859, 265)
buttonPlay.createButton()

buttonCredit = Button(521, 279, 859, 335)
buttonCredit.createButton()

local = "menu"

locais_esq = [(351, 427), (468, 427),  (298, 503), (421, 503)]
locais_dir = [(813, 421), (945, 421), (873, 496), (1023, 497)]

class Itens:
    def __init__(self):
        #self.ladoesq = data["mesaIndivEsq"]
        #self.ladodir = data["mesaIndivDir"]
#
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

    def drawSprites(self, obj, lado, num, f=counter_embaralho):
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
    for i in range(0, 4):
        inventory[i] = choice(itens_listt)

def chooseItens_Left():
    for i in range(4, 8):
        inventory[i] = choice(itens_listt)


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
                darPlay = buttonPlay.isButtonPressed(event.pos)
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
                    item2.drawSprites("faca", "dir", 1)
                if event.key == pygame.K_q:
                    print(f"Inventário: {inventory}")
            if event.type == pygame.MOUSEBUTTONDOWN:
                chooseItens_Right()
                chooseItens_Left()
                item3.drawSprites("faca", "exit", 2)
                itens.drawSprites(inventory[0], "exit", 1)
                item1.drawSprites(inventory[1], "exit", 2)
                item2.drawSprites(inventory[2], "exit", 3)
                item4.drawSprites(inventory[4], "exit", 1)
                item5.drawSprites(inventory[5], "exit", 2)
                item6.drawSprites(inventory[6], "exit", 3)
                item7.drawSprites(inventory[7], "exit", 4)
                print(inventory)

        screen.blit(gameplay_area, (0, 0))
        itens.drawSprites(inventory[0], "esq", 1)
        item1.drawSprites(inventory[1], "esq", 2)
        item2.drawSprites(inventory[2], "esq", 3)
        item3.drawSprites(inventory[3], "esq", 4)
        item4.drawSprites(inventory[4], "dir", 1)
        item5.drawSprites(inventory[5], "dir", 2)
        item6.drawSprites(inventory[6], "dir", 3)
        item7.drawSprites(inventory[7], "dir", 4)
        blitAll()
        pygame.display.update()