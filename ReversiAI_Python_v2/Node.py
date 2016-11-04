from copy import deepcopy
import logging
import time


class Node(object):
    def __init__(self, state, moveMade, isMax, parent, roundNum, me, depth):
        self.state = state
        self.moveMade = moveMade
        self.isMax = isMax
        self.parent = parent
        self.roundNum = roundNum
        self.me = me
        self.depth = depth

        self.bestVal = -64  # assign to value of the state
        self.bestMove = [None, None]
        logging.basicConfig(filename='player' + str(self.me) + '_' + str(time.time()) + '.log', level=logging.DEBUG)

    def calc_best_move(self):
        """
        returns a tuple (k, (x, y)) representing the value k after taking the best move (x,y)
        available from the set of valid moves
        :return:
        """
        if self.isMax:
            logging.info('MAX WITH THIS STARTING STATE at depth ' + str(self.depth))
        else:
            logging.info('MIN WITH THIS STARTING STATE at depth ' + str(self.depth))

        for row in reversed(self.state):
            logging.info(str(row))
        logging.info(' ')

        if self.me == 1:
            my_id = 0
            their_id = 1
        else:
            my_id = 1
            their_id = 0

        # get possible moves
        if self.isMax:
            validMoves = self.getValidMoves(self.roundNum, my_id + 1)
        else:
            validMoves = self.getValidMoves(self.roundNum, their_id + 1)

        # if this node is a designated leaf node
        if self.depth == 0 or len(validMoves) == 0:
            # return the value of this state
            return self.state_value(), self.moveMade



        # for each possible move[row][col]
        for move in validMoves:
            # at least once - create a node and calculate it's value
            temp_state = deepcopy(self.state)

            # make the move onto the given state
            # change the captured stones
            if self.isMax:
                temp_state[move[0]][move[1]] = my_id
                temp_state = self.make_move(temp_state, move, my_id)
            else:
                temp_state[move[0]][move[1]] = their_id
                temp_state = self.make_move(temp_state, move, their_id)

            next_isMax = not self.isMax
            next_roundNum = self.roundNum + 1

            move_node = Node(temp_state, move, next_isMax, self, next_roundNum, self.me, self.depth - 1)
            move_res = move_node.calc_best_move()

            if self.parent is None:
                # Handle the decision making of the root node
                if move_res[0] >= self.bestVal:
                    self.bestVal = move_res[0]
                    self.bestMove = move
            else:
                # Minimize or Maximize based on parent's best value
                if self.isMax:
                    # I am a max node and my parent is a min node
                    if move_res[0] >= self.parent.bestVal:
                        # if my move is greater than my parents, no matter how high I get they will never choose me
                        # I will now return the best choice out of all my turns
                        logging.error('pruning a MAX node')
                        return self.bestVal, self.bestMove
                    else:
                        # update personal best
                        self.bestVal = move_res[0]
                        self.bestMove = move_res[1]
                else:
                    # I am a min node and my parent is a max node
                    if move_res[0] <= self.parent.bestVal:
                        # if my move is less than my parents, no matter how low I get it, they will never choose me
                        # I will now return the best choice out of all my turns
                        logging.error('pruning a MIN node')
                        return self.bestVal, self.bestMove
                    else:
                        # update personal best
                        self.bestVal = move_res[0]
                        self.bestMove = move_res[1]

        logging.info('returning move: ' + str(self.bestMove) + '+++++++++++++++++++++++++++++++++++')
        return self.bestVal, self.bestMove

    def make_move(self, pre_state, move, player_id):
        """
        takes in a state and a move, returns the state after the move is made
        :return:
        """
        pre_state[move[0]][move[1]] = player_id + 1
        return self.changeColors(pre_state, move[0], move[1], player_id)

    def state_value(self):
        """
        calculates the difference between the white and black pieces and returns the "value" of the board
        for the player requesting the state value
        :return:
        """
        one_count = 0
        two_count = 0
        cornerVal = 10
        sideVal = 5
        basicVal = 1

        # top left corner
        if self.state[0][0] == 1:
            one_count += cornerVal
        if self.state[0][0] == 2:
            two_count += cornerVal

        # bottom left corner
        if self.state[0][7] == 1:
            one_count += cornerVal
        if self.state[0][7] == 2:
            two_count += cornerVal

        # top left corner
        if self.state[7][0] == 1:
            one_count += cornerVal
        if self.state[7][0] == 2:
            two_count += cornerVal

        # top right corner
        if self.state[7][7] == 1:
            one_count += cornerVal
        if self.state[7][7] == 2:
            two_count += cornerVal

        # top row
        for cell in range(1, 6):
            if self.state[cell][0] == 1:
                one_count += sideVal
            if self.state[cell][0] == 2:
                two_count += sideVal

        # bottom row
        for cell in range(1, 6):
            if self.state[cell][7] == 1:
                one_count += sideVal
            if self.state[cell][7] == 2:
                two_count += sideVal

        # left column
        for cell in range(1, 6):
            if self.state[0][cell] == 1:
                one_count += sideVal
            if self.state[0][cell] == 2:
                two_count += sideVal

        # right column
        for cell in range(1, 6):
            if self.state[7][cell] == 1:
                one_count += sideVal
            if self.state[7][cell] == 2:
                two_count += sideVal

        for y in range(1, 6):
            for x in range(1, 6):
                if self.state[x][y] == 1:
                    one_count += basicVal
                if self.state[x][y] == 2:
                    two_count += basicVal

        if self.me == 1:
            return one_count - two_count
        elif self.me == 2:
            return two_count - one_count
        else:
            return 0

    """
    OTHER
    """

    def changeColors(self, start_state, row, col, turn):
        for incx in range(-1, 2):
            for incy in range(-1, 2):
                if incx == 0 and incy == 0:
                    continue
                start_state = self.check_direction(start_state, row, col, incx, incy, turn)
        # for el in start_state:
        #     logging.debug(str(el))
        # logging.debug(' ')
        # logging.debug(' ')
        return start_state

    def check_direction(self, start_state, row, col, incx, incy, turn):
        sequence = []
        end_state = deepcopy(start_state)
        for i in range(1, 8):
            r = row + incy * i
            c = col + incx * i

            if (r < 0) or (r > 7) or (c < 0) or (c > 7):
                break

            sequence.append(self.state[r][c])

        count = 0
        for i in range(len(sequence)):
            if turn == 0:
                if sequence[i] == 2:
                    count += 1
                else:
                    if sequence[i] == 1 and count > 0:
                        count = 20
                    break
            else:
                if sequence[i] == 1:
                    count += 1
                else:
                    if sequence[i] == 2 and count > 0:
                        count = 20
                    break

        if count > 10:
            if turn == 0:
                i = 1
                r = row + incy * i
                c = col + incx * i
                while (end_state[r][c] == 2):
                    end_state[r][c] = 1
                    i += 1
                    r = row + incy * i
                    c = col + incx * i
            else:
                i = 1
                r = row + incy * i
                c = col + incx * i
                while (end_state[r][c] == 1):
                    end_state[r][c] = 2
                    i += 1
                    r = row + incy * i
                    c = col + incx * i

        return end_state

    """
    FROM AIguy
    """

    def checkDirection(self, row, col, incx, incy, me):
        sequence = []
        for i in range(1, 8):
            r = row + incy * i
            c = col + incx * i

            if (r < 0) or (r > 7) or (c < 0) or (c > 7):
                break

            sequence.append(self.state[r][c])

        count = 0
        for i in range(len(sequence)):
            if me == 1:
                if sequence[i] == 2:
                    count += 1
                else:
                    if (sequence[i] == 1) and (count > 0):
                        return True
                    break
            else:
                if sequence[i] == 1:
                    count += 1
                else:
                    if (sequence[i] == 2) and (count > 0):
                        return True
                    break
        return False

    def couldBe(self, row, col, me):
        for incx in range(-1, 2):
            for incy in range(-1, 2):
                if (incx == 0) and (incy == 0):
                    continue

                if self.checkDirection(row, col, incx, incy, me):
                    return True

        return False

    # generates the set of valid moves for the player; returns a list of valid moves (validMoves)
    def getValidMoves(self, roundNum, me):
        validMoves = []
        # print "Round: " + str(roundNum)

        # for i in range(8):
        #     print self.state[i]

        if roundNum < 4:
            if self.state[3][3] == 0:
                validMoves.append((3, 3))
            if self.state[3][4] == 0:
                validMoves.append((3, 4))
            if self.state[4][3] == 0:
                validMoves.append((4, 3))
            if self.state[4][4] == 0:
                validMoves.append((4, 4))
        else:
            for i in range(8):
                for j in range(8):
                    if self.state[i][j] == 0:
                        if self.couldBe(i, j, me):
                            validMoves.append((i, j))

        return validMoves
