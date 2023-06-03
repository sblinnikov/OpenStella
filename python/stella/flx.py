#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : flx.py
#
#  Purpose :
#
#  Creation Date : 30-10-2015
#
#  Last Modified : Wed 24 Aug 2016 18:42:16 CEST
#
#  Created By : UMN
#
# _._._._._._._._._._._._._._._._._._._._._.
import struct
import numpy as np
import astropy.units as units
import logging
import matplotlib.pyplot as plt


# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s -%(name)s - %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class _flx_record_reader(object):
    """Read a single fortran record of a Stella flx file.

    Used by flx_reader.

    Parameters
    ----------
    fstream : file
        file object associated with the Stella flx file

    Attributes
    ----------
    Lsave : int
        number of snapshots saved in the record
    Mfreq : int
        total number of frequency bins
    Tcurved : units.Quantity array
        time of the snapshots
    Nfrus : np.ndarray
        number of active frequency bins
    Flsave : 2D np.ndarray
        emergent Flux, shape: (Mfreq x Lsave)
    """
    def __init__(self, fstream):
        """
        Nomenclature:

        i4 -- 32 bit integer
        f4 -- 32 bit floating point number
        f8 -- 64 bit floating point number


        Format of flx binary file record:

        i4 -- Nrecord: record length in byte
        i4 -- Lsaved: number of save snapshots
        Lsaved repetitions:
            f4 -- Tcurved: time of snapshot
            i4 -- Nfrus: number of used frequencies
            Mfreq repetitions:
                f8 -- flsave: stored frequency-dependent flux
        i4 -- Nrecord: record length in byte

        Notes:
        * relevant information was extracted from:
            - node _flx in ttfitsimpler4.trf (stellam/strad)
            - node _stinfoflux in stradio.trf  (stellam/src)
        * Mfreq defined in zone.inc (not stored in flx file)
        """

        self.fstream = fstream

        self._read_record()

    def _read_record(self):
        """Parse one Stella flx file record"""

        self.Nrec = struct.unpack("i", self.fstream.read(4))[0]

        self.Lsave = struct.unpack("i", self.fstream.read(4))[0]

        self.Mfreq = (self.Nrec - 4 - 8 * self.Lsave)//(self.Lsave * 8)

        logging.info("Calculated Mfreq: %d" % self.Mfreq)

        self.Tcurv = np.zeros(self.Lsave)
        self.Nfrus = np.zeros(self.Lsave)
        self.Flsave = np.zeros((self.Mfreq, self.Lsave))

        for i in xrange(self.Lsave):

            self.Tcurv[i] = struct.unpack("f", self.fstream.read(4))[0]
            self.Nfrus[i] = struct.unpack("i", self.fstream.read(4))[0]
            self.Flsave[:,i] = np.array(
                struct.unpack("{:d}d".format(self.Mfreq),
                              self.fstream.read(8 * self.Mfreq)))
        try:
            assert(self.Nrec == struct.unpack("i", self.fstream.read(4))[0])
        except AssertionError:
            logger.exception(
                "Mismatch in record length at start and end stamps")
            raise IOError
        logger.info("Record successfully read")

        # Time is stored in days
        self.Tcurv = self.Tcurv * units.d
        # Units of Flsave not clear

