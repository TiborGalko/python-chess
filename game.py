from game_manager import ChessGame
import tkinter as tk
import string
import math
from pprint import pprint
from PIL import ImageTk, Image


class Application(tk.Frame):
    def __init__(self, width=800, height=600, master=None):
        super().__init__(master, width=width, height=height)
        self.master = master

        self.loaded_images = dict()  # kept to not be recycled by garbage collector
        self.images = dict()  # keeping piece images based on piece starting position as key

        self.offset_x = -40
        self.offset_y = -20
        self.width = 60
        self.game = ChessGame()
        self.moving = False
        self.moving_piece = None
        self.moving_piece_key = ""
        self.actual_moves_ids = []
        self.moves = []

        self.canvas = self.create_board()
        self.canvas.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.click_callback)
        # self.canvas.bind("<B1-Motion>", self.mouse_move_callback) TODO

        self.text = []
        self.add_annotations()
        self.populate_board()

        self.text_box = self.create_text()

    def create_board(self):
        """ Method creates new chess board on tkinter canvas and returns it"""
        canvas = tk.Canvas(master=self, width=530, height=550)
        canvas.configure(scrollregion=(self.offset_x, self.offset_y, 20, 20))

        # x1 y1 x2 y2
        for i in range(8):
            y = i * self.width
            for j in range(8):
                x = j * self.width
                if ((j+1) % 2) == 0:
                    if ((i+1) % 2) == 0:
                        canvas.create_rectangle(x, y, x+self.width, y+self.width,
                                                outline="#808080", fill="#fff")  # biela
                    else:
                        canvas.create_rectangle(x, y, x+self.width, y+self.width,
                                                outline="#808080", fill="#999")  # cierna
                else:
                    if ((i+1) % 2) == 1:
                        canvas.create_rectangle(x, y, x+self.width, y+self.width,
                                                outline="#808080", fill="#fff")  # biela
                    else:
                        canvas.create_rectangle(x, y, x+self.width, y+self.width,
                                                outline="#808080", fill="#999")  # cierna

        return canvas

    def add_annotations(self):
        """ Method adds numbers and letters to board sides """
        for i in range(8):
            self.text.append(self.canvas.create_text(-self.width/2,
                                                     (self.width/2)+(i*self.width),
                                                     font=("Purisa", 12), anchor="nw"))
            self.canvas.itemconfig(self.text[i], text=str((i-8)*-1))
        for i in range(8):
            self.text.append(self.canvas.create_text((self.width/2)+(i*self.width),
                                                     self.width*8+10, font=("Purisa", 12), anchor="nw"))
            self.canvas.itemconfig(self.text[i+8], text=string.ascii_lowercase[i])

    def populate_board(self):
        """ Method adds images on canvas board """
        for key, value in self.game.white_pieces.items():
            x_pos = self.width*value.x_pos
            y_pos = self.width * value.y_pos
            img = self.load_image("images/" + value.image, value.starting_position)
            self.place_image_on_canvas(x_pos, y_pos, img, "images/" + value.image, value.position)
        for key, value in self.game.black_pieces.items():
            x_pos = self.width * value.x_pos
            y_pos = self.width * value.y_pos
            img = self.load_image("images/" + value.image, value.starting_position)
            self.place_image_on_canvas(x_pos, y_pos, img, "images/" + value.image, value.position)

    def load_image(self, image_name, piece_name):
        """ Helper method for loading images """
        img = ImageTk.PhotoImage(Image.open(image_name))
        self.loaded_images[piece_name] = (img, image_name)
        return img

    def place_image_on_canvas(self, x, y, img, image_name, piece_starting_position):
        image_id = self.canvas.create_image(x, y, image=img, tags=(image_name, "piece"), anchor="nw")
        self.images[piece_starting_position] = image_id

    def remove_image_from_canvas(self, piece_position):
        print("Removing image on key ",piece_position)
        self.canvas.delete(self.images[piece_position])

    def move_image_on_canvas(self, new_x, new_y, piece_position):
        self.remove_image_from_canvas(piece_position)
        img, image_name = self.loaded_images[self.moving_piece.starting_position]
        self.place_image_on_canvas(self.width * new_x,
                                   self.width * new_y,
                                   img,
                                   image_name,
                                   self.moving_piece.starting_position)

    def show_moves_on_canvas(self, moves):
        for move in moves:
            self.actual_moves_ids.append(self.canvas.create_oval(move[0] * self.width + 15,
                                    move[1] * self.width + 15,
                                    move[0] * self.width + 15 + (self.width / 2),
                                    move[1] * self.width + 15 + (self.width / 2),
                                    fill="green"))

    def clear_moves_on_canvas(self):
        for move in self.actual_moves_ids:
            self.canvas.delete(move)

    def create_text(self):
        text_box = tk.Text(master=self, height=28, width=31)
        text_box.insert(tk.END, "Welcome.\nIt's been a long minute.\n\n")

        scrollbar = tk.Scrollbar(master=self, command=text_box.yview, orient=tk.VERTICAL)
        text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        text_box.configure(state=tk.DISABLED)
        text_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        return text_box

    def write_text(self, text):
        self.text_box['state'] = tk.NORMAL
        self.text_box.insert(tk.END, text)
        self.text_box['state'] = tk.DISABLED

    def click_callback(self, event):
        """ On click event callback """
        # print("clicked at ", event.x+self.offset_x, event.y+self.offset_y)
        # x = string.ascii_lowercase[math.ceil((event.x + self.offset_x) / self.width) - 1]
        # y = (math.ceil((event.y + self.offset_y) / self.width) - 9) * -1
        self.clear_moves_on_canvas()

        x = math.ceil((event.x + self.offset_x) / self.width) - 1
        y = math.ceil((event.y + self.offset_y) / self.width) - 1

        if 0 <= x < 8 and 0 <= y < 8:
            board_value = self.game.board[x][y]
            if self.moving:
                # check if second click isnt on another piece
                if board_value != "" and board_value[0] == self.game.current_player_color:
                    self.calculate_moves_for_moving_piece(x, y)
                else:
                    self.move_piece(x, y)  # method moves moving_piece
                    self.moving = False
            else:
                self.calculate_moves_for_moving_piece(x, y)  # method sets moving_piece

    def mouse_move_callback(self, event):
        """ On mouse move event callback """
        print("moving at ", event.x + self.offset_x, event.y + self.offset_y)

    def move_piece(self, x, y):
        if (x, y) in self.moves:
            print("clicked on move", x, y)
            print(" board: ", self.game.board[x][y])
            print(self.moving_piece.position)

            self.move_image_on_canvas(x, y, self.moving_piece.position)

            if self.game.board[x][y] != "":
                if self.game.board[x][y].startswith("w"):
                    self.remove_image_from_canvas(self.game.white_pieces[(self.game.board[x][y])[1:]].position)
                elif self.game.board[x][y].startswith("b"):
                    self.remove_image_from_canvas(self.game.black_pieces[(self.game.board[x][y])[1:]].position)

            self.game.board[self.moving_piece.x_pos][self.moving_piece.y_pos] = ""
            self.game.board[x][y] = self.moving_piece_key
            self.moving_piece.x_pos = x
            self.moving_piece.y_pos = y

            if not self.moving_piece.moved:
                self.moving_piece.moved = True

            pprint(self.game.board)

            made_move = string.ascii_lowercase[x] + str(y)
            print(str(self.game.current_turn) + ". " + made_move)
            if self.moving_piece.color == "w":
                self.write_text(str(self.game.current_turn) + ". ")

            self.write_text(made_move + " ")

            self.game.next_move()
            # TODO change position too
            # TODO update on board

    """
    Moves for each of the pieces
    """

    def calculate_moves_for_moving_piece(self, x, y):
        print("clicked at ", x, y)
        print(self.game.board[x][y])
        board_value = self.game.board[x][y]
        player_color = self.game.current_player_color
        if board_value != "" and board_value[0] == self.game.current_player_color:
            self.moving = True
            self.moving_piece_key = board_value

            if self.game.current_player_color == "w":
                self.moving_piece = self.game.white_pieces[board_value[1:]]
            elif self.game.current_player_color == "b":
                self.moving_piece = self.game.black_pieces[board_value[1:]]

            piece = self.moving_piece

            if piece.color == player_color:
                if piece.name == "" and player_color == "w":
                    self.moves = self.white_pawn_move(piece)
                elif piece.name == "" and player_color == "b":
                    self.moves = self.black_pawn_move(piece)
                elif piece.name == "K":
                    self.moves = self.king_move(piece)
                elif piece.name == "Q":
                    self.moves = self.queen_move(piece)
                elif piece.name == "B":
                    self.moves = self.bishop_move(piece)
                elif piece.name == "N":
                    self.moves = self.knight_move(piece)
                elif piece.name == "R":
                    self.moves = self.rook_move(piece)
                else:
                    print("Error, never should have got here.")
                    exit()

                self.show_moves_on_canvas(self.moves)

    def king_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.game.board
        if y < 7 and (board[x][y + 1] == "" or piece.color != board[x][y + 1][0]):
            moves.append((piece.x_pos, piece.y_pos + 1))
        if y > 0 and (board[x][y - 1] == "" or piece.color != board[x][y - 1][0]):
            moves.append((piece.x_pos, piece.y_pos - 1))
        if x > 0 and (board[x-1][y] == "" or piece.color != board[x-1][y][0]):
            moves.append((piece.x_pos - 1, piece.y_pos))
        if x < 7 and (board[x+1][y] == "" or piece.color != board[x+1][y][0]):
            moves.append((piece.x_pos + 1, piece.y_pos))

        if x < 7 and y < 7 and (board[x+1][y+1] == "" or piece.color != board[x+1][y+1][0]):
            moves.append((piece.x_pos + 1, piece.y_pos + 1))
        if x < 7 and y > 0 and (board[x+1][y-1] == "" or piece.color != board[x+1][y-1][0]):
            moves.append((piece.x_pos + 1, piece.y_pos - 1))
        if x > 0 and y < 7 and (board[x-1][y+1] == "" or piece.color != board[x-1][y+1][0]):
            moves.append((piece.x_pos - 1, piece.y_pos + 1))
        if x > 0 and y > 0 and (board[x-1][y-1] == "" or piece.color != board[x-1][y-1][0]):
            moves.append((piece.x_pos - 1, piece.y_pos - 1))

        self.show_moves_on_canvas(moves)
        return moves

    def queen_move(self, piece):
        moves = self.bishop_move(piece)
        moves.extend(self.rook_move(piece))
        return moves

    def bishop_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.game.board

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
                        moves.append((new_x, new_y,))
                    break
            else:
                break

        return moves

    def knight_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.game.board
        if y > 0 and x < 7 and (board[x + 1][y - 2] == "" or piece.color != board[x + 1][y - 2][0]):
            moves.append((x + 1, y - 2,))
        if y > 0 and x > 0 and (board[x - 1][y - 2] == "" or piece.color != board[x - 1][y - 2][0]):
            moves.append((x - 1, y - 2,))
        if y < 6 and x < 7 and (board[x + 1][y + 2] == "" or piece.color != board[x + 1][y + 2][0]):
            moves.append((x + 1, y + 2,))
        if y < 6 and x > 0 and (board[x - 1][y + 2] == "" or piece.color != board[x - 1][y + 2][0]):
            moves.append((x - 1, y + 2,))
        if y > 0 and x > 1 and (board[x - 2][y - 1] == "" or piece.color != board[x - 2][y - 1][0]):
            moves.append((x - 2, y - 1,))
        if y > 0 and x < 6 and (board[x + 2][y - 1] == "" or piece.color != board[x + 2][y - 1][0]):
            moves.append((x + 2, y - 1,))
        if y < 7 and x > 1 and (board[x - 2][y + 1] == "" or piece.color != board[x - 2][y + 1][0]):
            moves.append((x - 2, y + 1,))
        if y < 7 and x < 6 and (board[x + 2][y + 1] == "" or piece.color != board[x + 2][y + 1][0]):
            moves.append((x + 2, y + 1,))
        return moves

    def rook_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.game.board
        if x < 7:
            # move right
            for i in range(x + 1, 8):
                if board[i][y] == "":
                    moves.append((i, y,))
                elif piece.color != board[i][y][0]:
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
                    moves.append((x, k,))
                    break
                else:
                    break
        if y > 0:
            # move up
            for l in range(y - 1, -1, -1):
                print(l)
                if board[x][l] == "":
                    moves.append((x, l,))
                elif piece.color != board[x][l][0]:
                    moves.append((x, l,))
                    break
                else:
                    break

        return moves

    def white_pawn_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.game.board

        if board[x][y - 1] == "":
            moves.append((x, y - 1,))
            if not piece.moved and board[x][y - 2] == "":
                moves.append((x, y - 2,))
        if x > 0 and board[x - 1][y - 1].startswith("b"):
            moves.append((x - 1, y - 1,))
        if x < 7 and board[x + 1][y - 1].startswith("b"):
            moves.append((x + 1, y - 1,))

        return moves

    def black_pawn_move(self, piece):
        moves = []
        x, y = piece.get_indices_on_board()
        board = self.game.board

        if y < 7 and board[x][y + 1] == "":
            moves.append((x, y + 1,))
            if y < 7 and not piece.moved and board[x][y + 2] == "":
                moves.append((x, y + 2,))
        if x > 0 and y < 7 and board[x - 1][y + 1].startswith("w"):
            moves.append((x - 1, y + 1,))
        if x < 7 and y < 7 and board[x + 1][y + 1].startswith("w"):
            moves.append((x + 1, y + 1,))

        return moves

