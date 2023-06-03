# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : swdn_diag.py
#
#  Purpose : preliminary: swd_reader with some of the plotting tools of swdn.sm
#
#  Creation Date : 02-12-2015
#
#  Last Modified : Wed 02 Dec 2015 15:34:45 CET
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""Currently this module only serves as a container to hold all the plotting
and diagnostics tools related to swd files. These have been removed from
swdn.py so that that module only contains parsing and simple processing
processes.

**Warning:** Everything in this module is utterly untested and poorly
documented.
"""
class swd_diagnosis(swd_reader):
    def __init__(self, mname, parent_dir = None, explicit_fname=None):
        super(swd_diagnosis, self).__init__(mname, parent_dir = parent_dir, explicit_fname = explicit_fname)

    def show_evolution(self, xident, yident, xscale = "linear", yscale = "linear", tmode = "vs_cycle", cmap = None):

        if cmap is None:
            cmap = cm.spectral

        fig = plt.figure()
        ax = fig.gca()

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

        imax = len(xdat)
        if tmode == "vs_cycle":
            colors = [cmap(i / float(imax)) for i in xrange(imax)]
            norm = matplotlib.colors.Normalize(vmin = 0, vmax = imax)
            array = np.linspace(0, imax, 256)
            clabel = r"cycles"
        elif tmode == "vs_obstime":
            colors = [cmap((self.times[i] - self.times[0]) / (self.times[self.Ntimes-1] - self.times[0])) for i in xrange(imax)]
            norm = matplotlib.colors.Normalize(vmin = self.times[0], vmax = self.times[self.Ntimes -1 ])
            array = np.linspace(self.times[0], self.times[self.Ntimes-1], 256)
            clabel = r"observer time [day]"
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


    def show_density(self, i, fig = None):

        if fig is None:
            fig = plt.figure()

        data = self.snapshot(i)
        if data is None:
            print("Warning: No snapshot data")
            return None

        ax = fig.gca()

        ax.plot(data.lgr, data.lgrho)

        return fig

    def show_rhov9LTtau_vs_lgr(self, record, fig = None):
        """
        Shortcut for plotting density, velocity, temperature, luminosity and
        optical depth versus logarithmic radius. Calls internally
        'show_rhov9LTtau' with the appropriate xaxis identifier.

        Arguments:
        record -- index of the snapshot to be displayed
        fig    -- figure instance used for the plot; if None, a new figure is
                  created (default None)

        Returns:
        fig    -- figure instance containing the plot

        """

        fig = self.show_rhov9LTtau(record, fig = fig, xaxis = "lgr")

        return fig


    def show_rhov9LTtau_vs_mr(self, record, fig = None):
        """
        Shortcut for plotting density, velocity, temperature, luminosity and
        optical depth versus mass coordinate. Calls internally
        'show_rhov9LTtau' with the appropriate xaxis identifier.

        Arguments:
        record -- index of the snapshot to be displayed
        fig    -- figure instance used for the plot; if None, a new figure is
                  created (default None)

        Returns:
        fig    -- figure instance containing the plot

        """

        fig = self.show_rhov9LTtau(record, fig = fig, xaxis = "mr")

        return fig


    def show_rhov9LTtau(self, record, fig = None, xaxis = "lgr"):
        """
        Creates a summary plot containing: logarithmic density, velocity in
        units of 1e9 cm/s, logarithmic temperature, luminosity, optical depth.
        The quantity on the x-axis may be specified

        Arguments:
        record -- index of the snapshot to be displayed
        fig    -- figure instance used for the plot; if None, a new figure is
                  created (default None)
        xaxis  -- identifier for quantity on x-axis; possibilities are:
                  'lgr' (logarithmic radius), 'mr' (mass coordinate);
                  (default 'lgr')

        Returns:
        fig    -- figure instance containing the plot
           
        """

        xposs = ["lgr", "mr"]

        try:
            assert(xaxis in xposs)
        except:
            AssertionError
            print("Error: Identifier for quantity on x-axis, '%s', unknown: Possibilities are: '%s'" % (xaxis, ', '.join(xposs)))
            return False

        try:
            assert(record < self.Ntimes)
            assert(record >= 0)
        except:
            AssertionError
            print("Error: Specified record %d is not recorded in '%s'. Records only cover the range [0, %d]" % (record, self.fname, self.Ntimes))
            return False

        data = self.snapshots[record]

        if xaxis == "lgr":
            x = data.lgr
            xlabel = r"$\log r/\mathrm{cm}$"
        else:
            x = data.mr
            xlabel = r"$M_r/M_{\odot}$"

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()
        pax = ax.twinx()

        ax.plot(x, data.lgrho, color = "black", label = r"$\rho$")
        pax.plot(x, data.v8 / 10, color = "blue", label = r"$v_9$")
        pax.plot(x, data.lgT, color = "green", label = r"$\log T$")
        pax.plot(x, data.Llum, color = "magenta", label = r"$|L_{40}|$")
        pax.plot(x, data.tau, color = "red", label = r"$\tau_R$")
        pax.set_ylim([0, 7])
        ax.set_xlim([np.min(x), np.max(x)])
        pax.set_xlim([np.min(x), np.max(x)])

        lines = ax.get_lines() + pax.get_lines()

        pax.legend([line for line in lines], [line.get_label() for line in lines])

        ax.set_xlabel(xlabel)
        ax.set_ylabel(r"$\log \rho/\mathrm{g\,cm^{-3}}$")
        pax.set_ylabel(r"$v_9$, $\log T$, $|L_{40}|$, $\tau_R$")

        ax.set_title("Run '%s': Record %d, Day %.2f" % (self.mname, record, data.time))

        return fig

    def set_xaxis_quantity(self, i, xaxis = "lgr"):

        xposs = ["r", "lgr", "mr", "km"]

        try:
            assert(xaxis in xposs)
        except AssertionError:
            print("Error: Identifier for quantity on x-axis, '%s', unknown: Possibilities are: '%s'" % (xaxis, ', '.join(xposs)))
            return None

        data = self.snapshot(i)
        if data is None:
            print("Error: No snapshot data")
            return None

        return data.__getattribute__(xaxis)

