class Node(object):
    def __init__(self, state, isMax, parent):
        self.state = state
        self.isMax = isMax
        self.parent = parent
        self.bestVal = 0  # assign to value of the state
        self.bestMove = [None, None]
        self.calc_value()

    def calc_value(self):
        # get possible moves

        # for each possible move
        # at least once - get value of move
        #
        # if value is 'WORSE?' than our parents best ... break
        # update personal best

        pass

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
        print "Round: " + str(roundNum)

        for i in range(8):
            print self.state[i]

        if roundNum < 4:
            if self.state[3][3] == 0:
                validMoves.append([3, 3])
            if self.state[3][4] == 0:
                validMoves.append([3, 4])
            if self.state[4][3] == 0:
                validMoves.append([4, 3])
            if self.state[4][4] == 0:
                validMoves.append([4, 4])
        else:
            for i in range(8):
                for j in range(8):
                    if self.state[i][j] == 0:
                        if self.couldBe(i, j, me):
                            validMoves.append([i, j])

        return validMoves
