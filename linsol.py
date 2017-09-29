import numpy
import pprint

# https://www.pozyx.io/Documentation/how_does_positioning_work
# https://stackoverflow.com/questions/9747227/2d-trilateration

if __name__ == '__main__':
    pprint.pprint(numpy.linalg.solve([[3, 1], [1, 2]], [9, 8]))
