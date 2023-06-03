#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : stella.py
#
#  Purpose : Combined Stella output reader
#
#  Creation Date : 25-11-2015
#
#  Last Modified : Mon 14 Dec 2015 18:02:18 CET
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""Module containing a full stella_reader object which facilitates the parsing
and storing of all information produced by a Stella calculation.
"""
from __future__ import print_function
import os
import logging
import eve
import opa
import ph
import tt
import res
import swdn
import lbol
import prf
import flx
import dep
import util.elements as elements
import astropy.units as units
import astropy.constants as csts
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ehelper = elements.elements_helper()


class stella_reader(object):
    """
    General stella object, can read and hold all information associated with
    one particular Stella run.

    All files are assumed to be named according to the pattern
    <modelname>.[lbol,swd,res,...etc] and are assumed to be located in their
    standard directories

    - rootname/eve/run/<modelname>.rho
    - rootname/res/<modelname>.[tt,lbol,ph,swd]
    - rootname/strad/run/<modelname>.[res,log,prf,flx,dep]
    - rootname/vladsf/<modelname>.[1-6,ab]

    Parameters
    ----------
    mname : str
        model name, assumed to be the rootname for all files
    rootdir : str
        rootdir for of the Stella run (default cwd)
    load_eve : bool
        parse .rho file in eve directory (default True)
    load_res : bool
        parse .res file in strad/run directory (default False)
    load_tables : bool
        parse opacity tables in vladsf directory (default False)
    load_tt : bool
        parse .tt file in res directory (default False)
    load_ph : bool
        parse .ph file in res directory (default False)
    load_lbol : bool
        parse .lbol file in res directory (default True)
    load_swd : bool
        parse .swd file in res directory (default True)
    load_bins : bool
        parse .flx, .prf, .dep files in strad/run directory (default False)

    Attributes
    ----------
    eve : ~eve.everho_reader instance
    res : ~res.res_reader instance
    opacity : ~opa.opacity_table_reader instance
    tt : ~tt.tt_reader instance
    ph : ~ph.ph_reader instance
    lbol : ~lbol.lbol_reader instance
    swd : ~swdn.swd_reader instance
    flx : ~flx.flx_reader instance
    prf : ~prf.prf_reader instance
    dep : ~dep.dep_reader instance

    """
    def __init__(self, mname, rootdir=".", load_eve=True, load_res=False,
                 load_tables=False, load_tt=False, load_ph=False,
                 load_lbol=True, load_swd=True, load_bins=False,
                 load_all=False):

        self.mname = mname
        self.rootdir = rootdir

        self.eve = None
        self.res = None
        self.opacity = None
        self.tt = None
        self.ph = None
        self.swd = None
        self.flx = None
        self.prf = None
        self.dep = None

        if load_eve or load_all:
            logger.info("reading eve model")
            self.read_eve()
        if load_res or load_all:
            logger.info("reading results file")
            self.read_res()
        if load_tables or load_all:
            logger.info("reading opacity tables")
            self.read_tables()
        if load_tt or load_all:
            logger.info("reading tt file")
            self.read_tt()
        if load_ph or load_all:
            logger.info("reading ph file")
            self.read_ph()
        if load_swd or load_all:
            logger.info("reading shock wave details")
            self.read_swd()
        if load_lbol or load_all:
            logger.info("reading light curves")
            self.read_lbol()
        if load_bins or load_all:
            logger.info("reading Stella binary files: prf, flx and dep")
            self.read_prf()
            self.read_flx()
            self.read_dep()

    def read_eve(self):
        """
        Read eve .rho file; by default this is expected to lie in
        rootdir/eve/run/
        """

        fname = os.path.join(self.rootdir, "eve", "run", self.mname)

        try:
            self.eve = eve.everho_reader(fname)
        except IOError:
            logger.warning("Could not find .rho file: {}.rho".format(fname))

    def read_res(self):
        """
        Read results .res file; by default this is expected to lie in
        rootdir/res/
        """

        fname = os.path.join(self.rootdir, "res", self.mname)

        try:
            self.res = res.res_reader(fname)
        except IOError:
            logger.warning("Could not find .res file: {}.res".format(fname))

    def read_tables(self):
        """
        Read opacity tables; by default these are expected to lie in
        rootdir/vladsf/
        """

        fname = os.path.join(self.rootdir, "vladsf", self.mname)

        try:
            self.opacity = opa.opacity_table_reader(fname)
        except IOError:
            logger.warning("Could not find "
                           "opacity tables in: {}".format(fname))

    def read_tt(self):
        """
        Read .tt file; by default this is expected to lie in rootdir/res/
        """

        fname = os.path.join(self.rootdir, "res", self.mname)

        try:
            self.tt = tt.tt_reader(fname)
        except IOError:
            logger.warning("Could not find .tt file: {}.tt".format(fname))

    def read_ph(self):
        """
        Read .ph file; by default this is expected to lie in rootdir/res/
        """

        fname = os.path.join(self.rootdir, "res", self.mname)

        try:
            self.ph = ph.ph_reader(fname)
        except IOError:
            logger.warning("Could not find .ph file: {}.ph".format(fname))

    def read_swd(self):
        """
        Read shock wave details .swd file; by default this is expected to lie
        in rootdir/res/
        """

        fname = os.path.join(self.rootdir, "res")

        try:
            self.swd = swdn.swd_reader(mname=self.mname, parent_dir=fname)
        except IOError:
            logger.warning("Could not find "
                           ".swd file: {}/{}.swd".format(fname, self.mname))

    def read_lbol(self):
        """
        Read light curves .lbol file; by default this is expected to lie in
        rootdir/res/
        """

        fname = os.path.join(self.rootdir, "res", self.mname)

        try:
            self.lbol = lbol.lbol_reader(fname)
        except IOError:
            logger.warning("Could not find .lbol file: {}.lbol".format(fname))

    def read_flx(self):
        """Read .flx binary file; by default the file should be located in
        rootdir/strad/run
        """

        fname = os.path.join(self.rootdir, "strad", "run", self.mname + ".flx")

        try:
            self.flx = flx.flx_reader(fname)
        except IOError:
            logger.warning("Could not find .flx file {}".format(fname))

    def read_prf(self):
        """Read .prf binary file; by default, the file should be located in
        rootdir/strad/run
        """

        fname = os.path.join(self.rootdir, "strad", "run", self.mname + ".prf")

        try:
            self.prf = prf.prf_reader(fname)
        except IOError:
            logger.warning("Could not find .prf file {}".format(fname))

    def read_dep(self):
        """Read .dep binary file; by default, the file should be located in
        rootdir/strad/run
        """

        fname = os.path.join(self.rootdir, "strad", "run", self.mname + ".dep")

        try:
            self.dep = dep.dep_reader(fname)
        except IOError:
            logger.warning("Could not find .dep file {}".format(fname))


class stella_to_artis(stella_reader):
    """A Stella reader, specifically designed to map a Stella run into Artis

    For the mapping process, only the rho file of the eve process and the swd
    file of the Stella run are required. The data of specific snapshot is then
    mapped on a new grid of a requested resolution. In a last step properly
    formatted input files may be generated which may be directly used for Artis
    calculations.

    Note
    ----
    Since Artis assumes homology, a swd snapshot in which the model is already
    expanding close to homology should be selected. Otherwise, the mapping may
    not reflect the original Stella run very well.

    Parameters
    ----------
    mname : str
        root name of the Stella run
    rootdir : str
        root directory of the Stella run
    Nreq : int
        number of cells of the (uniformly spaced) Artis grid to be generated
    tswd_req : astropy.units.Quantity or float
        requested time of the Stella snapshot which should be mapped into
        Artis. If a float is provided, it is implicitly assumed that the time
        was given in days. Note that the requested time is not equal to the
        physical time since explosion due to the light travel time correction
        automatically applied by Stella. The Artis time will be corrected for
        this offset to reflect the time since explosion.
    artis_mode_fname : str
        file name of the Artis model file
    artis_abundance_fname : str
        file name of the Artis abundance file
    artis_dir : str
        directory into which the Artis files are saved
    """
    def __init__(self, mname, rootdir=".", Nreq=100, tswd_req=10 * units.d,
                 artis_model_fname="model.txt",
                 artis_abundance_fname="abundances.txt", artis_dir="."):

        super(stella_to_artis, self).__init__(mname, rootdir=rootdir,
                                              load_eve=True, load_swd=True,
                                              load_lbol=False)

        self.tswd_req = tswd_req
        if type(self.tswd_req) == float:
            logger.warning("tswd_req provided without specifying unit, "
                           "assuming d")
            self.tswd_req *= units.d

        self.Nreq = Nreq
        self.artis_dir = artis_dir
        self.artis_model_fname = artis_model_fname
        self.artis_abundance_fname = artis_abundance_fname

        self.construct_artis_model()
        self.write_artis_files()

    def construct_artis_model(self):
        """Construct the data for the Artis run, i.e. map from Stella to
        Artis

        Currently, a uniform Artis grid is set up uniformly spaced in the
        regime between 0 and the outer edge of the Stella computational domain.
        In the mapping process, a close representation of the original (Stella)
        radial distribution of mass and chemical elements on the new (Artis)
        grid is attempted.

        """

        snap = self.swd.snapshott(self.tswd_req)
        self.t_phys = snap.time + snap.r[-1] / csts.c

        tmp_r = np.linspace(0, snap.r[-1], self.Nreq + 1)
        self.artis_rl = tmp_r[:-1]
        self.artis_rr = tmp_r[1:]
        self.artis_rho = np.zeros(self.Nreq)
        self.artis_dm = np.zeros(self.Nreq)
        self.artis_mr = np.zeros(self.Nreq)
        self.artis_abunds = {}
        self.artis_ige = np.zeros(self.Nreq)
        self.artis_ni56 = np.zeros(self.Nreq)
        self.artis_co56 = np.zeros(self.Nreq)
        self.artis_fe52 = np.zeros(self.Nreq)
        self.artis_cr48 = np.zeros(self.Nreq)

        self.artis_volfactors = np.zeros((self.Nreq, self.swd.Nzones))

        stella_rr = snap.r
        stella_rl = np.append(0, snap.r)[:-1] * snap.r.unit
        stella_dm = ((self.eve.mass - np.append(0, self.eve.mass)[:-1]) *
                     units.solMass)

        j = 0
        # initialise parent grid
        while stella_rl[j] < self.artis_rl[0]:
            j += 1

        logger.info("starting with j = {:d}".format(j))

        for i in xrange(self.Nreq):

            # partial overlap at left artis boundary
            if stella_rr[j] >= self.artis_rl[i]:
                self.artis_volfactors[i, j] = ((stella_rr[j]**3 -
                                                self.artis_rl[i]**3) /
                                               (stella_rr[j]**3 -
                                                stella_rl[j]**3))
                if stella_rr[j] <= self.artis_rr[i]:
                    j += 1

            if j < self.swd.Nzones - 1:
                # completely enclosed cells
                while ((stella_rr[j] <= self.artis_rr[i])
                       and (j < self.swd.Nzones-1)):
                    self.artis_volfactors[i, j] = 1
                    j += 1

                # partial overlap at right artis boundary
                if stella_rl[j] <= self.artis_rr[i]:
                    self.artis_volfactors[i, j] = ((self.artis_rr[i]**3 -
                                                    stella_rl[j]**3) /
                                                   (stella_rr[j]**3 -
                                                    stella_rl[j]**3))

        for i in xrange(self.Nreq):
            self.artis_dm[i] = (self.artis_volfactors[i] *
                                stella_dm).sum().value
        self.artis_dm *= stella_dm.unit

        ehelper.capitalize()
        X_stella_ige = np.zeros(self.swd.Nzones)
        for z in xrange(1, 31):
            eve_abn_label = ehelper.inv_elements[z]
            self.artis_abunds[z] = np.zeros(self.Nreq)
            if eve_abn_label in self.eve.abundances.keys():
                if z > 20:
                    X_stella_ige += 10**self.eve.abundances[eve_abn_label]
                if z == 26:
                    X_stella = (10**self.eve.abundances[eve_abn_label] -
                                10**self.eve.abundances["Ni56"])
                elif z == 28:
                    X_stella = (10**self.eve.abundances[eve_abn_label] +
                                10**self.eve.abundances["Ni56"])
                    X_stella_Ni56 = 10**self.eve.abundances["Ni56"]
                else:
                    X_stella = 10**self.eve.abundances[eve_abn_label]

            for i in xrange(self.Nreq):
                if eve_abn_label in self.eve.abundances.keys():

                    self.artis_abunds[z][i] = ((self.artis_volfactors[i] *
                                                X_stella * stella_dm).sum() /
                                               self.artis_dm[i]).to("")

        for i in xrange(self.Nreq):
            self.artis_ni56[i] = ((self.artis_volfactors[i] * X_stella_Ni56 *
                                   stella_dm).sum() / self.artis_dm[i]).to("")
            self.artis_ige[i] = ((self.artis_volfactors[i] * X_stella_ige *
                                  stella_dm).sum() / self.artis_dm[i]).to("")

        self.artis_mr[0] = self.artis_dm[0].value
        for i in xrange(1, self.Nreq):
            self.artis_mr[i] = self.artis_dm[i].value + self.artis_mr[i-1]

        self.artis_mr = self.artis_mr * self.artis_dm.unit
        self.artis_rho = (3. * self.artis_dm /
                          (4. * np.pi * (self.artis_rr**3 -
                                         self.artis_rl**3))).to("g / cm^3")

        self.artis_v = (self.artis_rr / self.t_phys).to("km/s")

    def write_artis_files(self):
        """Write the model and abundance files for Artis"""

        model_data = np.array([np.arange(self.Nreq) + 1,
                               self.artis_v.to("km/s"),
                               np.log10(self.artis_rho.to("g/cm^3").value),
                               self.artis_ige, self.artis_ni56,
                               self.artis_co56, self.artis_fe52,
                               self.artis_cr48])

        abundance_data = np.append(np.array([np.arange(self.Nreq) + 1]),
                                   np.array([self.artis_abunds[z] for z in
                                             xrange(1, 31)]), axis=0)

        model_file = open(os.path.join(self.artis_dir, self.artis_model_fname),
                          "w")
        abundance_file = open(os.path.join(self.artis_dir,
                                           self.artis_abundance_fname), "w")

        model_file.write("{:d}\n{:.9f}\n".format(self.Nreq, self.t_phys.value))
        np.savetxt(model_file, model_data.T, delimiter="    ", fmt=["% 4d"] +
                   ["%.5e" for i in xrange(7)])

        np.savetxt(abundance_file, abundance_data.T, delimiter="    ",
                   fmt=["% 4d"] + ["%.5e" for i in xrange(30)])

        model_file.close()
        abundance_file.close()


def test():
    """
    Simple testing routine -- will only work for ulnoe@nct-2
    """

    test_mname = "m100101wgrid601"
    test_rootdir = os.path.join("/", "scratch", "ulnoe", "stellam", "runs",
                                test_mname)

    stella_reader(test_mname, rootdir=test_rootdir, load_all=True)

if __name__ == "__main__":

    test()
