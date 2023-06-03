#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : prf.py
#
#  Purpose : reading and processing Stella prf files
#
#  Creation Date : 02-11-2015
#
#  Last Modified : Fri 26 Aug 2016 15:51:46 CEST
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""This module provides a reader for the binary files with extension '.prf'
produced by Stella

Notes
-----

 - TODO: full astropy.units.Quantity support
 - TODO: PEP8 compliance

"""
from __future__ import print_function
import struct
import numpy as np
import logging
import astropy.constants as csts
import astropy.units as units
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cols


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class prf_snapshot_reader(object):
    """
    Parser for a single snapshot stored in the prf file

    Some quantities are not stored in the prf file itself, but are required to
    determine dimensions and lengths of several data blocks in the prf file.
    These are typically defined in one of the '.inc' files in the obj directory
    of the Stella source code. They have to be provided as parameters in the
    constructor.

    Currently only one parsing mode, emulating the _strinfomodel node in
    stradio.trf, is implemented: 'sm'

    Parameters
    ----------
    fname : str
        name of the Stella .prf file
    Natom : int
        number of atoms used in the Stella run, adopt value from zone.inc
    Maxder : int
        another array size parameter, adopt value from zone.inc
    Nfreq : int
        number of frequency bins used in the Stella run, adopt value from
        zone.inc
    Mfreq : int
        another array size parameter, related to the frequency grid, adopt
        value from zone.inc
    Nvars : int
        another array size parameter, adopt value from zone.inc
    Hntlen : int
        length of Hnt array, adopt value defined in snrad.inc
    mode : {'sm'}
        parsing mode, nomenclature adopted from stradio.trf

    Attributes
    ----------
    t : float
        time of snapshot in seconds/Utime
    Utime : astropy.units.Quantity scalar
        conversion factor between internal Stella time and seconds
    Utp : astropy.units.Quantity scalar
        conversion factor between Stella-internal and physical temperatures
    Urho : astropy.units.Quantity scalar
        conversion factor between Stella-internal and physical densities
    Ufreq : astropy.units.Quantity scalar
        conversion factor between Stella-internal and physical frequencies
    Uv : astrophy.units.Quantity scalar
        conversion factor between Stella-internal and physical velocities
    fstream : file object
        reference to file stream
    Y : array_like
        basic data block, containing information about density, velocity,
        temperature and details about the radiation field

    """
    def __init__(self, fstream, Natom=15, Maxder=4, Nfreq=300, Mfreq=330,
                 Nvars=3, Hntlen=7, mode="sm"):

        known_modes = ["sm"]

        try:
            assert(mode in known_modes)
        except AssertionError:
            logging.exception(
                "Unknown parsing mode '{:s}'; ".format(mode) +
                "currently only the following modes are implemented: " +
                "'{:s}'".format(",".join(known_modes)))
            raise ValueError

        self.fstream = fstream
        self.Natom = Natom
        self.Maxder = Maxder
        self.Nfreq = Nfreq
        self.Mfreq = Mfreq
        self.Nvars = Nvars
        self.Hntlen = Hntlen

        if mode == "sm":
            logging.info("Initialising reader in '{:s}' mode: ".format(mode) +
                         "corresponds to node _stinfomodel in stradio.trf")
            self.read_file_stinfomodel()
        else:
            raise ValueError

    def read_file_stinfomodel(self):
        """
        Reads general parameters and data from *.prf file

        The nomenclature is chosen to reflect the names of Stella variables

        This reader function is based on the node _strinfomodel in subroutine
        stradio, which is defined in stradio.trf (stellam/src/).

        Notes
        -----

        The following binary structure is expected (c.f. stradio.trf):

        - BegNrec: i4 -- start size stamp of unformatted fortran record
        - t: f8
        - Nstep: i4
        - Ktail: i4
        - Nzon: i4
        - Nqused: i4
        - Krad: i4
        - Ncnd: i4
        - Nfrus: i4
        - Nreg: Nzon x i4
        - Xa: d8
        - Ya: d8
        - Xyza: d8
        - Eko: d8
        - Radbeg: d8
        - Rce: d8
        - Elost: d8
        - Ulgcap: d8
        - Ulgeps: d8
        - Ulgp: d8
        - Ulgv: d8
        - Ulge: d8
        - Uepri: d8
        - Utime: d8
        - Up: d8
        - Upi: d8
        - Ue: d8
        - Uei: d8
        - Ck1: d8
        - Ck2: d8
        - Cfr: d8
        - Craold: d8
        - Um: d8
        - Uv: d8
        - Urm: d8
        - Dm: Nzon x f8
        - Am: Nzon x f8
        - Dmin: d8
        - Amini: d8
        - Dmout: d8
        - Amount: d8
        - Yabun: Nzon x Natom x f8
        - Y: (Nvars x Nzon + 2 x Krad) x f8
        - Jstart: i4
        - Meth: i4
        - Kflag: i4
        - Evalja: i4
        - Oldjac: i4
        - Badste: i4
        - Nclast: i4
        - Nfun: i4
        - Njac: i4
        - Niter: i4
        - Nfail: i4
        - Meo: i4
        - Nold: i4
        - Lnq: i4
        - Idoub: i4
        - Nthick: Nfreq x i4 (Fortran Logical)
        - Lthick: Nfreq x i4 (Fortran Logical)
        - Hused: d8
        - Rmax: d8
        - Trend: d8
        - Oldl0: d8
        - Rc: d8
        - Hold: d8
        - Edn: d8
        - E: d8
        - Eup: d8
        - Bnd: d8
        - Epsold: d8
        - Told: d8
        - Tauold: d8
        - Amht: d8
        - Eburst: d8
        - Tburst: d8
        - Amni: d8
        - Xmni: d8
        - Yentot: (Maxder+1) x f8
        - H: d8
        - Holdbl: d8
        - Etot0: d8
        - Freq: (Nfreq+1) x f8
        - Freqmn: (Nfreq+1) x f8
        - Dlognu: (Nfreq+1) x f8
        - Weight: Mfreq x f8
        - Hnt: 7 x f8
        - EndNrec: i4 -- end size stamp of unformatted fortran record

        """

        logging.info("Starting parsing of prf file in stinfomodel mode")

        self.startNrec = struct.unpack("i", self.fstream.read(4))[0]
        self.t = struct.unpack("d", self.fstream.read(8))[0]
        self.Nstep, self.Ktail, self.Nzon, self.Nqused, self.Krad, self.Ncnd,\
            self.Nfrus = struct.unpack("7i", self.fstream.read(7 * 4))
        self.Nreg = np.array(struct.unpack("{:d}i".format(self.Nzon),
                                           self.fstream.read(self.Nzon * 4)))
        self.Xa, self.Ya, self.Xuza, self.Eko, self.Radbeg, self.Rce, \
            self.Elost, self.Ulgcap, self.Ulgeps, self.Ulgp, self.Ulgv, \
            self.Ulge, self.Uepri, self.Utime, self.Up, self.Upi, self.Ue, \
            self.Uei, self.Ck1, self.Ck2, self.Cfr, self.Craold, self.Um, \
            self.Uv, self.Urm = struct.unpack("25d", self.fstream.read(25 * 8))
        self.Dm = np.array(struct.unpack("{:d}d".format(self.Nzon),
                                         self.fstream.read(self.Nzon * 8)))
        self.Am = np.array(struct.unpack("{:d}d".format(self.Nzon),
                                         self.fstream.read(self.Nzon * 8)))
        self.Dmin, self.Amini, self.Dmout, self.Amout = \
            struct.unpack("4d", self.fstream.read(4 * 8))
        self.Yabun = np.array(
            struct.unpack("{:d}d".format(self.Nzon * self.Natom),
                          self.fstream.read(self.Nzon * self.Natom * 8)))
        self.Y = np.array(
            struct.unpack("{:d}d".format(self.Nzon*self.Nvars+2*self.Krad),
                          self.fstream.read(
                              (self.Nzon*self.Nvars+2*self.Krad) * 8)))
        self.Jstart, self.Meth, self.Kflag, self.Evaldja, self.Oldjac,\
            self.Badste, self.Nclast, self.Nfun, self.Njac, self.Niter,\
            self.Nfail, self.Meo, self.Nold, self.Lng, self.Idoub = \
            struct.unpack("15i", self.fstream.read(15 * 4))
        self.Nthick = np.array(
            struct.unpack("{:d}i".format(self.Nfreq),
                          self.fstream.read(self.Nfreq * 4)))
        self.Lthick = np.array(
            struct.unpack("{:d}i".format(self.Nfreq * self.Nzon),
                          self.fstream.read(self.Nfreq * self.Nzon * 4)))
        self.Hused, self.Rmax, self.Trend, self.Oldl0, self.Rc, self.Hold,\
            self.Edn, self.E, self.Eup, self.Bnd, self.Epsold,\
            self.Told, self.Tauold, self.Amht, self.Eburst, self.Tburst,\
            self.Amni, self.Xmni = struct.unpack(
                "18d", self.fstream.read(18 * 8))
        self.Yentot = np.array(
            struct.unpack("{:d}d".format(self.Maxder+1),
                          self.fstream.read((self.Maxder + 1) * 8)))
        self.H, self.Holdbl, self.Etot0 = struct.unpack(
            "3d", self.fstream.read(3 * 8))
        self.Freq = np.array(
            struct.unpack("{:d}d".format(self.Nfreq+1),
                          self.fstream.read((self.Nfreq+1) * 8)))
        self.Freqmn = np.array(
            struct.unpack("{:d}d".format(self.Nfreq),
                          self.fstream.read(self.Nfreq * 8)))
        self.Dlognu = np.array(
            struct.unpack("{:d}d".format(self.Nfreq),
                          self.fstream.read(self.Nfreq * 8)))
        self.Weight = np.array(
            struct.unpack("{:d}d".format(self.Mfreq),
                          self.fstream.read(self.Mfreq * 8)))
        self.Hnt = np.array(
            struct.unpack("{:d}d".format(self.Hntlen),
                          self.fstream.read(self.Hntlen * 8)))

        self.endNrec = struct.unpack("i", self.fstream.read(4))[0]

        # assigning correct units (where possible and where units are known)
        self.Utime *= units.s
        self.Uv *= units.cm / units.s

        # we explicitly assume that UTP=1e5 (double check used *.inc files)
        self.Urho = 1e-6 * units.g / units.cm**3
        self.Utp = 1e5 * units.K
        self.Ufreq = self.Utp * csts.k_B / csts.h

        try:
            assert(self.startNrec == self.endNrec)
        except AssertionError:
            logging.exception("Mismatch in fortran record size stamps;")
            logging.info("\nStart size stamp {:d}\n".format(self.startNrec) +
                         "End size stamp   {:d}\n".format(self.endNrec) +
                         "Check your input Nfreq, Natom, Maxder, Mfreq, " +
                         "Nvars, Hntlen")
            raise IOError
        logging.info("stinfomodel parsing of prf file successful")


class prf_quantity(object):
    """Easy access utility wrapper for some quantities stored in the prf file

    With this wrapper the snapshot data may easily accessed in three different
    ways, either providing the snapshot index (access method), the nearest
    cycle number (cycle class method) or the nearest timestamp (time method).

    Parameters:
    -----------
    parent : prf_reader
        parent prf_reader object storing the source data

    """
    def __init__(self, parent):

        self.parent = parent

    def find_index_time(self, t, mode="obs"):
        """Identifies the snapshot which lies closest to the requested time

        Parameters:
        -----------
        t : float
            requested time
        mode : {'phys', 'obs', 'raw'}

        Returns:
        --------
        i : int
            index of the closest snapshot

        """

        possible_modes = ['phys', 'obs', 'raw']

        try:
            assert(mode in possible_modes)
        except AssertionError:
            logging.error("unknown mode '{:s}';".format(mode) +
                          "allowed modes are {:s}".format(
                              ", ".join(possible_modes)))
            raise ValueError

        if mode == "phys":
            snap_times = self.parent.phys_times
        elif mode == "obs":
            snap_times = self.parent.obs_times
        else:
            snap_times = self.parent.raw_times

        i = np.argmin(np.fabs(snap_times - t))
        logging.info("requested time {:s}, ".format(t) +
                     "found snapshot with t {}".format(
                         self.parent.snapshots[i].t))

        return i

    def _full_list(self):

        ntot = len(self.parent.raw_times)
        full = []

        for i in xrange(ntot):
            full.append(self.access(i))

        return full

    def _full_nparr(self):

        first = self.access(0)
        ntot = len(self.parent.raw_times)
        full = np.zeros([ntot] + list(first.shape))

        try:
            full = full * first.unit
        except AttributeError:
            pass

        for i in xrange(ntot):
            full[i] = self.access(i)

        return full

    def full(self):

        return self._full_nparr()

    def find_index_cycle(self, ncycle):
        """Identifies the snapshot with the step number closest to the requested cycle

        Parameters:
        -----------
        ncycle : int
            requested cycle

        Returns:
        --------
        i : int
            index of the closest snapshot

        """

        i = np.argmin(np.fabs(self.parent.nsteps - ncycle))
        logging.info(
            "requested cycle {:d}, ".format(ncycle) +
            "found snapshot with Nstep {:d}".format(
                self.parent.snapshots[i].Nstep))

        return i

    def access(self, i):
        """Access the data from the specified snapshot

        This method should be overloaded in the derived classes according to
        how the physical quantity of interest can be reconstructed from the
        data stored in the prf_snapshots

        Parameters:
        -----------
        i : int
            snapshot index

        """

        pass

    def cycle(self, ncycle):
        """Access the data from the snapshot with the step number closest to
        the requested cycle

        Parameters:
        ----------
        ncycle : int
            requested cycle

        """

        i = self.find_index_cycle(ncycle)

        return self.access(i)

    def time(self, t, mode="obs"):
        """Access the data from the snapshot being closest to the requested time

        Parameters:
        -----------
        t : float
            requested time

        """

        i = self.find_index_time(t, mode=mode)

        return self.access(i)


class prf_J(prf_quantity):
    """Easy Access wrapper for the mean intensity of the radiation field

    Parameters:
    -----------
    parent : prf_reader
        prf_reader object which holds the raw data

    """
    def __init__(self, parent):

        super(prf_J, self).__init__(parent)
        self.ident = "J"
        self.latex_symbol = r"$J_{\nu}$"

    def access(self, i):
        """Extracts the mean intensity from the prf data

        Parameters:
        -----------
        i : int
            index of the prf snapshot

        Returns:
        --------
        J : astropy.units.Quantity 2D array
            mean intensity J_nu
        """

        snap = self.parent.snapshots[i]

        J = (
            np.maximum(
                (snap.Y[snap.Nvars * snap.Nzon:snap.Nvars * snap.Nzon +
                        (snap.Nfrus * (snap.Nzon - snap.Ncnd))].reshape(
                            (snap.Nzon - snap.Ncnd, snap.Nfrus), order="F") *
                 snap.Freqmn[None, :snap.Nfrus]**3), 1e-20) *
            snap.Ufreq**3 * 2 * csts.h / csts.c**2).to(
                "erg / (Hz * s * cm**2)")

        return J

    def full(self):

        return self._full_list()


class prf_H(prf_quantity):
    """Easy Access wrapper for the radiation field flux

    Parameters:
    -----------
    parent : prf_reader
        prf_reader object which holds the raw data

    """
    def __init__(self, parent):

        super(prf_H, self).__init__(parent)
        self.ident = "H"
        self.latex_symbol = r"$H_{\nu}$"

    def access(self, i):
        """Extracts the radiation field flux from the prf data

        Parameters:
        -----------
        i : int
            index of the prf snapshot

        Returns:
        --------
        H : astropy.units.Quantity 2D array
            first moment of specific intensity (~radiative flux), H_nu

        """

        snap = self.parent.snapshots[i]

        H = (
            np.maximum((snap.Y[snap.Nvars * snap.Nzon + snap.Krad:snap.Nvars *
                               snap.Nzon + snap.Krad +
                               (snap.Nfrus * (snap.Nzon - snap.Ncnd))].reshape(
                                   (snap.Nzon - snap.Ncnd, snap.Nfrus),
                                   order="F") *
                        snap.Freqmn[None, :snap.Nfrus]**3), 1e-20) *
            snap.Ufreq**3 * 2 * csts.h / csts.c**2).to(
                "erg / (Hz * s * cm**2)")

        return H

    def full(self):

        return self._full_list()


class prf_v(prf_quantity):
    """Easy Access wrapper for the material velocity

    Parameters:
    ----------
    parent : prf_reader
        prf_reader object which holds the raw data

    """
    def __init__(self, parent):

        super(prf_v, self).__init__(parent)
        self.ident = "v"
        self.latex_symbol = r"$v$"

    def access(self, i):
        """Extracts the material velocity from the prf data


        Parameters:
        -----------
        i : int
            index of the prf snapshot

        Returns:
        --------
        v : astropy.units.Quantity array
            material velocity
        """

        snap = self.parent.snapshots[i]

        return snap.Y[snap.Nzon:snap.Nzon * 2] * snap.Uv


class prf_r(prf_quantity):
    """Easy Access wrapper for the radial coordinate


    Parameters:
    ----------
    parent : prf_reader
        prf_reader object which holds the raw data

    """
    def __init__(self, parent):

        super(prf_r, self).__init__(parent)
        self.ident = "r"
        self.latex_symbol = r"$r$"

    def access(self, i):
        """Extracts the radial coordinate from the prf data

        Parameters:
        -----------
        i : int
            index of the prf snapshot

        Returns:
        --------
        r : astropy.units.Quantity array
            material velocity
        """

        snap = self.parent.snapshots[i]

        return snap.Y[:snap.Nzon] * 1e14 * units.cm


class prf_T(prf_quantity):
    """Easy Access wrapper for the material temperature


    Parameters:
    ----------
    parent : prf_reader
        prf_reader object which holds the raw data

    """
    def __init__(self, parent):

        super(prf_T, self).__init__(parent)
        self.ident = "T"
        self.latex_symbol = r"$T$"

    def access(self, i):
        """Extracts the material temperature from the prf data

        Parameters:
        -----------
        i : int
            index of the prf snapshot

        Returns:
        --------
        T : astropy.units.Quantity array
            material temperature

        """

        snap = self.parent.snapshots[i]

        return snap.Y[2 * snap.Nzon:3 * snap.Nzon] * snap.Utp


class prf_rho(prf_quantity):
    """Easy Access wrapper for the material density

    Parameters:
    ----------
    parent : prf_reader
        prf_reader object which holds the raw data

    """
    def __init__(self, parent):

        super(prf_rho, self).__init__(parent)
        self.ident = "rho"
        self.latex_symbol = r"$\rho$"

    def access(self, i):
        """Extracts the material density from the prf data

        Parameters:
        -----------
        i : int
            index of the prf snapshot

        Returns:
        --------
        rho : astropy.units.Quantity
            material density

        """

        snap = self.parent.snapshots[i]

        r = self.parent.r.access(i).to("1e14 cm").value
        rl = np.append(snap.Rce, r[:-1])

        rho = 3. * snap.Dm / (r**3 - rl**3)

        return rho * snap.Urho


class prf_m(prf_quantity):
    """Easy Access wrapper for the mass coordinate

    Parameters:
    ----------
    parent : prf_reader
        prf_reader object which holds the raw data

    """
    def __init__(self, parent):

        super(prf_m, self).__init__(parent)
        self.ident = "M"
        self.latex_symbol = r"$M_r$"

    def access(self, i):
        """Extracts the mass coordinate in units of solar masses from the prf
        data

        Parameters:
        -----------
        i : int
            index of the prf snapshot

        Returns:
        --------
        m : astropy.units.Quantity array
            material density in solar masses

        """

        snap = self.parent.snapshots[i]

        return snap.Am * snap.Um * units.solMass


class prf_nu(prf_quantity):
    """Easy access wrapper for the frequency

    Parameters
    ----------
    parent : prf_reader
        prf_reader object holding the raw data

    """
    def __init__(self, parent):

        super(prf_nu, self).__init__(parent)
        self.ident = "nu"
        self.latex_symbol = r"$\nu$"

    def access(self, i):
        """Extracts the frequency grid in units of Hz from the prf data

        Parameters
        ----------
        i : int
            index of the prf snapshot

        Returns
        -------
        nu : astropy.units.Quantity array
            frequency grid
        """

        snap = self.parent.snapshots[i]

        return (snap.Freqmn * snap.Ufreq).to("Hz")


class prf_nu_4J(prf_nu):
    """Easy access wrapper for the frequency with an appropriate cut to be used
    together with J or H

    Only the first Nfrus frequencies are returned.

    Parameters
    ----------
    parent : prf_reader
        prf_reader object holding the raw data

    """
    def __init__(self, parent):

        super(prf_nu_4J, self).__init__(parent)

    def access(self, i):
        """Extracts frequency grid and performs cut

        Parameters
        ----------
        i : int
            index of the prf snapshot

        Returns
        -------
        nu : astropy.units.Quantity array
            cut frequency grid
        """

        nu = super(prf_nu_4J, self).access(i)
        snap = self.parent.snapshots[i]

        return nu[:snap.Nfrus]

    def full(self):

        return self._full_list()


class prf_r_4J(prf_r):
    """Easy access wrapper for the radial coordinate with an appropriate cut to
    be used together with J or H

    Only the radial points after Ncnd are returned, i.e. the conduction region
    is carved out.

    Parameters
    ----------
    parent : prf_reader
        prf_reader object holding the raw data

    """

    def __init__(self, parent):

        super(prf_r_4J, self).__init__(parent)

    def access(self, i):
        """Extracts radial coordinates and performs cut

        Parameters
        ----------
        i : int
            index of the prf snapshot

        Returns
        -------
        r : astropy.units.Quantity array
            radial coordinates of non-conduction region
        """

        r = super(prf_r_4J, self).access(i)
        snap = self.parent.snapshots[i]

        return r[snap.Ncnd:]

    def full(self):

        return self._full_list()


class prf_m_4J(prf_m):
    """Easy access wrapper for the mass coordinate with an appropriate cut to
    be used together with J or H

    Only the radial points after Ncnd are returned, i.e. the conduction region
    is carved out.

    Parameters
    ----------
    parent : prf_reader
        prf_reader object holding the raw data

    """
    def __init__(self, parent):

        super(prf_m_4J, self).__init__(parent)

    def access(self, i):
        """Extracts mass coordinates and performs cut

        Parameters
        ----------
        i : int
            index of the prf snapshot

        Returns
        -------
        m : astropy.units.Quantity array
            mass coordinates of non-conduction region
        """

        m = super(prf_m_4J, self).access(i)
        snap = self.parent.snapshots[i]

        return m[snap.Ncnd:]

    def full(self):

        return self._full_list()


class rawtime_quantity(units.Quantity):
    ident = "raw_times"
    latex_symbol = "raw times"


class obstimes_quantity(units.Quantity):
    ident = "observer time"
    latex_symbol = r"$t_{\mathrm{obs}}$"


class phystimes_quantity(units.Quantity):
    ident = "physical time"
    latex_symbol = r"$t_{\mathrm{phys}}$"


class prf_reader(object):
    """
    Parser for a Stella prf binary file

    Some quantities are not stored in the prf file itself, but are required to
    determine dimensions and lengths of several data blocks in the prf file.
    These are typically defined in one of the '.inc' files in the obj directory
    of the Stella source code. They have to be provided as parameters in the
    constructor.

    Currently only one parsing mode, emulating the _strinfomodel node in
    stradio.trf, is implemented: 'sm'

    Parameters
    ----------
    fname : str
        name of the Stella .prf file
    Natom : int
        number of atoms used in the Stella run, adopt value from zone.inc
    Maxder : int
        another array size parameter, adopt value from zone.inc
    Nfreq : int
        number of frequency bins used in the Stella run, adopt value from
        zone.inc
    Mfreq : int
        another array size parameter, related to the frequency grid, adopt
        value from zone.inc
    Nvars : int
        another array size parameter, adopt value from zone.inc
    Hntlen : int
        length of Hnt array, adopt value defined in snrad.inc
    mode : {'sm'}
        parsing mode, nomenclature adopted from stradio.trf

    Attributes
    ----------
    fstream : file object
        reference to file stream
    snapshots : list of prf_snapshot_reader
        holds all the prf_snapshot_reader which have been read
    times : numpy.array
        holds the timestamps of all stored prf snapshots
    nsteps: numpy.array
        holds the step numbers of all stored prf snapshots

    """
    def __init__(self, fname, Natom=15, Maxder=4, Nfreq=300, Mfreq=330,
                 Nvars=3, Hntlen=7, mode="sm"):
        self.fstream = open(fname, "rb")

        self.Natom = Natom
        self.Maxder = Maxder
        self.Nfreq = Nfreq
        self.Mfreq = Mfreq
        self.Nvars = Nvars
        self.Hntlen = Hntlen
        self.mode = mode

        self.snapshots = []
        self.raw_times = []
        self.nsteps = []

        self.parse()

        self.raw_times = rawtime_quantity(self.raw_times)
        self.nsteps = np.array(self.nsteps)

        self.J = prf_J(self)
        self.H = prf_H(self)
        self.v = prf_v(self)
        self.T = prf_T(self)
        self.r = prf_r(self)
        self.r_4J = prf_r_4J(self)
        self.rho = prf_rho(self)  # must be after self.r
        self.m = prf_m(self)
        self.m_4J = prf_m_4J(self)
        self.nu = prf_nu(self)
        self.nu_4J = prf_nu_4J(self)

        self.phys_times = phystimes_quantity(np.zeros(len(self.snapshots)),
                                             unit=units.d)
        self.obs_times = obstimes_quantity(np.zeros(len(self.snapshots)),
                                           unit=units.d)

        for i, snap in enumerate(self.snapshots):
            self.phys_times[i] = (self.raw_times[i] *
                                  snap.Utime).to(self.phys_times.unit)
            self.obs_times[i] = (self.raw_times[i] * snap.Utime -
                                 self.r.access(i)[-1] /
                                 csts.c.cgs).to(self.obs_times.unit)

    def parse(self):
        """Parse the entire prf file


        """

        cont_parse = True

        while cont_parse:

            fpos = self.fstream.tell()
            buffer = self.fstream.read(4)
            if buffer == "":
                # EOF
                break
            else:
                self.fstream.seek(fpos)
                cont_parse = self.parse_snapshot()

    def parse_snapshot(self):
        """Parse a single snapshot of the prf file and store it in a
        prf_snapshot_reader object


        """
        try:
            tmp_snap = prf_snapshot_reader(
                self.fstream, Natom=self.Natom,
                Maxder=self.Maxder, Nfreq=self.Nfreq, Mfreq=self.Mfreq,
                Nvars=self.Nvars, Hntlen=self.Hntlen, mode=self.mode)
            self.snapshots.append(tmp_snap)
            self.raw_times.append(tmp_snap.t)
            self.nsteps.append(tmp_snap.Nstep)
            return True
        except AssertionError:
            return False

    def visualize_evolution(self, xfunc, yfunc, t, cmap="afmhot", tlog=False):

        assert(isinstance(xfunc, prf_quantity))
        assert(isinstance(yfunc, prf_quantity))

        fig = plt.figure()
        ax = fig.add_subplot(111)

        X = xfunc.full()
        Y = yfunc.full()

        assert(X.shape == Y.shape)
        assert(X.shape[0] == t.shape[0])

        zlabel = r"{:s}".format(t.latex_symbol)
        try:
            if tlog:
                zlabel = zlabel + "$/$" + t.unit.to_string("latex")
            else:
                zlabel = zlabel + " [" + t.unit.to_string("latex") + "]"
            t = t.to("d").value
        except (AttributeError, units.UnitsError):
            pass

        if tlog:
            t = np.log10(t)
            zlabel = r"$\log$" + zlabel

        mappable = None
        if cmap in cm.cmap_d.keys():
            mappable = cm.ScalarMappable(cmap=cm.cmap_d[cmap],
                                         norm=cols.Normalize(vmin=np.min(t),
                                                             vmax=np.max(t)))
            mappable.set_array(np.linspace(np.min(t), np.max(t), 256))

            cmap = cm.cmap_d[cmap]
            colors = [cmap((ti - t[0]) / (t[-1] - t[0])) for ti in t]
        else:
            colors = [cmap for ti in t]

        [ax.plot(x, y, color=colori) for x, y, colori in zip(X, Y, colors)]
        if mappable is not None:
            cbar = plt.colorbar(mappable, ax=ax, orientation="horizontal")
            cbar.set_label(zlabel)

        xlabel = r"{:s}".format(xfunc.latex_symbol)
        ylabel = r"{:s}".format(yfunc.latex_symbol)

        try:
            xlabel = xlabel + " [" + X.unit.to_string("latex") + "]"
        except AttributeError:
            pass
        try:
            ylabel = ylabel + " [" + Y.unit.to_string("latex") + "]"
        except AttributeError:
            pass

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return fig, {"ax": ax}


if __name__ == "__main__":

    tester = prf_reader("m100101wgrid1304.prf", mode="sm")
