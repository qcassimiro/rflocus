#!/usr/bin/env python3


import sqlite3

from numpy import log
from scipy.spatial.distance import euclidean


def main():
    b = sqlite3.connect("rflocus.db")
    c = b.cursor()
    ns = ['a2:20:a6:14:ea:ec', 'a2:20:a6:17:37:d8', 'a2:20:a6:19:10:45', 'a2:20:a6:19:0e:30']
    ps = [[3, 11, 1], [20, 11, 1], [33, 12, 1], [0, 0, 0]]
    for x in range(1, 41):
        for y in range(1, 24):
            for z in range(1, 3):
                for n, p in zip(ns, ps):
                    d = euclidean([x, y, z], p)
                    r = int(-10 - 20 * log(d)) if d else 0
                    q = '''INSERT INTO `real` (`apid`, `rssi`, `posx`, `posy`, `posz`, `time`) VALUES ('{}', {}, {}, {}, {}, '{}')'''.format(n, r, x, y, z, 0)
                    c.execute(q)
    b.commit()
    b.close()


if __name__ == '__main__':
    main()
