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
class GameView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(label="Roll", style=discord.ButtonStyle.green, custom_id="roll_dice")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        return


class LobbyView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(label="Join Game", style=discord.ButtonStyle.red, custom_id="join_game")
    async def join_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        board = Board.objects(board_name="default").first()

        if board.state == "pending":
            board.players.append(str(interaction.user.name))
            board.save()

            embed = discord.Embed(title='You have joined the room')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            print("The Game has already started")

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.green, custom_id="start_game")
    async def start_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        board = Board.objects(board_name="default").first()

        if board.state == "pending" and len(board.players) > 1:
            board.state = "started"
            board.save()

            embed = discord.Embed(title='The Game has started')
            await interaction.response.send_message(embed=embed, ephemeral=False, view=GameView(self.ctx))



        

@bot.command(name="play")
async def display_lobby(ctx):

    tiles = [Tile(type="normal", occupied_by=[""]) for _ in range(25)]
    board = Board(board_name="default",players=[], tiles=tiles, state="pending")
    board.save()

    embed = discord.Embed(title="Lobby", description="Select an option to proceed:")
    await ctx.send(embed=embed,view=LobbyView(ctx))




try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
bot.run(os.getenv("BOT_KEY"))