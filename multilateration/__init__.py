#!/usr/bin/python3


import scipy.optimize
import scipy.spatial.distance


euclidean = scipy.spatial.distance.euclidean


def errors(position, references, distances):
    errsum = 0
    for i, reference in enumerate(references):
        distance = euclidean(position, reference)
        error = distance - distances[i]
        errsum += error * error
    return errsum


def estimate(references, distances):
    start = [0 for _ in range(len(references[0]))]
    result = scipy.optimize.minimize(errors,
                                     start,
                                     args=(references, distances),
                                     method='powell')
    return tuple(result.x)


if __name__ == '__main__':
    references = [[-4.0, 2.0], [4.0, 4.0], [2.0, -4.0], [0, 0]]
    distances = [4.47, 8.48, 4.47, 2.8]
    print(estimate(references, distances))
