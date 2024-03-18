# This makefile is for ronfndec with MPI
#PROG = ../vladsf/ronfpar.exe
PROG = ../run/vladsf/ronfpar.exe
#PROGIN = ../vladsf/xinshpar.exe
PROGIN = ../run/vladsf/xinsh.exe
PROGDAN = ronfpardan.exe ## no bf and ff
PROGBF = ronfparbf.exe
PROG1 = ronf1.exe

DEL = rm -f

#VPATH = ../eve:../src:../strad:../strad/run

#VPATH = ../src/

STLHOME  := ../
DIR_SRC := $(STLHOME)

vpath %.trf ../eve: ../strad:../vladsf:../src
vpath %.f ../eve:../strad:../vladsf:../src
vpath %.f90 ../strad/rada:../src:../src/util
vpath %.o ./
vpath %.inc ../src


VPATH := $(STLHOME)src  $(STLHOME)src/stl $(STLHOME)src/util $(STLHOME)vladsf
INCL_DIR := -I$(STLHOME)src/ -I$(STLHOME)src/stl -I$(STLHOME)src/util -I$(STLHOME)vladsf

#--------------------------
FILES_base =  kinds.f90  math_constants.f90  phys_constants.f90 stl_units.f90  \
              glob_matching.f90 string_utilities.f90 string_tools.f90 cp_files.f90 \
              chem_data.f90  stella_config.f90
TEMP := $(FILES_base:.trf=.F)
TEMP := $(patsubst %.F90,%.f90, $(TEMP:.f=.f90))
TEMP := $(patsubst %.F90,%.f90, $(TEMP:.F=.f90))
OBJS_base := $(patsubst %.f90,%.o, $(TEMP))

FILES_cross =  rad_photo_cross_section.f90
TEMP := $(FILES_cross:.trf=.F)
TEMP := $(patsubst %.F90,%.f90, $(TEMP:.F=.f90))
TEMP := $(TEMP:.f=.o)
OBJScross := $(patsubst %.f90,%.o, $(TEMP))

#--------------------------


FILES = ronfpar.trf ronfitab.trf bessi0.f bessk0ex.f \
        blas.f dmach.trf edensol.trf gffcalc.f gshfdxsec.f \
        hydxsecl.f hydxsecn.f hypho.f lineexpab_cor.trf \
        lnblnk.f ndex.f  pfsaha.f \
        sahaeqn.f setnucms.f sparseblas.f tablsort.f \
        valence_nl.f azdat.trf length.trf stradio.trf \
        hMinusAbsorp.trf opacityt.trf
OBJS := $(OBJS_base) $(OBJScross) $(patsubst %.f,%.o, $(FILES:.trf=.f))

FILESIN = ronfpar.trf ronfitab.trf bessi0.f bessk0ex.f \
        blas.f dmach.trf edensol.trf gffcalc.f gshfdxsec.f \
        hydxsecl.f hydxsecn.f hypho.f lineexpab_cor.trf \
        lnblnk.f ndex.f  pfsaha.f \
        sahaeqn.f setnucms.f sparseblas.f tablsort.f \
        valence_nl.f azdat.trf length.trf stradio.trf \
        hMinusAbsorp.trf opacityInSh.trf
OBJSIN := $(OBJS_base) $(OBJScross) $(patsubst %.f,%.o, $(FILESIN:.trf=.f))


OBJSDAN = ronfpar.o ronfitab.o bessi0.o bessk0ex.o \
        blas.o dmach.o edensol.o gffcalc.o gshfdxsec.o \
        hydxsecl.o hydxsecn.o hypho.o lineexpab_cor.o \
        lnblnk.o ndex.o opacitydan.o pfsaha.o \
        sahaeqn.o setnucms.o sparseblas.o tablsort.o \
        valence_nl.o azdat.o length.o stradio.o

