#!/usr/bin/env python
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : opacity.py
#
#  Purpose :
#
#  Creation Date : 15-10-2015
#
#  Last Modified : Fri 16 Oct 2015 17:54:34 CEST
#
#  Created By :  
#
# _._._._._._._._._._._._._._._._._._._._._.
from __future__ import print_function
import scipy.interpolate
import numpy as np
import matplotlib.pyplot as plt

class opacity_diagnostics(object):
    """Diagnostics tool for a detailed opacity table

    The main purpose of this class is to provide the post-processing
    possibility of determining the opacity used in the Stella calculation in a
    given zone at a given time. This requires multiple interpolation steps on
    the opacity tables. Currently, this tool is designed to work with a
    detailed_table_reader object (see stella.opa.py). Consequently the
    importance of the different interaction processes in a particular zone may
    be explored as well.

    IMPORTANT: all interpolation steps are performed linearly. In cases in
    which the requested points lie outside of the recorded tables, linear
    extrapolation is performed.
    """
    def __init__(self, shock_details, detailed_tables):
        """Inits the opacity_diagnostics

        Arguments:
            shock_details = a swd object, containing the shock wave details
                (see stella.swd.py)
            detailed_tables = a detailed_table_reader object (see
                stella.opa.py)

        Attributes:
            sdet: the provided shock wave details object
            op: the provided detailed_table_reader object
            op_times: an array of the snapshots recorded for which opacity
                tables are available
        """

        self.sdet = shock_details
        self.op = detailed_tables

        self.op_times = np.array(self.op.times)

        self.rho_tab = np.e**self.op.tables[0].rhos
        self.T_tab = np.e**self.op.tables[0].temps
        self.nu_tab = self.op.tables[0].nus
        self.zones = self.op.tables[0].zones

    def calculate_for_t(self, snapshot_t):
        """Calculates the interpolated opacity tables for a requested time

        The opacity tables are interpolated between the two closest tables
        available in the detailed_opacity record for the sdet snapshot which is
        closest to the requested time.

        As a first step, the opacity tables of the two enclosing snapshots are
        interpolated on the temperature and density grid according to the
        material properties (T, rho) at the sdet snapshot. In a second step, a
        time interpolation is performed between these interpolated tables.

        Arguments:
            snapshot_t = requested time

        Returns:
            bbs = interpolated bound-bound scattering table
            bba = interpolated bound-bound absorption table
            bfa = interpolated bound-free absorption table
            ffa = interpolated free-free absorption table

            All outputs are np.ndarray of shape(Nzones x Nfreqs); Nzones
            denotes the number of mesh points for which tables are available,
            i.e. Nradial//skip
        """

        print("Entering calculate_for_t for t = %.2f..." % snapshot_t)

        model = self.sdet.snapshott(snapshot_t)

        dt = np.array(self.op.times) - model.time

        if dt[-1] > 0 and dt[0] < 0:
            itab_u = np.argwhere(dt < 0).reshape(-1)[-1] + 1
            itab_l = np.argwhere(dt > 0).reshape(-1)[0] - 1
        elif dt[-1] <= 0:
            itab_u = len(dt)-1
            itab_l = itab_u -1
        elif dt[0] >= 0:
            itab_l = 0
            itab_u = itab_l + 1

        bbs_l, bba_l, bfa_l, ffa_l = self.interpolate_rho_T(self.op.tables[itab_l], model)
        bbs_u, bba_u, bfa_u, ffa_u = self.interpolate_rho_T(self.op.tables[itab_u], model)

        fdt_l = (self.op.times[itab_u] - model.time) / (self.op.times[itab_u] - self.op.times[itab_l])
        fdt_u = (model.time - self.op.times[itab_l]) / (self.op.times[itab_u] - self.op.times[itab_l])

        bbs = bbs_l * fdt_l + bbs_u * fdt_u
        bba = bba_l * fdt_l + bba_u * fdt_u
        bfa = bfa_l * fdt_l + bfa_u * fdt_u
        ffa = ffa_l * fdt_l + ffa_u * fdt_u

        return bbs, bba, bfa, ffa


    def interpolate_rho_T(self, table, model):
        """Interpolates an opacity table with respect to rho and T

        An interpolation is performed for each cell for which opacity tables are available.

        Arguments:
            table = table to be interpolated
            model = sdet snapshot containing the fluid state

        Returns:
            bbs = interpolated bound-bound scattering table
            bba = interpolated bound-bound absorption table
            bfa = interpolated bound-free absorption table
            ffa = interpolated free-free absorption table

            All outputs are np.ndarray of shape(Nzones x Nfreqs); Nzones
            denotes the number of mesh points for which tables are available,
            i.e. Nradial//skip
        """

        print("Entering interpolate_rho_T for t = %.2f..." % table.Stime)

        bbs = np.zeros([len(table.zones),len(self.nu_tab)])
        bba = np.zeros([len(table.zones),len(self.nu_tab)])
        bfa = np.zeros([len(table.zones),len(self.nu_tab)])
        ffa = np.zeros([len(table.zones),len(self.nu_tab)])

        for i, iz in enumerate(table.zones):

            rho = model.rho[iz]
            T = model.T[iz]

            pts = np.array([[nui, T, rho] for nui in self.nu_tab])

            bbs[i,:] = scipy.interpolate.interpn((self.nu_tab, self.T_tab, self.rho_tab), table.bbs.iloc[:,:,:,i].values, pts, bounds_error=False, fill_value=None)
            bba[i,:] = scipy.interpolate.interpn((self.nu_tab, self.T_tab, self.rho_tab), table.bba.iloc[:,:,:,i].values, pts, bounds_error=False, fill_value=None)
            bfa[i,:] = scipy.interpolate.interpn((self.nu_tab, self.T_tab, self.rho_tab), table.bfa.iloc[:,:,:,i].values, pts, bounds_error=False, fill_value=None)
            ffa[i,:] = scipy.interpolate.interpn((self.nu_tab, self.T_tab, self.rho_tab), table.ffa.iloc[:,:,:,i].values, pts, bounds_error=False, fill_value=None)

        return bbs, bba, bfa, ffa

    def mean_opacities_nu(self, snapshot_t, nu_min, nu_max):
        """Interpolates opacities for a given time and performs averaging in
        frequency window


        Arguments:
            snapshot_t = requested time
            nu_min = lower boundary for frequency window for averaging
            nu_max = upper boundary for frequency window for averaging
            
        Returns:
            bbs = interpolated and nu-averaged bound-bound scattering table
            bba = interpolated and nu-averaged bound-bound absorption table
            bfa = interpolated and nu-averaged bound-free absorption table
            ffa = interpolated and nu-averaged free-free absorption table

            All outputs are np.ndarray of shape(Nzones); Nzones
            denotes the number of mesh points for which tables are available,
            i.e. Nradial//skip
        """

        print("Entering mean_opacities_nu...")

        mask = (nu_min <= self.nu_tab) * (self.nu_tab <= nu_max)
        dnu = self.nu_tab[1:] - self.nu_tab[:-1]
        dnu = np.append(dnu, dnu[-1])

        nu_int = np.sum(dnu[mask])

        bbs, bba, bfa, ffa = self.calculate_for_t(snapshot_t)

        bbs_b = np.zeros(bbs.shape[0])
        bba_b = np.zeros(bbs.shape[0])
        bfa_b = np.zeros(bbs.shape[0])
        ffa_b = np.zeros(bbs.shape[0])

        for i in xrange(bbs.shape[0]):

            bbs_b[i] = np.sum(bbs[i,mask] * dnu[mask]) / nu_int
            bba_b[i] = np.sum(bba[i,mask] * dnu[mask]) / nu_int
            bfa_b[i] = np.sum(bfa[i,mask] * dnu[mask]) / nu_int
            ffa_b[i] = np.sum(ffa[i,mask] * dnu[mask]) / nu_int


        return bbs_b, bba_b, bfa_b, ffa_b

    def mean_opacities_nu_r(self, snapshot_t, nu_min, nu_max, i_min, i_max):
        """Interpolates opacities for a given time, performs averaging in
        frequency window and weighted by relative cell width

        Only parts of the full tables are returned, namely the data for cells
        in with i_min<=i<=i_max.

        Arguments:
            snapshot_t = requested time
            nu_min = lower boundary for frequency window for averaging
            nu_max = upper boundary for frequency window for averaging
            i_min = lower cell index for weighting and cutting process
            i_max = upper cell index for weighting and cutting process
            
        Returns:
            bbs = interpolated and nu-averaged bound-bound scattering table
            bba = interpolated and nu-averaged bound-bound absorption table
            bfa = interpolated and nu-averaged bound-free absorption table
            ffa = interpolated and nu-averaged free-free absorption table

            All outputs are np.ndarray of shape(Nzones); Nzones
            denotes the number of mesh points for which tables are available,
            i.e. (Nradial[i_max] - Nradial[i_min])//skip
        """


        print("Entering mean_opacities_nu_r...")

        bbs, bba, bfa, ffa = self.mean_opacities_nu(snapshot_t, nu_min, nu_max)

        mask = (i_min <= self.zones) * (self.zones <= i_max)
        iz = self.zones[mask]

        model = self.sdet.snapshott(snapshot_t)
        dr = model.r[1:] - model.r[:-1]
        dr = np.append(dr[0], dr)

        dr_int = np.mean(dr[mask])

        bbs_b =bbs[mask] * dr[mask]  / dr_int
        bba_b =bba[mask] * dr[mask]  / dr_int
        bfa_b =bfa[mask] * dr[mask]  / dr_int
        ffa_b =ffa[mask] * dr[mask]  / dr_int

        return bbs_b, bba_b, bfa_b, ffa_b

    def mean_opacities_all_t(self, nu_min, nu_max, i_min, i_max):
        """Interpolates opacities for each time of sdet file, performs averaging in
        frequency window and weighted by relative cell width

        Only parts of the full tables are returned, namely the data for cells
        in with i_min<=i<=i_max.

        Arguments:
            snapshot_t = requested time
            nu_min = lower boundary for frequency window for averaging
            nu_max = upper boundary for frequency window for averaging
            i_min = lower cell index for weighting and cutting process
            i_max = upper cell index for weighting and cutting process
            
        Returns:
            bbs = interpolated and nu-averaged bound-bound scattering table
            bba = interpolated and nu-averaged bound-bound absorption table
            bfa = interpolated and nu-averaged bound-free absorption table
            ffa = interpolated and nu-averaged free-free absorption table

            All outputs are np.ndarray of shape(Ntimes x Nzones); Nzones
            denotes the number of mesh points for which tables are available,
            i.e. (Nradial[i_max] - Nradial[i_min])//skip
        """

        print("Entering mean_opacities_all_t...")

        bbs = []
        bba = []
        bfa = []
        ffa = []

        for t in self.sdet.times.values():

            tmp = self.mean_opacities_nu_r(t, nu_min, nu_max, i_min, i_max)
            bbs.append(tmp[0])
            bba.append(tmp[1])
            bfa.append(tmp[2])
            ffa.append(tmp[3])

        return np.array(bbs), np.array(bba), np.array(bfa), np.array(ffa)



if __name__ == "__main__":

    pass
