from game_manager import ChessGame
from moves_manager import MovesManager
import tkinter as tk
import string
import math
from pprint import pprint
from PIL import ImageTk, Image
from time import strftime, strptime


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
        self.moves_manager = MovesManager()
        self.moving = False
        self.moving_piece = None
        self.moving_piece_key = ""
        self.actual_moves_ids = []
        self.moves = []

        self.panel_top = tk.PanedWindow(master=self, width=530, height=40)
        self.panel_top.grid(column=0, row=1)
        self.panel_mid = tk.PanedWindow(master=self, width=530, height=550)
        self.panel_mid.grid(column=0, row=2)
        self.panel_bot = tk.PanedWindow(master=self, width=530, height=40)
        self.panel_bot.grid(column=0, row=3)

        self.canvas = self.create_board()
        self.canvas.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.click_callback)
        # self.canvas.bind("<B1-Motion>", self.mouse_move_callback) TODO drag and drop ?

        self.text = []
        self.add_annotations()
        self.populate_board()

        self.text_box = self.create_text()

        # TODO konfigurovatelny cas pre tahy v nejakom menu mozno
        self.configured_time = "05:00"
        self.time_p1 = strptime(self.configured_time, "%M:%S")
        self.time_p2 = strptime(self.configured_time, "%M:%S")
        self.timers = self.create_timers()
        self.running_timer = None

    def create_board(self):
        """ Method creates new chess board on tkinter canvas and returns it"""
        canvas = tk.Canvas(master=self.panel_mid, width=530, height=550)
        canvas.configure(scrollregion=(self.offset_x, self.offset_y, 20, 20))

        # x1 y1 x2 y2
        for i in range(8):
            y = i * self.width
            for j in range(8):
                x = j * self.width
                if ((j + 1) % 2) == 0:
                    if ((i + 1) % 2) == 0:
                        canvas.create_rectangle(x, y, x + self.width, y + self.width,
                                                outline="#808080", fill="#fff")  # biela
                    else:
                        canvas.create_rectangle(x, y, x + self.width, y + self.width,
                                                outline="#808080", fill="#999")  # cierna
                else:
                    if ((i + 1) % 2) == 1:
                        canvas.create_rectangle(x, y, x + self.width, y + self.width,
                                                outline="#808080", fill="#fff")  # biela
                    else:
                        canvas.create_rectangle(x, y, x + self.width, y + self.width,
                                                outline="#808080", fill="#999")  # cierna

        return canvas

    def add_annotations(self):
        """ Method adds numbers and letters to board sides """
        for i in range(8):
            self.text.append(self.canvas.create_text(-self.width / 2,
                                                     (self.width / 2) + (i * self.width),
                                                     font=("Purisa", 12), anchor="nw"))
            self.canvas.itemconfig(self.text[i], text=str((i - 8) * -1))
        for i in range(8):
            self.text.append(self.canvas.create_text((self.width / 2) + (i * self.width),
                                                     self.width * 8 + 10, font=("Purisa", 12), anchor="nw"))
            self.canvas.itemconfig(self.text[i + 8], text=string.ascii_lowercase[i])

    def populate_board(self):
        """ Method adds images on canvas board """
        for key, value in self.game.white_pieces.items():
            x_pos = self.width * value.x_pos
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
        print("Removing image on key ", piece_position)
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

    """
    Create textbox on right side and method to write to it
    """

    def create_text(self):
        text_box = tk.Text(master=self.panel_mid, height=28, width=31)
        text_box.insert(tk.END, "Welcome.\nIt's been a long minute.\n\n")

        scrollbar = tk.Scrollbar(master=self.panel_mid, command=text_box.yview, orient=tk.VERTICAL)
        text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        text_box.configure(state=tk.DISABLED)
        text_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        return text_box

    def write_text(self, text):
        self.text_box['state'] = tk.NORMAL
        self.text_box.insert(tk.END, text)
        self.text_box['state'] = tk.DISABLED

    """
    Timers
    """

    def create_timers(self):
        timers = []

        timer1_textbox = tk.Label(master=self.panel_top, height=1, width=8)
        timer1_textbox.configure(text=str(self.time_p1.tm_min).zfill(2) + ":" + str(self.time_p1.tm_sec).zfill(2))
        timer1_textbox.pack(side=tk.TOP, expand=True)
        timers.append(timer1_textbox)

        timer2_textbox = tk.Label(master=self.panel_bot, height=1, width=8)
        timer2_textbox.configure(text=str(self.time_p2.tm_min).zfill(2) + ":" + str(self.time_p2.tm_sec).zfill(2))
        timer2_textbox.pack(side=tk.RIGHT, expand=True)
        timers.append(timer2_textbox)

        return timers

    def start_opponents_timer(self, timer, p):
        """
        Starts timer on opponents clock and stops players timer
        :param timer: timer from timer array
        :param p: index of opponent 1 - white, 2 - black
        """
        if self.running_timer is not None:
            self.after_cancel(self.running_timer)
            self.running_timer = None
            self.running_timer = self.after(1000, self.show_time, timer, p)
        else:
            # First move
            self.running_timer = self.after(1000, self.show_time, timer, p)

    def show_time(self, timer, p):
        if p == 2:
            sec = self.time_p1.tm_sec
            min = self.time_p1.tm_min
        else:
            sec = self.time_p2.tm_sec
            min = self.time_p2.tm_min

        sec = sec - 1
        if sec < 0:
            sec = 59
            min = min - 1

        if min <= 0:
            # TODO ukonci hru lebo skoncil cas
            self.stop_game(p)

        if p == 2:
            self.time_p1 = strptime(str(min) + ":" + str(sec), "%M:%S")
        else:
            self.time_p2 = strptime(str(min) + ":" + str(sec), "%M:%S")

        timer.configure(text=str(min).zfill(2) + ":" + str(sec).zfill(2))
        self.running_timer = self.after(1000, self.show_time, timer, p)

    """
    Other game methods
    """

    def raise_check(self):
        # TODO dokoncit metodu
        self.write_text("CHECK!")

    def stop_game(self, p):
        print("Game stopped because of timeout, player " + str(p) + " wins")
        self.canvas.unbind("<Button-1>", self.click_callback)
        self.after_cancel(self.running_timer)
        if p == 1:
            self.write_text("# 1-0")
        else:
            self.write_text("# 0-1")

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
        # TODO
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

            made_move = string.ascii_lowercase[x] + str(((y - 8) * -1) % 9)
            if self.moving_piece.color == "w":
                self.write_text(str(self.game.current_turn) + ". ")

            # TODO CHECK FOR CHECK AND CHECK MATE
            # TODO zmenit meno pre piece po pohnuti

            print(self.moving_piece)
            print(self.moving_piece.name)

            # POPIS notacie :
            # Pawn - destination square
            # Pawn pri vyhodeni - exd5 - pesiak z e isiel na d5 a vyhodil
            # TODO En passant vyhodenia - exd6e.p. - pesiak z e isiel na d6 a vyhodil toho na e5 cez en passant
            # Ostatne Be5 - strelec sa posunul na e5, e5 je destination
            # TODO Pri vyhodeni - Bxe5 - strelec vyhodil na e5

            # TODO Ak mozu robit pohyby rovnake figurky na rovnake pole treba rozlisit, priorita
            # TODO 1. ak su rozdielne zaciatocne polia - Bdb8 je strelec ktory bol na zaciatku na d poli ak ten druhy strelec je na inom poli
            # TODO 2. zapise sa riadok ak su na rovnakom stlpci - R1a3
            # TODO 3. zapise sa riadok aj stlpec ak nestaci jeden - Qh4e1 - vyhodenie je Qh4xe1

            # TODO Zmena pesiaka na kralovnu napr. - e8Q

            # TODO Navrh remizy je oznaceny =

            # TODO Rosady (castling)
            # TODO Na strane krala - 0-0
            # TODO Na strane kralovnej - 0-0-0

            # TODO Sach (check) - prida na koniec +
            # TODO Sachmat (checkmate) - prida sa na koniec #
            # TODO Po skonceni sa 1-0 znamena ze biely vyhral, 0-1 ze cierny vyhral
            # TODO 1|2-1|2 indikuje remizu

            # TODO zistit ci sa vyhodilo alebo nie
            self.write_text(self.moving_piece.name + made_move + " ")

            # TODO nejak treba zastavit
            # Start timers
            if not self.game.game_started:
                self.game.game_started = True

            if self.game.current_player_color == 'w':
                self.start_opponents_timer(self.timers[0], 2)
            else:
                self.start_opponents_timer(self.timers[1], 1)

            self.game.next_move()

            # TODO change position too
            # TODO update on board

    def calculate_moves_for_moving_piece(self, x, y):
        """
        Calculating moves for pieces. Has to set self.moves
        :param x: x coordinate on board
        :param y: y coordinate on board
        """
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
                self.moves = self.moves_manager.get_moves(piece, self.game.board)
                self.show_moves_on_canvas(self.moves)