OBJBF = ronfpar.o ronbffitab.o bessi0.o bessk0ex.o \
        blas.o dmach.o edensol.o gffcalc.o gshfdxsec.o \
        hydxsecl.o hydxsecn.o hypho.o lineexpab_cor.o \
        lnblnk.o ndex.o opacitybf.o pfsaha.o \
        sahaeqn.o setnucms.o sparseblas.o tablsort.o \
        valence_nl.o azdat.o length.o stradio.o

OBJBF1 = ronbftab1.o bessi0.o bessk0ex.o \
        blas.o dmach.o edensol.o gffcalc.o gshfdxsec.o \
        hydxsecl.o hydxsecn.o hypho.o lineexpab_cor.o \
        lnblnk.o ndex.o opacitybf.o pfsaha.o \
        sahaeqn.o setnucms.o sparseblas.o tablsort.o \
        valence_nl.o azdat.o length.o stradio.o

#mzalloc.o



#LIBS = -L/opt/SUNWhpc/lib -R/opt/SUNWhpc/lib -lmpi
LIBS =
#mpich.lib

#CC = bcc32 -c -D_NAME
#CC = bcc32 -c

#FC = fl32

FC = f77
#FFLAGS = -c -static -fast -tune:k7  # for optimization
#FFLAGS = -c -static -iface:cref -debug:full -traceback -tune:k7  # for debug
#FFLAGS = -c -static -debug:full -traceback -tune:k7  # for debug


#FFLAGS = -c # -Ox    # for optimization
#FFLAGS = -c -4Yb # for debug
#FFLAGS = -c -check:all -debug:full -fpe:0 -traceback # for DEC debug
#FFLAGS = -c -check:all -traceback -list -show:all  # for DEC debug
#FFLAGS = -c -optimize:5 -xarch=v9

FFLAGS =  -v -c -fast  -xcode=abs64  -xarch=native -dalign -I/opt/SUNWhpc/include

#FFLAGS = -c -fast
#FFLAGS = -c -g -C -xregs=syst -dalign -I/opt/SUNWhpc/include # for debug

FC = mpif95f # fujutsu

FC = mpif95i # Intel
FC = f95i # Intel

#FFLAGS =  -v -c -fast -xregs=syst
# fujutsu:
FFLAGS = -c  -sav -g  --trap  --ap   --chkglobal   --pca # debug
FFLAGS = -c  -sav --trap  --tpp   --o2   --ntrace   --f95   --info
FFLAGS = -c  -sav  --tpp   --o2   --ntrace   --f95   --info

#FFLAGS =   -c -save -zero  -r8   -tpp7   -xW   -ip
FFLAGS =   -c -save -zero -O3
FFLAGS = -c -save -g -CB -traceback -inline_debug_info  -DD

SYSTYPE="gfortran"
#SYSTYPE="pgf"
#SYSTYPE="par_f95i"
#SYSTYPE="par_ifcit"
#SYSTYPE="MPA_f95i"
#SYSTYPE="MPA_f95f"
#SYSTYPE="MPA_f95n"

LDFLAGS =

########################################
## For gfortran fortran
ifeq ($(SYSTYPE),"gfortran")
  #FC = gfortran
  FC = mpif90
  #FFLAGS_COMMON := -c -cpp -g -ffpe-trap='invalid,overflow' # -fbounds-check -Wall -ffpe-trap='invalid,zero,overflow,underflow,precision,denormal'
  FFLAGS_COMMON = -c -cpp -O3 -fbounds-check
  FFLAGS_FIX := $(FFLAGS_COMMON) -ffixed-line-length-none -fno-automatic -Wno-unused -Wno-unused-dummy-argument -std=legacy
  FFLAGS := $(FFLAGS_COMMON) -ffree-form -ffree-line-length-none -Wno-tabs
  LDFLAGS =
  LIBS =
endif

########################################
## For Intel fortran
ifeq ($(SYSTYPE),"MPA_f95i")
  FC = f95i  # Intel fortran
  #FFLAGS = -c -save -zero -fpe0  -check bounds -g -traceback # -- for debug
  #FFLAGS = -c -O3 -save -zero -tpp7   -ip # -xW # -- optimize for Pentium
  #FFLAGS =   -c -save -static -zero -O3
  #FFLAGS = -c -save -static -fpe0 -g -CB -traceback -inline_debug_info  -DD
  FFLAGS_FIX =   -c -save -static -zero -O2 -fpe0 -traceback -g -CB -traceback
  FFLAGS = -free
  FFLAGS := $(FFLAGS_FIX) $(FFLAGS)
