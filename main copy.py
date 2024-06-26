from classes import *
from commands import *

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

@bot.command(name="cr_board")
async def create_board(ctx):

    tiles = [Tile(type="normal", occupied_by=[""]) for _ in range(25)]
    board = Board(board_name="default",players=[], tiles=tiles)
    board.save()

@bot.command(name="cr_player")
async def create_player(ctx):

    name = str(ctx.message.author)

    player = Player(name=name, position=0)
    player.save()

@bot.command(name="add")
async def add(ctx):

    player_name = str(ctx.message.author)    
    player = Player.objects(name=player_name).first()
    if not player:
        await ctx.send(f"Player {player_name} not found.")
        return
    board = Board.objects().first() 
    if not board:
        await ctx.send("Board not found.")
        return

    board.tiles[0].occupied_by.append(str(player.name))
    if player_name not in board.players:
        board.players.append(str(player_name))
    board.save()



    await ctx.send(f"Player {player_name} has been added to the first tile.")







try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
bot.run(os.getenv("BOT_KEY"))