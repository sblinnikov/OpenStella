#!/usr/bin/env python
from __future__ import print_function
import os
import numpy as np
import matplotlib.pyplot as plt

class lbol_reader(object):
    """
    Data reader for a *.lbol file as created by the Stella code
    """
    def __init__(self, mname, expfname = None, verbose = False):
        """
        Arguments:
        mname -- name of the model, i.e. of the lbol file without the extension

        Keyword Arguments:
        expfname -- explicit name/path of the lbol file; if None, it is assumed
                    that a mname.lbol file exists; otherwise mname is
                    interpreted solely as an identifier for the model and
                    expfname is used to load the file; (default None)
        verbose --  print detailed information
        """
        self.verbose = verbose
        self.mname = mname.rsplit("/")[-1]
        if expfname is None:
            self.fname = mname + ".lbol"
        else:
            self.fname = expfname

        self.process_lbol_file()

    @property
    def tl(self):
        """first column in *.lbol file, encodes time"""
        return self._tl

    @tl.setter
    def tl(self, val):
        self._tl = val

    @property
    def lubvri(self):
        """2nd column in *.lbol file, encodes UBVRI luminosity"""
        return self._lubvri

    @lubvri.setter
    def lubvri(self, val):
        self._lubvri = val

    @property
    def lbol(self):
        """3rd column in *.lbol file, encodes bolometric luminosity"""
        return self._lbol

    @lbol.setter
    def lbol(self, val):
        self._lbol = val

    @property
    def lxeuv(self):
        """4th column in *.lbol file, x-ray and extreme UV luminosity"""
        return self._lxeuv

    @lxeuv.setter
    def lxeuv(self, val):
        self._lxeuv = val

    @property
    def lfarir(self):
        """5th column in *.lbol file, far IR luminosity"""
        return self._lfarir

    @lfarir.setter
    def lfarir(self, val):
        self._lfarir = val


    def process_lbol_file(self):
        """
        Read and process the data of the lbol file
        """

        if self.verbose:
            print("Reading bolometric luminosity file for run '%s'" % self.mname)
        raw_data = np.loadtxt(self.fname, skiprows = 1)
        if self.verbose:
            print("'%s' found and read" % self.fname)

        self.raw_data = raw_data

        self.tl = raw_data[:,0]
        self.lubvri = raw_data[:,1]
        self.lbol = raw_data[:,2]
        self.lxeuv = raw_data[:,3]
        self.lfarir = raw_data[:,4]
        if self.verbose:
            print("read %d data points, ranging from %.1f to %.1f days" % (len(self.tl), self.tl[0], self.tl[-1]))

    def show_lightcurves(self, fig = None):
        """
        Create a plot of bolometric, UBVRI, far-IR and X-ray+UV lightcurves.

        Arguments:
        fig -- figure instance; if None, a new instance is created 
               (default None)

        Returns:
        fig -- figure instance containing the plot
        """

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        ax.plot(self.tl, self.lfarir, color = "red", label = "Far-IR")
        ax.plot(self.tl, self.lubvri, color = "green", label = "UBVRI")
        ax.plot(self.tl, self.lxeuv, color = "blue", label = "X-Ray + Far UV")
        ax.plot(self.tl, self.lbol, color = "black", label = "bolometric")
        ax.set_xlim([-20, 120])
        ax.set_ylim([40, 46])

        ax.set_xlabel(r"$t$ [d]")
        ax.set_ylabel(r"$\log L$ $[\mathrm{erg\,s^{-1}}]$")
        ax.set_title("Run '%s'" % self.mname)
        ax.legend()

        return fig


    def show_lbol_lightcurve(self, fig = None):
        """
        Create a plot of the pseudo-bolometric lightcurve

        Arguments:
        fig -- figure instance; if None, a new instance is created 
               (default None)

        Returns:
        fig -- figure instance containing the plot
        """

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        ax.plot(self.tl, self.lbol)
        ax.set_xlim([-20, 120])
        ax.set_ylim([40, 44])

        ax.set_xlabel(r"$t$ [d]")
        ax.set_ylabel(r"$\log L_{\mathrm{bol}}$ $[\mathrm{erg\,s^{-1}}]$")
        ax.set_title("Run '%s'" % self.mname)

        return fig

    def show_lubvri_lightcurve(self, fig = None):
        """
        Create a plot of the UBVRI light curve

        Arguments:
        fig -- figure instance; if None, a new instance is created 
               (default None)

        Returns:
        fig -- figure instance containing the plot
        """

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        ax.plot(self.tl, self.lubvri)
        ax.set_xlim([-20, 120])
        ax.set_ylim([40, 44])

        ax.set_xlabel(r"$t$ [d]")
        ax.set_ylabel(r"$\log L_{\mathrm{UBVRI}}$ $[\mathrm{erg\,s^{-1}}]$")
        ax.set_title("Run '%s'" % self.mname)

        return fig

    def show_lbol_lubvri_lightcurve(self, fig = None):
        """
        Show both UBVRI and pseudo-bolometric light curves
        Arguments:
        fig -- figure instance; if None, a new instance is created 
               (default None)

        Returns:
        fig -- figure instance containing the plot
        """

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        p, = ax.plot(self.tl, self.lbol, ls = "dotted", label = "pseudo-bolometric")
        color = p.get_color()
        ax.plot(self.tl, self.lubvri, ls = "solid", color = color, label = "UBVRI")
        ax.set_xlim([-20, 120])
        ax.set_ylim([40, 44])

        ax.set_xlabel(r"$t$ [d]")
        ax.set_ylabel(r"$\log L$ $[\mathrm{erg\,s^{-1}}]$")
        ax.legend()
        ax.set_title("Run '%s'" % self.mname)

        return fig



