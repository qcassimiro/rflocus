#!/usr/bin/python3

import pprint

import scipy.optimize
import scipy.spatial.distance


def errors(position, references, distances):
    errsum = 0
    for i, reference in enumerate(references):
        distance = scipy.spatial.distance.euclidean(position, reference)
        error = distance - distances[i]
        errsum += error * error
    return errsum


def main():
    real = [-2.0, -2.0]
    references = [[-4.0, 2.0], [4.0, 4.0], [2.0, -4.0], [0, 0]]
    distances = [4.47, 8.48, 4.47, 2.8]
    res = scipy.optimize.minimize(errors,
                                  [0, 0],
                                  args=(references, distances),
                                  method='powell')
    estimate = res.x
    print(estimate)

if __name__ == '__main__':
    main()
