from copy import deepcopy


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

    def calc_best_move(self):
        """
        returns a tuple (k, (x, y)) representing the value k after taking the best move (x,y)
        available from the set of valid moves
        :return:
        """
        print('starting calc_best_move - ' + 'depth:' + str(self.depth))
        # if this node is a designated leaf node
        if self.depth == 0:
            # return the value of this state
            print('handling depth zero case')
            return self.state_value(), self.moveMade

        # get possible moves
        print('getting valid moves')
        validMoves = self.getValidMoves(self.roundNum, self.me)

        # for each possible move
        for move in validMoves:
            print('validMove: ' + str(move))
            # at least once - create a node and calculate it's value
            temp_state = deepcopy(self.state)
            temp_state[move[0]][move[1]] = self.me
            temp_isMax = not self.isMax
            temp_roundNum = self.roundNum + 1

            move_node = Node(temp_state, move, temp_isMax, self, temp_roundNum, self.me, self.depth - 1)
            move_res = move_node.calc_best_move()
            print('moveValue: ' + str(move_res))

            if self.parent is None:
                # Handle the decision making of the root node
                if move_res[0] >= self.bestVal:
                    self.bestVal = move_res[0]
                    self.bestMove = move_res[1]
            else:
                # Minimize or Maximize based on parent's best value
                if self.isMax:
                    # I am a max node and my parent is a min node
                    if move_res[0] >= self.parent.bestVal:
                        # if my move is greater than my parents, no matter how high I get they will never choose me
                        # I will now return the best choice out of all my turns
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
                        return self.bestVal, self.bestMove
                    else:
                        # update personal best
                        self.bestVal = move_res[0]
                        self.bestMove = move_res[1]

        return self.bestVal, self.bestMove

    def state_value(self):
        """
        calculates the difference between the white and black pieces and returns the "value" of the board
        for the player requesting the state value
        :return:
        """
        one_count = 0
        two_count = 0
        for el in self.state:
            for el2 in el:
                if el2 == 1:
                    one_count += 1
                if el2 == 2:
                    two_count += 1

        if self.me == 1:
            return one_count - two_count
        elif self.me == 2:
            return two_count - one_count
        else:
            return 0

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
