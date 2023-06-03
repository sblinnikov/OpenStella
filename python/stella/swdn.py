#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : swdn.py
#
#  Purpose : read and process Stella swd files
#
#  Creation Date : 02-12-2015
#
#  Last Modified : Wed 02 Dec 2015 18:03:41 CET
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""This module provides readers to parse swd (shock wave details) files
produced by Stella

Notes
-----
The SM script [1]_ has been used as a blueprint to interpret the different data
blocks of the swd files.

.. [1] stella/strad/run/swdn.sm
"""
from __future__ import print_function
import numpy as np
import astropy.units as units
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class log_quantity(object):
    """A simple class to emulate the behaviour of logQuantities of astrophy
    v1.1

    Parameters
    ----------
    logval : float/int scalar or np.ndarray
        the logarithmic values of the quantity of interest
    unit : astropy.units.UnitBase
        unit of the quantity of interest
    base : float
        base of the logarithm (default 10)

    Examples
    --------
    >>> logL = log_quantity(42, units.erg / units.s)
    >>> logL.value
    42.0
    >>> logL.physical
    <Quantity 1e+42 erg / s>

    Notes
    -----
    Should be replaced by astropy's  logarithmic units framework once v1.1
    becomes the current stable version.

    """
    def __init__(self, logval, unit, base=10):
        self.logval = logval
        self.unit = unit
        self.base = base

    @property
    def value(self):
        """Return the logarithmic value (without units)"""
        return self.logval

    @property
    def physical(self):
        """Return the physical value"""
        return self._to_physical()

    def _to_physical(self):
        """Return the physical value
        Returns:
        -------
        physical : astropy.units.Quantity
            the physical values underlying the logarithmic quantity
        """

        return self.base**self.logval * self.unit


class swd_snapshot(object):
    """
    A single snapshot, i.e. time step of a Stella swd file

    Parameters
    ----------
    raw_data : numpy.ndarray (of shape Nzones x 13)
        snapshot data, provided in a 2D numpy array

    Attributes
    ----------
    rtot : astropy.units.Quantity scalar
        total radius of the model
    v : astropy.units.Quantity array
        model velocity
    T : astropy.units.Quantity array
        gas temperature
    Tr : astropy.units.Quantity array
        radiation temperature
    mr : astropy.units.Quantity array
        mass coordinate (solar masses)
    mtot : astropy.units.Quantity scalar
        total mass (solar masses)
    rho : astropy.units.Quantity array
        gas density
    tau : numpy array
        optical depth
    Llum : astrophy.units.Quantity array
        some quantity related to luminosity (@Seb: clarification required)
    time : astropy.units.Quantity scalar
        time of the snapshot (corrected for light travel time to model center)
    nzones : int
        number of radial shells
    km : numpy array (int)
        shell index
    lgm : log_quantity of array
        logarithmic mass (mass in solar masses)
    lgr : log_quantity of array
        logarithmic radius
    r : astropy.units.Quantity array
        radius (of right shell interface)
    dr : astropy.units.Quantity array
        cell width
    v8 : log_quantity of array
        fluid velocity (units of 10cm/s)
    lgT : log_quantity of array
        gas temperature
    lgTr : log_quantity of array
        radiation temperature
    lgrho : log_quantity of array
        gas density (units of 1e-6 g/cm^3)
    lgP : log_quantity of array
        pressure
    lgqv : numpy array
        meaning unknown, @Seb please clarify
    lgeng12 : log_quantity of array
        specific gamma ray heating rate (units of 1e12 erg/s/g)
    lum40 : numpy array
        meaning unknown, something related to luminosity, @Seb please clarify
    cap : astropy.units.Quantity array
        specific interaction cross section
    gheating : astropy.units.Quantity array
        gamma hearing rate (units erg/s)
    igheating : astropy.units.Quantity array
        integrated gamma heating rate, i.e. total gamma heating in all cells
        below and including the one of interest
    totgheating : astropy.units.Quantity scalar
        total gamma ray heating rate
    righeating : astrophy.units.Quantity array
        integrated gamma heating rate relative to total one

    Notes:
    ------
    - one could think about introducing a caching system for some (all) derived
      quantities
    """
    def __init__(self, raw_data):

        self._tau = None
        self._gheating = None
        self._igheating = None
        self._righeating = None
        self._totgheating = None

        # UMN - snapshot time in days; corrected for light travel time from r=0
        # to outer edge of model
        self.time = raw_data[0, 0] * units.d
        self.nzones = raw_data.shape[0]
        self.raw_data = raw_data

        self.km = raw_data[:, 1]
        self.lgm = log_quantity(raw_data[:, 2], units.M_sun)
        self.lgr = log_quantity(raw_data[:, 3], units.cm)
        self.v = raw_data[:, 4] * 1e8 * units.cm/units.s
        self.lgT = log_quantity(raw_data[:, 5], units.K)
        self.lgTr = log_quantity(raw_data[:, 6], units.K)
        self.lgrho = log_quantity(raw_data[:, 7], 1e-6 * units.g/units.cm**3)
        self.lgP = log_quantity(raw_data[:, 8], units.dyn/units.cm**2)
        self.lgqv = raw_data[:, 9]
        self.lgeng12 = log_quantity(raw_data[:, 10], 1e12 *
                                    units.erg/units.s/units.g)
        self.lum40 = raw_data[:, 11]
        self.cap = raw_data[:, 12] * units.cm**2/units.g

    @property
    def r(self):
        """physical radius"""
        return self.lgr.physical

    @property
    def dr(self):
        """cell width"""
        # UMN - Rcore currently neglected (i.e. set to 0)
        return self.r - np.append(0, self.r[:-1]) * self.r.unit

    @property
    def rtot(self):
        """maximum radius"""
        return self.r[-1]

    @property
    def mtot(self):
        """total mass of model"""
        return self.lgm.physical[0]

    @property
    def mr(self):
        """total mass enclosed within radius r"""
        return self.mtot - self.lgm.physical

    @property
    def dm(self):
        """shell mass"""
        # UMN - Mcore currently neglected (i.e. set to 0)
        return self.mr - np.append(0, self.mr)[:-1] * self.mr.unit

    @property
    def v8(self):
        """fluid velocity in units of cm/s"""
        return self.v.to(1e8 * units.cm/units.s)

    @property
    def T(self):
        """gas temperature in K"""
        return self.lgT.physical

    @property
    def Tr(self):
        """radiation temperature in K"""
        return self.lgTr.physical

    @property
    def Llum(self):
        """unknown luminosity quantity, units unclear"""
        return 0.5 * np.log10(self.lum40**2)

    @property
    def rho(self):
        """density in g/cm^3"""
        return self.lgrho.physical

    @property
    def tau(self):
        """optical depth"""
        if self._tau is None:
            self._tau = np.zeros(self.nzones)
            for i in xrange(self.nzones - 2, -1, -1):
                self._tau[i] = (self._tau[i+1] + (self.cap)[i] * (self.rho)[i]
                                * ((self.r)[i+1] - (self.r)[i]))
            self._tau[-1] = self._tau[-2] * 0.5
        return self._tau

    @property
    def gheating(self):
        """gamma heating rate"""
        if self._gheating is None:
            self._gheating = (self.lgeng12.physical * self.dm).to("erg / s")
        return self._gheating

    @property
    def igheating(self):
        """integrated gamma heating rate"""
        if self._igheating is None:
            self._igheating = np.zeros(self.nzones)
            self._igheating[0] = self.gheating[0].value
            for i in xrange(1, self.nzones):
                self._igheating[i] = (self._igheating[i-1] +
                                      self.gheating[i].value)
            self._igheating *= self.gheating.unit
        return self._igheating

    @property
    def righeating(self):
        """relative integrated gamma heating rate"""
        if self._righeating is None:
            self._righeating = self.igheating / self.totgheating
        return self._righeating

    @property
    def totgheating(self):
        """total gamma heating rate"""
        if self._totgheating is None:
            self._totgheating = self.igheating[-1]
        return self._totgheating


class swd_reader(object):
    """Parser for an entire *.swd file created by Stella

    Parameters
    ----------
    mname : str
        model name: if parent_dir and explicit_fname are both None, it is
        assumed that a <mname.swd> exists in the current working directory.
    parent_dir : None or str (optional)
        if provided (i.e. not None), a <mname.swd> file is opened not in the
        current working directory but in the path specified by parent_dir
    explicit_fname : None or str (optional)
        if provided (i.e. not None; should be full absolute or relative path to
        file), the specified file is opened. In this case, parent_dir has no
        effect. Use this parameter for example in cases in which the shock wave
        detail file has to not the comment extension 'swd'.

    Attributes
    ----------
    mname : str
        model name
    fname : str
        absolute path to swd file
    times : astropy.units.Quantity array
        time stamps of the different snapshots
    times_dict : dict
        dictionary linking time stamps with snapshot indices
    """
    def __init__(self, mname, parent_dir=None, explicit_fname=None):

        self.mname = mname.rsplit("/")[-1]

        if self.mname[-4:] is ".swd":
            self.mname = self.mname[:-4]
        else:
            mname = mname + ".swd"

        if parent_dir is None:
            parent_dir = "./"

        if explicit_fname is None:
            self.fname = os.path.abspath(os.path.join(parent_dir, mname))
        else:
            self.fname = os.path.abspath(explicit_fname)

        self.process_swd_file()

    def process_swd_file(self):
        """
        Process the swd file, i.e. store contents in the snapshots array
        """

        logger.info("Reading shock wave details \
                    file for model {}".format(self.mname))
        logger.debug("Loading file {}".format(self.fname))
        tmpdata = np.loadtxt(self.fname)

        self.Nzones = int(np.max(tmpdata[:, 1]))
        logger.info("Found grid with {:d} cells".format(self.Nzones))
        self.Ntimes = tmpdata.shape[0]//self.Nzones

        self.snapshots = [swd_snapshot(tmpdata[self.Nzones * (i-1):
                                               self.Nzones * i, :])
                          for i in xrange(1, self.Ntimes + 1)]
        self.times = (np.array([self.snapshots[i].time.value
                                for i in xrange(self.Ntimes)]) *
                      self.snapshots[0].time.unit)
        self.times_dict = dict([(i, self.snapshots[i].time)
                                for i in xrange(self.Ntimes)])

        logger.info("processed the following {:d} \
                    snapshots:".format(self.Ntimes))
        for t in xrange(self.Ntimes):
            logger.info("{: 4d}: {: 6.1f} days".format(t, self.times[t].value))

    def snapshot(self, i):
        """Return snapshot with index i

        Parameters:
        -----------
        i : int
            index of requested snapshot

        Returns:
        --------
        snapshot : ~swd_snapshot or None
            requested snapshot, None if i is invalid index

        """
        try:
            return self.snapshots[i]
        except IndexError:
            logger.warning("Warning: Invalid snapshot index {:d}".format(i))
            return None

    def snapshott(self, t):
        """Return snapshot lying closest to requested time

        Parameters:
        -----------
        t : astropy.units.Quantity scalar
            requested time

        Returns:
        --------
        snapshot : ~swd_snapshot
            snapshot lying closest to requested time
        """

        try:
            t.unit
        except AttributeError:
            logger.warning("Warning: time passed without unit; assuming 'day'")
            t = t * units.day

        i = np.argmin(np.fabs(self.times - t))

        return self.snapshot(i)


def test(mname="m030307mhomo"):
    """
    A simple script to test the swd_reader; automatically called in main

    Will only work without adjustment of mname if m030307mhomo.swd is in
    current working directory.

    Arguments:
    ----------
    mname : str
        model name (default 'm03037mhomo')

    """

    test_reader = swd_reader(mname)
    print("Model has {:d} zones".format(test_reader.Nzones))


if __name__ == "__main__":

    test()
