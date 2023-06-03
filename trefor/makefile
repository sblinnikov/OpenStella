
SYSTEM= -Dunix
PERF=-DPOINTER
CC=gcc
# debug version
#CCOPT= -D_DEBUG_TRF_ -fbounds-check
#CCOPT=-DWITH_LOGO

.c.o:
	$(CC) $(CCOPT) $(SYSTEM) $(PERF) -c  $*.c


help:
	@echo "Type:"
	@echo " 'make conf'    for configuration"
	@echo " 'make all'     for make all executables"
	@echo " 'make all95'   for make all executables for f95"
	@echo " 'make clean'   to delete all work files"

all: trf trefor

all95: trf trefor95

trf:  trfu.c
	$(CC) $(CCOPT) trfu.c -o trf

trefor:  trefor.o pass1.o pass2.o dtcdia.o
	$(CC)  -o  trefor  trefor.o pass1.o pass2.o dtcdia.o

trefor95:  trefor_95.o pass1.o pass2_95.o dtcdia.o
	$(CC)  -o  trefor95  trefor_95.o pass1.o pass2_95.o dtcdia.o

pass1.o:      pass1.c trfgen.h trfcode.h chargen.h tree.h pass1dep.h align.h

dtcdia.o:     dtcdia.c trfgen.h trfcode.h chargen.h

pass2.o:      pass2.c trfgen.h trfcode.h chargen.h tree.h pass2dep.h align.h

pass2_95.o:   pass2_95.c trfgen95.h trfcode.h chargen.h tree.h pass2dep.h align.h

trefor.o:     trefor.c trfgen.h trfcode.h chargen.h tree.h align.h

trefor_95.o:  trefor_95.c trfgen.h trfcode.h chargen.h tree.h align.h

tun.o:        tun.c trfcode.h trfgen.h

tun:
	$(CC) $(CCOPT) $(SYSTEM) $(PERF) tun.c -o tun
pass1dep.h : tun
	./tun
pass2dep.h : tun
	./tun
align.h : tun
	./tun
clean:
	rm -f trefor.o trefor_95.o pass1.o pass2.o pass2_95.o dtcdia.o tun.o \
	tun chargen.h  pass1dep.h pass2dep.h align.h core
conf : tun
	./tun
