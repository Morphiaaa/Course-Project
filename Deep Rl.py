from game2048 import *
from valueFunction import ValueFunction
import random
from datetime import datetime
import json

class memory_buffer:
    def __init__(self, size, gamma, lamda):
        self.max_size = size
        self.buffer = []
        self.gamma = gamma
        self.lamda = lamda
    def push(self, s):
        buffer = self.buffer
        buffer.append(s)
        if len(buffer) > self.max_size:
            del buffer[0]

    def randomGet(self):
        length = len(self.buffer)
        ind = random.randint(0, length - 1)
        factor = (self.lamda * self.gamma) ** ind
        return [factor, self.buffer[- ind - 1]]


class deepRL:
    def __init__(self, episode, valueFunc, T=2000, gamma=0.99):
        self.episode = episode
        self.valueFunc = valueFunc
        self.T = T
        self.gamma = gamma
        self.lamda= 0.9
        self.epsilon = 0.5
        self.buffer_size = 5
        self.savefile = datetime.now().strftime('%Y-%m-%d %Hh%Mm')

    def getOptimalAction(self, state, epsilon):
        actions = state.getAvailableActions()
        if len(actions) == 1:
            return actions[0]
        if random.random() < epsilon:
            return random.sample(actions, 1)[0]
        else:
            expectation = [self.Q(state, a) for a in actions]
            return np.argmax(expectation)

    def get_epsilon(self):
        min_ep = 0.05
        if self.epsilon > min_ep:
            self.epsilon -= (self.epsilon - min_ep) / (5 * self.T)
        return  self.epsilon


    def Q(self, s, a, m = 3):
        gamma = self.gamma
        states = s.move(a, m)
        values = [r + gamma * self.valueFunc.get(state) for r, state in states]
        return sum(values) / m

    def train(self):
        valueFunc = self.valueFunc
        for episode in xrange(self.episode):
            game = game2048()
            buffer = memory_buffer(self.buffer_size, self.gamma, self.lamda)
            s_t = game.state
            grid = s_t.grid
            v_st = valueFunc.get(grid)
            for t in xrange(self.T):
                buffer.push([s_t.grid, v_st])
                if game.gameover:
                    break
                a_t = self.getOptimalAction(s_t, self.get_epsilon())
                game.operation(a_t)
                s_t1 = game.state
                if game.gameover:
                    v_st1 = 0
                else:
                    v_st1 = valueFunc.get(s_t1.grid)
                r = np.log2(game.reward)
                delta = r + self.gamma * v_st1 - v_st
                factor, [s0, y0] = buffer.randomGet()
                valueFunc.update(s0, y0 + factor * delta)
                s_t = s_t1
                v_st = v_st1
            result = {"episode": episode + 1, "steps": game.steps, "score": game.score, "max": np.max(game.state.grid)}
            self.saveEpisode(result)
            #print result
        self.valueFunc.saveWeight(self.savefile + " weights")

    def saveEpisode(self, d):
        with open(self.savefile, 'a') as outfile:
            json.dump(d, outfile)
            outfile.write('\n')

if __name__ == '__main__':
    func = ValueFunction()
    learner = deepRL(100, func)
    learner.train()
