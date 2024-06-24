from classes import *

import discord
from discord.ext import tasks, commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
print("Current Working Directory:", os.getcwd())

uri = str(os.getenv("MONGODB_URI"))
client = MongoClient(uri, server_api=ServerApi('1'))

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# -------------------------------------------------------------------------

@bot.command(name="create_board")
async def create_board(ctx):

    tiles = [Tile(type="normal") for _ in range(25)]
    board = Board(players=[], tiles=tiles)
    board.save()

@bot.command(name="cr")
async def create_player(ctx):

    name = str(ctx.message.author)

    player = Player(name=name, position=0)
    player.save()

@bot.command(name="add")
async def add(ctx):
    player_name = str(ctx.message.author)
    
    # Fetch the player
    player = Player.objects(name=player_name).first()
    if not player:
        await ctx.send(f"Player {player_name} not found.")
        return


    board = Board.objects().first() 

    if not board:
        await ctx.send("Board not found.")
        return

    # Add the player to the first tile
    board.tiles[0].occupied_by.append(str(player.name))
    board.save()

    await ctx.send(f"Player {player_name} has been added to the first tile.")


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
bot.run(os.getenv("BOT_KEY"))