class MovesManager:
    def __init__(self):
        self.board = []

    def get_moves(self, piece, board):
        moves = []
        self.board = board

        if piece.name == "" and piece.color == "w":
            moves = self.white_pawn_move(piece)
        elif piece.name == "" and piece.color == "b":
            moves = self.black_pawn_move(piece)
        elif piece.name == "K":
            moves = self.king_move(piece)
        elif piece.name == "Q":
            moves = self.queen_move(piece)
        elif piece.name == "B":
            moves = self.bishop_move(piece)
        elif piece.name == "N":
            moves = self.knight_move(piece)
        elif piece.name == "R":
            moves = self.rook_move(piece)
        else:
            print("Error, never should have got here.")
            exit()

        return moves

    """
    Moves for each of the pieces
    """

    def king_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.board
        if y < 7 and (board[x][y + 1] == "" or piece.color != board[x][y + 1][0]):
            if not board[x][y + 1].__contains__("K"):
                moves.append((piece.x_pos, piece.y_pos + 1))

        if y > 0 and (board[x][y - 1] == "" or piece.color != board[x][y - 1][0]):
            if not board[x][y - 1].__contains__("K"):
                moves.append((piece.x_pos, piece.y_pos - 1))

        if x > 0 and (board[x - 1][y] == "" or piece.color != board[x - 1][y][0]):
            if not board[x - 1][y].__contains__("K"):
                moves.append((piece.x_pos - 1, piece.y_pos))

        if x < 7 and (board[x + 1][y] == "" or piece.color != board[x + 1][y][0]):
            if not board[x + 1][y].__contains__("K"):
                moves.append((piece.x_pos + 1, piece.y_pos))

        if x < 7 and y < 7 and (board[x + 1][y + 1] == "" or piece.color != board[x + 1][y + 1][0]):
            if not board[x + 1][y + 1].__contains__("K"):
                moves.append((piece.x_pos + 1, piece.y_pos + 1))

        if x < 7 and y > 0 and (board[x + 1][y - 1] == "" or piece.color != board[x + 1][y - 1][0]):
            if not board[x + 1][y - 1].__contains__("K"):
                moves.append((piece.x_pos + 1, piece.y_pos - 1))

        if x > 0 and y < 7 and (board[x - 1][y + 1] == "" or piece.color != board[x - 1][y + 1][0]):
            if not board[x - 1][y + 1].__contains__("K"):
                moves.append((piece.x_pos - 1, piece.y_pos + 1))

        if x > 0 and y > 0 and (board[x - 1][y - 1] == "" or piece.color != board[x - 1][y - 1][0]):
            if not board[x - 1][y - 1].__contains__("K"):
                moves.append((piece.x_pos - 1, piece.y_pos - 1))

        return moves

    def queen_move(self, piece):
        moves = self.bishop_move(piece)
        moves.extend(self.rook_move(piece))
        return moves

    def bishop_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.board

        # down right
        new_x = x
        new_y = y
        for i in range(x, 8):
            new_x += 1
            new_y += 1
            if new_x < 8 and new_y < 8:
                if board[new_x][new_y] == "":
                    moves.append((new_x, new_y,))
                else:
                    if piece.color != board[new_x][new_y][0]:
                        if not board[new_x][new_y].__contains__("K"):
                            moves.append((new_x, new_y,))
                    break
            else:
                break

        # up left
        new_x = x
        new_y = y
        for i in range(0, x):
            new_x -= 1
            new_y -= 1
            if new_x >= 0 and new_y >= 0:
                if board[new_x][new_y] == "":
                    moves.append((new_x, new_y,))
                else:
                    if piece.color != board[new_x][new_y][0]:
                        if not board[new_x][new_y].__contains__("K"):
                            moves.append((new_x, new_y,))
                    break
            else:
                break

        # up right
        new_x = x
        new_y = y
        for i in range(x, 8):
            new_x += 1
            new_y -= 1
            if new_x < 8 and new_y >= 0:
                if board[new_x][new_y] == "":
                    moves.append((new_x, new_y,))
                else:
                    if piece.color != board[new_x][new_y][0]:
                        if not board[new_x][new_y].__contains__("K"):
                            moves.append((new_x, new_y,))
                    break
            else:
                break

        # down left
        new_x = x
        new_y = y
        for i in range(0, x):
            new_x -= 1
            new_y += 1
            if new_x >= 0 and new_y < 8:
                if board[new_x][new_y] == "":
                    moves.append((new_x, new_y,))
                else:
                    if piece.color != board[new_x][new_y][0]:
                        if not board[new_x][new_y].__contains__("K"):
                            moves.append((new_x, new_y,))
                    break
            else:
                break

        return moves

    def knight_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.board
        if y > 0 and x < 7 and (board[x + 1][y - 2] == "" or piece.color != board[x + 1][y - 2][0]):
            if not board[x + 1][y - 2].__contains__("K"):
                moves.append((x + 1, y - 2,))

        if y > 0 and x > 0 and (board[x - 1][y - 2] == "" or piece.color != board[x - 1][y - 2][0]):
            if not board[x - 1][y - 2].__contains__("K"):
                moves.append((x - 1, y - 2,))

        if y < 6 and x < 7 and (board[x + 1][y + 2] == "" or piece.color != board[x + 1][y + 2][0]):
            if not board[x + 1][y + 2].__contains__("K"):
                moves.append((x + 1, y + 2,))

        if y < 6 and x > 0 and (board[x - 1][y + 2] == "" or piece.color != board[x - 1][y + 2][0]):
            if not board[x - 1][y + 2].__contains__("K"):
                moves.append((x - 1, y + 2,))

        if y > 0 and x > 1 and (board[x - 2][y - 1] == "" or piece.color != board[x - 2][y - 1][0]):
            if not board[x - 2][y - 1].__contains__("K"):
                moves.append((x - 2, y - 1,))

        if y > 0 and x < 6 and (board[x + 2][y - 1] == "" or piece.color != board[x + 2][y - 1][0]):
            if not board[x + 2][y - 1].__contains__("K"):
                moves.append((x + 2, y - 1,))

        if y < 7 and x > 1 and (board[x - 2][y + 1] == "" or piece.color != board[x - 2][y + 1][0]):
            if not board[x - 2][y + 1].__contains__("K"):
                moves.append((x - 2, y + 1,))

        if y < 7 and x < 6 and (board[x + 2][y + 1] == "" or piece.color != board[x + 2][y + 1][0]):
            if not board[x + 2][y + 1].__contains__("K"):
                moves.append((x + 2, y + 1,))

        return moves

    def rook_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.board
        if x < 7:
            # move right
            for i in range(x + 1, 8):
                if board[i][y] == "":
                    moves.append((i, y,))
                elif piece.color != board[i][y][0]:
                    if not board[i][y].__contains__("K"):
                        moves.append((i, y,))
                        break
                else:
                    break
        if x > 0:
            # move left
            for j in range(x - 1, -1, -1):
                if board[j][y] == "":
                    moves.append((j, y,))
                elif piece.color != board[j][y][0]:
                    if not board[j][y].__contains__("K"):
                        moves.append((j, y,))
                        break
                else:
                    break
        if y < 7:
            # move down
            for k in range(y + 1, 8):
                if board[x][k] == "":
                    moves.append((x, k,))
                elif piece.color != board[x][k][0]:
                    if not board[x][k].__contains__("K"):
                        moves.append((x, k,))
                        break
                else:
                    break
        if y > 0:
            # move up
            for l in range(y - 1, -1, -1):
                if board[x][l] == "":
                    moves.append((x, l,))
                elif piece.color != board[x][l][0]:
                    if not board[x][l].__contains__("K"):
                        moves.append((x, l,))
                        break
                else:
                    break

        return moves

    def white_pawn_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.board

        if board[x][y - 1] == "":
            moves.append((x, y - 1,))
            if not piece.moved and board[x][y - 2] == "":
                moves.append((x, y - 2,))
        if x > 0 and board[x - 1][y - 1].startswith("b"):
            if not board[x - 1][y - 1].__contains__("K"):
                moves.append((x - 1, y - 1,))

        if x < 7 and board[x + 1][y - 1].startswith("b"):
            if not board[x + 1][y - 1].__contains__("K"):
                moves.append((x + 1, y - 1,))

        return moves

    def black_pawn_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.board

        if y < 7 and board[x][y + 1] == "":
            moves.append((x, y + 1,))
            if y < 7 and not piece.moved and board[x][y + 2] == "":
                moves.append((x, y + 2,))
        if x > 0 and y < 7 and board[x - 1][y + 1].startswith("w"):
            if not board[x - 1][y + 1].__contains__("K"):
                moves.append((x - 1, y + 1,))

        if x < 7 and y < 7 and board[x + 1][y + 1].startswith("w"):
            if not board[x + 1][y + 1].__contains__("K"):
                moves.append((x + 1, y + 1,))
        return moves
