import asyncio
import discord
from discord.ext import commands
from random import randint


intents = discord.Intents.all()
bot = commands.Bot(command_prefix = ("?", "!"), intents = intents)

# Make the gameboard
def generate_board(coords: list[tuple[int, int]]) -> str:
    gameboard = []
    for i in range(11):
        list = []
        for j in range(11):
            list.append("⬛")
        gameboard.append(list)
    
    for c in coords:
        x, y = c
        try:
            gameboard[y - 1][x - 1] = "🟩"
        except IndexError:
            return "Game over!"
        else:
            pass
    
    board = ''
    for i in gameboard:
        for j in i:
            board += str(j)
        board += '\n'
    
    return board

class Snake:
    def __init__(self):
        self.direction = "right"
        self.length = 3
        self.coords = [(4, 6), (5, 6), (6, 6)]

    def collide(self, placement):
        head = self.coords[-1]

        if head[0] >= 0 and head[0] < 11:
            if head[1] >= 0 and head[1] < 11:
                pass
            else:
                return "Game over!"
        else:
            return "Game over!"

        if placement in self.coords:
            return "Game over!"
        else:
            return False

    def move(self):
        head = self.coords[-1]

        directions = {
            "right": (head[0] + 1, head[1]),
            "left": (head[0] - 1, head[1]),
            "up": (head[0], head[1] - 1),
            "down": (head[0], head[1] + 1)
        }
        
        placement = directions[self.direction]
        self.coords.append(placement)
        
        del self.coords[0]
        return self.coords


class Directions(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label='Left', style=discord.ButtonStyle.green)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "left"
        print(self.value)
     
    @discord.ui.button(label='Up', style=discord.ButtonStyle.green)
    async def up(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "up"
        print(self.value)
    
    @discord.ui.button(label='Down', style=discord.ButtonStyle.green)
    async def down(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "down"
        print(self.value)
    
    @discord.ui.button(label='Right', style=discord.ButtonStyle.green)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = "right"
        print(self.value)
    
    @discord.ui.button(label='❌', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        print(self.value)
        self.stop()


# -------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print("Logged in!")

@bot.command()
async def penis(ctx):
    length = randint(1, 20)
    size = ''
    for i in range(length):
        size += "="
    await ctx.send(f"Your penis size: 8{size}D ({length} cm!)")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def delete(ctx, limit):
    limit = int(limit)
    if limit > 100:
        await ctx.channel.purge(limit = 100)
    else:
        await ctx.channel.purge(limit = int(limit))
    await ctx.send("done", delete_after = 0.75)

@bot.command()
async def snake(ctx):
    snake = Snake()
    old_direction = snake.direction

    msg = await ctx.send("loading...")
    await asyncio.sleep(0.5)
    await msg.delete()
    message = await ctx.send("snake")
    new_board = generate_board(snake.move())

    while new_board != "Game over!" or snake.collide != "Game over!":
        embed = discord.Embed(
            title = "Snake",
            description = new_board,
            color = 0x00cc00
        )
        
        view = Directions()
        await message.edit(content = None, embed = embed, view = view)

        if view.value is None:
            continue
        elif not view.value:
            break
        else:
            snake.direction = view.value
        
        await asyncio.sleep(0.75)
        new_board = generate_board(snake.move())

    await message.delete()
    await ctx.send("the end!", delete_after = 1)

@bot.command()
async def edits(ctx):
    message = await ctx.send("hello")    
    edit_msgs = ["hi", "greetings", "penis", "how are you", "send me money", "free robux"]
    
    for msg in edit_msgs:
        await asyncio.sleep(0.25)
        await message.edit(content = msg)
    
    await ctx.send("Done!")

bot.run("OTAzMDkzOTU2ODIzMzY3Njgw.GM3mGw.U9jXwUIoTXcHp2SL8DzLO10fAbuA-utdkJJf3A")