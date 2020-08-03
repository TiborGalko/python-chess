from piece import Piece


class ChessGame:
    """ Class representing chess game """
    def __init__(self):
        self.white_pieces = dict({
            "K": Piece("e1", "e1", "klt.png", "w", x_pos=4, y_pos=7, name="K"),
            "Q": Piece("d1", "d1", "qlt.png", "w", x_pos=3, y_pos=7, name="Q"),
            "B1": Piece("c1", "c1", "blt.png", "w", x_pos=2, y_pos=7, name="B"),
            "B2": Piece("f1", "f1", "blt.png", "w", x_pos=5, y_pos=7, name="B"),
            "N1": Piece("b1", "b1", "nlt.png", "w", x_pos=1, y_pos=7, name="N"),
            "N2": Piece("g1", "g1", "nlt.png", "w", x_pos=6, y_pos=7, name="N"),
            "R1": Piece("a1", "a1", "rlt.png", "w", x_pos=0, y_pos=7, name="R"),
            "R2": Piece("h1", "h1", "rlt.png", "w", x_pos=7, y_pos=7, name="R"),
            "P1": Piece("a2", "a2", "plt.png", "w", x_pos=0, y_pos=6),
            "P2": Piece("b2", "b2", "plt.png", "w", x_pos=1, y_pos=6),
            "P3": Piece("c2", "c2", "plt.png", "w", x_pos=2, y_pos=6),
            "P4": Piece("d2", "d2", "plt.png", "w", x_pos=3, y_pos=6),
            "P5": Piece("e2", "e2", "plt.png", "w", x_pos=4, y_pos=6),
            "P6": Piece("f2", "f2", "plt.png", "w", x_pos=5, y_pos=6),
            "P7": Piece("g2", "g2", "plt.png", "w", x_pos=6, y_pos=6),
            "P8": Piece("h2", "h2", "plt.png", "w", x_pos=7, y_pos=6),
        })

        self.black_pieces = dict({
            "K": Piece("e8", "e8", "kdt.png", "b", x_pos=4, y_pos=0, name="K"),
            "Q": Piece("d8", "d8", "qdt.png", "b", x_pos=3, y_pos=0, name="Q"),
            "B1": Piece("c8", "c8", "bdt.png", "b", x_pos=2, y_pos=0, name="B"),
            "B2": Piece("f8", "f8", "bdt.png", "b", x_pos=5, y_pos=0, name="B"),
            "N1": Piece("b8", "b8", "ndt.png", "b", x_pos=1, y_pos=0, name="N"),
            "N2": Piece("g8", "g8", "ndt.png", "b", x_pos=6, y_pos=0, name="N"),
            "R1": Piece("a8", "a8", "rdt.png", "b", x_pos=0, y_pos=0, name="R"),
            "R2": Piece("h8", "h8", "rdt.png", "b", x_pos=7, y_pos=0, name="R"),
            "P1": Piece("a7", "a7", "pdt.png", "b", x_pos=0, y_pos=1),
            "P2": Piece("b7", "b7", "pdt.png", "b", x_pos=1, y_pos=1),
            "P3": Piece("c7", "c7", "pdt.png", "b", x_pos=2, y_pos=1),
            "P4": Piece("d7", "d7", "pdt.png", "b", x_pos=3, y_pos=1),
            "P5": Piece("e7", "e7", "pdt.png", "b", x_pos=4, y_pos=1),
            "P6": Piece("f7", "f7", "pdt.png", "b", x_pos=5, y_pos=1),
            "P7": Piece("g7", "g7", "pdt.png", "b", x_pos=6, y_pos=1),
            "P8": Piece("h7", "h7", "pdt.png", "b", x_pos=7, y_pos=1),
        })

        # [RIADOK][STLPEC] 0,0 je naspodu vlavo
        self.board = [["" for j in range(8)] for i in range(8)]

        for k, v in self.white_pieces.items():
            self.board[v.x_pos][v.y_pos] = "w" + k
        for k, v in self.black_pieces.items():
            self.board[v.x_pos][v.y_pos] = "b" + k

        #pprint(self.board)

        self.current_player_color = "w"  # White starts game

        self.score_sheet = []

        self.current_turn = 1

        # Check whether game started to turn on timers
        self.game_started = False

    def next_move(self):
        if self.current_player_color == "w":
            self.current_player_color = "b"
            return self.current_player_color
        elif self.current_player_color == "b":
            self.current_player_color = "w"
            self.current_turn += 1
            return self.current_player_color
