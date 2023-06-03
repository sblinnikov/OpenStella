#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class tt_reader(object):
    """
    Data reader for a *.tt file created by the Stella code
    """
    def __init__(self, mname, verbose = False):
        """
        Arguments:
        mname -- name of the model, i.e. of the tt file without extension

        Keyword Arguments:
        verbose -- print detailed information if True
        """

        self.verbose = verbose

        self.mname = mname.rsplit("/")[-1]
        self.fname = mname + ".tt"

        self.process_tt_file()

    def process_tt_file(self):
        """
        Read and process the data of the tt file
        """

        if self.verbose:
            print("Reading tt file for run '%s'" % self.mname)
        with open(self.fname, "r") as f:

            buffer = f.readline()

            while buffer != "":
                tmp = buffer.rsplit()
                if len(tmp) != 0:
                    if tmp[0] == "time":
                        break
                buffer = f.readline()
            else:
                print("Warning: no appropriate data header found, file not properly processed")
                return

            fpos = f.tell()
            buffer = f.readline()
            tmp = buffer.rsplit()
            if tmp[0] != "XNianm":
                f.seek(fpos)

            raw_data = np.loadtxt(f)
            if self.verbose:
                print("'%s' found and read" % self.fname)

        self.raw_data = raw_data

        self.time = raw_data[:,0]
        self.Tbb = raw_data[:,1]
        self.rbb = raw_data[:,2]
        self.Teff = raw_data[:,3]
        self.Rlast_sc = raw_data[:,4]
        self.Rtau23 = raw_data[:,5]
        self.Mbol = raw_data[:,6]
        self.MU = raw_data[:,7]
        self.MB = raw_data[:,8]
        self.MV = raw_data[:,9]
        self.MI = raw_data[:,10]
        self.MR = raw_data[:,11]
        self.Mbolavg = raw_data[:,12]
        self.gdepos = raw_data[:,13]

        if self.verbose:
            print("read %d data points, ranging from %.3f to %.3f days" % (len(self.time), self.time[0], self.time[-1]))

    def show_colour_lightcurves(self, fig = None):

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        ax.plot(self.time, self.MU, label = r"U")
        ax.plot(self.time, self.MB, label = r"B")
        ax.plot(self.time, self.MV, label = r"V")
        ax.plot(self.time, self.MI, label = r"I")
        ax.plot(self.time, self.MR, label = r"R")
        ax.plot(self.time, self.Mbol, label = r"bolometric", ls = "dashed", color = "grey")

        ax.set_ylim([-14, -22])
        ax.set_xlim([0, 60])
        ax.set_ylabel("magnitude")
        ax.set_xlabel(r"$t$")

        ax.legend()


        return fig

    def show_photospheric_velocity(self, fig = None):

        if fig is None:
            fig = plt.figure()

        ax = fig.gca()

        thb_prop = self.time * 86400. + self.rbb / 2.9979e10
        tph23_prop = self.time * 86400. + self.Rtau23/ 2.9979e10

        vphb = (self.rbb * 1e-8) / (thb_prop)
        vph23 = (self.Rtau23 * 1e-8) / (tph23_prop)

        ax.plot(self.time, vphb, label = "black body fit")
        ax.plot(self.time, vph23, label = r"$\tau = 2/3$")

        ax.set_xlim([-5, 200])
        ax.set_ylim([0,15])
        ax.legend()

        return fig



def test():

    mname = "W7fwindCObqeps601"

    tt_tester =  tt_reader(mname)
    tt_tester.show_colour_lightcurves()
    tt_tester.show_photospheric_velocity()



if __name__ == "__main__":

    test()
    plt.show()

