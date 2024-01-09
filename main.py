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

print(data)


send_save = False
def sendsave(yorn):
    global send_save
    with lockar:
        send_save = yorn

fechar = False
def fechar_game(soun):
    global fechar
    with lockar:
        fechar = soun

def bot():
    intents = discord.Intents.default()
    intents.message_content = True

    client=commands.Bot(command_prefix=".", intents=discord.Intents.all())

    class Buttons(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="Button SIM",style=discord.ButtonStyle.green)
        async def blurple_button(self,interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.response.edit_message(content=f"just edit this message..\nDESAFIO ACEITO!",view=self)
            print('Pressionado!')
            fechar_game(True)

    @client.command()
    async def battle(ctx):
        await ctx.send("Você quer batalhar?",view=Buttons())
        
    token="NzY3NDQ1MzIyMTUwMzEzOTg1.GU2Dzh.NillPwxSIcai4qluqOuISNypTdFfRd3vpMxC8Y"
    client.run(token)


def game():
    pygame.init()
    screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)

    running = True
    score = 0
    clock = pygame.time.Clock()

    player_x = 500
    player_y = 338

    player_username = "lotusvi"

    class Player():
        def __init__(self, player_xx, player_yy):
            self.player_x = player_xx
            self.player_y = player_yy
            self.ft_player = 0

            self.pl_mud_x_d = False
            self.pl_mud_x_e = False
            self.pl_mud_y_c = False
            self.pl_mud_y_b = False
            self.player_spr = list()

            self.virado = False
            self.player_esquerda = False
            self.player_direita = True
            self.ataque = pygame.Rect((self.player_x-25, self.player_y+25), (50, 20))
            self.tiro = pygame.Rect((0, 0), (20, 20))


        def takeSprites(self):
            for foto in range(1, 11):
                for i in range(0, 7):
                    self.player_spr.append(pygame.transform.scale(pygame.image.load(f"sprites/player_sprites/player_{foto}.png"), (50, 50)))


        def isColliding(self, collisions_list):
            self.pl_baixo = pygame.Rect((self.player_x+25, self.player_y+50), (2, 2))
            self.pl_esq = pygame.Rect((self.player_x, self.player_y+25), (2, 2))
            self.pl_dir = pygame.Rect((self.player_x+50, self.player_y+25), (2, 2))
            self.pl_cima = pygame.Rect((self.player_x+25, self.player_y), (2, 2))

            if self.pl_mud_x_e:
                if self.pl_esq.collidelist(collisions_list) == -1:
                    self.player_x -= 6
                if self.ft_player < 9:
                    self.ft_player += 1
                else:
                    self.ft_player = 0
            if self.pl_mud_x_d:
                if self.pl_dir.collidelist(collisions_list) == -1:
                    self.player_x += 6
                if self.ft_player < 9:
                    self.ft_player += 1
                else:
                    self.ft_player = 0
            if self.pl_mud_y_c:
                if self.pl_cima.collidelist(collisions_list) == -1:
                    self.player_y -= 6
                if self.ft_player < 9:
                    self.ft_player += 1
                else:
                    self.ft_player = 0
            if self.pl_mud_y_b:
                if self.pl_baixo.collidelist(collisions_list) == -1:
                    self.player_y += 6
                if self.ft_player < 9:
                    self.ft_player += 1
                else:
                    self.ft_player = 0
        
        def blitPlayer(self):
            if not self.virado:
                screen.blit(self.player_spr[self.ft_player], (self.player_x, self.player_y))
            else:
                screen.blit(pygame.transform.flip(self.player_spr[self.ft_player], True, False), (self.player_x, self.player_y))

        def attack(self):
            if not self.virado:
                self.ataque = pygame.Rect((self.player_x-25, self.player_y+25), (50, 20))
            else:
                self.ataque = pygame.Rect((self.player_x+25, self.player_y+25), (50, 20))
        
        def Tiro(self, init_x, init_y):
            self.tiro = pygame.Rect((init_x+25, init_y+25), (20, 20))
            mouse_pos = pygame.mouse.get_pos()
            if init_x < mouse_pos[0]:
                init_x += 1
            else:
                init_x -= 1
            if init_y < mouse_pos[1]:
                init_y += 1
            else:
                init_y -= 1


    up_forca = False

    atacando = False

    boss_battle_running = True


    class Enemy():
        def __init__(self, x, y):
            self.ft_enemy = 0
            self.enemy_x = x
            self.enemy_y = y
            self.enemy_spr = list()
            self.enemy_collision = pygame.Rect((self.enemy_x, self.enemy_y), (30, 30))
            self.enemy_morto = False
            for foto in range(1, 3):
                for i in range(0, 4):
                    self.enemy_spr.append(pygame.transform.scale(pygame.image.load(f"sprites/ghost{foto}_e.png"), (30, 30)))

        def changeSprites(self):
            if self.ft_enemy <7:
                self.ft_enemy += 1
            else:
                self.ft_enemy = 0

        def followPlayer(self, x, y):
            if x > self.enemy_x:
                self.enemy_x += 1
                self.enemy_collision = pygame.Rect((self.enemy_x, self.enemy_y), (30, 30))
            else: 
                self.enemy_x -= 1
                self.enemy_collision = pygame.Rect((self.enemy_x, self.enemy_y), (30, 30))

            if y > self.enemy_y:
                self.enemy_y += 1
                self.enemy_collision = pygame.Rect((self.enemy_x, self.enemy_y), (30, 30))
            else:
                self.enemy_y -= 1
                self.enemy_collision = pygame.Rect((self.enemy_x, self.enemy_y), (30, 30))

        def isDead(self, att):
            att = player.ataque
            if att.colliderect(self.enemy_collision):
                self.enemy_morto = True
                print("colisao")
        def blitEnemy(self):
            screen.blit(self.enemy_spr[self.ft_enemy], (self.enemy_x, self.enemy_y))


    def montar_inimigo(var):
        var.changeSprites()
        var.followPlayer(player.player_x, player.player_y)
        if atacando:
            if player.ataque.colliderect(var.enemy_collision):
                var.enemy_morto = True
                up_forca = True
        if not var.enemy_morto:
            var.blitEnemy()

    def Respawn(var, x, y):
        var.enemy_morto = False
        var.enemy_x = x
        var.enemy_y = y




    if True:
        back1 = pygame.image.load("sprites/scenario/scnd_overworld.jpg")
        back1 = pygame.transform.scale(back1, (740, 676))

        boss_battle_back = pygame.image.load("sprites/scenario/boss_battle.jpg")
        boss_battle_back = pygame.transform.scale(boss_battle_back, (740, 676))

    def draw_screen(cor, obj, sla=False):
        if not sla:
            pygame.draw.rect(screen, cor, obj)
        else:
            pygame.draw.rect(screen, cor, obj, 1)

    if True:
        grama1 = pygame.Rect((368, 195), (136, 30))
        grama1_1 = pygame.Rect((586, 195), (138, 30))
        grama2 = pygame.Rect((368, 12), (354, 30))
        grama3 = pygame.Rect((367, 12), (30, 213))
        grama4 = pygame.Rect((694, 12), (30, 213))
        grama5 = pygame.Rect((692, 379), (30, 175))
        block1 = pygame.Rect((299, 10), (10, 999))
        bl2 = pygame.Rect((1040, 11), (10, 999))
        barreira_1 = pygame.Rect((289, 10), (69, 301))
        grama6 = pygame.Rect((725, 377), (315, 30))
        barraquinha_collision = pygame.Rect((735, 11), (83, 82))
        casinha_collision  = pygame.Rect((879, 36), (128, 129))
        caixinha_collision = pygame.Rect((856, 171), (25, 33))
        caixinha_collision2 = pygame.Rect((971, 283), (25, 33))
        caixinha_collision3 = pygame.Rect((769, 327), (25, 33))
        caixinha_collision4 = pygame.Rect((372, 260), (25, 33))

        collision = [grama1, grama2, grama3, grama4, grama5, grama1_1, block1, barreira_1, grama6, bl2, barraquinha_collision, casinha_collision, caixinha_collision, caixinha_collision2, caixinha_collision3, caixinha_collision4]

    draw_attack = False

    player = Player(player_x, player_y)
    player.takeSprites()


    enemy1 = Enemy(450, 70)
    enemy2 = Enemy(906, 558)

    boss_battle = pygame.Rect((474, 523), (50, 50))
    enter_bossBattle = False

    while running:
        player.attack()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                data[player_username]["bot"]["forca"] += 10
                draw_attack = True
                atacando = True
            if event.type == pygame.MOUSEBUTTONUP:
                draw_attack = False
                atacando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    data[player_username]["bot"]["forca"] += 10
                if event.key == pygame.K_q:
                    with open('local_database.json', 'w') as file:
                        file = json.dump(data, file, indent=4)
                if event.key == pygame.K_w:
                    player.pl_mud_y_c = True
                if event.key == pygame.K_s:
                    player.pl_mud_y_b = True
                if event.key == pygame.K_a:
                    player.pl_mud_x_e = True
                    player.virado = False
                if event.key == pygame.K_d:
                    player.pl_mud_x_d = True
                    player.virado = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.pl_mud_y_c = False
                if event.key == pygame.K_s:
                    player.pl_mud_y_b = False
                if event.key == pygame.K_a:
                    player.pl_mud_x_e = False
                if event.key == pygame.K_d:
                    player.pl_mud_x_d = False
        
        player.isColliding(collision)

        screen.fill((0, 0, 0))
        screen.blit(back1, (300, 10))
        player.blitPlayer()

        montar_inimigo(enemy1)
        montar_inimigo(enemy2)


        if casinha_collision.collidelist([player.pl_baixo, player.pl_cima, player.pl_dir, player.pl_esq]) != -1:
            Respawn(enemy1, 450, 70)
            Respawn(enemy2, 906, 558)

        if draw_attack:                                                         # shows attack colision when pressed 
            draw_screen((255, 255, 255), player.ataque)
        draw_screen((255, 0, 0), boss_battle)
        
        if up_forca:
            data[player_username]["bot"]["forca"] += 10
            up_forca = False

        if boss_battle.collidelist([player.pl_baixo, player.pl_cima, player.pl_dir, player.pl_esq]) != -1:
            enter_bossBattle = True

        if enter_bossBattle:
            while boss_battle_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        boss_battle_running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        boss_battle_running = False

                screen.blit(boss_battle_back, (0, 0))
                pygame.display.update()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    t1 = threading.Thread(target=game)
    t2 = threading.Thread(target=bot)
    t2.start()
    #sleep(20)
    t1.start()

    t2.join()
    t1.join()