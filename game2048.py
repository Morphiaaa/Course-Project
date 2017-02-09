import numpy as np
import random
import Minimax as mm

class in2048:
    def __init__(self, grid=None):
        if grid is not None:
            self.grid = grid
        else:
            self.grid = np.zeros([4, 4])
            for i in xrange(2):
                self.grid = self.addRandomTile(self.grid)
        self.states = [None, None, None, None];

    def availableCell(self, grid):
        return np.argwhere(grid == 0)

    def randomAvailableCell(self, grid):
        pos = self.availableCell(grid)
        if len(pos):
            return random.sample(pos, 1)
        return None

    def addRandomTile(self, grid):
        ngrid = grid.copy()
        value = np.random.choice([2, 4], 1, p=[0.9, 0.1])
        pos = self.randomAvailableCell(ngrid)[0]
        ngrid[tuple(pos)] = value
        return ngrid

    def getActions(self):
        s = self.grid
        states = [s, np.flipud(s.T), np.flipud(s), s.T]
        reward = np.zeros(4)
        for i, state in enumerate(states):
            reward[i], states[i] = self.getState(state)
        states[1:4] = np.flipud(states[1]).T, np.flipud(states[2]), states[3].T
        for i, state in enumerate(states):
            if not np.array_equal(s, state):
                self.states[i] = [reward[i], state]
            else:
                self.states[i] = None
        return self.getAvailableActions()

    def getAvailableActions(self):
        return [i for i, v in enumerate(self.states) if v is not None]

    def getState(self, grid):  # move up
        reward = 0
        grid = grid.copy()
        for col in xrange(4):
            prow, value = -1, -1
            for row in xrange(4):
                v = grid[row, col]
                if v > 0:
                    if v == value:
                        value = 2 * v
                        reward = reward + value
                        grid[row, col] = 0
                        grid[prow, col] = value
                        value = -1
                    else:
                        prow = prow + 1
                        value = v
                        if row > prow:
                            grid[prow, col] = v
                            grid[row, col] = 0
        return [reward, grid]

    def move(self, operation, results_num=1):
        # 0:up 1:right 2:down 3:left
        state = self.states[operation]
        if state is None:
            return [[0, self.grid]]
        results = []
        r = state[0]
        s = state[1]
        for i in xrange(results_num):
            results.append([r, self.addRandomTile(s)])
        return results


class game2048:
    def __init__(self, grid = None):
        if grid is None:
            self.state = in2048()
        else:
            self.state = in2048(grid)
        self.updateState()
        self.score = 0
        self.steps = 0
        self.reward = 0
        self.gameover = False

    def operation(self, op = None):
        reward, state = self.state.move(op)[0]
        self.state = in2048(state)
        self.updateState()
        self.reward = reward
        self.score += reward
        self.steps += 1
        self.display()


    def updateState(self):
        a = self.state.getActions()
        self.gameover = not bool(a)

    def display(self):
        grid = np.int_(self.state.grid)
        print('{0:4} {1:4} {2:4} {3:4}'.format(grid[0][0], grid[0][1], grid[0][2], grid[0][3]))
        print('{0:4} {1:4} {2:4} {3:4}'.format(grid[1][0], grid[1][1], grid[1][2], grid[1][3]))
        print('{0:4} {1:4} {2:4} {3:4}'.format(grid[2][0], grid[2][1], grid[2][2], grid[2][3]))
        print('{0:4} {1:4} {2:4} {3:4}'.format(grid[3][0], grid[3][1], grid[3][2], grid[3][3]))
        print('reward: {0:4}'.format(self.reward))
        print('score: {0:4}'.format(self.score))
        print('steps: {0:4}'.format(self.steps))
        print('actions: {0:4}'.format(self.state.getAvailableActions()))


    def play(self):
        self.display()
        s = in2048()
        m = mm.miniMax(s)
        while not self.gameover:
            #op = raw_input('operator: ')
            #print ("AI")
            op = m.find_best_move(s,3)
            #commands = ['w','d','s','a']
            #op = commands.index(op)
            self.operation(op)
            self.display()
        # self.display()
        # while not self.gameover:
        #     op = raw_input('operator: ')
        #     commands = ['w','d','s','a']
        #     op = commands.index(op)
        #     self.operation(op)
        #     self.display()


if __name__ == '__main__':
    newgame = game2048()
    newgame.play()
