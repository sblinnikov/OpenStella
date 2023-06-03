# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : eve_diag.py
#
#  Purpose :
#
#  Creation Date : 13-11-2015
#
#  Last Modified : Wed 02 Dec 2015 15:37:28 CET
#
#  Created By :  
#
# _._._._._._._._._._._._._._._._._._._._._.
"""Like swdn_diag, this module serves as a container for all plotting and
diagnostic tools related to eve.py

**Warning** Untested and poorly documented
"""
from __future__ import print_function
import stella.eve
import itertools
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

elements = { 'neut': 0, 'h': 1, 'he': 2, 'li': 3, 'be': 4, 'b': 5, 'c': 6, 'n': 7, 'o': 8, 'f': 9, 'ne': 10, 'na': 11, 'mg': 12, 'al': 13, 'si': 14, 'p': 15, 's': 16, 'cl': 17, 'ar': 18, 'k': 19,    'ca': 20, 'sc': 21, 'ti': 22, 'v': 23, 'cr': 24, 'mn': 25, 'fe': 26, 'co': 27, 'ni': 28, 'cu': 29, 'zn': 30, 'ga': 31, 'ge': 32, 'as': 33, 'se': 34, 'br': 35, 'kr': 36, 'rb': 37, 'sr': 38, 'y': 39,  'zr': 40, 'nb': 41, 'mo': 42, 'tc': 43, 'ru': 44, 'rh': 45, 'pd': 46, 'ag': 47, 'cd': 48}
inv_elements = dict([(v,k) for k, v in elements.items()])

class eve_diagnostics(object):
    def __init__(self, everho):

        if type(everho) == type("a"):
            self.everho = eve.everho_reader(everho)
        else:
            self.everho = everho

    def show_abundances(self, ax = None, cmap = cm.nipy_spectral):

        ni56_pres = False

        if ax is None:
            ax = plt.figure().add_subplot(111)

        atomz = []
        atomk = []
        for k in self.everho.abundances:
            if k != "Ni56":
                atomz.append(elements[k.lower()])
                atomk.append(k)
            else:
                ni56_pres = True

        atomz = np.array(atomz)
        atomk = np.array(atomk)[atomz.argsort()]
        atomz = atomz[atomz.argsort()]

        if ni56_pres:
            atomz = np.append(atomz, 28)
            atomk = np.append(atomk, 'Ni56')

        zmin = atomz.min()
        zmax = atomz.max()
        dashes = [
                [7,3],
                [2,2],
                [7,3,2,3],
                [7,3,2,3,2,3],
                [7,3,7,3,2,3],
                [7,3,7,3,2,3,2,3],
                [7,3,2,3,2,3,2,3],
                ]

        styles = itertools.cycle(dashes)

        for z, k in zip(atomz, atomk):
            dash = styles.next()
            ax.plot(self.everho.mass, 10**self.everho.abundances[k], dashes = dash, color = cmap(float(z - zmin)/(zmax - zmin)), dash_capstyle = "round", label = k)

        ax.set_ylim([0,1.1])
        ax.legend(ncol = len(atomz)//4)

        return ax

