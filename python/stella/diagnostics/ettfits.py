#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : ettfits.py
#
#  Purpose :
#
#  Creation Date : 23-10-2015
#
#  Last Modified : Mon 26 Oct 2015 14:17:03 CET
#
#  Created By :  
#
# _._._._._._._._._._._._._._._._._._._._._.
from __future__ import print_function
import os
import numpy as np
import matplotlib.pyplot as plt

class access_mixin(object):
    def closest_i(self, i):

        i = np.argmin(np.fabs(self.cycles - i))

        return i

    def closest_t(self, t):

        i = np.argmin(np.fabs(self.times - t))

        return i

    def xt(self, t):

        i = self.closest_t(t)

        return self.x(i)

    def yt(self, t):

        i = self.closest_t(t)

        return self.y(i)

    def xi(self, i):

        i = self.closest_i(i)

        return self.x(i)

    def yi(self, i):

        i = self.closest_i(i)

        return self.y(i)


class etts1d_reader(object):
    def __init__(self, fname):

        self.lines = open(fname, "r").readlines()

        self.headers = self.lines[::3]
        self.xdat = self.lines[1::3]
        self.ydat = self.lines[2::3]

        self.cycles = np.array([int(header.rsplit()[0]) for header in self.headers])
        self.times = np.array([float(header.rsplit()[1]) for header in self.headers])

        self.xdat = np.array([map(float, xdat.rsplit()) for xdat in self.xdat])
        self.ydat = np.array([map(float, ydat.rsplit()) for ydat in self.ydat])

    def x(self, i):

        return self.xdat[i]

    def y(self, i):

        return self.ydat[i]



class etts2d_reader(object):
    def __init__(self, fname):

        self.lines = open(fname, "r").readlines()

        self.xdat = np.array(map(float, self.lines[0].rsplit()))

        headerlocs = np.argwhere(np.array([len(line.rsplit()) for line in self.lines]) == 4).reshape(-1)
        self.cycles = []
        self.times = []
        self.nfrus = []
        self.ncnd = []
        self.ydat = []

        for i, iloc in enumerate(headerlocs[:-1]):
            tmp = self.lines[iloc].rsplit()
            assert(len(tmp) == 4)

            self.cycles.append(int(tmp[0]))
            self.times.append(float(tmp[1]))
            self.nfrus.append(int(tmp[2]))
            self.ncnd.append(int(tmp[3]))

            nlines = headerlocs[i+1]-1 - iloc

            self.ydat.append(np.loadtxt(self.lines[iloc+1:iloc+1+nlines]))

        iloc = headerlocs[-1]
        tmp = self.lines[iloc].rsplit()
        assert(len(tmp) == 4)

        self.cycles.append(int(tmp[0]))
        self.times.append(float(tmp[1]))
        self.nfrus.append(int(tmp[2]))
        self.ncnd.append(int(tmp[3]))

        self.ydat.append(np.loadtxt(self.lines[iloc+1:]))

    def x(self, i):

        return self.xdat[:self.nfrus[i]+1]

    def y(self, i):

        return self.ydat[i]


class ettsrho_reader(access_mixin, etts1d_reader):
    pass

class ettsJ_reader(access_mixin, etts2d_reader):
    pass


class ettsfile_reader(object):
    def __init__(self, rootdir = "."):

        self.rho = ettsrho_reader(os.path.join(rootdir, "density.txt"))
        self.T = ettsrho_reader(os.path.join(rootdir, "temperature.txt"))
        self.v = ettsrho_reader(os.path.join(rootdir, "velocity.txt"))
        self.J = ettsJ_reader(os.path.join(rootdir, "intensity.txt"))


