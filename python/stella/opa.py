#!/usr/bin/env python
from __future__ import print_function
import struct
import numpy as np
import glob
import pandas as pd

class detailed_table(object):
    """Holds a detailed Stella opacity table

    When using xronfictd.exe, in addition to the common Stella opacity tables,
    a detailed table is written, containing the contributions of the different
    interaction processes. This class holds such a detailed table.

    Each interaction process is stored in an own pandas ND-panel with dimension
    Nfreq x Ntemps x Nrhos x Nzones/skip.

    The following contributions are stored separately:
    - bound-bound scattering, i.e. Thomson scattering
    - bound-bound absorption
    - bound-free absorption
    - free-free absorption
    """
    def __init__(self):
        """Inits the detailed_table"""

        self._Nzones = None
        self._skip = None
        self._Nfreq = None
        self._nus = None
        self._lamdas = None
        self._Nrho = None
        self._Ntemp = None
        self._rhos = None
        self._temps = None

        self._tabshape = None
        self._zones = None

        self._bbs = None
        self._bba = None
        self._bfa = None
        self._ffa = None

    @property
    def Nzones(self):
        """Number of radial zones"""
        return self._Nzones

    @Nzones.setter
    def Nzones(self, val):
        self._Nzones = val

    @property
    def Nfreq(self):
        """Number of frequency bins in the table"""
        return self._Nfreq

    @Nfreq.setter
    def Nfreq(self, val):
        self._Nfreq = val

    @property
    def Nrho(self):
        """Number of density points in the table"""
        return self._Nrho

    @Nrho.setter
    def Nrho(self, val):
        self._Nrho = val

    @property
    def Ntemp(self):
        """Number of temperature points in the table"""
        return self._Ntemp

    @Ntemp.setter
    def Ntemp(self, val):
        self._Ntemp = val

    @property
    def skip(self):
        """@skip parameter of opacity.inc; determines for how many radiation
        zones (i.e. compositions) tables are calculated
        """

        return self._skip

    @skip.setter
    def skip(self, val):
        self._skip = val

    @property
    def nus(self):
        """Frequency points in the table (Hz)"""
        return self._nus

    @nus.setter
    def nus(self, val):
        self._nus = val

    @property
    def lambdas(self):
        """Wavelengths in the table (AA)"""
        return self._lambdas

    @lambdas.setter
    def lambdas(self, val):
        self._lambdas = val

    @property
    def rhos(self):
        """density grid - ATTENTION ln(rho)"""
        return self._rhos

    @rhos.setter
    def rhos(self, val):
        self._rhos = val

    @property
    def temps(self):
        """temperature grid - ATTENTION ln(T)"""
        return self._temps

    @temps.setter
    def temps(self, val):
        self._temps = val

    @property
    def bbs(self):
        """bound-bound scattering table - i.e. Thomson scattering"""
        return self._bbs

    @bbs.setter
    def bbs(self, val):
        self._bbs = val

    @property
    def bba(self):
        """bound-bound absorption table"""
        return self._bba

    @bba.setter
    def bba(self, val):
        self._bba = val

    @property
    def bfa(self):
        """bound-free absorption table"""
        return self._bfa

    @bfa.setter
    def bfa(self, val):
        self._bfa = val

    @property
    def ffa(self):
        """free-free absorption table"""
        return self._ffa

    @ffa.setter
    def ffa(self, val):
        self._ffa = val

    @property
    def zones(self):
        """array of radial zone indices for which opacity tables have been
        calculated
        """
        if self._zones is None:
            #self._zones = np.append(np.arange(0, self.Nzones, self.skip),-1)
            #self._zones = np.append(np.arange(0, self.Nzones-1, self.skip),(self.Nzones//self.skip) * self.skip)
            self._zones = np.arange(0, self.Nzones-1, self.skip)
            if len(self._zones) < (self.Nzones//self.skip+1):
                self._zones = np.append(self._zones, (self.Nzones//self.skip) * self.skip)
        return self._zones

    @property
    def tabshape(self):
        """tuple holding the shape of the different opacity tables"""
        if self._tabshape is None:
            self._tabshape = (self.Nfreq, self.Ntemp, self.Nrho, self.Nzones//self.skip+1)
        return self._tabshape

    def read_real_record_from_stream(self, stream):
        """helper function to read a fortran array of single precision
        floats

        Notation:
        i4 -> signed 32 bit integer
        f4 -> 32 bit float (single precision, real4)
        f8 -> 64 bit float (double precision, real8)

        The data block consists of:
        i4 - size of the data block (Nsize)
        Nsize x f4 - opacity table
        i4 - size of the data block (Nsize)

        Arguments:
            stream = file stream object (at the beginning of the fortran record)
        """

        Nsize = struct.unpack("i", stream.read(4))[0]
        data = np.array(struct.unpack("%d" % (Nsize//4) + "f", stream.read(Nsize)))
        endNsize = struct.unpack("i", stream.read(4))[0]

        assert(Nsize == endNsize)

        return data, Nsize

    def read_header_from_stream(self, stream):
        """read header of the detailed table

        Notation:
        i4 -> signed 32 bit integer
        f4 -> 32 bit float (single precision, real4)
        f8 -> 64 bit float (double precision, real8)

        The header contains:
        i4 - size of the header block
        i4 - skip
        i4 - Nzones
        i4 - nw (purpose unknown)
        f8 - Stime
        i4 - Nfreq
        i4 - Msta (number of snapshots for which tables are calculated)
        i4 - Nrho
        i4 - Ntemp
        Nfreq x f8 - lambdas
        Nfreq+1 x f8 - Freq (frequency bin boundaries)
        Nfreq x f8 - nus 
        Ntemp x f8 - temps
        Nrho x f8 - rhos
        i4 - size of the header block

        Arguments:
            stream = file stream object (at the beginning of the fortran record)
        """
        Nsize = struct.unpack("i", stream.read(4))[0]
        self.skip = struct.unpack("i", stream.read(4))[0]
        self.Nzones = struct.unpack("i", stream.read(4))[0]
        self.nw = struct.unpack("i", stream.read(4))[0]
        self.Stime = struct.unpack("d", stream.read(8))[0]
        self.Nfreq, self.Msta, self.Nrho, self.Ntemp = struct.unpack("4i", stream.read(16))
        self.lambdas = np.array(struct.unpack("%d" % self.Nfreq + "d", stream.read(self.Nfreq * 8)))
        self.Freq = np.array(struct.unpack("%d" % (self.Nfreq+1) + "d", stream.read((self.Nfreq+1) * 8)))
        self.nus = np.array(struct.unpack("%d" % self.Nfreq + "d", stream.read(self.Nfreq * 8)))
        self.temps = np.array(struct.unpack("%d" % self.Ntemp + "d", stream.read(self.Ntemp * 8)))
        self.rhos = np.array(struct.unpack("%d" % self.Nrho + "d", stream.read(self.Nrho * 8)))
        endNsize = struct.unpack("i", stream.read(4))[0]

        assert(Nsize == endNsize)

    def read_tables_from_stream(self, stream):
        """read opacity tables of different interactions processes

        The data blocks for bbs, bba, bfa, ffa are read in.


        Arguments:
            stream = file stream object (at the beginning of the fortran record)
        """
        data, Nsize = self.read_real_record_from_stream(stream)

        self.bbs = pd.Panel4D(data.reshape(self.tabshape, order = "F"), labels = self.nus, items = self.temps, major_axis = self.rhos, minor_axis = self.zones)

        data, Nsize = self.read_real_record_from_stream(stream)

        self.bba = pd.Panel4D(data.reshape(self.tabshape, order = "F"), labels = self.nus, items = self.temps, major_axis = self.rhos, minor_axis = self.zones)

        data, Nsize = self.read_real_record_from_stream(stream)

        self.bfa = pd.Panel4D(data.reshape(self.tabshape, order = "F"), labels = self.nus, items = self.temps, major_axis = self.rhos, minor_axis = self.zones)

        data, Nsize = self.read_real_record_from_stream(stream)

        self.ffa = pd.Panel4D(data.reshape(self.tabshape, order = "F"), labels = self.nus, items = self.temps, major_axis = self.rhos, minor_axis = self.zones)

    def read_from_stream(self, stream):
        """reads the entire data associated with one snapshot

        First the header and then the data block, containing the opacity tables
        of the different interaction processes are read

        Arguments:
            stream = file stream object (at the beginning of the fortran record)
        """

        self.read_header_from_stream(stream)
        self.read_tables_from_stream(stream)



class detailed_table_reader(object):
    """Reader of a detailed Stella opacity table file

    Reads the entire binary file (typically called 'detailedopacity.bin')
    generated by xronfictd.exe. It holds a sequence of detailed tables, one for
    each snapshot
    
    Attributes:
        times: list of times for which tables are available (i.e. snapshots)
        tables: list of detailed_tables (one detailed_table per snapshot)
    """
    def __init__(self, fname):
        """Inits detailed_table_reader

        Arguments:
            fname = filename of detailed opacity file
        """
        self.fname = fname
        self.stream = open(fname, "rb")

        self.times = []
        self.tables = []

        self.read_tables()

    def read_tables(self):
        """Reads all opacity tables"""

        count = None

        while 1:
            table = detailed_table()
            table.read_from_stream(self.stream)

            self.tables.append(table)
            self.times.append(table.Stime)

            if count is None:
                count = table.Msta

            count -= 1

            if count == 0:
                break

        self.stream.close()



class absorption_opacity_table_reader(object):
    def __init__(self, fname):
        self.fname = fname

        self.read_table()

    def read_table(self):
        """
        Read absorption opacity table produced for stella

        Notation:
        i4 -> signed 32 bit integer
        f4 -> 32 bit float (single precision, real4)
        f8 -> 64 bit float (double precision, real8)

        The following format of the binary file is expected (see *.trf and *.f
        files in vladsf):

        record header - record data - record footer

        record header:
        i4: Nsize; size of record data in byte

        record data:
        Nsize x f4: hpbanab1

        record footer:
        i4: size of record data in byte

        hpbanab1 4 dimensional array (Nfreq x NTp x Nrho x Nzon)

        here: Nzon: number of zones for which opacities are calculated
        (typically not equal to Nshells in simulation)
        
        """

        f = open(self.fname, "rb")

        self.Nsize = struct.unpack("i", f.read(4))[0]

        self.hpbanab1 = np.array(struct.unpack("%d" % (self.Nsize//4) + "f", f.read(self.Nsize)))

        f.close()

    def reshape_opacity(self, Nfreq, NTp, Nrho, Nzon):

        self.hpbanab1 = np.reshape(self.hpbanab1, (Nfreq, NTp, Nrho, Nzon), order = "F")

    def calculate_raw_opacity(self, rho):

        """
        hpbanab1 = alog(sngl(opac * 10**UlgR / (rho / Urho))) c.f. ronftfixed.trf

        alog = natural logarithm
        sngl = conversion to single precision

        UlgR = 14 (see obj/fundrad.inc)
        Urho = 1e-6 (see obj/fundrad.inc)

        rho = current density in of density grid/table (stored as RhoTab)
        """

        self.opac = np.exp(self.hpbanab1) * 1e-8 * rho[None, None,:, None]

class scattering_opacity_table_reader(object):
    def __init__(self, fname):
        self.fname = fname

        self.read_table()

    def read_table(self):
        """
        Read scattering opacity table produced for stella

        Notation:
        i4 -> signed 32 bit integer
        f4 -> 32 bit float (single precision, real4)
        f8 -> 64 bit float (double precision, real8)

        The following format of the binary file is expected (see *.trf and *.f
        files in vladsf):

        record header - record data - record footer

        record header:
        i4: Nsize; size of record data in byte

        record data:
        i4: nw
        f8: Stime
        i4: Nfreq
        i4: Msta
        i4: Nrho
        i4: NTp
        Nfreq x f8: Wavel
        Nfreq+1 x f8: Freq
        Nfreq x f8: Freqmn
        NTp x f8: TbTab 
        Nrho x f8: RhoTab 
        Nsize-2660 x f4: hpbansc1

        record footer:
        i4: size of record data in byte

        hpbansc1 4 dimensional array (Nfreq x NTp x Nrho x Nzon)

        here: Nzon: number of zones for which opacities are calculated
        (typically not equal to Nshells in simulation)

        Stime = time for which opacity table was calculated
        Nfreq = number of frequency bins
        Msta = number of tables written (i.e. number of time snapshots)
        Nrho = size of rho table (see obj/zone.inc)
        NTp = size of temperature table (see obj/zone.inc)
        Wavel = wavelength associated with bin (in A)
        Freq = frequencies of bin boundaries
        Freqmn = frequencies associated with bin
        TpTab = temperature table
        RhoTab = density table

        hpbansc1 = total scattering and absorption opacity (after some transformations)
        """

        f = open(self.fname, "rb")

        self.Nsize = struct.unpack("i", f.read(4))[0]
        self.nw = struct.unpack("i", f.read(4))[0]
        self.Stime = struct.unpack("d", f.read(8))[0]
        self.Nfreq, self.Msta, self.Nrho, self.NTp = struct.unpack("4i", f.read(16))
        self.Wavel = np.array(struct.unpack("%d" % self.Nfreq + "d", f.read(self.Nfreq * 8)))
        self.Freq = np.array(struct.unpack("%d" % (self.Nfreq+1) + "d", f.read((self.Nfreq+1) * 8)))
        self.Freqmn = np.array(struct.unpack("%d" % self.Nfreq + "d", f.read(self.Nfreq * 8)))
        self.TbTab = np.array(struct.unpack("%d" % self.NTp + "d", f.read(self.NTp * 8)))
        self.RhoTab = np.array(struct.unpack("%d" % self.Nrho + "d", f.read(self.Nrho * 8)))


        self.rho = np.exp(self.RhoTab)
        self.rho[0] = self.rho[0] * 10.
        self.rho[-1] = self.rho[-1] / 10.

        self.T = np.exp(self.TbTab)
        self.T[0] = self.T[1]
        self.T[-1] = self.T[-2]

        headerlen = f.tell() - 4
        self.Nopsize = self.Nsize - headerlen

        self.Nzon = self.Nopsize//4//self.Nfreq//self.NTp//self.Nrho

        hpbansc1 = np.array(struct.unpack("%d" % (self.Nopsize//4) + "f", f.read(self.Nopsize)))
        self.hpbansc1 = np.reshape(hpbansc1, (self.Nfreq, self.NTp, self.Nrho, self.Nzon), order = "F")

        f.close()

    def calculate_raw_opacity(self, opac):

        """
        hpbanab1 = alog(sngl(scatop + opac * 10**UlgR / (rho / Urho))) c.f. ronftfixed.trf

        alog = natural logarithm
        sngl = conversion to single precision

        UlgR = 14 (see obj/fundrad.inc)
        Urho = 1e-6 (see obj/fundrad.inc)

        rho = current density in of density grid/table (stored as RhoTab)
        """

        self.scatop = np.exp(self.hpbansc1) - opac * 1e8 / self.rho[None, None,:, None]

class opacity_table_reader(object):
    def __init__(self, mname, verbose = False):

        self.mname = mname

        scat_fnames = sorted(glob.glob(self.mname + ".[0-9]"))
        ab_fname = self.mname + ".ab"

        self.scat_tables = [scattering_opacity_table_reader(fname) for fname in scat_fnames]
        self.ab_table = absorption_opacity_table_reader(ab_fname)

        self.check_scattering_tables_consistency()

        self.ab_table.reshape_opacity(self.Nfreq, self.NTp, self.Nrho, self.Nzon)

        self.ab_table.calculate_raw_opacity(self.rho)
        [table.calculate_raw_opacity(self.ab_table.opac) for table in self.scat_tables]

    def check_scattering_tables_consistency(self):

        self.Nfreq = self.scat_tables[0].Nfreq
        self.Nrho = self.scat_tables[0].Nrho
        self.NTp = self.scat_tables[0].NTp
        self.Nzon = self.scat_tables[0].Nzon

        self.RhoTab = self.scat_tables[0].RhoTab
        self.TbTab = self.scat_tables[0].TbTab
        self.Wavel = self.scat_tables[0].Wavel
        self.Freq = self.scat_tables[0].Freq
        self.Freqmn = self.scat_tables[0].Freqmn

        self.rho = self.scat_tables[0].rho
        self.T = self.scat_tables[0].T

        for i, table in enumerate(self.scat_tables):

            try:
                assert(self.Nfreq == table.Nfreq)
                assert(self.Nrho == table.Nrho)
                assert(self.NTp == table.NTp)
                assert(self.Nzon == table.Nzon)

                np.testing.assert_almost_equal(self.RhoTab, table.RhoTab)
                np.testing.assert_almost_equal(self.TbTab, table.TbTab)
                np.testing.assert_almost_equal(self.Wavel, table.Wavel)
                np.testing.assert_almost_equal(self.Freq, table.Freq)
                np.testing.assert_almost_equal(self.Freqmn, table.Freqmn)

            except AssertionError:
                print("Warning: inconsistencies between info block of table %d and %d" % (1, i+1))
                pass

if __name__ == "__main__":

    opacity_table_reader("m100101wgrid801")
