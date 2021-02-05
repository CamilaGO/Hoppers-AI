""" Paula Camila Gonzalez Ortega
carnet 18398 - Inteligencia Artificial
Febrero 2021 - Semestre 7 """

import sys
import time
import math

from casilla import Casilla


class Hopper():

    def __init__(self, tab_size=10, t_limit=60, c_player=Casilla.P_RED):

        # Create initial tablero
        tablero = [[None] * tab_size for _ in range(tab_size)]
        
        for row in range(tab_size):
            for col in range(tab_size):

                if row + col < 5:
                    element = Casilla(2, 2, row, col)
                elif 1 + row + col > 2 * (tab_size - 3):
                    
                    element = Casilla(1, 1, row, col)
                else:
                    element = Casilla(0, 0, row, col)

                tablero[row][col] = element
        #print(tablero)
        # Save member variables
        self.tab_size = tab_size
        self.t_limit = t_limit
        self.c_player = c_player
        self.tablero = tablero
        self.current_player = Casilla.P_GREEN
        self.selected_casilla = None
        self.valid_moves = []
        self.computing = False
        self.total_plies = 0

        self.ply_depth = 3
        self.ab_enabled = True

        self.r_goals = [t for row in tablero
                        for t in row if t.casilla == Casilla.T_RED]
        self.g_goals = [t for row in tablero
                        for t in row if t.casilla == Casilla.T_GREEN]

        if self.c_player == self.current_player:
            print("hooola")
            self.execute_computer_move()
        
        print("JUGADOr:")
        print(c_player)

        # Print initial program info
        print("Hopper Solver Basic Information")
        print("==============================")
        print("AI opponent enabled:", "no" if self.c_player is None else "yes")
        print("A-B pruning enabled:", "yes" if self.ab_enabled else "no")
        print("Turn time limit:", self.t_limit)
        print("Max ply depth:", self.ply_depth)
        print()

    def casilla_clicked(self, row, col):
        """row = input("Ingrese tecla que desea mover:")
        col = input("Ingrese posición nueva :")"""
        print(row, col)

        if self.computing:  # Block clicks while computing
            return

        new_casilla = self.tablero[row][col]

        # If we are selecting a friendly piece
        if new_casilla.piece == self.current_player:

            self.outline_casillas(None)  # Reset outlines

            # Outline the new and valid move casillas
            new_casilla.outline = Casilla.O_MOVED
            self.valid_moves = self.get_moves_at_casilla(new_casilla,
                self.current_player)
            self.outline_casillas(self.valid_moves)

            # Update status and save the new casilla
            print("Casilla `" + str(new_casilla) + "` selected")
            self.selected_casilla = new_casilla

        # If we already had a piece selected and we are moving a piece
        elif self.selected_casilla and new_casilla in self.valid_moves:
            """selected = input("Ingrese tecla que desea mover:")
            move_to = input("Ingrese posición nueva :")"""
            
            self.outline_casillas(None)  # Reset outlines
            print("******************************")
            print(self.selected_casilla, new_casilla)
            self.move_piece(self.selected_casilla, new_casilla)  # Move the piece

            # Update status and reset tracking variables
            self.selected_casilla = None
            self.valid_moves = []
            self.current_player = (Casilla.P_RED
                if self.current_player == Casilla.P_GREEN else Casilla.P_GREEN)

            # If there is a winner to the game
            winner = self.find_winner()
            if winner:
                print("The " + ("green"
                    if winner == Casilla.P_GREEN else "red") + " player has won!")
                self.current_player = None

            elif self.c_player is not None:
                self.execute_computer_move()

        else:
            print("Invalid move attempted")

    def minimax(self, depth, player_to_max, max_time, a=float("-inf"),
                b=float("inf"), maxing=True, prunes=0, tableros=0):

        # Bottomed out base case
        if depth == 0 or self.find_winner() or time.time() > max_time:
            return self.utility_distance(player_to_max), None, prunes, tableros

        # Setup initial variables and find moves
        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.get_next_moves(player_to_max)
        else:
            best_val = float("inf")
            moves = self.get_next_moves((Casilla.P_RED
                    if player_to_max == Casilla.P_GREEN else Casilla.P_GREEN))
        # For each move
        for move in moves:
            #print(move)
            for to in move["to"]:
                #print(to)

                # Bail out when we're out of time
                if time.time() > max_time:
                    return best_val, best_move, prunes, tableros

                # Move piece to the move outlined
                piece = move["from"].piece
                move["from"].piece = Casilla.P_NONE
                to.piece = piece
                tableros += 1

                # Recursively call self
                #se vuelve a llamar de acuerdo a la profundidad programada para poder ver la mejor jugada a largo plazo
                val, _, new_prunes, new_tableros = self.minimax(depth - 1,
                    player_to_max, max_time, a, b, not maxing, prunes, tableros)
                prunes = new_prunes
                tableros = new_tableros

                # Move the piece back
                to.piece = Casilla.P_NONE
                move["from"].piece = piece

                if maxing and val > best_val:
                    best_val = val
                    """print("*************************")
                    print(to.loc)"""
                    best_move = (move["from"].loc, to.loc)
                    a = max(a, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    b = min(b, val)

                if self.ab_enabled and b <= a:
                    return best_val, best_move, prunes + 1, tableros

        return best_val, best_move, prunes, tableros

    def execute_computer_move(self):
        #print(self.c_player, "c_player")

        # Print out search information
        current_turn = (self.total_plies // 2) + 1
        print("Turn", current_turn, "Computation")
        print("=================" + ("=" * len(str(current_turn))))
        print("Executing search ...", end=" ")
        sys.stdout.flush()

        # self.tablero_view.set_status("Computing next move...")
        self.computing = True
        max_time = time.time() + self.t_limit

        # Execute minimax search
        start = time.time()
        _, move, prunes, tableros = self.minimax(self.ply_depth,
            self.c_player, max_time)
        end = time.time()

        # Print search result stats
        print("complete")
        print("Time to compute:", round(end - start, 4))
        print("Total tableros generated:", tableros)
        print("Total prune events:", prunes)

        # Move the resulting piece
        self.outline_casillas(None)  # Reset outlines
        """MOVE ES EL MOVIMIENTO DE AI"""
        print("MOVEEE")
        print(move)
        move_from = self.tablero[move[0][0]][move[0][1]]
        move_to = self.tablero[move[1][0]][move[1][1]]
        self.move_piece(move_from, move_to)

        winner = self.find_winner()
        if winner:
            print("The " + ("green"
                if winner == Casilla.P_GREEN else "red") + " player has won!")
            self.current_player = None

            print()
            print("Final Stats")
            print("===========")
            print("Final winner:", "green"
                if winner == Casilla.P_GREEN else "red")
            print("Total # of plies:", self.total_plies)

        else:  # Toggle the current player
            self.current_player = (Casilla.P_RED
                if self.current_player == Casilla.P_GREEN else Casilla.P_GREEN)

        self.computing = False
        print()

    def get_next_moves(self, player=1):

        moves = []  # All possible moves
        for col in range(self.tab_size):
            for row in range(self.tab_size):

                curr_casilla = self.tablero[row][col]

                # Skip tablero elements that are not the current player
                if curr_casilla.piece != player:
                    continue

                move = {
                    "from": curr_casilla,
                    "to": self.get_moves_at_casilla(curr_casilla, player)
                }
                moves.append(move)

        return moves

    def get_moves_at_casilla(self, casilla, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = casilla.loc[0]
        col = casilla.loc[1]

        # List of valid casilla types to move to
        valid_casillas = [Casilla.T_NONE, Casilla.T_GREEN, Casilla.T_RED]
        if casilla.casilla != player:
            #print("ya estas aqui men")
            valid_casillas.remove(player)  # Moving back into your own goal
        if casilla.casilla != Casilla.T_NONE and casilla.casilla != player:
            #print("pa que te vassssss")
            valid_casillas.remove(Casilla.T_NONE)  # Moving out of the enemy's goal

        # Find and save immediately adjacent moves
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Check adjacent casillas

                new_row = row + row_delta
                new_col = col + col_delta

                # Skip checking degenerate values
                #para revisar que no me estoy saliendo del tablero
                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.tab_size or new_col >= self.tab_size):
                    continue

                # Handle moves out of/in to goals
                new_casilla = self.tablero[new_row][new_col]
                
                if new_casilla.casilla not in valid_casillas: # para no poder regresar a mi área después de salir
                    """print("no es valid casillas")
                    print(valid_casillas)
                    print(new_casilla.casilla)"""
                    continue
                

                if new_casilla.piece == Casilla.P_NONE:
                    if adj:  # Don't consider adjacent on subsequent calls 
                    #si hay un movimiento para seguirle dando
                        moves.append(new_casilla)
                    continue

                # Check jump casillas

                new_row = new_row + row_delta
                new_col = new_col + col_delta

                # Skip checking degenerate values
                if (new_row < 0 or new_col < 0 or
                    new_row >= self.tab_size or new_col >= self.tab_size):
                    continue

                # Handle returning moves and moves out of/in to goals
                new_casilla = self.tablero[new_row][new_col] #para no poder regresar a mi área 
                if new_casilla in moves or (new_casilla.casilla not in valid_casillas):
                    continue

                if new_casilla.piece == Casilla.P_NONE:
                    moves.insert(0, new_casilla)  # Prioritize jumps
                    self.get_moves_at_casilla(new_casilla, player, moves, False)

        return moves

    def move_piece(self, from_casilla, to_casilla):

        # Handle trying to move a non-existant piece and moving into a piece
        if from_casilla.piece == Casilla.P_NONE or to_casilla.piece != Casilla.P_NONE:
            print("Invalid move")
            return

        # Move piece
        to_casilla.piece = from_casilla.piece
        from_casilla.piece = Casilla.P_NONE

        # Update outline
        to_casilla.outline = Casilla.O_MOVED
        from_casilla.outline = Casilla.O_MOVED

        self.total_plies += 1

        print("Piece moved from `" + str(from_casilla) +
            "` to `" + str(to_casilla) + "`, " + ("green's" if
            self.current_player == Casilla.P_RED else "red's") + " turn...")

    def find_winner(self):

        if all(g.piece == Casilla.P_GREEN for g in self.r_goals):
            return Casilla.P_GREEN
        elif all(g.piece == Casilla.P_RED for g in self.g_goals):
            return Casilla.P_RED
        else:
            return None

    def outline_casillas(self, casillas=[], outline_type=Casilla.O_SELECT):

        if casillas is None:
            casillas = [j for i in self.tablero for j in i]
            outline_type = Casilla.O_NONE

        for casilla in casillas:
            casilla.outline = outline_type

    def utility_distance(self, player):

        def point_distance(p0, p1):
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0

        for col in range(self.tab_size):
            for row in range(self.tab_size):

                casilla = self.tablero[row][col]

                if casilla.piece == Casilla.P_GREEN:
                    distances = [point_distance(casilla.loc, g.loc) for g in
                                 self.r_goals if g.piece != Casilla.P_GREEN]
                    value -= max(distances) if len(distances) else -50

                elif casilla.piece == Casilla.P_RED:
                    distances = [point_distance(casilla.loc, g.loc) for g in
                                 self.g_goals if g.piece != Casilla.P_RED]
                    value += max(distances) if len(distances) else -50

        if player == Casilla.P_RED:
            value *= -1

        return value
    
    #mi jugada
    def execute_player_move(self):

        current_turn = (self.total_plies // 2) + 1
        print("Turn", current_turn, "Player")
        print("=================" + ("=" * len(str(current_turn))))
        sys.stdout.flush()

        row_old = int(input("Ingrese fila actual: "))
        col_old = int(input("Ingrese columna actual: "))

        row_new = int(input("Ingrese fila objetivo: "))
        col_new = int(input("Ingrese columna objetivo: "))
        
        move_from = self.tablero[row_old][col_old]
        move_to = self.tablero[row_new][col_new]
        self.move_piece(move_from, move_to)

        winner = self.find_winner()
        #print(self.c_player, "c_player")
        if winner:
            print("The " + ("green"
                if winner == Casilla.P_GREEN else "red") + " player has won!")
            self.current_player = None

            print()
            print("Final Stats")
            print("===========")
            print("Final winner:", "green"
                if winner == Casilla.P_GREEN else "red")
            print("Total # of plies:", self.total_plies)
        elif self.c_player is not None:
            self.execute_computer_move()
        else:  # Toggle the current player
            self.current_player = (Casilla.P_RED
                if self.current_player == Casilla.P_GREEN else Casilla.P_GREEN)
