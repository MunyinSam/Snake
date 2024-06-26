


def test():
    
    board = Board.objects(board_name="default").first()
    board.players.append("munyin")
    board.save()