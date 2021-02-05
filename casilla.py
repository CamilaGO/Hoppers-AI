# tipos de casilla (primer argumento)
#   0 = casilla en blanco, las de en medio
#   1 = casillas objetivo verdes, player 1 (derecha superior)
#   2 = casillas objetivo rojo, player 2 (izquierda inferior)
#
# tipos de fichas (segundo argumento) 
#   0 = sin pieza
#   1 = ficha verde, player 1
#   2 = ficha roja, player 2
#
# index 2 is the outline type
#   0 = no outline
#   1 = selected outline
#   2 = just moved


class Casilla():

    # Goal constants
    T_NONE = 0
    T_GREEN = 1
    T_RED = 2

    # Piece constants
    P_NONE = 0
    P_GREEN = 1
    P_RED = 2

    # Outline constants
    O_NONE = 0
    O_SELECT = 1
    O_MOVED = 2

    def __init__(self, casilla=0, piece=0, row=0, col=0):
        self.casilla = casilla
        """print("--------------------------")
        print(self.casilla)"""
        self.piece = piece
        #print(self.piece)

        self.row = row
        self.col = col
        self.loc = (row, col)

    def __str__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)

    def __repr__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)