#define
  FFLAGS := $(FFLAGS) -D__INTEL
  LIBS =
endif

########################################
## For Intel fortran itanium parallel
ifeq ($(SYSTYPE),"par_ifcit")
  FC = ifort  # Intel fortran
  #FFLAGS = -c -save -zero -fpe0  -check bounds -g -traceback # -- for debug
  #FFLAGS = -c -O3 -save -zero -tpp7   -ip # -xW # -- optimize for Pentium
  FFLAGS =   -c -132 -save -static -zero -O3 -I/usr/local/include/
  #FFLAGS =   -c -save -static -zero -O2 -fpe0 -traceback # -CB -traceback
      # -fpe0 crashes in MPICH
  #FFLAGS = -c -save -static -fpe0 -g -CB -traceback -inline_debug_info  -DD
  LIBS = -L/usr/local/lib -lmpich -lfmpich -lmpichf90
endif

########################################
## For Intel fortran parallel
ifeq ($(SYSTYPE),"par_f95i")
  FC = mpif95i  # Intel fortran
  #FFLAGS = -c -save -zero -fpe0  -check bounds -g -traceback # -- for debug
  #FFLAGS = -c -O3 -save -zero -tpp7   -ip # -xW # -- optimize for Pentium
  FFLAGS =   -c -132 -save -static -zero -O3
  #FFLAGS =   -c -save -static -zero -O2 -fpe0 -traceback # -CB -traceback
      # -fpe0 crashes in MPICH
  #FFLAGS = -c -save -static -fpe0 -g -CB -traceback -inline_debug_info  -DD
  LIBS =
endif

########################################
## For NAG fortran
ifeq ($(SYSTYPE),"MPA_f95n")
  FC = f95n  # NAG fortran
  FFLAGS = -c  -save
  FFLAGS = -c -O3 -save -f77
  LIBS = # for NAG
endif


########################################
## For Fujutsu fortran
ifeq ($(SYSTYPE),"MPA_f95f")
  FC = f95f  # fujutsu fortran
  FFLAGS = -c  -sav -g  --trap  --ap   --chkglobal   --pca # debug
#  FFLAGS = -c  -sav --trap  --tpp   --o2   --ntrace   --f95   --info
#  FFLAGS = -c  -sav  --tpp   --o2   --ntrace   --f95   --info
  LIBS =
endif

########################################
## For Portland Group fortran
ifeq ($(SYSTYPE),"pgf")
  FC = pgf90  # pgf fortran
  FFLAGS = -c -fast -Minform,warn -Msave -I/raid/mpich/include
 #FFLAGS = -c -C -g -Mbounds -Minform,warn -Msave
  LIBS = /home/blinn/prg/lib/libsparse.a \
              /home/blinn/prg/lib/liblnag.a
 LDFLAGS = -L /raid/mpich/lib -lmpich -lfmpich
endif

#LDFLAGS = -incremental:no
#LDFLAGS = -fast

TREFOR = -trf

# for ctrf:
TRFFLAGS = -nfs
#TRFFLAGS = @ne
#TRFFLAGS =

.IGNORE:

%.o : %.trf
	$(TREFOR) $(TRFFLAGS) $<
	$(FC) $(FFLAGS_FIX) $(patsubst %.trf,%.f,$<) $(INCL_DIR)

%.o: %.f
	$(FC) $(FFLAGS_FIX) $< $(INCL_DIR)

%.o %.mod:: %.f90
	$(FC) $(FFLAGS) $< $(INCL_DIR)
%.o %.mod:: %.F90
	$(FC) $(FFLAGS) $< $(INCL_DIR)
%.o: %.F
	$(FC) $(FFLAGS) $< $(INCL_DIR)

