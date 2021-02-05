from hopper import Hopper

hopper = Hopper()
while hopper.find_winner() == None:
    print("Primera fila: ", hopper.tablero[0])
    i = 0
    print("\nTABLERO")
    for fila in hopper.tablero:
        if fila == hopper.tablero[0]:
            print("    0  1  2  3  4  5  6  7  8  9")
            print("  |*******************************|")
        for casilla in fila:
            if casilla == fila[0]:
                print(i,"|", end=" ")
            print(casilla.piece, end="  ")
            if casilla == fila[-1]:
                print("|",i, end=" ")
        print()
        i += 1
        if fila == hopper.tablero[-1]:
            print("  |*******************************|")
            print("    0  1  2  3  4  5  6  7  8  9")
    #print("  |*******************************|")
    hopper.execute_player_move()