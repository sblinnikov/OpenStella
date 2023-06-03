#!/usr/bin/env python
from __future__ import print_function
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors

class NoDataError(Exception):
    def __init__(self, message, error):
        super(NoDataError, self).__init__(message)
        self.error = error


class res_snapshot(object):
    """
    A single snapshot, i.e. one output block in the Stella res file
    """
    def __init__(self, fstream, verbose = False):
        """
        Arguments
        fstream -- file object, containing the res file

        Keyword Arguments:
        verbose -- print detailed information if True 
        """

        self.verbose = verbose

        self._nstep = None
        self._kflag = None
        self._jstart = None
        self._nqused = None
        self._nfun = None
        self._njac = None
        self._n = None
        self._nfrus = None
        self._ncnd = None
        self._niter = None
        self._nfail = None
        self._nzmod = None
        self._obstime = None
        self._proptime = None
        self._stepused = None
        self._steptried = None
        self._zone = None
        self._mr = None
        self._r14 = None
        self._v8 = None
        self._T5 = None
        self._Trad5 = None
        self._lgrho = None
        self._rho = None
        self._lgP = None
        self._lgQv = None
        self._lgQRT = None
        self._XHI = None
        self._eng = None
        self._lum = None
        self._nbar = None
        self._ne = None
        self._Fe = None
        self._II = None
        self._III = None
        self.rad_e = None
        self.tot_e = None
        self.kin_e = None
        self.gain_e = None
        self.grav_e = None
        self.visc_vir = None
        self.vir_e = None
        self.vir_bal = None
        self.th_e = None
        self.tot_bal = None

        self._nzones = None
        self._tauLubvB = None
        self._tauU = None
        self._tauB = None
        self._tauV = None
        self._tauR = None
        self._tauI = None

        self.process_block_header(fstream)
        self.process_block_data(fstream)
        self.process_tau_block(fstream)
        self.process_balance_block(fstream)

    @property
    def nzones(self):
        """number of zones"""
        if self._nzones is None:
            self._nzones = self.zones[-1]
        return self._nzones

    @property
    def tauLubvB(self):
        """optical depth in the UBV bands?"""
        return self._tauLubvB

    @tauLubvB.setter
    def tauLubvB(self, val):
        self._tauLubvB = val

    @property
    def tauU(self):
        """optical depth in the U band?"""
        return self._tauU

    @tauU.setter
    def tauU(self, val):
        self._tauU = val

    @property
    def tauB(self):
        """optical depth in the B band"""
        return self._tauB

    @tauB.setter
    def tauB(self, val):
        self._tauB = val

    @property
    def tauV(self):
        """optical depth in the V band"""
        return self._tauV

    @tauV.setter
    def tauV(self, val):
        self._tauV = val

    @property
    def tauR(self):
        """optical depth in the R band"""
        return self._tauR

    @tauR.setter
    def tauR(self, val):
        self._tauR = val

    @property
    def tauI(self):
        """optical depth in the I band"""
        return self._tauI

    @tauI.setter
    def tauI(self, val):
        self._tauI = val

    @property
    def nstep(self):
        """number of step performed until snapshot"""
        return self._nstep

    @nstep.setter
    def nstep(self, val):
        self._nstep = val

    @property
    def kflag(self):
        """unknown"""
        return self._kflag

    @kflag.setter
    def kflag(self, val):
        self._kflag = val

    @property
    def jstart(self):
        """unknown"""
        return self._jstart

    @jstart.setter
    def jstart(self, val):
        self._jstart = val

    @property
    def nqused(self):
        """unknown"""
        return self._nqused

    @nqused.setter
    def nqused(self, val):
        self._nqused = val

    @property
    def nfun(self):
        """unknown"""
        return self._nfun

    @nfun.setter
    def nfun(self, val):
        self._nfun = val

    @property
    def njac(self):
        """unknown"""
        return self._njac

    @njac.setter
    def njac(self, val):
        self._njac = val

    @property
    def n(self):
        """unknown"""
        return self._n

    @n.setter
    def n(self, val):
        self._n = val

    @property
    def nfrus(self):
        """unknown"""
        return self._nfrus

    @nfrus.setter
    def nfrus(self, val):
        self._nfrus = val

    @property
    def ncnd(self):
        """number of grid cells in which thermal conduction is used"""
        return self._ncnd

    @ncnd.setter
    def ncnd(self, val):
        self._ncnd = val

    @property
    def niter(self):
        """unknown"""
        return self._niter

    @niter.setter
    def niter(self, val):
        self._niter = val

    @property
    def nfail(self):
        """unknown"""
        return self._nfail

    @nfail.setter
    def nfail(self, val):
        self._nfail = val

    @property
    def nzmod(self):
        """unknown"""
        return self._nzmod

    @nzmod.setter
    def nzmod(self, val):
        self._nzmod = val

    @property
    def obstime(self):
        """observer time in days (proper time minus light travel time)"""
        return self._obstime

    @obstime.setter
    def obstime(self, val):
        self._obstime = val

    @property
    def proptime(self):
        """proper time in days"""
        return self._proptime

    @proptime.setter
    def proptime(self, val):
        self._proptime = val

    @property
    def stepused(self):
        """length of used time step"""
        return self._stepused

    @stepused.setter
    def stepused(self, val):
        self._stepused = val

    @property
    def steptried(self):
        """unknown"""
        return self._steptried

    @steptried.setter
    def steptried(self, val):
        self._steptried = val

    @property
    def zones(self):
        """zone index"""
        return self._zone

    @zones.setter
    def zones(self, val):
        self._zone = val

    @property
    def mr(self):
        """mass coordinate (solar mass units)"""
        return self._mr

    @mr.setter
    def mr(self, val):
        self._mr = val

    @property
    def r14(self):
        """radial coordinate (10^14cm ?)"""
        return self._r14

    @r14.setter
    def r14(self, val):
        self._r14 = val

    @property
    def v8(self):
        """velocity in 10^8 cm/s"""
        return self._v8

    @v8.setter
    def v8(self, val):
        self._v8 = val

    @property
    def T5(self):
        """gas temperature in 10^5 K"""
        return self._T5

    @T5.setter
    def T5(self, val):
        self._T5 = val

    @property
    def Trad5(self):
        """radiation temperature in 10^5 K"""
        return self._Trad5

    @Trad5.setter
    def Trad5(self, val):
        self._Trad5 = val

    @property
    def lgrho(self):
        """logarithmic density -6"""
        return self._lgrho

    @lgrho.setter
    def lgrho(self, val):
        self._lgrho = val

    @property
    def rho(self):
        """density"""
        if self._rho is None:
            self._rho = 10**(self.lgrho + 6)
        return self._rho

    @property
    def lgP(self):
        """logarithmic pressure (-/+7?)"""
        return self._lgP

    @lgP.setter
    def lgP(self, val):
        self._lgP = val

    @property
    def lgQv(self):
        """artificial viscosity"""
        return self._lgQv

    @lgQv.setter
    def lgQv(self, val):
        self._lgQv = val

    @property
    def lgQRT(self):
        """artificial viscosity"""
        return self._lgQRT

    @lgQRT.setter
    def lgQRT(self, val):
        self._lgQRT = val

    @property
    def XHI(self):
        """logarithmic abundance of neutral hydrogen"""
        return self._XHI

    @XHI.setter
    def XHI(self, val):
        self._XHI = val

    @property
    def eng(self):
        """radial coordinate (10^14cm ?)"""
        return self._eng

    @eng.setter
    def eng(self, val):
        self._eng = val

    @property
    def lum(self):
        """luminosity"""
        return self._lum

    @lum.setter
    def lum(self, val):
        self._lum = val

    @property
    def nbar(self):
        """unknown"""
        return self._nbar

    @nbar.setter
    def nbar(self, val):
        self._nbar = val

    @property
    def ne(self):
        """electron density"""
        return self._ne

    @ne.setter
    def ne(self, val):
        self._ne = val

    @property
    def Fe(self):
        """unknown"""
        return self._Fe

    @Fe.setter
    def Fe(self, val):
        self._Fe = val

    @property
    def II(self):
        """unknown"""
        return self._II

    @II.setter
    def II(self, val):
        self._II = val

    @property
    def III(self):
        """unknown"""
        return self._III

    @III.setter
    def III(self, val):
        self._III = val

    @property
    def rad_e(self):
        """radiative energy in 10^50 erg"""
        return self._rad_e

    @rad_e.setter
    def rad_e(self, val):
        self._rad_e = val

    @property
    def tot_e(self):
        """total energy in 10^50 erg"""
        return self._tot_e

    @tot_e.setter
    def tot_e(self, val):
        self._tot_e = val

    @property
    def kin_e(self):
        """kinetic energy in 10^50 erg"""
        return self._kin_e

    @kin_e.setter
    def kin_e(self, val):
        self._kin_e = val

    @property
    def gain_e(self):
        """gained energy in 10^50 erg"""
        return self._gain_e

    @gain_e.setter
    def gain_e(self, val):
        self._gain_e = val

    @property
    def grav_e(self):
        """gravitational energy in 10^50 erg"""
        return self._grav_e

    @grav_e.setter
    def grav_e(self, val):
        self._grav_e = val

    @property
    def visc_vir(self):
        """unknown"""
        return self._visc_vir

    @visc_vir.setter
    def visc_vir(self, val):
        self._visc_vir = val

    @property
    def vir_e(self):
        """virial energy in 10^50 erg"""
        return self._vir_e

    @vir_e.setter
    def vir_e(self, val):
        self._vir_e = val

    @property
    def vir_bal(self):
        """virial balance, i.e. accumulated error in 10^50 erg"""
        return self._vir_bal

    @vir_bal.setter
    def vir_bal(self, val):
        self._vir_bal = val

    @property
    def th_e(self):
        """thermal energy in 10^50 erg"""
        return self._th_e

    @th_e.setter
    def th_e(self, val):
        self._th_e = val

    @property
    def tot_bal(self):
        """total balance, i.e accumulated error in 10^50 erg"""
        return self._tot_bal

    @tot_bal.setter
    def tot_bal(self, val):
        self._tot_bal = val


    def print_att_info(self):
        """
        Prompts all array attributes of the snapshot object, obtained from the swd file
        """

        attribs = []
        notnone_attribs = []
        for key in self.__dict__.keys():
            if key[0] == "_":
                attribs.append(key[1:])
                if self.__dict__[key] is not None:
                    notnone_attribs.append(key[1:])


        print("the following data arrays may be accessed in each snapshot:")
        print(", ".join(attribs))
        print("the following data arrays may are not None:")
        print(", ".join(notnone_attribs))
        print("consult the corresponding docstrings to learn more about their physical meaning")


    def process_block_header(self, fstream):
        """
        Process the two header lines of a snapshot block in the res file

        The res file should already have been processed until the first line of
        the data header (see res_reader object).

        Arguments:
        fstream -- file object of res file, at location of the header of the data block

        """

        buffer = fstream.readline()
        vals = buffer.rsplit()

        try:
            assert(len(vals) == 12)
        except AssertionError:
            print("Error: could not process first line of block header: expected 12 elements, found %d" % len(vals))
            raise ValueError

        self.nstep = int(vals[0])
        self.kflag = int(vals[1])
        self.jstart = int(vals[2])
        self.nqused = int(vals[3])
        self.nfun = int(vals[4])
        self.njac = int(vals[5])
        self.n = int(vals[6])
        self.nfrus = int(vals[7])
        self.ncnd = int(vals[8])
        self.niter = int(vals[9])
        self.nfail = int(vals[10])
        self.nzmod = int(vals[11])

        buffer = fstream.readline()

        exp = re.compile(r".*TIME=(.*)D.*T=(.*)S.*STEP USED=(.*)STEP TRIED=(.*)S.*")
        tmp = re.match(exp, buffer)

        try:
            assert(tmp is not None)
        except AssertionError:
            print("Error: could not process second line of block header")
            raise ValueError

        self.obstime = float(tmp.groups()[0])
        self.proptime = float(tmp.groups()[1])
        self.stepused = float(tmp.groups()[2])
        self.steptried = float(tmp.groups()[3])


    def process_block_data(self, fstream):
        """
        Process the data block of the res snapshot

        The res file should already have been processed  until and including
        the header lines of the data block (see process_block_header).

        Arguments:
        fstream -- file object of res file, at location of first entry of data block
        """

        #c.f. Format 93 in lbalsw.trf
        fieldlengths = [3,9,12,8,10,8,7,7,7,8,10,10,10,10,5,10,10,10,10,10]

        buffer = fstream.readline()
        buffer = buffer.replace(".", "").replace("V 8", "V_8").replace("T 5", "T_5").replace("lgP 7", "lgP_7")
        self.labels = buffer.rsplit()

        buffer = fstream.readline()
        data = []

        j = 0
        while buffer[1] != "B":

            j += 1
            line = []
            b = 1
            for i,label in enumerate(self.labels):

                l = fieldlengths[i]
                try:
                    line.append(float(buffer[b:b+l]))
                except ValueError:
                    line.append(np.nan)
                b = b + l

            data.append(line)
            buffer = fstream.readline()

        data = np.array(data)

        for d, label in zip(data.T, self.labels):
            self.set_quantity(label, d)

        if j > 0:
            if self.verbose:
                print("read data block for snapshot %d: observer t %f d" % (self.nstep, self.obstime))
        else:
            if self.verbose:
                print("discarding snapshot %d: observer t %f d: no data!" % (self.nstep, self.obstime))
            raise NoDataError("blub", 1)

    def process_tau_block_helper(self, fstream, ident):
        """
        Helper routine for parsing the tau blocks

        This routine stores the values of one particular tau block in an array
        and returns it. All cells for which no information is found in the
        block (typically the innermost ones) are set to -1.

        Arguments:
        fstream -- file stream at the starting location of the tau block
        ident   -- regular expression string, matching the first line after the
                   tau block
        Returns:
        tmp_tau -- array with tau values
        """

        tmp_tau = np.ones(self.nzones) * -1

        exp = re.compile(ident)
        buffer = fstream.readline()

        while buffer != "":
            if re.match(exp, buffer) is not None:
                break
            elems = "".join(buffer.rsplit("->")).strip().rsplit()
            for i in xrange(0, len(elems), 2):
                tmp_tau[int(elems[i])-1] = float(elems[i+1])
            buffer = fstream.readline()

        return tmp_tau


    def process_tau_block(self, fstream):
        """
        Process the block of the snapshot containing information about the
        optical depth of the cells in which radiative transfer is active

        The routine will continue reading the file until the first keyword of
        the tau block is found. The data is parsed.

        Arguments:
        fstream -- file object of the res file, at the location prior to the
                   tau block
        """

        exp = re.compile(".*K/.*tau:.LubvB.*")
        buffer = fstream.readline()

        while buffer != "":
            if re.match(exp, buffer) is not None:
                break
            buffer = fstream.readline()
        else:
            print("Warning: tau block not found")
            return False

        tmp_tau = self.process_tau_block_helper(fstream, ".*K/.*tauU:.*")
        self.tauLubvB = tmp_tau

        tmp_tau = self.process_tau_block_helper(fstream, ".*K/.*tauB:.*")
        self.tauU = tmp_tau

        tmp_tau = self.process_tau_block_helper(fstream, ".*K/.*tauV:.*")
        self.tauB = tmp_tau

        tmp_tau = self.process_tau_block_helper(fstream, ".*K/.*tauR:.*")
        self.tauV = tmp_tau

        tmp_tau = self.process_tau_block_helper(fstream, ".*K/.*tauI:.*")
        self.tauR = tmp_tau

        tmp_tau = self.process_tau_block_helper(fstream, ".*EFFECTIVE.TEMPERATURE.*")
        self.tauI = tmp_tau

    def process_balance_block(self, fstream):
        """
        Process the block of the snapshot containing information about the
        energy budget and balance

        The routine will continue reading the file until the first keyword of
        the balance block is found. Then, the energy data is parsed.

        Arguments:
        fstream -- file object of the res file, at any location prior to the 
                   balance block
        """

        exp = re.compile(".*RADIAT.*")
        buffer = fstream.readline()

        while buffer != "":
            if re.match(exp, buffer) is not None:
                break
            buffer = fstream.readline()
        else:
            print("Warning: balance block not found")
            return False

        exp = re.compile(".*RADIAT.*=(.*)TOTAL.*ENERGY.*=(.*)")
        tmp = re.match(exp, buffer)
        self.rad_e = float(tmp.groups()[0])
        self.tot_e = float(tmp.groups()[1])

        buffer = fstream.readline()
        exp = re.compile(".*KINETIC.*=(.*)GAINED.*ENERGY.*=(.*)")
        tmp = re.match(exp, buffer)
        self.kin_e = float(tmp.groups()[0])
        self.gain_e = float(tmp.groups()[1])

        buffer = fstream.readline()
        exp = re.compile(".*GRAVIT.*=(.*)VISCOUS.*VIRIAL.*=(.*)")
        tmp = re.match(exp, buffer)
        self.grav_e = float(tmp.groups()[0])
        self.visc_vir = float(tmp.groups()[1])

        buffer = fstream.readline()
        exp = re.compile(".*VIRIAL.*=(.*)VIRIAL.*BALANCE.*=(.*)")
        tmp = re.match(exp, buffer)
        self.vir_e = float(tmp.groups()[0])
        self.vir_bal = float(tmp.groups()[1])

        buffer = fstream.readline()
        exp = re.compile(".*THERMAL.*=(.*)TOTAL.*BALANCE.*=(.*)")
        tmp = re.match(exp, buffer)
        self.th_e = float(tmp.groups()[0])
        self.tot_bal = float(tmp.groups()[1])

    def set_quantity(self, label, data):
        """
        Helper routine to set the attributes of the class

        Actually, quite cumbersome and not very elegant, but I didn't come up
        with a quick solution for having all the class properties and
        potentially not all res file containing the same physical quantities.
        Happy to replace it by a more efficient scheme (see also eve.py)

        Arguments:
        name -- identifier of the quantity
        data  -- data array associated with the quantity
        """

        if label == "ZON":
            self.zones = data
        elif label == "AM/SOL":
            self.mr = data
        elif label == "R14":
            self.r14 = data
        elif label == "V_8":
            self.v8 = data
        elif label == "T_5":
            self.T5 = data
        elif label == "Trad5":
            self.Trad5 = data
        elif label == "lgD-6":
            self.lgrho = data
        elif label == "lgP_7":
            self.lgP7 = data
        elif label == "lgQv":
            self.lgQv = data
        elif label == "lgQRT":
            self.lgQRT = data
        elif label == "XHI":
            self.XHI = data
        elif label == "ENG":
            self.eng = data
        elif label == "LUM":
            self.lum = data
        elif label == "CAPPA":
            self.cappa = data
        elif label == "n_bar":
            self.nbar = data
        elif label == "n_e":
            self.n_e = data
        elif label == "Fe":
            self.Fe = data
        elif label == "II":
            self.II = data
        elif label == "III":
            self.III = data
        else:
            print("Warning: Unknown quantity '%s' encountered" % label)

