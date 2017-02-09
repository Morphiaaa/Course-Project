from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution1D, MaxPooling1D
import numpy as np
import math

class ValueFunction:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Convolution1D(64, 3, border_mode='valid', input_shape=(16, 1)))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(MaxPooling1D(pool_length=2))

        self.model.add(Convolution1D(32, 3, border_mode='valid'))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(MaxPooling1D(pool_length=2))

        self.model.add(Flatten())
        self.model.add(Dense(32,init='normal'))
        self.model.add(Activation('relu'))

        self.model.add(Dense(1,init='normal'))
        self.model.add(Activation('relu'))
        self.model.compile(loss='mean_squared_error', optimizer="sgd")
        self.dataList = list()
        self.labelList = list()

    def  get(self, grid):
        test_data = np.reshape(self.process(grid),(1,16,1))
        predictedValue = self.model.predict(test_data, batch_size=1)
        return predictedValue

    def update(self, grid, label):
        self.dataList.append(self.process(grid))
        self.labelList.append(label)
        if len(self.dataList) == 8:
            new_data = np.reshape(self.dataList,(8,16,1))
            new_label = np.reshape(self.labelList,(8,1))
            self.model.fit(new_data, new_label, nb_epoch=1, batch_size=8)
            self.dataList = list()
            self.labelList = list()

    def saveWeight(self, weightID):
        #self.model.save_weights('my_model_weights.h5')
        self.model.save_weights(weightID + '.h5')

    def process(self,grid):
        zeros = (grid == 0)
        grid = grid + zeros
        grid = np.log2(grid)
        grid = grid/10.0
        return grid
