import sys
import socket
import time
from random import randint
from ReversiAI_Python_v3 import Node
from threading import Thread


class AiGuyThread(Thread):
    # ADAPTED FROM MAIN CALL
    # call: python AIGuy.py [ipaddress] [player_number]
    #   ipaddress is the ipaddress on the computer the server was launched on.  Enter "localhost" if it is on the same computer
    #   player_number is 1 (for the black player) and 2 (for the white player)
    #   searchDepth
    def __init__(self, ipadr, player_num, search_depth):
        Thread.__init__(self)
        self.t1 = 0.0  # the amount of time remaining to player 1
        self.t2 = 0.0  # the amount of time remaining to player 2
        self.state = [[0 for x in range(8)] for y in
                      range(8)]  # state[0][0] is the bottom left corner of the board (on the GUI)

        self.playGame(int(player_num), ipadr, search_depth)

    def run(self):
        pass

    # You should modify this function
    # validMoves is a list of valid locations that you could place your "stone" on this turn
    # Note that "state" is a global variable 2D list that shows the state of the game
    def move(self, validMoves):
        # just return a random move
        myMove = randint(0, len(validMoves) - 1)

        return myMove


    # establishes a connection with the server
    def init_client(self, me, thehost):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (thehost, 3333 + me)
        sock.connect(server_address)

        info = sock.recv(1024)
        print(info)

        return sock


    # reads messages from the server
    def read_message(self, sock):
        message = sock.recv(1024).split("\n")
        # print message
        turn = int(message[0])
        print("Turn: " + str(turn))

        if turn == -999:
            time.sleep(1)
            sys.exit()

        round_num = int(message[1])
        self.t1 = float(message[2])  # update of the amount of time available to player 1
        self.t2 = float(message[3])  # update of the amount of time available to player 2

        count = 4
        for i in range(8):
            for j in range(8):
                self.state[i][j] = int(message[count])
                count += 1

        return turn, round_num


    # main function that (1) establishes a connection with the server, and then plays whenever it is this player's turn
    def playGame(self, me, thehost, searchDepth):
        # create a random number generator

        sock = self.init_client(me, thehost)

        while True:
            print("Read")
            status = self.read_message(sock)

            if status[0] == me:
                print("Move")

                root_node = Node(self.state, None, True, None, status[1], me, int(searchDepth))
                my_move = root_node.calc_best_move()[1]

                sel = str(my_move[0]) + "\n" + str(my_move[1]) + "\n"

                print("<" + sel + ">")
                sock.send(sel)
                print("sent the message")
            else:
                print("It isn't my turn")

        return


if __name__ == '__main__':
    ai = AiGuyThread(sys.argv[1], sys.argv[2], sys.argv[3])