class res_reader(object):
    """
    Data reader for a *.res file created during a Stella run
    """
    def __init__(self, mname, verbose = False):
        """
        Arguments:
        mname -- name of the model, i.e. of the swd file without extension

        Keyword Arguments:
        verbose -- prints detailed information if True
        """

        self.verbose = verbose

        self.mname = mname
        self.fname = mname + ".res"

        self._cycles = None
        self._obstimes = None
        self._proptimes = None
        self._steptried = None
        self._stepused = None
        self._nsteps = None
        self._nsnapshots = None

        self.snapshots = []
        self.process_res_file()

    @property
    def cycles(self):
        """
        Array containing the indices of the snapshots
        """
        if self._cycles is None:
            self._cycles = np.arange(len(self.snapshots))
        return self._cycles

    @property
    def obstimes(self):
        """
        Dictionary linking the snapshot index and the observer time
        """
        if self._obstimes is None:
            self._obstimes = dict([(i, s.obstime) for i, s in zip(self.cycles, self.snapshots)])
        return self._obstimes

    @property
    def proptimes(self):
        """
        Dictionary linking the snapshot index and the proper time
        """
        if self._proptimes is None:
            self._proptimes = dict([(i, s.proptime) for i, s in zip(self.cycles, self.snapshots)])
        return self._proptimes

    @property
    def nsteps(self):
        """
        Dictionary linking the snapshot index and the number of steps
        """
        if self._nsteps is None:
            self._nsteps = dict([(i, s.nstep) for i, s in zip(self.cycles, self.snapshots)])
        return self._nsteps

    @property
    def stepused(self):
        """
        Dictionary linking the snapshot index and the length of the used step
        """
        if self._stepused is None:
            self._stepused = dict([(i, s.stepused) for i, s in zip(self.cycles, self.snapshots)])
        return self._stepused

    @property
    def steptried(self):
        """
        Dictionary linking the snapshot index and the length of the used step
        """
        if self._steptried is None:
            self._steptried = dict([(i, s.steptried) for i, s in zip(self.cycles, self.snapshots)])
        return self._steptried

    @property
    def nsnapshots(self):
        """
        Number of snapshots
        """
        if self._nsnapshots is None:
            self._nsnapshots = len(self.cycles)
        return self._nsnapshots

    def process_res_file(self):
        """
        Process the res file, i.e. store contents in the snapshots array
        """

        if self.verbose:
            print("Reading results file for run '%s'" % self.mname)
        f = open(self.fname, "r")
        if self.verbose:
            print("%s found and opened" % self.fname)


        buffer = f.readline()
        exp = re.compile(".*NSTEP.*")

        while buffer != "":
            if re.match(exp, buffer) is not None:
                try:
                    tmp = res_snapshot(f, verbose = self.verbose)
                    self.snapshots.append(tmp)
                except NoDataError:
                    pass


            buffer = f.readline()

        if self.verbose:
            print("found %d snapshots" % self.nsnapshots)
            if self.nsnapshots > 0:
                print("access snapshot data via self.snapshots array of self.snapshot()")
                self.snapshot(0).print_att_info()

        f.close()

    def snapshot(self, i):
        """
        Helper routine to quickly access a specific snapshot

        Arguments:
        i -- index of snapshot; consult self.obstimes, self.proptimes to
             identify the snapshot you are looking for 
        """

        try:
            return self.snapshots[i]
        except IndexError:
            print("Warning: wrong index ,", i)

    def show_balance(self, fig = None, xscale = "log"):
        """
        Create a plot of the energy balance of the run

        Arguments:
        fig -- figure instance; if None, a new one is created; (default None)

        Returns:
        fig -- figure instance containing the plot
        """

        times = np.array([self.proptimes[i] for i in self.cycles])
        tot_bal = np.array([self.snapshot(i).tot_bal for i in self.cycles])
        vir_bal = np.array([self.snapshot(i).vir_bal for i in self.cycles])

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        ax.plot(times, vir_bal, label = "virial balance")
        ax.plot(times, tot_bal, label = "total balance")
        ax.set_title(r"Run %s" % self.mname)
        ax.legend()
        ax.set_xlabel(r"proper time [days]")
        ax.set_ylabel(r"balance [$\mathrm{10^{50}\, erg}]$")
        ax.set_xscale(xscale)

        return fig

    def show_evolution(self, xident, yident, xscale = "log", yscale = "log", tmode = "vs_cycle", cmap = None):
        """
        Illustration of the evolution of a fluid or radiation property during the simulation

        Both the quantity displayed on the x-axis and on the y-axis have to be
        specified. Also one can the quantity which tracks "time".

        Arguments:
        xident -- identifier for the quantity on the x-axis; has to be an
                  attribute of res_snapshot
        yident -- identifier for the quantity on the y-axis; has to be an
                  attribute of res_snapshot
        tmode   -- identifier for the quantity which tracks time; possible
                  values are: 'vs_cycle', 'vs_nsteps', 'vs_obstime',
                  'vs_proptime' (default 'vs_cycle')
        xscale -- scaling on x-axis; 'linear' or 'log' possible (default 'log')
        yscale -- scaling on u-axis; 'linear' or 'log' possible (default 'log')
        cmap   -- colormap instance used for color-coding evolution; if None,
                  cm.jet will be used (default None)

        Returns:
        fig -- figure instance containing the plot
        """

        try:
            xdat = [s.__getattribute__(xident) for s in self.snapshots]
        except AttributeError:
            print("Error: 'xident' must be an attribute of the res_snapshot class")
            raise ValueError("xident '%s' unknown" % xident)
        try:
            ydat = [s.__getattribute__(yident) for s in self.snapshots]
        except AttributeError:
            print("Error: 'yident' must be an attribute of the res_snapshot class")
            raise ValueError("yident '%s' unknown" % yident)

        if cmap is None:
            cmap = cm.jet


        fig = plt.figure()
        ax = fig.gca()

        imax = len(xdat)
        if tmode == "vs_cycle":
            colors = [cmap(i / float(imax)) for i in xrange(imax)]
            norm = matplotlib.colors.Normalize(vmin = 0, vmax = imax)
            array = np.linspace(0, imax, 256)
            clabel = r"cycles"
        elif tmode == "vs_nsteps":
            colors = [cmap((self.nsteps[i] - self.nsteps[0]) / float(self.nsteps[self.cycles[-1]] - self.nsteps[0])) for i in xrange(imax)]
            norm = matplotlib.colors.Normalize(vmin = self.nsteps[0], vmax = self.nsteps[self.cycles[-1]])
            array = np.linspace(self.nsteps[0], self.nsteps[self.cycles[-1]], 256)
            clabel = r"steps"
        elif tmode == "vs_obstime":
            colors = [cmap((self.obstimes[i] - self.obstimes[0]) / (self.obstimes[self.cycles[-1]] - self.obstimes[0])) for i in xrange(imax)]
            norm = matplotlib.colors.Normalize(vmin = self.obstimes[0], vmax = self.obstimes[self.cycles[-1]])
            array = np.linspace(self.obstimes[0], self.obstimes[self.cycles[-1]], 256)
            clabel = r"observer time [day]"
        elif tmode == "vs_proptime":
            colors = [cmap((self.proptimes[i] - self.proptimes[0]) / (self.proptimes[self.cycles[-1]] - self.proptimes[0])) for i in xrange(imax)]
            norm = matplotlib.colors.Normalize(vmin = self.proptimes[0], vmax = self.proptimes[self.cycles[-1]])
            array = np.linspace(self.proptimes[0], self.proptimes[self.cycles[-1]], 256)
            clabel = r"proper time [day]"
        else:
            raise ValueError("unknown mode '%s'" % tmode)

        mappable = cm.ScalarMappable(norm, cmap = cmap)
        mappable.set_array(array)
        [ax.plot(x, y, color = color) for x, y, color in zip(xdat, ydat, colors)]

        ax.set_xscale(xscale)
        ax.set_yscale(yscale)

        cmap = plt.colorbar(mappable, ax = ax, orientation = "horizontal")
        cmap.set_label(clabel)

        return fig

    def show_density_evolution(self, xmode = "vs_r14", tmode = "vs_cycle", xscale = "log", yscale = "log", cmap = None):
        """
        Shows evolution of density during the simulation

        Arguments:
        xmode  -- quantity on x-axis; possible values 'vs_r14', 'vs_mr' (default
                 'vs_r14')
        tmod   -- identifier for quantity tracking "time" (see self.show_evolution)
        xscale -- scaling on x-axis; 'log' and 'linear' (default 'log')
        yscale -- scaling on y-axis; 'log' and 'linear' (default 'log')
        cmap   -- colormap instance used for color-coding evolution; if None,
                  cm.jet will be used (default None)

        Returns
        fig    -- figure instance containing plot
        """

        if yscale == "log":
            ylabel = r"$\log \rho$ - 6"
            yscale = "linear"
            yident = "lgrho"
        elif yscale == "linear":
            ylabel = r"$\rho$ [$\mathrm{g\,cm^{-3}}$]"
            yident = "rho"
        else:
            print("Error: unknown yscale '%s'" % yscale)
            raise ValueError

        if xmode == "vs_r14":
            xident = "r14"
            xlabel = r"$R_{14}$"
        else:
            print("Error: unknown xmode '%s'" % xmode)
            raise ValueError

        fig = self.show_evolution(xident, yident, xscale = xscale, yscale = yscale, tmode = tmode, cmap = cmap)

        ax = fig.gca()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return fig


def test(mname = "out24p2e30"):
    """
    A simple script to test the res_reader; automatically called in the main

    Arguments:
    mname --- model name (default 'out24p2e30')
    """

    test_reader = res_reader(mname)
    test_reader.show_balance()
    test_reader.show_density_evolution(tmode = "vs_obstime")

if __name__ == "__main__":

    test()

    plt.show()