#%.o: %.mod ## if make wants m2c thinking that mod is from Modula language

# %.mod : %.o
# 	@if [! -f $@ ]; then \
# 	rm $< \
# 	$(MAKE) $< \
# 	fi

help:
	@echo "You can do: "
	@echo " ron    -- compile parallel version ronfndec "
	@echo " inner  -- compile parallel version ronfndec with opacityInSh "
	@echo " dan    -- ronfict with bb opacities only (for comparison with D.Kasen) "
	@echo " bf     -- compile ?"
	@echo " bf1    -- compile ?"
	@echo " " $(PROG1) "   -- compile ?"
	@echo " clean  -- clean files"

all: help

ron: $(PROG)

$(PROG): $(OBJS)
	$(FC) -o $(PROG) $(LDFLAGS) $(OBJS) $(LIBS)

inner: $(PROGIN)

$(PROGIN): $(OBJSIN)
	$(FC) -o $(PROGIN) $(LDFLAGS) $(OBJSIN) $(LIBS)

dan: $(PROGDAN)

$(PROGDAN): $(OBJSDAN)
	$(FC) -o $(PROGDAN) $(LDFLAGS) $(OBJSDAN) $(LIBS)

bf: $(PROGBF)

$(PROGBF): $(OBJBF)
	$(FC) -o $(PROGBF) $(LDFLAGS) $(OBJBF) $(LIBS)

bf1: $(PROG1)

$(PROG1): $(OBJBF1)
	$(FC) -o $(PROG1) $(LDFLAGS) $(OBJBF1) $(LIBS)
#   $(MV) $(PROG) $(DEST)
#
# Here are all the dependencies:
#

ronfpar.o:                     ronfpar.trf
ronfitab.o:                    ronfitab.trf  ../src/opacity.inc ../src/zone.inc
ronbffitab.o : ronbffitab.trf  ../src/opacity.inc ../src/zone.inc
ronbftab1.o : ronbftab1.trf  ../src/opacity.inc ../src/zone.inc
azdat.o     : ../src/azdat.trf ../src/zone.inc
stradio.o   : ../src/stradio.trf ../src/snrad.inc ../src/abo.inc ../src/zone.inc
length.o    : ../src/length.trf
dmach.o:           dmach.trf
edensol.o:         edensol.trf
kinds.o         :  kinds.f90
lineexpab_cor.o:   lineexpab_cor.trf
opacity.o:                     opacity.trf ../src/zone.inc
opacityInSh.o:                 opacityInSh.trf ../src/zone.inc
opacitydan.o:                  opacitydan.trf # removed ../src/zone.inc
opacitybf.o:                   opacitybf.trf ../src/zone.inc
hMinusAbsorp.o:                hMinusAbsorp.trf

bessi0.o:                      bessi0.f
bessk0ex.o:                    bessk0ex.f
blas.o:                        blas.f
gffcalc.o:                     gffcalc.f
gshfdxsec.o:                   gshfdxsec.f
hydxsecl.o:                    hydxsecl.f
hydxsecn.o:                    hydxsecn.f
hypho.o:                       hypho.f
lnblnk.o:                      lnblnk.f
#mzalloc.o:                    mzalloc.f
ndex.o:                        ndex.f
pfsaha.o:                      pfsaha.f
sahaeqn.o:                     sahaeqn.f
setnucms.o:                    setnucms.f
sparseblas.o:                  sparseblas.f
tablsort.o:                    tablsort.f
valence_nl.o:                  valence_nl.f

clean:
	$(DEL) ../vladsf/ronfpar.f ../vladsf/ronbffitab.f ../vladsf/ronfitab.f \
               ../vladsf/edensol.f ../vladsf/lineexpab_cor.f ../src/azdat.f \
               ../vladsf/opacity.f ../vladsf/opacitybf.f ../vladsf/opacitydan.f \
               ../src/stradio.f  ../src/length.f ../vladsf/dmach.f
	$(DEL) *.o  *.mod ../vladsf/*.o ../vladsf/*.mod ../vladsf/*.lst ../src/*.lst
