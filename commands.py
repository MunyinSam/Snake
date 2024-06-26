from classes import *
import random

def random_number():
    number = random.randint(1,6)
    return number

def find_position(strings, item):
    try:
        position = strings.index(item)
        return position
    except ValueError:
        return -1

def move_player(player_name, current_pos, next_pos):

    player_obj = Player.objects(name=str(player_name)).first()
    board = Board.objects(board_name="default").first()

    if not player_obj:
        print("Player object not found")
        return

    if not board:
        print("Board not found")
        return

    if player_name not in board.players:
        print("Player not in the board")
        return

    # Debugging statements
    print(f"Current Position: {current_pos}, Next Position: {next_pos}")
    print(f"Current Tile Occupants (Position {current_pos}): {board.tiles[current_pos].occupied_by}")
    print(f"Next Tile Occupants (Position {next_pos}): {board.tiles[next_pos].occupied_by}")

    if str(player_name) in board.tiles[current_pos].occupied_by:
        board.tiles[current_pos].occupied_by.remove(str(player_name))
        board.tiles[next_pos].occupied_by.append(str(player_name))
        
        board.save()

        print(f"Player '{player_name}' moved from position {current_pos} to {next_pos}.")
        print(f"Updated Tile Occupants (Position {current_pos}): {board.tiles[current_pos].occupied_by}")
        print(f"Updated Tile Occupants (Position {next_pos}): {board.tiles[next_pos].occupied_by}")
    else:
        print(f"Player '{player_name}' is not on tile {current_pos}.")