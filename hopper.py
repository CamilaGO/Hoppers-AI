""" Paula Camila Gonzalez Ortega
carnet 18398 - Inteligencia Artificial
Febrero 2021 - Semestre 7 """

import sys
import time
import math
from xml.dom import minidom
from casilla import Casilla


class Hopper():

    def __init__(self, tab_size=10, t_limit=60, ai_player=Casilla.F_BLANCA):

        # tamaño del tablero e inicializacion de variables
        tablero = [[None] * tab_size for _ in range(tab_size)]

        self.tab_size = tab_size
        self.t_limit = t_limit
        self.ai_player = ai_player
        self.tablero = tablero
        self.current_player = Casilla.F_NEGRA #empieza a jugar el humano, jugador 1
        self.casilla_selected = None
        self.valid_movs = []
        self.calculando = False
        self.jugadas_totales = 0
        # se activa alpha-beta con profundidad 3
        self.profundidad = 3
        self.moves_ai=[]
        self.crear_tablero()


    def minimax(self, depth, player_to_max, max_time, alpha=float("-inf"),
                beta=float("inf"), maxing=True, prunes=0, tableros=0):

        if depth == 0 or self.deter_ganador() or time.time() > max_time:
            return self.distancia_util(player_to_max), None, prunes, tableros

        # variables iniciales para encontrar movimientos
        best_mov = None
        if maxing:
            best_val = float("-inf")
            movs = self.siguientes_movs(player_to_max)
        else:
            best_val = float("inf")
            movs = self.siguientes_movs((Casilla.F_BLANCA
                    if player_to_max == Casilla.F_NEGRA else Casilla.F_NEGRA))
        # revisar cada movimiento 
        for mov in movs:
            for to in mov["to"]:

                # Se acaba el tiempo
                if time.time() > max_time:
                    return best_val, best_mov, prunes, tableros

                # mover la ficha seleccionada
                ficha = mov["from"].ficha
                mov["from"].ficha = Casilla.F_VACIA
                to.ficha = ficha
                tableros += 1

                # Recursividad
                # para ver la mejor llamada a futuro se vuelve a llamar segun a la profundidad determinada
                val, _, nueva_prunes, nueva_tableros = self.minimax(depth - 1,
                    player_to_max, max_time, alpha, beta, not maxing, prunes, tableros)
                prunes = nueva_prunes
                tableros = nueva_tableros

                # se regresa la ficha
                to.ficha = Casilla.F_VACIA
                mov["from"].ficha = ficha

                if maxing and val > best_val:
                    #si es max (jugador 1)
                    best_val = val
                    best_mov = (mov["from"].posicion, to.posicion)
                    alpha = max(alpha, val)

                if not maxing and val < best_val:
                    #si no es max (jugador AI)
                    best_val = val
                    best_mov = (mov["from"].posicion, to.posicion)
                    beta = min(beta, val)

                if beta <= alpha:
                    return best_val, best_mov, prunes + 1, tableros

        return best_val, best_mov, prunes, tableros

    def ejecutar_mov_ai(self):
        print("\n___________________________________________")
        print("|     Turno de la computadora con AI      |")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
        print("Buscando la mejor movida ...")
        sys.stdout.flush()

        #se calcula los movimiento del AI
        self.calculando = True
        max_time = time.time() + self.t_limit

        # Execute minimax search
        inicio = time.time()
        _, mov, prunes, tableros = self.minimax(self.profundidad, self.ai_player, max_time)
        fin = time.time()

        #movimiento seleccionado que se ejecuta y guarda para XML
        move_from_ai = self.tablero[mov[0][0]][mov[0][1]]
        self.moves_ai = self.buscar_movs_casilla(move_from_ai, self.ai_player)

        # Se imprime el tiempo
        print("Tiempo de busqueda:", round(fin - inicio, 4))
        #print("Total tableros generados:", tableros)
        #print("Total eventos cortados:", prunes)

        # Movimiento realizado
        print("Movimiento realizado:", mov[0], "-->", mov[1])
        mov_from = self.tablero[mov[0][0]][mov[0][1]]
        mov_to = self.tablero[mov[1][0]][mov[1][1]]
        self.mover_ficha(mov_from, mov_to)

        #se guarda el path hecho
        for i in self.moves_ai:
            if (i.posicion==mov_to.posicion):
                break #para no agregar el path que no hace

        ganador = self.deter_ganador()
        if ganador:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if ganador == Casilla.F_NEGRA:
                print("El jugador 1 (humano) es el ganador!")
            else:
                print("El jugador 2 (AI) es el ganador!")
            print("¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
            self.current_player = None

            print()
            print("Total de jugadas: ", self.jugadas_totales)

        else:  # Se cambia de jugador
            self.current_player = (Casilla.F_BLANCA
                if self.current_player == Casilla.F_NEGRA else Casilla.F_NEGRA)

        self.calculando = False
        print()

        # XML de movimiento reaizado por AI
        root = minidom.Document()
  
        xml = root.createElement('move') 
        root.appendChild(xml)
        
        productChild = root.createElement('from')
        productChild.setAttribute('row', str(mov[0][0]))
        productChild.setAttribute('col', str(mov[0][1]))

        toChild = root.createElement('to')
        toChild.setAttribute('row', str(mov[1][0]))
        toChild.setAttribute('col', str(mov[1][1]))
        
        xml.appendChild(productChild)
        xml.appendChild(toChild)

        path = root.createElement('path')
        xml.appendChild(path)
        for a in reversed(self.moves_ai):
            pos1 = root.createElement('pos')
            pos1.setAttribute('row', str(a.posicion[0]))
            pos1.setAttribute('col', str(a.posicion[1]))
            path.appendChild(pos1)
            if (a.posicion==mov_to.posicion):
                break
          
        xml_str = root.toprettyxml(indent ="\t") 

        print(xml_str)
        return  

    def siguientes_movs(self, player=1):
        movs = []  # All possible movs
        for col in range(self.tab_size):
            for fila in range(self.tab_size):

                curr_casilla = self.tablero[fila][col]

                # Ignorar las fichas que no son del jugador
                if curr_casilla.ficha != player:
                    continue

                mov = {
                    "from": curr_casilla,
                    "to": self.buscar_movs_casilla(curr_casilla, player)
                }
                movs.append(mov)

        return movs

    def buscar_movs_casilla(self, casilla, player, movs=None, adj=True):
        valid_casillas = [Casilla.C_VACIA, Casilla.C_NEGRA, Casilla.C_BLANCA]

        if movs is None:
            movs = []

        fila = casilla.posicion[0]
        col = casilla.posicion[1]

    
        if casilla.casilla != player:
            #No se le permite regresar a su lado su ya salio
            valid_casillas.remove(player) 
        if casilla.casilla != Casilla.C_VACIA and casilla.casilla != player:
            #No se le permite salir si ya llego al lado del contrincante
            valid_casillas.remove(Casilla.C_VACIA)  

        # Movimientos a casillas vecinas
        for col_vecina in range(-1, 2):
            for fila_vecina in range(-1, 2):

                # Casillas adyacentes en fila y columna

                nueva_fila = fila + fila_vecina
                nueva_col = col + col_vecina

                #comprobar que el movimiento sea dentro del tablero o no sea estatico
                if ((nueva_fila == fila and nueva_col == col) or
                    nueva_fila < 0 or nueva_col < 0 or
                    nueva_fila >= self.tab_size or nueva_col >= self.tab_size):
                    continue

                # Obtener la ubicacion de la nueva casilla en el tablero
                nueva_casilla = self.tablero[nueva_fila][nueva_col]
                
                if nueva_casilla.casilla not in valid_casillas: 
                    # Movimiento invalido
                    # evita poder regresar a su área después de salir
                    continue
                

                if nueva_casilla.ficha == Casilla.F_VACIA:
                    if adj:   
                    # se siguen buscando mas movimeintos desde la nueva casilla
                        movs.append(nueva_casilla)
                    continue

                # saltar varias veces entre fichas (recursion)

                nueva_fila = nueva_fila + fila_vecina
                nueva_col = nueva_col + col_vecina

                # Ignorar ubicaciones fuera del tablero
                if (nueva_fila < 0 or nueva_col < 0 or
                    nueva_fila >= self.tab_size or nueva_col >= self.tab_size):
                    continue

                # No permitir retroceso 
                nueva_casilla = self.tablero[nueva_fila][nueva_col] 
                if nueva_casilla in movs or (nueva_casilla.casilla not in valid_casillas):
                    continue

                if nueva_casilla.ficha == Casilla.F_VACIA:
                    movs.insert(0, nueva_casilla)  # mas saltos con recursividad
                    self.buscar_movs_casilla(nueva_casilla, player, movs, False)

        return movs

    def mover_ficha(self, from_casilla, to_casilla):

        # introdujo una casilla de salida vacia o una de meta ocupada
        if from_casilla.ficha == Casilla.F_VACIA or to_casilla.ficha != Casilla.F_VACIA:
            print("Invalid mov")
            return

        # Se actualizan las casillas, es decir que se ocupa y libera 
        to_casilla.ficha = from_casilla.ficha
        from_casilla.ficha = Casilla.F_VACIA

        self.jugadas_totales += 1


    def deter_ganador(self):

        negrosListos = []
        for n in self.lado_blanco:
            if n.ficha == Casilla.F_NEGRA:
                #el negra llego a la casilla blanca
                negrosListos.append(n)
        
        blancosListos = []
        for b in self.lado_negro:
            if b.ficha == Casilla.F_BLANCA:
                #el blanco llego a la casilla negra
                blancosListos.append(b)
        
        if (negrosListos == self.lado_blanco):
            #gano el humano, devuelve 1
            return Casilla.F_NEGRA
        elif (blancosListos == self.lado_negro):
            #gano el AI, devuelve 2
            return Casilla.F_BLANCA
        else:
            #nadie gano
            return None


    def distancia_util(self, player):

        def heuristic(p0, p1):
            #basada en la lectura de http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
            D = 1
            dx = abs(p0[0] - p1[0])
            dy = abs(p0[1] - p1[1])
            return D * (dx + dy)

        value = 0
        
        for col in range(self.tab_size):
            for fila in range(self.tab_size):

                casilla = self.tablero[fila][col]

                if casilla.ficha == Casilla.F_NEGRA:
                    distances = []
                    for i in self.lado_blanco:
                        if i.ficha != Casilla.F_NEGRA:
                            distances.append(heuristic(casilla.posicion, i.posicion))

                    value -= max(distances) if len(distances) else -50

                elif casilla.ficha == Casilla.F_BLANCA:
                    distances = []
                    for i in self.lado_negro:
                        if i.ficha != Casilla.F_BLANCA:
                            distances.append(heuristic(casilla.posicion, i.posicion))

                    value += max(distances) if len(distances) else -50

        if player == Casilla.F_BLANCA:
            value *= -1

        return value
    

    def ejecutar_mov_humano(self):
        print("\n___________________________________________")
        print("|             Tu turno humano             |")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
        sys.stdout.flush()

        inputOld = (input("Ingrese fila, columna actual: "))
        oldLocation = inputOld.split(", ")

        inputNew = (input("Ingrese fila, columna objetivo: "))
        nuevaLocation = inputNew.split(", ")
        print("Movimiento realizado: ("+inputOld+") --> ("+inputNew+")" )
        
        mov_from = self.tablero[int(oldLocation[0])][int(oldLocation[1])]
        mov_to = self.tablero[int(nuevaLocation[0])][int(nuevaLocation[1])]
        self.mover_ficha(mov_from, mov_to)

        ganador = self.deter_ganador()
        if ganador:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if ganador == Casilla.F_NEGRA:
                print("El jugador 1 (humano) es el ganador!")
            else:
                print("El jugador 2 (AI) es el ganador!")
            print("¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
            self.current_player = None

            print()
            print("Total de jugadas: ", self.jugadas_totales)
        elif self.ai_player is not None:
            self.ejecutar_mov_ai()
        else:  # Se cambia de jugador
            self.current_player = (Casilla.F_BLANCA
                if self.current_player == Casilla.F_NEGRA else Casilla.F_NEGRA)

    def crear_tablero(self):
            # creacion del tablero segun la ubicacion de las casillas
            for fila in range(self.tab_size):
                for col in range(self.tab_size):

                    if fila + col < 5:
                        #si es la diagonal izquierda superior se coposicionan las fichas de AI (player 2)
                        espacio = Casilla(2, 2, fila, col)
                    elif 1 + fila + col > 2 * (self.tab_size - 3):
                        #si es la diagonal derecha inferior se coposicionan las fichas del humano (player 1)
                        espacio = Casilla(1, 1, fila, col)
                    else:
                        #si es el centro se deja en blanco, campo para jugar 
                        espacio = Casilla(0, 0, fila, col)

                    self.tablero[fila][col] = espacio

            #se ven las ubicaciones de las casilla blancas y se guardan
            self.lado_blanco = []
            for fila in self.tablero:
                for i in fila:
                    if i.casilla == Casilla.C_BLANCA:
                        self.lado_blanco.append(i)
            #se ven las ubicaciones de las casilla negras y se guardan
            self.lado_negro = []
            for fila in self.tablero:
                for i in fila:
                    if i.casilla == Casilla.C_NEGRA:
                        self.lado_negro.append(i)