#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : planckmean.py
#
#  Purpose : the tools defined here should be used instead of the deprecated
#  diagnostics/opacity.py file. With these tools, the Planck mean interaction
#  coefficients of the different processes (bound-bound, free-free, etc.) may
#  be calculated for a Stella run.
#
#  Note: Most docstrings should be disregarded until this file is properly
#  documented.
#
#  Creation Date : 26-10-2015
#
#  Last Modified : Fri 22 Jan 2016 19:01:28 CET
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
from __future__ import print_function
import astropy.units as units
# import astropy.constants as csts
import logging
import os
import numpy as np
import scipy.interpolate as interpolate
import stella.opa as opa
import stella.prf as prf

logging.basicConfig(format='%(asctime)s - %(levelname)s - '
                    '%(message)s', level=logging.DEBUG)


class planck_mean(object):
    """A basic calculator to determine Planck-mean opacities and optical depths

    With this calculator, Planck-mean opacities and corresponding optical
    depths according to the following prescription are calculated for a
    specific Stella run:

    .. math::

       \\begin{eqnarray}
            \\bar \\chi & = & \\frac{\\int J_{\\nu}
            \\chi_{\\nu}\\mathrm{d}\\nu}{\\int J_{\\nu} \\mathrm{d}\\nu} \\\\
            \\tau & = & \\int \\mathrm{d} r \\bar \\chi
       \\end{eqnarray}

    This requires, that a prf-file and a detailed opacity table (generated by
    UMN's versions of xronfict.exe, i.e. xronfictd.exe) are available for the
    run.

    To determine the Planck-mean opacity multiple interpolation steps, namely
    in temperature, density and time, are required to determine the
    frequency-dependent opacity in the computational domain for a specific
    snapshot. All interpolation procedures are carried out linearly.

    Arguments
    ---------
    mname : str
        model name
    rootdir : str
        root path of model directory (standard stella folder hierarchy is
        expected)
    """
    def __init__(self, mname, rootdir=".", prf_args={}):

        self.mname = mname

        self.rootdir = rootdir
        self.load_files(prf_args=prf_args)
        self.prepare_table_data()

    def load_files(self, prf_args={}):
        """Load data files

        The prf file, containing amongst others information about specific
        intensity, radius, density and temperature is read together with the
        detailed opacity table file.
        """

        logging.info("Reading files")

        opafname = os.path.join(self.rootdir, "vladsf", "detailedopacity.bin")
        prffname = os.path.join(self.rootdir, "strad",
                                "run", self.mname + ".prf")

        self.prfdat = prf.prf_reader(prffname, **prf_args)
        logging.info("Read prf file")

        self.tab = opa.detailed_table_reader(opafname)
        logging.info("Read detailed opacity table")

    def prepare_table_data(self):
        """Convert physical quantities stored in the opacity table to normal
        CGS form

        """

        logging.info("Preparing table data")

        self.tab_times = np.array(self.tab.times)
        self.tab_rho = np.e**self.tab.tables[0].rhos
        self.tab_T = np.e**self.tab.tables[0].temps
        self.tab_nus = self.tab.tables[0].nus
        self.tab_zones = self.tab.tables[0].zones
        self.tab_dnus = (self.tab.tables[0].Freq[1:] -
                         self.tab.tables[0].Freq[:-1])

    def planck_mean_av(self):
        """ Determine Planck-mean opacity averaged over entire domain

        .. note:: Deprectated
        """

        mr = self.tt.rho.x(0)[self.tab_zones]
        X, Y = np.meshgrid(self.tt.J.xdat, mr)

        bbs_rel = []
        bba_rel = []
        bfa_rel = []
        ffa_rel = []

        for i in xrange(len(self.tt.rho.cycles)):
            bbs, bba, bfa, ffa = self.planck_mean_for_i_av(i)
            optot = bbs + bba + bfa + ffa
            bbs_rel.append(bbs / optot)
            bba_rel.append(bba / optot)
            bfa_rel.append(bfa / optot)
            ffa_rel.append(ffa / optot)

        return (X, Y, np.array(bbs_rel), np.array(bba_rel), np.array(bfa_rel),
                np.array(ffa_rel))

    def animate_planck_mean_av(self, fname="out.mp4"):
        """Create animation of temporal evolution of the relative importance of
        the different interaction processes in terms of their Planck-mean

        .. note:: Deprectated
        """
        import os
        import matplotlib.pyplot as plt
        import colormap.colormaps as cmaps
        from matplotlib.offsetbox import AnchoredText
        from mpl_toolkits.axes_grid1 import AxesGrid

        try:
            os.mkdir("tmpdir")
        except OSError:
            pass

        labels = ["Thomson", "bound-bound", "bound-free", "free-free"]

        X, Y, bbs, bba, bfa, ffa = self.planck_mean_av()

        fig = plt.figure()

        for i in xrange(len(bbs)):

            logging.info("Plotting step %03d" % i)

            fig.clear()
            grid = AxesGrid(fig, 111, nrows_ncols=(2, 2), axes_pad=0.05,
                            share_all=False, label_mode="L",
                            cbar_location="right", cbar_mode="single",
                            aspect=False)
            for j, op in enumerate([bbs, bba, bfa, ffa]):
                im = grid[j].pcolormesh(X, Y, op[i], vmin=0, vmax=1,
                                        cmap=cmaps.plasma)
                grid[j].axis("tight")
                at = AnchoredText(labels[j], loc=2, frameon=False,
                                  prop={"color": "white"})
                grid[j].add_artist(at)
            cbar = grid.cbar_axes[0].colorbar(im)
            cbar.set_label_text(r"relative importance of Planck mean "
                                "interaction coefficient")
            grid[0].set_yticks([0.5, 1, 1.5, 2])
            grid[0].set_ylabel(r"$M_r$ [$\mathrm{M}_{\odot}$]")
            grid[2].set_ylabel(r"$M_r$ [$\mathrm{M}_{\odot}$]")
            grid[2].set_xlabel(r"$\log\lambda/\mathrm{\AA}$")
            grid[3].set_xlabel(r"$\log\lambda/\mathrm{\AA}$")

            plt.figtext(0.5, 0.95, r"$N_{{\mathrm{{cycle}}}}$ = {:>6d}, $t = "
                        "{:>8.3f}\,\mathrm{{d}}$".format(self.tt.J.cycles[i],
                                                         self.tt.J.times[i]))

            fname = "tmpdir/tmp_%03d.png" % i

            logging.info("Saving figure {:s}".format(fname))

            plt.savefig(fname)

    def planck_mean_for_i_av(self, i):
        """
        .. note:: Deprecated and broken
        """

        model_rho = 10**self.tt.rho.y(i)
        model_T = 10**self.tt.T.y(i)
        model_t = self.tt.J.times[i]
        ncnd = self.tt.J.ncnd[i]
        nfrus = self.tt.J.nfrus[i]
        mr = self.tt.rho.x(i)
        dm = mr - np.insert(mr, 0, 0)[:-1]

        dm_av = []
        for j, iz in enumerate(self.tab_zones):
            if iz > ncnd:
                dm_av.append(dm[iz])
        dm_av = np.mean(dm_av)

        bbs_t, bba_t, bfa_t, ffa_t = self.calculate_for_t(model_rho, model_T,
                                                          model_t)
        bbs = np.zeros((len(self.tab_zones), len(self.tab_dnus)))
        bba = np.zeros((len(self.tab_zones), len(self.tab_dnus)))
        bfa = np.zeros((len(self.tab_zones), len(self.tab_dnus)))
        ffa = np.zeros((len(self.tab_zones), len(self.tab_dnus)))

        for j, iz in enumerate(self.tab_zones):
            if iz > ncnd:
                Jnu = 10**self.tt.J.y(i)[iz - ncnd, :]
                Jtot = (Jnu * self.tab_dnus[:nfrus+1] * dm[iz]).mean()

                bbs[j, :nfrus+1] = (Jnu * bbs_t[j, :nfrus+1] *
                                    self.tab_dnus[:nfrus+1]) / Jtot
                bba[j, :nfrus+1] = (Jnu * bba_t[j, :nfrus+1] *
                                    self.tab_dnus[:nfrus+1]) / Jtot
                bfa[j, :nfrus+1] = (Jnu * bfa_t[j, :nfrus+1] *
                                    self.tab_dnus[:nfrus+1]) / Jtot
                ffa[j, :nfrus+1] = (Jnu * ffa_t[j, :nfrus+1] *
                                    self.tab_dnus[:nfrus+1]) / Jtot

        return bbs, bba, bfa, ffa

    def planck_mean_tau_for_i(self, i, nu_min, nu_max):
        """
        Document!
        """

        rzones, bbs, bba, bfa, ffa = self.planck_mean_for_i(i, nu_min, nu_max)

        r = self.prfdat.r.access(i).to("cm")
        dr = r[1:] - r[:-1]
        dr = np.insert(dr, 0, r[0])

        zones = self.tab_zones
        bbsfull = np.interp(r, rzones, bbs)
        bbafull = np.interp(r, rzones, bba)
        bfafull = np.interp(r, rzones, bfa)
        ffafull = np.interp(r, rzones, ffa)

        bbsdtau = bbsfull * dr
        bbadtau = bbafull * dr
        bfadtau = bfafull * dr
        ffadtau = ffafull * dr
        bbstau = np.zeros(bbsdtau.shape) * bbsdtau.unit
        bbatau = np.zeros(bbadtau.shape) * bbadtau.unit
        bfatau = np.zeros(bfadtau.shape) * bfadtau.unit
        ffatau = np.zeros(ffadtau.shape) * ffadtau.unit
        bbstau[-1] = bbsdtau[-1]
        bbatau[-1] = bbadtau[-1]
        bfatau[-1] = bfadtau[-1]
        ffatau[-1] = ffadtau[-1]

        for j in xrange(len(bbsdtau)-2, -1, -1):
            bbstau[j] = bbstau[j+1] + bbsdtau[j]
            bbatau[j] = bbatau[j+1] + bbadtau[j]
            bfatau[j] = bfatau[j+1] + bfadtau[j]
            ffatau[j] = ffatau[j+1] + ffadtau[j]

        return r, bbstau, bbatau, bfatau, ffatau

    def planck_mean_for_i(self, i, nu_min, nu_max):

        model_rho = self.prfdat.rho.access(i)
        model_T = self.prfdat.T.access(i)
        model_t = self.prfdat.phys_times[i]
        ncnd = self.prfdat.snapshots[i].Ncnd
        nfrus = self.prfdat.snapshots[i].Nfrus

        r = self.prfdat.r.access(i).to("cm")

        mask = (nu_min <= self.tab_nus[:nfrus]) * (self.tab_nus[:nfrus] <=
                                                   nu_max)

        bbs_t, bba_t, bfa_t, ffa_t = self.calculate_for_t(model_rho, model_T,
                                                          model_t)
        bbs = np.zeros(len(self.tab_zones)) * bbs_t.unit
        bba = np.zeros(len(self.tab_zones)) * bba_t.unit
        bfa = np.zeros(len(self.tab_zones)) * bfa_t.unit
        ffa = np.zeros(len(self.tab_zones)) * ffa_t.unit

        for j, iz in enumerate(self.tab_zones):
            if iz > ncnd:
                Jnu = self.prfdat.J.access(i)[iz-ncnd,
                                              :].to("erg/cm^2/s/Hz").value
                Jtot = (Jnu * self.tab_dnus[:nfrus] * mask).sum()

                bbs[j] = (Jnu * bbs_t[j, :nfrus] * self.tab_dnus[:nfrus] *
                          mask).sum() / Jtot
                bba[j] = (Jnu * bba_t[j, :nfrus] * self.tab_dnus[:nfrus] *
                          mask).sum() / Jtot
                bfa[j] = (Jnu * bfa_t[j, :nfrus] * self.tab_dnus[:nfrus] *
                          mask).sum() / Jtot
                ffa[j] = (Jnu * ffa_t[j, :nfrus] * self.tab_dnus[:nfrus] *
                          mask).sum() / Jtot

        return r[self.tab_zones], bbs, bba, bfa, ffa

    def calculate_for_t(self, model_rho, model_T, model_t):
        """Calculates the interpolated opacity tables for a requested time

        The opacity tables are interpolated between the two closest tables
        available in the detailed_opacity record for the sdet snapshot which is
        closest to the requested time.

        As a first step, the opacity tables of the two enclosing snapshots are
        interpolated on the temperature and density grid according to the
        material properties (T, rho) at the sdet snapshot. In a second step, a
        time interpolation is performed between these interpolated tables.

        Arguments
        ---------
        model_rho :
            model densities (in cgs)
        model_T :
            model temperatures (in cgs)
        model_t :
            requested time

        Returns:
            bbs = interpolated bound-bound scattering table
            bba = interpolated bound-bound absorption table
            bfa = interpolated bound-free absorption table
            ffa = interpolated free-free absorption table

            All outputs are np.ndarray of shape(Nzones x Nfreqs); Nzones
            denotes the number of mesh points for which tables are available,
            i.e. Nradial//skip
        """


        model_t = model_t.to("d").value
        logging.info("Starting table interpolation for "
                     "t = {:.2f}".format(model_t))

        dt = np.array(self.tab.times) - model_t

        if dt[-1] > 0 and dt[0] < 0:
            itab_u = np.argwhere(dt < 0).reshape(-1)[-1] + 1
            itab_l = np.argwhere(dt > 0).reshape(-1)[0] - 1
        elif dt[-1] <= 0:
            itab_u = len(dt) - 1
            itab_l = itab_u - 1
        elif dt[0] >= 0:
            itab_l = 0
            itab_u = itab_l + 1

        bbs_l, bba_l, bfa_l, ffa_l = \
            self.interpolate_rho_T(self.tab.tables[itab_l], model_rho, model_T)
        bbs_u, bba_u, bfa_u, ffa_u = \
            self.interpolate_rho_T(self.tab.tables[itab_u], model_rho, model_T)

        fdt_l = (self.tab.times[itab_u] - model_t) / (self.tab.times[itab_u] -
                                                      self.tab.times[itab_l])
        fdt_u = (model_t - self.tab.times[itab_l]) / (self.tab.times[itab_u] -
                                                      self.tab.times[itab_l])

        bbs = bbs_l * fdt_l + bbs_u * fdt_u
        bba = bba_l * fdt_l + bba_u * fdt_u
        bfa = bfa_l * fdt_l + bfa_u * fdt_u
        ffa = ffa_l * fdt_l + ffa_u * fdt_u

        return bbs, bba, bfa, ffa

    def interpolate_rho_T(self, table, model_rho, model_T):
        """Interpolates an opacity table with respect to rho and T

        An interpolation is performed for each cell for which opacity tables
        are available.

        All outputs are np.ndarray of shape(Nzones x Nfreqs); Nzones
        denotes the number of mesh points for which tables are available,
        i.e. Nradial//skip


        Arguments:
        ----------
        table : stella.opa.detailed_table
            opacity table to be interpolated
        model_rho : np.ndarray
            model densities (in cgs)
        model_T : np.ndarray
            model temperatures (in cgs)

        Returns:
        --------
        bbs : astropy.units.Quantity ndarray
            interpolated bound-bound scattering table
        bba : astropy.units.Quantity ndarray
            interpolated bound-bound absorption table
        bfa : astropy.units.Quantity ndarray
            interpolated bound-free absorption table
        ffa : astropy.units.Quantity ndarray
            interpolated free-free absorption table

        """

        logging.info("Interpolating tables at t = {:.4f} in rho and"
                     " T".format(table.Stime))

        bbs = np.zeros([len(table.zones), len(self.tab_nus)])
        bba = np.zeros([len(table.zones), len(self.tab_nus)])
        bfa = np.zeros([len(table.zones), len(self.tab_nus)])
        ffa = np.zeros([len(table.zones), len(self.tab_nus)])

        for i, iz in enumerate(table.zones):

            rho = model_rho[iz].to("g/cm^3").value
            T = model_T[iz].to("K").value

            pts = np.array([[nui, T, rho] for nui in self.tab_nus])

            bbs[i, :] = interpolate.interpn((self.tab_nus, self.tab_T,
                                             self.tab_rho),
                                            table.bbs.iloc[:, :, :, i].values,
                                            pts, bounds_error=False,
                                            fill_value=None)
            bba[i, :] = interpolate.interpn((self.tab_nus, self.tab_T,
                                             self.tab_rho),
                                            table.bba.iloc[:, :, :, i].values,
                                            pts, bounds_error=False,
                                            fill_value=None)
            bfa[i, :] = interpolate.interpn((self.tab_nus, self.tab_T,
                                             self.tab_rho),
                                            table.bfa.iloc[:, :, :, i].values,
                                            pts, bounds_error=False,
                                            fill_value=None)
            ffa[i, :] = interpolate.interpn((self.tab_nus, self.tab_T,
                                             self.tab_rho),
                                            table.ffa.iloc[:, :, :, i].values,
                                            pts, bounds_error=False,
                                            fill_value=None)

        bbs = bbs / units.cm
        bba = bba / units.cm
        bfa = bfa / units.cm
        ffa = ffa / units.cm

        return bbs, bba, bfa, ffa


if __name__ == "__main__":

    planck_mean("m100101wgrid1304")
