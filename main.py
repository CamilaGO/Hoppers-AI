from hopper import Hopper

hopper = Hopper()
print("=======================================")
ready = input("Ready to play Hoppers with AI? y/n: ")
if ready == "y":
    #se empieza el juego
    print("\n================== GAME STARTED ==================\n")
    while hopper.deter_ganador() == None:
        i = 0
        for fila in hopper.tablero:
            if fila == hopper.tablero[0]:
                print("    0  1  2  3  4  5  6  7  8  9")
                print("  |*******************************|")
            for casilla in fila:
                if casilla == fila[0]:
                    print(i,"|", end=" ")
                print(casilla.ficha, end="  ")
                if casilla == fila[-1]:
                    print("|",i, end=" ")
            print()
            i += 1
            if fila == hopper.tablero[-1]:
                print("  |*******************************|")
                print("    0  1  2  3  4  5  6  7  8  9")
        #print("  |*******************************|")
        hopper.ejecutar_mov_humano()
elif ready == "n":
    print("\nBye!!!")
else:
    print("\nRespuesta invalida")