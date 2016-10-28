import sys
import socket
import time
from random import randint
from Node import Node
t1 = 0.0  # the amount of time remaining to player 1
t2 = 0.0  # the amount of time remaining to player 2

state = [[0 for x in range(8)] for y in range(8)]  # state[0][0] is the bottom left corner of the board (on the GUI)


# You should modify this function
# validMoves is a list of valid locations that you could place your "stone" on this turn
# Note that "state" is a global variable 2D list that shows the state of the game
def move(validMoves):
    # just return a random move
    myMove = randint(0, len(validMoves) - 1)

    return myMove


# establishes a connection with the server
def initClient(me, thehost):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (thehost, 3333 + me)
    print >> sys.stderr, 'starting up on %s port %s' % server_address
    sock.connect(server_address)

    info = sock.recv(1024)

    print info

    return sock


# reads messages from the server
def readMessage(sock):
    mensaje = sock.recv(1024).split("\n")
    # print mensaje

    turn = int(mensaje[0])
    print "Turn: " + str(turn)

    if turn == -999:
        time.sleep(1)
        sys.exit()

    roundNum = int(mensaje[1])
    print "Round: " + str(roundNum)
    t1 = float(mensaje[2])  # update of the amount of time available to player 1
    # print t1
    t2 = float(mensaje[3])  # update of the amount of time available to player 2
    # print t2

    count = 4
    for i in range(8):
        for j in range(8):
            state[i][j] = int(mensaje[count])
            count += 1
        print state[i]

    return turn, roundNum


# main function that (1) establishes a connection with the server, and then plays whenever it is this player's turn
def playGame(me, thehost):
    # create a random number generator

    sock = initClient(me, thehost)

    while True:
        print "Read"
        status = readMessage(sock)

        if status[0] == me:
            print "Move"

            rootNode = Node(state, True, None, status[1])

            validMoves = rootNode.getValidMoves(status[1], me)
            print validMoves

            myMove = rootNode.bestMove

            sel = str(validMoves[myMove][0]) + "\n" + str(validMoves[myMove][1]) + "\n"
            print "<" + sel + ">"
            sock.send(sel)
            print "sent the message"
        else:
            print "It isn't my turn"

    return


# call: python AIGuy.py [ipaddress] [player_number]
#   ipaddress is the ipaddress on the computer the server was launched on.  Enter "localhost" if it is on the same computer
#   player_number is 1 (for the black player) and 2 (for the white player)
if __name__ == "__main__":
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    print str(sys.argv[1])

    playGame(int(sys.argv[2]), sys.argv[1])