class flx_reader(object):
    """Reader for Stella flx binary files

    Relies on _flx_record_reader

    Parameters
    ----------
    fname : str
        full filename (including extension) of the flx file
    """
    def __init__(self, fname):

        self.fname = fname
        self.fstream = open(fname, "rb")

        self.records = []

        self._read_flx_file()
        self._prep_easy_access()

    def _read_flx_file(self):
        """Main Parser"""

        while 1:
            fpos = self.fstream.tell()
            buffer = self.fstream.read(4)
            if buffer == "":
                #EOF
                logger.info("EOF triggered")
                break
            else:
                if struct.unpack("i", buffer)[0] == 4:
                    #last record with Lsave = 0
                    logger.info("Last, empty, record found: stopping")
                    break
                else:
                    self.fstream.seek(fpos)
            self.records.append(_flx_record_reader(self.fstream))
            logger.info("Now at stream position {:d}".format(self.fstream.tell()))

        self.fstream.close()

    def _prep_easy_access(self):
        """Facilitates access of important record information

        Generates arrays holding the information of all records concerning the
        quantities:
        - Tcurv
        - Nfrus
        - Flsave

        """

        ntot = np.sum([rec.Lsave for rec in self.records])

        self.time = np.zeros(ntot) * rec.Tcurv.unit
        self.Nfrus = np.zeros(ntot)
        self.Flsave = np.zeros((rec.Mfreq, ntot))

        n = 0
        for rec in self.records:
            k = rec.Lsave
            self.time[n:n+k] = rec.Tcurv
            self.Nfrus[n:n+k] = rec.Nfrus
            self.Flsave[:, n:n+k] = rec.Flsave
            n = n+k

    def show_emergent_Fl(self, nu=None, logx=True, logy=True, logz=True,
                         cmap="afmhot", floor=1e-20, vmax=1e3, vmin=1e-7):
        """Visualize time-dependent evolution of Flsave

        A pcolormesh plot of Flsave will be created, with time on the y-axis
        and the frequency grid on the x-axis. The frequency grid is not stored
        in the .flx file and thus has be provided (for example from the prf
        file reader). If no nu values are provided, the plot will display
        Flsave against the nu grid indices.

        WARNING: unit of Flsave is still unknown

        WARNING: the nu grid in the prf file typically has the shape (Nfreq),
        while Flsave uses (Mfreq). However, the additional Flsave values are
        not used in any case (IMHO) so they are not displayed. In other words,
        we always display the first n values of Flsave, with n being the length
        of nu. If nu is None, n is Mfreq.

        Parameters
        ----------
        nu : None, units.Quantity array
            the frequency grid; has to be supplied by hand. If None, Flsave
            will be shown versus the index of the frequency bins (default None)
        logx : bool
            use logarithmic scaling on the x-Axis (default True)
        logy : bool
            use logarithmic scaling on the y-Axis (default True)
        logz : bool
            use logarithmic scaling for the Flsave values (default True)
        floor : float
            floor value for Flsave to eliminate zeros and negative values which
            cause problems in the logz=True mode (default 1e-20)
        cmap : str
            name of the colormap
        vmin : float
            minimum value for the color representation of the Flsave
            values (smaller values will be clipped). If logz=True, the
            logarithm of the vmin value will be passed to pcolormesh (default
            1e-7)
        vmax : float
            maximum value for the color representation of the Flsave
            values (larger values will be clipped). If logz=True, the
            logarithm of the vmin value will be passed to pcolormesh (default
            1e3)

        Returns
        -------
        fig : plt.figure
            figure instance containing plot
        aux : dict
            a dictionary containing references to other important plotting
            objects
        """

        if nu is None:
            logger.warning("No frequencies supplied - will plot vs. bin index")
            x = np.arange(self.records[0].Mfreq).astype(np.float) + 1
            xlabel = r"frequency bin index"
        else:
            try:
                x = nu.to("Hz").value
            except (units.UnitsError, AttributeError):
                logger.error(
                    "nu must be astropy quantity with a frequency unit")
                raise
            xlabel = r"$\nu$ [Hz]"

        lenZ = len(x)

        y = self.time.to("d").value
        X, Y = np.meshgrid(x, y)
        Z = np.maximum(self.Flsave[:lenZ, :].T, 1e-20)

        if logz:
            Z = np.log10(Z)
            vmax = np.log10(vmax)
            vmin = np.log10(vmin)
            zlabel = r"$\log$ Flsave"
        else:
            zlabel = r"Flsave"

        fig = plt.figure()
        ax = fig.add_subplot(111)
        im = ax.pcolormesh(X, Y, Z, rasterized="True", cmap=cmap, vmin=vmin,
                           vmax=vmax)

        cbar = plt.colorbar(im)
        if logx:
            ax.set_xscale("log")
        if logy:
            ax.set_yscale("log")

        ax.set_xlabel(xlabel)
        ax.set_ylabel(r"$t$ [d]")
        cbar.set_label(zlabel)
        ax.axis("tight")

        return fig, {"ax": ax, "cbar": cbar, "im": im}


if __name__ == "__main__":

    test = flx_reader("m100101wgrid1304.flx")
