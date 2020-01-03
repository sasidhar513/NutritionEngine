import operator
import functools
import numpy as np
import pickle
import os
import constants


def range_cost(x, theta, y_min, y_max):
    pass


def compute_cost(x, theta, y):
    pred = dot_product(x, theta)
    return sum(sum((y-pred)**2))


def dot_product(x, theta):
    product = x*theta
    return np.array([functools.reduce(operator.add, lis) for lis in product])


def gradient_descent(x, y, theta):
    nutrients_count = x.shape[2]
    input_sample_size = x.shape[0]
    temp_theta = np.zeros(shape=theta.shape)
    for i in range(0, theta.shape[0]):
        temp_theta[i] = [
            (constants.ALPHA/input_sample_size) * sum(sum(((
                (dot_product(x, theta)-y)
                * x[:, i:i+1].reshape(input_sample_size, nutrients_count)
            ))))
        ] * nutrients_count
    for i in range(0, theta.shape[0]):
        theta[i] = theta[i] - temp_theta[i]
    for i in range(0, theta.shape[0]):
        theta[i] = [max(x, 0) for x in theta[i]]
