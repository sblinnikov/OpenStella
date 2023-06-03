#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : lbol.py
#
#  Purpose : reading and processing Stella eve files
#
#  Creation Date : ???
#
#  Last Modified : Fri 28 Oct 2016 11:02:48 CEST
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""This module provides a reader for the '.rho' files produces by the Stella
eve executables

"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class everho_reader(object):
    """
    Parser for a '.rho' file produced by one the Stella eve executables, e.g.
    eve1a.exe

    Note
    ----

    Nomenclature is adopted from the header in the .rho file.  The
    interpretation of the physical quantities is based on [1]_ and [2]_

    .. [1] eve.sm
    .. [2] evesnia.trf


    Parameters
    -----------
    mname : str
        rootname of the model or path to the .rho file

    Attributes
    -----------
    time : float
        initial time, i.e. time since explosion
    Nzones : int
        number of radial zones
    zone : numpy.array
        radial zone indices
    mass : numpy.array
        radial mass coordinate in solar masses
    lg_r : numpy.array
        logarithmic cell radius in cm
    lg_Tp : numpy.array
        logarithmic gas temperature in K
    lg_rho : numpy.array
        logarithmic gas density in g/cm^3
    lg_dm: numpy.array
        logarithmic cell mass in solar masses (?? needs confirmation)
    u : numpy.array
        material velocity in 1e8 cm/s
    Ni56 : numpy.array
        logarithmic mass fraction of radioactive nickel
    H : numpy.array
        logarithmic hydrogen mass fraction
    He : numpy.array
        logarithmic helium mass fraction
    C : numpy.array
        logarithmic carbon mass fraction
    N : numpy.array
        logarithmic nitrogen mass fraction
    O : numpy.array
        logarithmic oxygen mass fraction
    Ne : numpy.array
        logarithmic neon mass fraction
    Na : numpy.array
        logarithmic sodium mass fraction
    Mg : numpy.array
        logarithmic magnesium mass fraction
    Al : numpy.array
        logarithmic aluminium mass fraction
    Si : numpy.array
        logarithmic silicon mass fraction
    S : numpy.array
        logarithmic sulfur mass fraction
    Ar : numpy array
        logarithmic argon mass fraction
    Ca : numpy array
        logarithmic calcium mass fraction
    Fe : numpy array
        logarithmic iron mass fraction (includes Ni56)
    Ni : numpy array
        logarithmic stable nickel mass fraction (excluding Ni56 ?? needs confirmation)
    abundances : dict
        contains all read abundances
    read_quantities : list of str
        contains identifiers for class attributes holding the read quantities
    derived_quantities : list of str
        contains identifiers for class attributes holding quantities which are derived from the read data


    """
    def __init__(self, mname):
        """
        Constructor for the eve_rhoreader

        """

        self._lg_r = None
        self._lg_rho = None
        self._lg_Tp = None
        self._lg_dm = None

        #derived quantities
        self._dm = None
        self._r = None
        self._Tp = None
        self._rho = None

        self.read_quantities = []
        self.derived_quantities = []
        self.abundances = {}

        if mname[-4:] == ".rho":
            self.fname = mname
            self.mname = os.path.split(mname)[-1][:-4]
        else:
            self.fname = mname + ".rho"
            self.mname = os.path.split(mname)[-1]

        self.process_rho_file()

    def print_att_info(self):
        """
        Prompts all the attribute names of all read and derived physical
        quantities

        This is intended to help an interactive user to quickly find the
        attribute which stores the desired physical quantity
        """

        print("the following quantities have been read from the '.rho' file and may be accessed as class attributes:")
        print("\n".join(self.read_quantities))
        print("the following derived quantities are also available and may be accessed as class attributes:")
        print("\n".join(self.derived_quantities))

    def set_data(self, name, val):
        """
        Helper routine to set the attributes of the class

        Actually, quite cumbersome and not very elegant, but I didn't come up
        with a quick solution for having all the class properties and not every
        rho file containing the same physical quantities. Happy to replace it
        by a more efficient scheme.

        Parameters
        ----------
            name : str
                identifier of the quantity
            val : numpy.array
                data array associated with the quantity

        """

        self.read_quantities.append(name)

        if name == "zone":
            self.zone = val
        elif name == "mass":
            self.mass = val
        elif name == "lg_r":
            self.lg_r = val
            self.derived_quantities.append("r")
        elif name == "lg_Tp":
            self.lg_Tp = val
            self.derived_quantities.append("Tp")
        elif name == "lg_rho":
            self.lg_rho = val
            self.derived_quantities.append("rho")
        elif name == "lg_dm":
            self.lg_dm = val
            self.derived_quantities.append("dm")
        elif name == "u":
            self.u = val
        elif name == "Ni56":
            self.Ni56 = val
            self.abundances[name] = self.Ni56
        elif name == "H":
            self.H = val
            self.abundances[name] = self.H
        elif name == "He":
            self.He = val
            self.abundances[name] = self.He
        elif name == "C":
            self.C = val
            self.abundances[name] = self.C
        elif name == "N":
            self.N = val
            self.abundances[name] = self.N
        elif name == "O":
            self.O = val
            self.abundances[name] = self.O
        elif name == "Ne":
            self.Ne = val
            self.abundances[name] = self.Ne
        elif name == "Na":
            self.Na = val
            self.abundances[name] = self.Na
        elif name == "Mg":
            self.Mg = val
            self.abundances[name] = self.Mg
        elif name == "Al":
            self.Al = val
            self.abundances[name] = self.Al
        elif name == "Si":
            self.Si = val
            self.abundances[name] = self.Si
        elif name == "S":
            self.S = val
            self.abundances[name] = self.S
        elif name == "Ar":
            self.Ar = val
            self.abundances[name] = self.Ar
        elif name == "Ca":
            self.Ca = val
            self.abundances[name] = self.Ca
        elif name == "Fe":
            self.Fe = val
            self.abundances[name] = self.Fe
        elif name == "Ni":
            self.Ni = val
            self.abundances[name] = self.Ni
        else:
            logging.warn("name {} unknown, ignoring".format(name))

    @property
    def lg_r(self):
        """logarithmic radius"""
        return self._lg_r
    @lg_r.setter
    def lg_r(self, val):
        self._lg_r = val

    @property
    def lg_rho(self):
        """logarithmic gas density"""
        return self._lg_rho
    @lg_rho.setter
    def lg_rho(self, val):
        self._lg_rho = val

    @property
    def lg_Tp(self):
        """logarithmic gas temperature"""
        return self._lg_Tp
    @lg_Tp.setter
    def lg_Tp(self, val):
        self._lg_Tp = val

    @property
    def lg_dm(self):
        """logarithmic cell mass in solar mass (?? needs confirmation)"""
        return self._lg_dm
    @lg_dm.setter
    def lg_dm(self, val):
        self._lg_dm = val

    @property
    def r(self):
        """physical radius in cm"""
        if self._r is None and self._lg_r is not None:
            self._r = 10**self.lg_r
        return self._r

    @property
    def Tp(self):
        """physical gas temperature in K"""
        if self._Tp is None and self._lg_Tp is not None:
            self._Tp = 10**self.lg_Tp
        return self._Tp

    @property
    def rho(self):
        """physical density in g/cm^3"""
        if self._rho is None and self._lg_rho is not None:
            self._rho = 10.**self.lg_rho
        return self._rho

    @property
    def dm(self):
        """physical shell mass in solar mass units"""
        if self._dm is None and self._lg_dm is not None:
            self._dm = 10**self.lg_dm
        return self._dm


    def process_rho_file(self):
        """
        Process the rho file, i.e. store the contents in the class attributes
        """

        logger.info("Reading density file for model '{}'".format(self.mname))
        f = open(self.fname, "r")

        raw_labels = f.readline()
        self.labels = raw_labels.replace("Ni", "Ni56", 1).replace("lg ", "lg_").replace("(", "_").replace(")", "").rsplit()
        logger.debug("read and processed 1st header")

        logger.debug("Found the following entries in the header line:\n\t {}".format(", ".join(self.labels)))

        buffer = f.readline()
        self.Nzones = int(buffer.rsplit()[0])
        try:
            self.time = float(buffer.rsplit()[1])
        except IndexError:
            self.time = None

        logger.debug("read and processed 2nd header")
        logger.info("model has {:d} zones".format(self.Nzones))
        if self.time is not None:
            logger.info("starts at {:e} seconds after explosion".format(self.time))

        tmpdata = np.loadtxt(f)

        try:
            assert(tmpdata.shape[-1] == len(self.labels))
        except AssertionError:
            logger.error("Error: numbers of columns in the header and data section don't match:\nheader: %d columns; data section: %d columns\nAborting! File corrupt?" % (tmpdata.shape[-1], len(self.labels)))
            raise IOError("Unable to read and process data section of %s" % self.fname)

        for label, data in zip(self.labels, tmpdata.T):
            self.set_data(label, data)