class lightcurve_comparer(object):
    """
    Helper with which light curves of different models may be compared
    """
    def __init__(self, *args, **kwargs):
        """
        Arguments:
        *args -- any number of models (either instances of lbol_reader or model
                 names)
        Keyword Arguments:
        verbose -- print detailed information if True
        """

        self.verbose = kwargs.get("verbose", False)
        self.models = []
        for arg in args:
            try:
                self.models.append(lbol_reader(arg, verbose = self.verbose))
            except TypeError:
                self.models.append(arg)

            try:
                assert(isinstance(self.models[-1], lbol_reader))
            except AssertionError:
                raise ValueError("Error: args must be model names or lbob_reader instances")

        if len(self.models) > 8:
            print("Warning: many models are provided (N >8), readability of comparison plots may suffer")


    def compare_lbol_lightcurve(self, fig = None):

        if fig is None:
            fig = plt.figure()

        for model in self.models:
            fig = model.show_lbol_lightcurve(fig = fig)
            fig.gca().get_lines()[-1].set_label(model.mname)

        fig.gca().legend()

        return fig

    def compare_lubvri_lightcurve(self, fig = None):

        if fig is None:
            fig = plt.figure()

        for model in self.models:
            fig = model.show_lubvri_lightcurve(fig = fig)
            fig.gca().get_lines()[-1].set_label(model.mname)

        fig.gca().legend()

        return fig

    def compare_lbol_lubvri_lightcurve(self, fig = None):

        if fig is None:
            fig = plt.figure()

        i = 0
        for model in self.models:
            fig = model.show_lbol_lubvri_lightcurve(fig = fig)
            if i == 0:
                line1 = fig.gca().get_lines()[-1]
                line2 = fig.gca().get_lines()[-2]
                label1 = line1.get_label()
                label2 = line2.get_label()
            fig.gca().get_lines()[-1].set_label(model.mname)
            fig.gca().get_lines()[-2].set_label(None)
            i += 1

        first_legend = fig.gca().legend()
        second_legend = plt.legend((line1, line2), (label1, label2), loc=4)
        plt.gca().add_artist(first_legend)

        return fig


def test(mname = "m030307mhomo"):
    """
    A simple script to test the lbol_reader; automatically called in main

    Arguments:
    mname -- model name (default 'm03037mhomo')

    """

    test_reader = lbol_reader(mname, verbose = True)
    test_reader.show_lubvri_lightcurve()

    plt.show()


if __name__ == "__main__":

    test()

