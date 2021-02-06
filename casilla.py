""" Argumentos a recibir
tipos de casilla (primero)
 0 = casilla en blanco, las de en medio
 1 = casillas objetivo verdes, player 1 (derecha superior)
 2 = casillas objetivo rojo, player 2, AI (izquierda inferior)

tipos de fichas (segundo) 
 0 = sin pieza
 1 = ficha verde, player 1
 2 = ficha roja, player 2, AI
"""



class Casilla():

    # constantes segun la ubicacion de la casilla
    C_VACIA = 0
    C_VERDE = 1
    C_ROJA = 2

    # constantes segun la ficha
    F_VACIA = 0
    F_VERDE = 1
    F_ROJA = 2

    def __init__(self, casilla=0, ficha=0, fila=0, col=0):
        self.casilla = casilla #el color/valor de la casilla
        self.ficha = ficha #el color/valor de la ficha
        #print(self.ficha)

        self.fila = fila
        self.col = col
        self.posicion = (fila, col)

    def __str__(self):
        return chr(self.posicion[1] + 97) + str(self.posicion[0] + 1)

    def __repr__(self):
        return chr(self.posicion[1] + 97) + str(self.posicion[0] + 1)