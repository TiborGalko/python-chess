class Piece:
    """ Class representing chess pieces """
    def __init__(self, starting_position, position, image, color, x_pos=0, y_pos=0, name=""):
        self.starting_position = starting_position
        self.position = position
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.name = name
        self.color = color
        self.moved = False
        self.active = True

    def __str__(self):
        return self.name + self.position

    def get_indices_on_board(self):
        return self.x_pos, self.y_pos
