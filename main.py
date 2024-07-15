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
        
        board = Board.objects(board_name="default").first()
        player = Player.objects(name=str(interaction.user.name)).first()

        if board.current_turn == str(interaction.user.name):

            previous_player_pos = player.position

            board.tiles[int(player.position)].occupied_by.remove(str(player.name))
            roll = random_number()
            player.position += roll
            player.save()

            tile_type = board.tiles[int(player.position)].type
            if tile_type == "normal":
                board.tiles[int(player.position)].occupied_by.append(str(player.name))
                board.save()
            if tile_type == "up":
                roll = random_number()
                player.position += roll*2
                board.tiles[int(player.position)].occupied_by.append(str(player.name))
                board.save()
            if tile_type == "down":
                roll = random_number()
                player.position -= roll*2
                board.tiles[int(player.position)].occupied_by.append(str(player.name))
                board.save()

            

            pos = find_position(board.players, str(player.name))

            board.current_turn = board.players[(int(pos) + 1) % len(board.players)]
            board.save()
            current_player_pos = player.position

            


            embed = discord.Embed(title=f'{player.name} has moved from {previous_player_pos} to {current_player_pos}')
            await interaction.response.send_message(embed=embed, ephemeral=False, delete_after=10)
        
        else:
            embed = discord.Embed(title='Wait for your Turn!', description=f'current turn: {board.current_turn}')
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)

class LobbyView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(label="Join Game", style=discord.ButtonStyle.red, custom_id="join_game")
    async def join_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        player_obj = Player.objects(name=str(interaction.user.name)).first()
        if player_obj:
            pass
        else:
            player = Player(name=str(interaction.user.name), position=0)
            player.save()

        board = Board.objects(board_name="default").first()

        if board.state == "pending":
            board.players.append(str(interaction.user.name))
            board.tiles[0].occupied_by.append(str(interaction.user.name))
            board.save()

            player_list = [player for player in board.players]

            embed = discord.Embed(title='You have joined the room',description=player_list)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            print("The Game has already started")
            embed = discord.Embed(title='The game has already started')
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.green, custom_id="start_game")
    async def start_game_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        board = Board.objects(board_name="default").first()

        if board.state == "pending" and len(board.players) > 1:
            board.state = "started"

            random.shuffle(board.players)
            board.current_turn = board.players[0]
            board.save()

            for player_name in board.players:
                player = Player.objects(name=str(player_name)).first()
                player.position = 0
                player.save()

            embed = discord.Embed(title=f'The Game has started. {board.current_turn} goes first')
            await interaction.response.send_message(embed=embed, ephemeral=False, view=GameView(self.ctx))



@bot.command(name="play")
async def display_lobby(ctx):

    tiles = [Tile(type="normal", occupied_by=[""]) for _ in range(25)]
    board = Board(board_name="default",players=[], tiles=tiles, state="pending", current_turn="")
    board.save()

    embed = discord.Embed(title="Lobby", description="Select an option to proceed:")
    await ctx.send(embed=embed,view=LobbyView(ctx))




try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
bot.run(os.getenv("BOT_KEY"))