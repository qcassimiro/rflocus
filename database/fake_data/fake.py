#!/usr/bin/env python3


import sqlite3

from numpy import log
from scipy.spatial.distance import euclidean


def main():
    b = sqlite3.connect("fake.db")
    c = b.cursor()
    with open("schema.sql") as s:
        q = s.read()
        c.executescript(q)
    ns = ['A', 'B', 'C', 'D']
    ps = [[8, 18, 2], [8, 8, 2], [32, 18, 2], [32, 5, 2]]
    for x in range(1, 24):
        for y in range(1, 41):
            for z in range(1, 3):
                for n, p in zip(ns, ps):
                    d = euclidean([x, y, z], p)
                    r = int(-10 - 20 * log(d)) if d else 0
                    print("{}\t{}\t{}\t{}\t{}".format(n, r, x, y, z))
                    q = '''INSERT INTO `real` (`apid`, `rssi`, `posx`, `posy`, `posz`, `time`) VALUES ('{}', {}, {}, {}, {}, '{}')'''.format(n, r, x, y, z, 0)
                    c.execute(q)
                print("---")
    b.commit()
    b.close()


if __name__ == '__main__':
    main()
