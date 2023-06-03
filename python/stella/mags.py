# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : mags.py
#
#  Purpose :
#
#  Creation Date : 03-11-2015
#
#  Last Modified : Tue 10 Nov 2015 11:41:11 CET
#
#  Created By : U.M.Noebauer (UMN) 
#
# _._._._._._._._._._._._._._._._._._._._._.
import numpy as np
import astropy.constants as csts
import logging
import os
import flx
import prf

logging.basicConfig(format= '%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)
# will only work for UMN
datadir = "/afs/mpa/data/ulnoe/syncedworkspace/projects/Photometry/UBVRI/"
swiftdir = "/afs/mpa/data/ulnoe/syncedworkspace/projects/Photometry/SWIFT/umn_data"

class cardelli_extinction_law(object):
    def __init__(self, source = "Cardelli et al. 1989"):

        self.source = source
        self.trans = 1e4

    def infrared(self, x):

        a = 0.574 * x**1.61
        b = -0.527 * x**1.61

        return a, b

    def optical_nearir(self, x):

        y = (x - 1.82)

        a = 1. + 0.17699 * y - 0.50447 * y**2 - 0.02427 * y**3\
                + 0.72085 * y**4 + 0.01979 * y**5 - 0.77530 * y**6\
                + 0.32999 * y**7
        b = 1.41338 * y + 2.28305 * y**2 + 1.07233 * y**3 - 5.38434 * y**4\
                - 0.62251 * y**5 + 5.30260 * y**6 - 2.09002 * y**7

        return a, b

    def uv_faruv(self, x):

        Fa = np.zeros(len(x))
        Fb = np.zeros(len(x))

        mask = (5.9 <= x) * (x <= 8)
        Fa[mask] = -0.04473 * (x[mask] - 5.9)**2 - 0.009779 * (x[mask] - 5.9)**3
        Fb[mask] = 0.2130 * (x[mask] - 5.9)**2 + 0.1207 * (x[mask] - 5.9)**3

        a = 1.752 - 0.316 * x - 0.104 / ((x - 4.67)**2 + 0.341) + Fa
        b = -3.090 + 1.825 * x + 1.206 / ((x - 4.62)**2 + 0.263) + Fb

        return a, b

    def sample(self, lamA, Rv):

        try:
            len(lamA)
            lamA = np.array(lamA)
        except TypeError:
            lamA = np.array([lamA])
            pass

        lamA = np.array(lamA)

        x = self.trans / lamA
        a = np.zeros(len(x))
        b = np.zeros(len(x))

        mask_ir = (0.3 <= x) * (x <= 1.1)
        mask_opnir = (1.1 <= x) * (x <= 3.3)
        mask_uv = (3.3 <= x) * (x <= 8)

        a[mask_ir], b[mask_ir] = self.infrared(x[mask_ir])
        a[mask_opnir], b[mask_opnir] = self.optical_nearir(x[mask_opnir])
        a[mask_uv], b[mask_uv] = self.uv_faruv(x[mask_uv])

        Alam_over_Av = a + b / Rv

        if len(Alam_over_Av) == 1:
            return Alam_over_Av[0]
        else:
            return Alam_over_Av


class filter(object):
    def __init__(self, ident, source, system):
        self.ident = ident
        self.source = source
        self.system = system

        self.lamA = None
        self.trA = None

class BesselU(filter):
    def __init__(self, source):

        super(BesselU, self).__init__("U", source, "Bessel")

class BesselB(filter):
    def __init__(self, source):

        super(BesselB, self).__init__("B", source, "Bessel")

class BesselV(filter):
    def __init__(self, source):

        super(BesselV, self).__init__("V", source, "Bessel")

class CousinsR(filter):
    def __init__(self, source):

        super(CousinsR, self).__init__("R", source, "Cousins")

class CousinsI(filter):
    def __init__(self, source):

        super(CousinsI, self).__init__("I", source, "Cousins")

class Swiftuvw2(filter):
    def __init__(self, source):

        super(Swiftuvw2, self).__init__("uvw2", source, "SWIFT")

class Swiftuvw1(filter):
    def __init__(self, source):

        super(Swiftuvw1, self).__init__("uvw1", source, "SWIFT")

class Swiftuvm2(filter):
    def __init__(self, source):

        super(Swiftuvm2, self).__init__("uvm2", source, "SWIFT")

class Swiftu(filter):
    def __init__(self, source):

        super(Swiftu, self).__init__("u", source, "SWIFT")

class Swiftb(filter):
    def __init__(self, source):

        super(Swiftb, self).__init__("b", source, "SWIFT")

class Swiftv(filter):
    def __init__(self, source):

        super(Swiftv, self).__init__("v", source, "SWIFT")

class STaubenU(BesselU):
    def __init__(self):

        super(STaubenU, self).__init__("S.Taubenberger; based on Bessell & Murphy 2012 + telluric features")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(datadir, "bess12_flux_u.dat"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

        dlamA = tmpdat[1] - tmpdat[0]
        self.lamA = np.append(np.insert(self.lamA, 0, self.lamA[0] - dlamA), self.lamA[-1] + dlamA)
        self.trA = np.append(np.insert(self.trA, 0, 0), 0)


class STaubenB(BesselB):
    def __init__(self):

        super(STaubenB, self).__init__("S.Taubenberger; based on Bessell & Murphy 2012 + telluric features")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(datadir, "bess12_flux_b.dat"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

        dlamA = tmpdat[1] - tmpdat[0]
        self.lamA = np.append(np.insert(self.lamA, 0, self.lamA[0] - dlamA), self.lamA[-1] + dlamA)
        self.trA = np.append(np.insert(self.trA, 0, 0), 0)

class STaubenV(BesselV):
    def __init__(self):

        super(STaubenV, self).__init__("S.Taubenberger; based on Bessell & Murphy 2012 + telluric features")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(datadir, "bess12_flux_v.dat"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

        dlamA = tmpdat[1] - tmpdat[0]
        self.lamA = np.append(np.insert(self.lamA, 0, self.lamA[0] - dlamA), self.lamA[-1] + dlamA)
        self.trA = np.append(np.insert(self.trA, 0, 0), 0)

class STaubenR(CousinsR):
    def __init__(self):

        super(STaubenR, self).__init__("S.Taubenberger; based on Bessell & Murphy 2012 + telluric features")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(datadir, "bess12_flux_r.dat"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

        dlamA = tmpdat[1] - tmpdat[0]
        self.lamA = np.append(np.insert(self.lamA, 0, self.lamA[0] - dlamA), self.lamA[-1] + dlamA)
        self.trA = np.append(np.insert(self.trA, 0, 0), 0)

class STaubenI(CousinsI):
    def __init__(self):

        super(STaubenI, self).__init__("S.Taubenberger; based on Bessell & Murphy 2012 + telluric features")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(datadir, "bess12_flux_i.dat"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

        dlamA = tmpdat[1] - tmpdat[0]
        self.lamA = np.append(np.insert(self.lamA, 0, self.lamA[0] - dlamA), self.lamA[-1] + dlamA)
        self.trA = np.append(np.insert(self.trA, 0, 0), 0)

class umnSwiftuvw2(Swiftuvw2):
    def __init__(self):

        super(umnSwiftuvw2, self).__init__("UMN; based on effective area curves provided by M.Kromer")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(swiftdir, "umn_uvot_uvw2.txt"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

class umnSwiftuvw1(Swiftuvw1):
    def __init__(self):

        super(umnSwiftuvw1, self).__init__("UMN; based on effective area curves provided by M.Kromer")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(swiftdir, "umn_uvot_uvw1.txt"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

class umnSwiftuvm2(Swiftuvm2):
    def __init__(self):

        super(umnSwiftuvm2, self).__init__("UMN; based on effective area curves provided by M.Kromer")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(swiftdir, "umn_uvot_uvm2.txt"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]

class umnSwiftu(Swiftu):
    def __init__(self):

        super(umnSwiftu, self).__init__("UMN; based on effective area curves provided by M.Kromer")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(swiftdir, "umn_uvot_u.txt"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]


class umnSwiftb(Swiftb):
    def __init__(self):

        super(umnSwiftb, self).__init__("UMN; based on effective area curves provided by M.Kromer")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(swiftdir, "umn_uvot_b.txt"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]


class umnSwiftv(Swiftv):
    def __init__(self):

        super(umnSwiftv, self).__init__("UMN; based on effective area curves provided by M.Kromer")
        self.domain = "wavelength"
        self.type = "S*lambda"

        tmpdat = np.loadtxt(os.path.join(swiftdir, "umn_uvot_v.txt"))

        self.lamA = tmpdat[:,0]
        self.trA = tmpdat[:,1]


class StellaU(BesselU):
    def __init__(self):

        super(StellaU, self).__init__("Stella-ttfitsimpler4.trf")
        self.domain = "wavelength"
        self.type = "S*lambda"

        self.lamA = np.array([
                3000., 3050., 3100., 3150., 3200., 3250., 3300., 3350.,
                3400., 3450., 3500., 3550., 3600., 3650., 3700., 3750.,
                3800., 3850., 3900., 3950., 4000., 4050., 4100., 4150., 4200.
                ])

        self.trA = np.array([
                0.000, 0.016, 0.068, 0.167, 0.287, 0.423, 0.560, 0.673,
                0.772, 0.841, 0.905, 0.943, 0.981, 0.993, 1.000, 0.989, 0.916,
                0.804, 0.625, 0.423, 0.238, 0.114, 0.051, 0.019, 0.000
                ])

class StellaB(BesselB):
    def __init__(self):

        super(StellaB, self).__init__("Stella-ttfitsimpler4.trf")

        self.lamA = np.array([
                3600.,  3700.,  3800.,  3900.,
                4000.,  4100.,  4200.,  4300.,  4400.,
                4500.,  4600., 4700.,  4800.,  4900.,  5000.,  5100.,
                5200.,  5300.,  5400.,  5500., 5600.
                ])

        self.trA = np.array([
                0.000, 0.030, 0.134, 0.567, 0.920, 0.978, 1.000, 0.978,
                0.935, 0.853, 0.740, 0.640, 0.536, 0.424, 0.325, 0.235, 0.150,
                0.095, 0.043, 0.009, 0.000
                ])

class StellaV(BesselV):
    def __init__(self):

        super(StellaV, self).__init__("Stella-ttfitsimpler4.trf")

        self.lamA = np.array([
                4700., 4800.,  4900.,  5000.,  5100.,
                5200.,  5300.,  5400.,  5500.,  5600.,  5700.,  5800.,  5900.,
                6000.,  6100.,  6200.,  6300.,  6400.,
                6500.,  6600.,  6700.,  6800.,  6900.,  7000.
                ])

        self.trA = np.array([
                0.000, 0.030,  0.163,  0.458,  0.780,
                0.967,  1.000, 0.973, 0.898, 0.792, 0.684, 0.574,
                0.461, 0.359, 0.270, 0.197, 0.135, 0.081, 0.045, 0.025, 0.017,
                0.013, 0.009, 0.000
                ])

class StellaR(CousinsR):
    def __init__(self):

        super(StellaR, self).__init__("Stella-ttfitsimpler4.trf")

        self.lamA = np.array([

                5500., 5600., 5700., 5800., 5900., 6000., 6100., 6200., 6300.,
                6400., 6500., 6600., 6700., 6800., 6900., 7000., 7100., 7200.,
                7300., 7400., 7500., 8000., 8500., 9000.
                ])

        self.trA = np.array([
                0.00,  0.23,  0.74,  0.91,  0.98,  1.00,  0.98,  0.96,  0.93,
                0.90,  0.86,  0.81,  0.78,  0.72,  0.67,  0.61,  0.56,  0.51,
                0.46,  0.40,  0.35,  0.14,  0.03,  0.00
                ])

class StellaI(CousinsI):
    def __init__(self):

        super(StellaI, self).__init__("Stella-ttfitsimpler4.trf")

        self.lamA = np.array([
                7000., 7100., 7200., 7300., 7400., 7500., 7600., 7700., 7800.,
                7900., 8000., 8100., 8200., 8300.,
                8400., 8500., 8600., 8700., 8800., 8900., 9000., 9100., 9200.
                ])

        self.trA = np.array([
                0.000, 0.024, 0.232, 0.555, 0.785, 0.910, 0.965, 0.985, 0.990,
                0.995, 1.000, 1.000, 0.990, 0.980,
                0.950, 0.910, 0.860, 0.750, 0.560, 0.330, 0.150, 0.030, 0.000
                ])

class FilterSystem(object):
    def __init__(self, ident, source, system):

        self.ident = ident
        self.source = source
        self.system = system

        self.filters = {}

class StellaUBVRI(FilterSystem):
    def __init__(self):

        super(StellaUBVRI, self).__init__("UBVRI", "Stella-ttfitsimpler4.trf", "Bessel-Cousins")

        self.filters["U"] = StellaU()
        self.filters["B"] = StellaB()
        self.filters["V"] = StellaV()
        self.filters["R"] = StellaR()
        self.filters["I"] = StellaI()

class STaubenUBVRI(FilterSystem):
    def __init__(self):

        super(STaubenUBVRI, self).__init__("UBVRI", "S.Taubenberger; after Bessell & Murphy 2012 + telluric features", "Bessel-Cousins")

        self.domain = "wavelength"
        self.type = "S*lambda"

        self.filters["U"] = STaubenU()
        self.filters["B"] = STaubenB()
        self.filters["V"] = STaubenV()
        self.filters["R"] = STaubenR()
        self.filters["I"] = STaubenI()

class umnSWIFT(FilterSystem):
    def __init__(self):

        super(umnSWIFT, self).__init__("uvw2uvm2uvw1ubv", "UMN; based on filter curves provided by M. Kromer", "SWIFT")

        self.domain = "wavelength"
        self.type = "S*lambda"

        self.filters["uvw2"] = umnSwiftuvw2()
        self.filters["uvw1"] = umnSwiftuvw1()
        self.filters["uvm2"] = umnSwiftuvm2()
        self.filters["u"] = umnSwiftu()
        self.filters["b"] = umnSwiftb()
        self.filters["v"] = umnSwiftv()

class StellaUBVRIzeros(object):
    def __init__(self):

        self.ident = "UBVRI"
        self.source = "Stella-ttfitsimpler4.trf"
        self.system = "Bessel-Cousins"

        self.zeropoints = {}

        self.zeropoints["U"] = -13.90
        self.zeropoints["B"] = -13.00
        self.zeropoints["V"] = -13.72
        self.zeropoints["R"] = -13.66
        self.zeropoints["I"] = -14.42


class vega_spectrum(object):
    def __init__(self, name, source):
        self.name = name
        self.source = source

    def load_from_ascii(self, fname):

        tmpdat = np.loadtxt(fname)
        self.lamA = data[:,0]
        self.FA = data[:,1]

    def load_from_fits(self, fname):
        import astropy.io.fits as fits

        tmpdat = fits.open(fname)

        self.lamA = tmpdat[1].data["WAVELENGTH"]
        self.FA = tmpdat[1].data["FLUX"]

class vega_zeros(object):
    def __init__(self, spectrum, filtersystem, mag_anchor = 0.03):

        self.spec = spectrum
        self.mag_anchor = mag_anchor
        self.filtersystem = filtersystem
        self.zeropoints = {}

    def convolve_integrate_spec(self, filter):

        scr = np.argwhere(filter.trA > 0).reshape(-1)
        first_nonzero_tr_lam = filter.lamA[scr.min() - 1]
        last_nonzero_tr_lam = filter.lamA[scr.max() + 1]

        try:
            ispec_min = np.max(np.argwhere(self.spec.lamA < first_nonzero_tr_lam).reshape(-1))
            ispec_max = np.min(np.argwhere(self.spec.lamA > last_nonzero_tr_lam).reshape(-1))
        except ValueError:
            logging.exception("Spectrum does not cover full filter window with non-zero transmission")

        fil_x = filter.lamA[scr.min()-1:scr.max()+2]
        fil_y = filter.trA[scr.min()-1:scr.max()+2]
        spec_x = self.spec.lamA[ispec_min:ispec_max+1]
        spec_y = self.spec.FA[ispec_min:ispec_max+1]

        if len(fil_x) >= len(spec_x):
            y = np.interp(fil_x, spec_x, spec_y)
            dx = (fil_x[1:] - fil_x[:-1])

            Fband = np.sum(y * fil_y * np.append(dx, dx[-1]))
        else:
            y = np.interp(spec_x, fil_x, fil_y)
            dx = (spec_x[1:] - spec_x[:-1])

            Fband = np.sum(spec_y * y * np.append(dx, dx[-1]))

        return Fband

    def calc_zeropoints_appflux(self):

        for k in self.filtersystem.filters:

            Fband = self.convolve_integrate_spec(self.filtersystem.filters[k])

            Mband = -2.5 * np.log10(Fband)

            self.zeropoints[k] = self.mag_anchor - Mband


class StellaMagnitudeCalculator(object):
    def __init__(self, flxinp, prfinp):

        if type(flxinp) == type("a"):
            self.flxdat = flx.flx_reader(flxinp)
        else:
            self.flxdat = flxinp

        if type(prfinp) == type("a"):
            self.prfdat = prf.prf_reader(prfinp)
        else:
            self.prfdat = prfinp

        self.Utp = 1e5
        self.Ur = 1e14
        self.Upc = 3.0856776000e18

        self.Ufreq = csts.k_B.cgs.value * self.Utp / (csts.h.cgs.value)
        self.ccl = csts.c.cgs.value * 1e8 / (self.Ufreq)
        self.cflux = 60.*csts.sigma_sb.cgs.value*(self.Utp / np.pi)**4
        self.Scale = -2.5 * np.log10(self.cflux*(self.Ur/(10.*self.Upc))**2)

        self.Dlognu = -1. / np.log(self.prfdat.Freqmn[1:] / self.prfdat.Freqmn[:-1])

        self.iblow = {}
        self.Mzero = {}

    def add_filter_system(self, filtersystem):

        self.filtersystem = filtersystem

        for k, filter in self.filtersystem.filters.items():

            self.find_filter_band(filter)

    def add_filter_zeropoint(self, zeropoints):

        incomplete = False

        for k in self.filtersystem.filters:

            try:
                self.Mzero[k] = zeropoints[k]
            except KeyError:
                logging.warn("Missing zeropoint for filter with ident '{}'".format(k))
                incomplete = True
                pass

        if incomplete:
            logging.warn("Missing zeropoints; call add_filter_zeropoints again with appropriate zeropoints dict")


    def find_filter_band(self, filter):

        nu = self.prfdat.Freqmn

        lamA = self.ccl / filter.lamA
        self.iblow[filter.ident] = np.zeros(len(lamA))
        for i, lam in enumerate(lamA):
            self.iblow[filter.ident][i] = np.max(np.argwhere((nu - lam) < 0).reshape(-1))

    def calculate_colour_magnitudes(self):

        self.t = {}
        self.M = {}

        for k, filter in self.filtersystem.filters.items():
            self.t[k] = np.array([])
            self.M[k] = np.array([])

            for record in self.flxdat.records:

                ttmp, Mtmp = self.calculate_band_magnitude(filter, record)
                self.t[k] = np.append(self.t[k], ttmp)
                self.M[k] = np.append(self.M[k], Mtmp)

    def calculate_band_magnitude(self, filter, record):

        N = len(filter.lamA)
        Flxavg = np.zeros(record.Flsave.shape[-1])
        sumfhx = np.zeros(record.Flsave.shape[-1])

        # assumes that first and last entry of filter transmission equal 0
        wlstep = (filter.lamA[1] - filter.lamA[0]) / self.ccl
        for i in xrange(1,N-1):

            j = self.iblow[filter.ident][i]

            F = record.Flsave[j,:]
            Fp = record.Flsave[j+1,:]

            if j < record.Nfrus[-1]:
                Fhx = np.exp(np.log(np.fabs(Fp)) + np.log(np.fabs(F/Fp)) * self.Dlognu[j] * np.log((self.ccl / filter.lamA[i]) / self.prfdat.Freqmn[j+1]))
            else:
                Fhx = np.fabs(F)

            Fhx *= filter.trA[i] * (self.ccl / filter.lamA[i])**5
            stepn = (filter.lamA[i+1] - filter.lamA[i]) / self.ccl
            if (np.fabs(wlstep - stepn) / wlstep < 1e-4) and i != N-2:
                sumfhx = sumfhx + Fhx
            else:
                Flxavg += sumfhx * wlstep + Fhx * (wlstep + stepn) / 2.
                sumfhx = np.zeros(record.Flsave.shape[-1])
                wlstep = stepn

        M = -2.5 * np.log10(Flxavg) + self.Mzero[filter.ident] + self.Scale
        t = record.Tcurv

        return t, M
