#!/usr/bin/env python
from __future__ import print_function
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse

c = 2.9979e10

class ph_reader(object):
    """
    Data reader for a *.ph file created by the Stella code
    """
    def __init__(self, mname, verbose = False):
        """
        Arguments:
        mname -- name of the model, i.e. of the lbol file without the extension

        Keyword Arguments:
        verbose -- print detailed information if True
        """
        self.verbose = verbose

        self.mname = mname.rsplit("/")[-1]
        self.fname = mname + ".ph"

        self._lgnu = None
        self._nu = None
        self._lam = None
        self._time = None
        self._lgLnu = None
        self._Lnu = None
        self._Llam = None

        self.process_ph_file()

    @property
    def lgnu(self):
        """logarithm of the bin frequency"""
        return self._lgnu

    @lgnu.setter
    def lgnu(self, val):
        self._lgnu = val

    @property
    def nu(self):
        """bin frequency (Hz)"""
        if self._nu is None:
            self._nu = 10**self.lgnu
        return self._nu

    @property
    def lam(self):
        """bin wavelength (cm)"""
        if self._lam is None:
            self._lam = c / self.nu
        return self._lam

    @property
    def lamA(self):
        """bin wavelength (Angstrom)"""
        return self.lam * 1e8


    @property
    def time(self):
        """time of snapshot"""
        return self._time

    @time.setter
    def time(self, val):
        self._time = val

    @property
    def lgLnu(self):
        """
        logarithm of monochromatic (with respect to nu in Hz) luminosity

        two-dimensional array with shape len(time) x len(nu), containing
        information of each frequency bin for every snapshot
        """
        return self._lgLnu

    @lgLnu.setter
    def lgLnu(self, val):
        self._lgLnu = val

    @property
    def Lnu(self):
        """
        monochromatic (with respect to nu in Hz) luminosity

        two-dimensional array with the same shape as lgLnu
        """
        if self._Lnu is None:
            self._Lnu = 10**self.lgLnu
        return self._Lnu

    @property
    def Llam(self):
        """
        monochromatic (with respect to nu in cm) luminosity

        tow-dimensional array with the same shape as lgLnu
        """
        if self._Llam is None:
            self._Llam = self.Lnu * self.nu**2 / c
        return self._Llam

    @property
    def LlamA(self):
        """
        monochromatic (with respect to nu in Angstrom) luminosity

        tow-dimensional array with the same shape as lgLnu
        """
        return self.Llam * 1e-8

    def process_ph_file(self):
        """
        Read and process the data of the ph file
        """

        if self.verbose:
            print("Reading spectral energy distribution file for run '%s'" % self.mname)
        f = open(self.fname, "r")

        self.lgnu = np.array(map(float, f.readline().rsplit()))
        raw_data = np.loadtxt(f)
        f.close()
        if self.verbose:
            print("'%s' found and read" % self.fname)

        self.raw_data = raw_data
        self.time = raw_data[:,0]
        self.lgLnu = raw_data[:,3:]

    def find_index_closest_snapshot(self, t):
        """
        Finds index of snapshot which is closest to requested time

        Arguments:
        t -- requested tim

        Returns
        i -- index of closest snapshot
        """

        i = np.argmin(np.fabs(self.time - t))

        if self.verbose:
            print("Time requested: %e" % t)
            print("Closest snapshot: %e" % self.time[i])

        return i

    def set_axis(self, ident):
        """
        Sets x and y values for the SED plots according to identifier

        Arguments:
        ident -- identifier for the x-axis; possible values are
                 'lg_nu', 'nu', 'lam', 'lg_lamA', 'lamA'

        Returns:
        xaxis -- quantity for the xaxis
        yaxis -- quantity on the yaxis; if one of the frequency modes has been
                 selected, this will be lgLnu, otherwise lgLlam, or LgLamA
        """

        possibilities = ["lg_nu", "nu", "lam", "lg_lamA", "lamA"]

        try:
            assert(ident in possibilities)
        except AssertionError:
            print("Warning: unknown ident '%s'; axis not set" % ident)
            print("Possibilities are: %s" % ", ".join(possibilities))
            xaxis = None
            yaxis = None
            return xaxis, yaxis

        if ident is "lg_nu":
            xaxis = self.lgnu
            yaxis = self.lgLnu
        elif ident is "nu":
            xaxis = self.nu
            yaxis = self.lgLnu
        elif ident is "lam":
            xaxis = self.lam
            yaxis = np.log10(self.Llam)
        elif ident is "lg_lam":
            xaxis = np.log10(self.lam)
            yaxis = np.log10(self.Llam)
        elif ident is "lamA":
            xaxis = self.lamA
            yaxis = np.log10(self.LlamA)
        elif ident is "lg_lamA":
            xaxis = np.log10(self.lamA)
            yaxis = np.log10(self.LlamA)
        else:
            print("Warning: Implementation Error!")
            print("ident '%s' known but no rule defined; axis not set" % ident)
            xaxis = None
            yaxis = None

        return xaxis, yaxis


    def plot_emergent_sed_t(self, t, fig = None, mode = "lg_nu"):
        """
        Plots the emergent SED for a defined time

        Arguments
        t -- requested time

        Keyword Arguments:
        fig -- figure instance for plot; if None a new one is created (default
               None)
        mode -- identifier for x-axis and y-axis quantities, see self.set_axis()

        Returns:
        fig -- figure instance containing the plot
        """

        i = self.find_index_closest_snapshot(t)
        self.plot_emergent_sed(i, fig = fig, mode = mode)

    def plot_emergent_sed(self, i, fig = None, mode = "lg_nu"):
        """
        Plots the emergent SED for a defined snapshot index

        Arguments
        i -- requested snapshot index

        Keyword Arguments:
        fig -- figure instance for plot; if None a new one is created (default
               None)
        mode -- identifier for x-axis and y-axis quantities, see self.set_axis()

        Returns:
        fig -- figure instance containing the plot
        """

        xaxis, yaxis = self.set_axis(mode)
        if xaxis is None:
            print("Warning: no plot produced!")
            return None

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()
        plt.plot(xaxis, yaxis[i,:])

        return fig

    def construct_light_curve(self, lam_min, lam_max, no_clipping = False):
        """
        Constructs a light curve based on the emergent SEDs in the defined
        wavelength range.

        Arguments:
        lam_min -- minimum wavelength (in Angstrom) for light curve construction
        lam_max -- maximum wavelength (in Angstrom) for light curve construction

        Keyword Arguments:
        no_clipping -- if True, also luminosity in boundary bins which are only
                       partly in requested range are included (default False)

        Returns:
        L -- log L array
        """
        if self.verbose:
            print("Constructing light curve for range: %.4fA - %.4fA" % (lam_min, lam_max))

        mask = (self.lamA > lam_min) * (self.lamA < lam_max)
        dnu = self.nu[1:] - self.nu[:-1]
        dnu = np.append(dnu, dnu[-1])


        L = np.sum(self.Lnu[:,mask] * dnu[mask], axis = 1)

        if no_clipping is True:
            src = np.argwhere(mask == 1).reshape(-1)
            if np.min(src) > 0:
                #lam_max
                i = np.min(src) - 1
                weight = 1e8 * c * (1. / lam_max - 1. / self.lamA)[i] / dnu[i]
                dL = self.Lnu[:,i] * weight * dnu[i]
                L += dL
            if np.max(src) < len(mask) - 2:
                i = np.max(src)
                #lam_max
                weight = 1e8 * c * (1. / lam_min - 1. / self.lamA)[i] / dnu[i]
                dL = self.Lnu[:,i] * weight * dnu[i]
                L += dL

        return L


    def construct_and_plot_light_curve(self, lam_min, lam_max, no_clipping = False, fig = None):
        """
        Constructs a light curve based on the emergent SEDs in the defined
        wavelength range.

        Arguments:
        lam_min -- minimum wavelength (in Angstrom) for light curve construction
        lam_max -- maximum wavelength (in Angstrom) for light curve construction

        Keyword Arguments:
        no_clipping -- if True, also luminosity in boundary bins which are only
                       partly in requested range are included (default False)
        fig -- figure instance for plot; if None a new one is created (default
               None)

        Returns:
        fig -- figure instance containing the plot
        """


        L = self.construct_and_plot_light_curve(lam_min, lam_max, no_clipping = no_clipping)

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        ax.plot(self.time, np.log10(L), label = r"$%.2f\AA$ -  $%.2f\AA$" % (lam_min, lam_max))
        ax.set_ylim([40, 46])
        ax.set_xlim([-5, 150])
        ax.legend()
        ax.set_xlabel(r"$t_{\mathrm{obs}}$")
        ax.set_ylabel(r"$L$ [$\mathrm{erg\,s^{-1}}$]")
        ax.set_title("Run %s" % self.mname)

        return fig



def main(mname, show = True):
    """
    main routine, creating a ph_reader for the provided model and producing
    some standard light curves and spectral plots.

    Arguments:
    mname -- root name of model

    Keyword Arguments:
    show -- if True, plt.show() is called and the figures are displayed
            (default True)

    """

    reader = ph_reader(mname)
    fig = reader.construct_light_curve(0, 100000)
    fig = reader.construct_light_curve(0, 1700, fig = fig)
    fig = reader.construct_light_curve(1700, 3250, fig = fig)
    fig = reader.construct_light_curve(3250, 8900, fig = fig)
    fig = reader.construct_light_curve(8900, 100000, fig = fig)


    if show:
        plt.show()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Stella ph file reader")
    parser.add_argument("name", help = "Model root name")
    parser.add_argument("-s", "--show", action="store_true", help="Show figures")

    args = parser.parse_args()

    main(args.name, show = args.show)

