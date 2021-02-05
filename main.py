from hopper import Hopper

hopper = Hopper()
while hopper.find_winner() == None:
    for i in hopper.tablero:
        for j in i:
            print(j.piece, end=" ")
        print()
    print("------------------------------------")
    hopper.execute_player_move()