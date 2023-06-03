#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : sn2009dc.py
#
#  Purpose : Process data files for SN 2009dc observations
#
#  Creation Date : 29-10-2015
#
#  Last Modified : Tue 24 Nov 2015 11:28:43 CET
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""This module provides a number of parsers to read-in the various data source
files of supernova observations.

Note
----

This module has been specifically written for data files related to
observations of SN 2009dc. It will most likely not work out-of-the-box with
data files for other SN.
"""
from __future__ import print_function
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class luminosity_table(object):
    """Read observed supernova luminosity from file

    This reader is intended for data files compiled by S. Taubenberger,
    containing phase and observed luminosity for a particular supernova.

    Parameters
    ----------
    fname : str
        name of data file 
    mode : {'cust-tauben'}
        identifier for file format; currently only S. Taubenberger's formatting
        is supported

    Attributes
    ----------
    phase : numpy array
        time in days relative to B-maximum
    lgL : numpy array
        observed logarithmic luminosity ([erg/s])
    lgL_err : numpy array
        luminosity uncertainty 

    """

    def __init__(self, fname, mode = "cust-tauben"):

        self.mode = mode
        self.fname = fname

        known_mode = "cust-tauben"
        try:
            assert(self.mode == known_mode)
        except AssertionError:
            logger.error("Unknown mode {}, known mode: {}".format(self.mode, known_mode))
            raise ValueError

        if self.mode == known_mode:
            self.read_table_cust_tauben()

    def read_table_cust_tauben(self):
        """Read observed luminosity from file, assuming S. Taubenberger's
        formatting

        """

        self.raw_data = np.loadtxt(self.fname)

        self.phase = self.raw_data[:,0]
        self.lgL = self.raw_data[:,1]

        if self.raw_data.shape[1] == 3:
            self.lgL_err = self.raw_data[:,2]

class swift_table(object):
    """Read data files with Swift UVOT photometric observations

    As with most other readers in this module, this parser is currently
    designed to work with different parsing methods, one for each data format.
    Currently, only Peter Brown's data formatting is supported.

    Note
    ----

    This could (should) be combined with the photometric_table class.

    Parameters
    ----------
    fname : str
        file name of the SWIFT data table
    mode : {'pbrown'}
        identifier for the parsing mode; currently only Peter Brown's format is
        supported

    Attributes
    ----------
    filters: list of str
        identifiers for the different swift filters
    data : dict of numpy arrays
        for each filter, a data record (time, apparent mags, errors, etc.) are
        stored

    """
    def __init__(self, fname, mode = "pbrown"):

        known_mode = "pbrown"

        self.mode = mode
        self.fname = fname

        if self.mode == known_mode:
            self.parse_table_pbrown()
        else:
            logger.error("unknown mode {}; only known mode: {}".format(mode, known_mode))
            raise ValueError

    def parse_table_pbrown(self):
        """Parse table with Peter Brown's formatting

        """

        f = open(self.fname, "r")
        lines = f.readlines()
        filters = ["uvw2", "uvm2", "uvw1", "u", "b", "v", "uvot"]

        self.data = {}


        for i in xrange(len(lines)):
            tmp = lines[i].rsplit()

            if tmp[0] == "#":
                if len(tmp) > 1:
                    if tmp[1] in filters:
                        if tmp[1] == "uvot":
                            ident = tmp[2]
                        else:
                            ident = tmp[1]
                        self.data[ident] = []
            else:
                self.data[ident].append(lines[i])

        for k in self.data:
            self.data[k] = np.genfromtxt(self.data[k])

class photometric_table(object):
    def __init__(self, fname, mode = "cust-tauben"):
        """
        Reads photometric data of a supernova from a data file.

        The current design allows different readers for different data formats.
        However, a minimum set of data has to be contained in these files (c.f.
        class attributes). Currently, only a reader for the photometric table
        format of S. Taubenberger is available.

        Note
        ----
        
        In the future, one may change the design and work with inheritance
        instead of having multiple reader methods and only one class.

        Parameters
        ----------
        fname : str
            file name of the photometric table
        mode : {'cust-tauben'}
            identifier for the reader which should be used for data parsing;
            currently only one parser exists

        Attributes
        ----------
        mu : float
            distance modulus
        mu_err : float
            distance modulus uncertainty
        JD_Bmax : float
            Julian date of maximum light in Bessel B
        EBmV : float
            E(B-V) extinction parameter
        EBmV_err : float
            uncertainty of E(B-V) extinction parameter
        bands : list of strings 
            list of identifiers for filters in which data has been taken
        data : dict of numpy arrays
            contains the observed data in the different bands; keys are
            identical with identifiers of bands
        data_err : dict of numpy arrays
            uncertainties associated with observed data
        jd : dict of numpy arrays
            contains the epochs (in Julian days) of the observations for each
            filter separately 
        t : dict of numpy arrays
            time relative to B_max in days for all observations
        """

        known_mode = "cust-tauben"

        self.mode = mode
        self.fname = fname

        if self.mode == known_mode:
            self.parse_table_cust_tauben()
        else:
            logger.error("unknown mode {}; only known mode: {}".format(mode, known_mode))
            raise ValueError

    def parse_table_cust_tauben(self):
        """Parse photometric table generated by S. Taubenberger

        """

        logger.info("parsing photometric table, expecting S. Taubenberger's formatting")
        f = open(self.fname, "r")
        lines = f.readlines()
        f.close()

        self.EBmV = float(lines[3].rsplit()[2])
        self.EBmV_err = float(lines[3].rsplit()[4])

        self.mu = float(lines[4].rsplit()[2])
        self.mu_err = float(lines[4].rsplit()[4])

        self.JD_Bmax = float(lines[6].rsplit()[2])


        header = [elem.replace("'", "") for elem in lines[9].rsplit()]
        self.bands = header[1:-1:2]

        dtype = [(ident, "f8") for ident in header[:-1]] + [("src", "i4")] + [(header[-1], "S16")]

        self.raw_data = np.genfromtxt(self.fname, skip_header=11, usecols=range(19), skip_footer=6, deletechars="*'", dtype = dtype)
        self.t = {}
        self.jd = {}
        self.data = {}
        self.data_err = {}

        for band in self.bands:
            notnan_mask = True - np.isnan(self.raw_data[band])
            self.jd[band] = self.raw_data["JD"][notnan_mask]
            self.t[band] = self.jd[band] - self.JD_Bmax
            self.data[band] = self.raw_data[band][notnan_mask]
            self.data_err[band] = self.raw_data[band+"err"][notnan_mask]


class conversion_table(object):
    """Parser for a simple table containing to correct for the filter-specific
    extinction

    As with the photometric_table class, this parser is designed to have a
    separate reader routine for each file format. Currently, only one reader
    exists, targeted at S. Taubenberger's formatting.

    Parameter
    ---------
    fname : str
        file name of the conversion factor table
    mode : {'cust-tauben'}
        file format identifier; currently only one format is supported

    Attributes
    ----------
    R_X : dict of floats
        R_X * E(B-V) gives filter-specific extinction 


    Notes
    -----
    $R_X = A_X / E(B-V)$

    """
    def __init__(self, fname, mode = "cust-tauben"):

        self.mode = mode

        self.fname = fname

        if self.mode == "cust-tauben":
            self.parse_table_cust_tauben()

    def parse_table_cust_tauben(self):
        """Parse the table with the conversion factors according to S.
        Taubenberger's formatting
        """

        f = open(self.fname, "r")
        lines = f.readlines()
        f.close()

        self.R_X = {}

        for line in lines[5:]:
            tmp = line.rsplit()
            self.R_X[tmp[0].replace("'", "")] = float(tmp[-1])

class sn_colour_calculator(object):
    """Calculator to determine absolute colour magnitudes

    Note
    ----
    We specifically work in the Vega magnitude system.

    Parameters
    ----------
    phot_fname : str or photometric_table instance
        file name of photometric table or corresponding photometric_table
        instance
    conv_fname : str or conversion_table instance
        file name of conversion table or corresponding conversion_table
        instance

    Attributes
    ----------
    m : dict of numpy arrays
        apparent magnitudes of different filters (not extinction corrected)
    m_err : dict of numpy arrays
        uncertainties of the apparent magnitudes
    M : dict of numpy arrays
        absolute magnitudes, extinction corrected
    M_err : dict of numpy arrays
        uncertainties of absolute magnitudes

    """
    def __init__(self, phot_fname, conv_fname, mode = "cust-tauben"):
        if type(phot_fname) == type("a"):
            self.phot = photometric_table(phot_fname, mode = mode)
        else:
            self.phot = phot_fname
        if type(conv_fname) == type("a"):
            self.conv = conversion_table(conv_fname, mode = mode)
        else:
            self.conv = conv_fname

        self.get_apparent_mags()
        self.calc_absolute_mags()

    def get_apparent_mags(self):
        """
        Gather apparent magnitudes from the photometric tables and store them
        in m. Analogous procedure for their uncertainties
        """

        self.m = dict([(band, self.phot.data[band]) for band in self.phot.bands])
        self.m_err = dict([(band, self.phot.data_err[band]) for band in self.phot.bands])

    def calc_absolute_mags(self):
        """
        Calculate absolute magnitudes

        Note
        ----
        $M_{\mathrm{X}} = m - \mu - E(B-V) R_{\mathrm{X}}$

        """

        self.M = {}
        self.M_err = {}
        for band in self.phot.bands:
            self.M[band] = self.m[band] - self.phot.mu - self.phot.EBmV * self.conv.R_X[band]
            self.M_err[band] = self.m_err[band] + self.phot.mu_err - self.phot.EBmV_err * self.conv.R_X[band]

    def show_mags(self, mode = "app"):
        """
        Plot the colour magnitudes for all bands

        Parameters
        ----------
        mode : {'app','abs'}
            plot either apparent or absolute magnitudes

        Note
        ----

        This routine explicitly assumes that an X-server is available by
        calling plt.show().
        """

        known_modes = ["app", "abs"]

        try:
            assert(mode in known_modes)
        except AssertionError:
            logger.error("Unknown mode {}; known modes are: {}".format(mode, ", ".join(known_modes)))
            raise ValueError

        import matplotlib.pyplot as plt
        colors = plt.rcParams["axes.color_cycle"]

        fig = plt.figure()
        ax = fig.add_subplot(111)

        for color, band in zip(colors, self.phot.bands):

            if mode == "app":
                ax.errorbar(self.phot.t[band], self.m[band], yerr = self.m_err[band], color = color, marker = "o", capsize = 0, markeredgecolor = color, label = band, ls = "")
            elif mode == "abs":
                ax.errorbar(self.phot.t[band], self.M[band], yerr = self.M_err[band], color = color, marker = "o", capsize = 0, markeredgecolor = color, label = band, ls = "")

        ax.legend()
        ylim = ax.get_ylim()
        ax.set_ylim([ylim[-1], ylim[0]])

        plt.show()

if __name__ == "__main__":

    phot_fname = "mags_Scorr_Kcorr_100729_pure_psf_err_final.txt"
    conv_fname = "conv_2009dc.txt"

    sn09dc_calc = sn_colour_calculator(phot_fname, conv_fname)
    sn09dc_calc.show_apparent_mags(mode = "abs")
