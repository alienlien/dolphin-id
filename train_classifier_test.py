#!/usr/bin/env python3
from keras.models import Sequential
from keras.layers import Dense
import train_classifier as t


def test_setup_to_transfer_learn_by_layer():
    model = Sequential()
    model.add(Dense(32, input_shape=(16, ), activation='relu'))
    model.add(Dense(16, activation='softmax'))
    model.add(Dense(32, activation='relu'))
    print('Summary:', model.summary())

    t.setup_to_transfer_learn_by_layer(model, 2)

    for layer in model.layers[:1]:
        assert not layer.trainable

    for layer in model.layers[1:]:
        assert layer.trainable
