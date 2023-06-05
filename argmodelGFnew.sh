#!/bin/bash
#   Script for Stella run on a toy SNIa model
# This shell uses parts of fancyo script written by Wayne Pollock, Tampa FL 1996

# Define a shell function called Pause
#Pause()
#{
#    echo
#    echo -n Hit Enter to continue....
#    read
#}

Pause()
{
    key=""
    echo -n Hit any key to continue....
    stty -icanon
    key=`dd count=1 2>/dev/null`
    stty icanon
}

echo This script will run a model produced with Weaver-Woosley KEPLER code
echo Do not use it for W7* models!!!
echo appropriate files *.hyd and *.abn are needed in modmake dir, as well as *.dat file in run/strad .
echo The file lineatom.dat will be symbolically linked to run/vladsf by this script
echo Input the second argument "1" if a new opacity table must be computed
Pause
#   Set model remap parameters:
 InputModel=$1
# RezonedModel=${InputModel}f
# RezonedModel=${InputModel}h  # normally, suffix h for half number and f for fixed number of zones
 run=${InputModel}   # or any other name for ${run}.dat file in run/strad
                       # the ${run}.dat file must be prepared before the run
 Cutmass=0.  # 4.d-5
 Nkeep=1    # number of original zones after cutmass kept and not merged
 Nmult=1    # factor to multiply Nkeep zones to refine cenral zoning

 BuildNewModel=1         # Set this to 1 if a new model must be computed
 KeepModelZones=1        # Set this to 1 to keep original number of zones
 OpacityTable=${InputModel}
# OpacityTable=${RezonedModel}
 NewOpacity=$2            # Set this to 1 if a new opacity table must be computed
 RunTTfit=0              # Set this to 1 if the run has not produced *.tt file
#Composition=uniform     # for opacity, mostly for tests
 Composition=mixed       # for opacity, may be a crude zoning table with @skip of zones
#Composition=OutUniform  # for opacity, all central zones, outer -- uniform
 echo '******'
 echo InputModel Cutmass Nkeep Nmult
 echo $InputModel $Cutmass $Nkeep $Nmult
 echo '******'
 #SYSTYPE="pgf"
 #SYSTYPE="MPA_f95i"
 #SYSTYPE="ifort"
  SYSTYPE="gfortran"
 # SYSTYPE="cygwin_ifort"
 # SYSTYPE="cygwin_f90"
 # SYSTYPE="MPA_f95n"
 echo SYSTYPE ${SYSTYPE}
 export SYSTYPE=${SYSTYPE}

 case "${SYSTYPE}" in
      'ifort')
            FC=ifort
               ;;
      'gfortran')
            FC=gfortran
               ;;
      'MPA_f95i')
            FC=f95i
               ;;
      'MPA_f95n')
            FC=f95n
               ;;
      'pgf')
            FC=pgf95
               ;;
      'cygwin_ifort')
            FC=ifl
               ;;
      'cygwin_f90')
            FC=f90
               ;;
 esac

 echo Fortran Compiler version:
 $FC -v
 rc=$?
if [ $rc != 0 ] ; then
   echo Fortran Compiler $FC not found!
   echo I exit now due to this error...
   exit 1
else
   echo Fortran Compiler $FC
#   exit 0
fi

# ----------------------------------  Start of preparations
 HOMEStella=`pwd`
 echo '******'
 echo current directory is:
 echo $HOMEStella
 echo '******'
 export HOMEStella=$HOMEStella


if [ ! -e $HOMEStella/bin  ]; then
   mkdir $HOMEStella/bin
   echo directory $HOMEStella/bin created
fi

if [ ! -e $HOMEStella/run/strad/${run}.dat  ]; then
   echo $HOMEStella/run/strad/${run}.dat does not exist
   echo I exit now due to this error...
   exit 2
fi


# ----------------------------------  Start of Processing
# Compile the "put" command
#if [ ! -e put ]; then
#   cc -o put  $HOMEStella/src/put.c
#   mv put $HOMEStella/bin
#   echo '******'
#   echo put command created
#   echo '******'
#fi

# Compile the "trf" command
Pause				# invoke the function Pause.
echo trf command and trefor preprocessor are needed.
echo If they are not found  in /usr/local/bin they will be built in $HOMEStella/bin/trf
echo For future work save trf and trefor in your PATH, and $HOMEStella/trefor/.trfrc in your $HOME
Pause
if [ ! -e $HOMEStella/bin/trf ]; then
  if [ ! -e /usr/local/bin/trf ]; then
   cd $HOMEStella/trefor
   pwd
   make conf
   make all
   make all95
   mv trf trefor trefor95 $HOMEStella/bin
   echo HOME/.tr*  $HOME/.tr*
   if [ ! -e $HOME/.trfrc ]; then
     echo checking HOME/.trfrc
     cp .trfrc $HOME
     echo copying .trfrc to HOME
     Pause
   fi
   make clean
   echo '******'
   echo "trf (Trefor preprocessor) created"
   echo '******'
  else
     echo trf found in /usr/local/bin
   if [ ! -e $HOME/.trfrc ]; then
     echo checking HOME/.trfrc
     cp $HOMEStella/trefor/.trfrc $HOME
     echo copying .trfrc to HOME
     Pause
   fi
  fi
fi
echo HOME $HOME
# add $HOMEStella/bin/ to PATH
 export PATH=$HOMEStella/bin:"$PATH"
 echo PATH after trf build $PATH
 Pause
# which put

if [ $BuildNewModel == 1 ]
then
# Prepare to build a model for Stella run
 echo '******'
 echo start building model
 echo '******'
Pause				# invoke the function Pause.
echo Be sure zone.inc is what you need!
echo if zone.inc is not defined then zoneSample.inc is used

PS3='Be sure zone.inc is what you need, and remember that Mzon may be adjusted
 by this script to your model, but *hh toy models need *45* inc files
 hit Enter to see menu again or ctrl-C to stop the script and edit zone.inc
 enter the number from the above menu to choose zone*.inc  and inspect it: '

zoneIncList=($(ls $HOMEStella/src/zone*.inc |awk '{print $1}'))

select CHOICE in ${zoneIncList[*]} Quit
do
    case "$CHOICE" in
    "") echo Be sure zone.inc is what you need, hit Enter to see menu again!
	continue
	;;
    Quit) break			# exit the loop
    	;;
    *)	less -X $CHOICE
	;;
    esac
done
if [ ! -e $HOMEStella/src/zone.inc ]; then
     cp -p $HOMEStella/src/zoneSample.inc $HOMEStella/src/zone.inc
fi
 echo current directory is:
 cd $HOMEStella/modmake
 pwd
 echo '******' `pwd`
Pause
 if [ ! -e zone.inc ]; then
   ln -s $HOMEStella/src/zone.inc .
 fi
 if [ ! -e fundrad.inc ]; then
   ln -s $HOMEStella/src/fundrad.inc .
 fi
 if [ ! -e sahaandd.inc ]; then
   ln -s $HOMEStella/src/sahaandd.inc .
 fi
# The next link is needed if AZZn is outside azdat.trf
#  if [ ! -e azzn.inc ]; then
#    ln -s $HOMEStella/src/azzn.inc .
#  fi

#currently, no processing in modmake, hyd and abn must be already there
#  if [ $KeepModelZones=1 ]
#  then
#    make -f mntomi.mak w7like
#    echo '******'
#    echo xw7like.exe created
#    echo '******'
#    ./xw7like.exe  $InputModel
#  else
#  #if [ ! -e xrtomi.exe ]; then
#    make -f mntomi.mak rtomi
#    echo '******'
#    echo xrtomi.exe created
#    echo '******'
#  #   make -f mntomi.mak clean
#  #fi
# #if [[ ! -e "${RezonedModel}.hyd" || ! -e "${RezonedModel}.abn" ]]; then
#    ./xrtomi.exe  $InputModel $Cutmass $Nkeep $Nmult
# #fi
#  fi
fi

# Prepare to build libraries
 echo '******'
 echo start building libraries
 echo '******'
if [ ! -e $HOMEStella/lib  ]; then
   mkdir $HOMEStella/lib
   echo directory $HOMEStella/lib created
fi

if [ ! -e $HOMEStella/lib/liblnagGF.a  ]; then
   echo current directory is:
   cd $HOMEStella/LNAG
   pwd
   echo '******'
   make -f lnaglibGF.mak
   echo LNAG library created
   make -f lnaglibGF.mak clean
fi

if [ ! -e $HOMEStella/lib/libsparseGF.a  ]; then
   echo current directory is:
   cd $HOMEStella/sparse
   pwd
   echo '******'
   make -f sparselibGF.mak
   echo sparselib library created
   make -f sparselibGF.mak clean
fi

Pause
echo 'check sparselibGF!!!'

######################################
#  NZON


if [ -f $HOMEStella/modmake/${InputModel}.hyd ]
then
    model_name=$HOMEStella/modmake/${InputModel}.hyd
else
    echo "File \"$HOMEStella/modmake/${InputModel}.hyd\" does not exist."
    exit 3
fi

mzon=`sed q $model_name | awk '{print $2}'`
echo Mzon needed:  $mzon
Pause				# invoke the function Pause.

if [ -f $HOMEStella/src/zone.inc ]
then
    inc_name=$HOMEStella/src/zone.inc
else
    echo "File \"$HOMEStella/src/zone.inc\" does not exist."
    exit 4
fi

old_pattern=Mzon=[0-9]*
new_pattern=Mzon=$mzon

echo old_pattern $old_pattern
echo new_pattern $new_pattern


###################################################################
# old_param=`sed -n '/--/!s/Mzon=[0-9]*/&/p' $inc_name`			  #
# new_param="PARAMETER($new_pattern);"							  #
# echo old_param $old_param										  #
# echo new_param $new_param										  #
# 																  #
# 																  #
# if [ "${old_param}" == "${new_param}" ]						  #
# then															  #
#   echo Mzon is not changed									  #
# else															  #
#  echo sed modifies zone.inc									  #
# #  Here is where the heavy work gets done.					  #
# # -----------------------------------------------				  #
#   sed -e "/--/!s/$old_pattern/$new_pattern/" $inc_name > qq.inc #
# # -----------------------------------------------				  #
# #  's' is, of course, the substitute command in sed,			  #
# #  /--/! means except for lines with "--"						  #
# #+ and /pattern/ invokes address matching.					  #
#  mv qq.inc $inc_name											  #
# fi															  #
###################################################################

old_param=`sed -n '/--/!s/Mzon\s*=\s*\d*\b.*/&/p' $inc_name`
new_param=`echo "${old_param}" | sed -e "s/[0-9]\+/${mzon}/" `

echo old_param: "'${old_param}'"
echo new_param: "'${new_param}'"


if [ "${old_param}" == "${new_param}" ]
then
	echo 'Mzon is not changed'
else
	echo 'sed modifies zone.inc'
	sed -e "/--/!s/${old_param}/${new_param}/"  $inc_name > qq.inc
    mv qq.inc $inc_name
fi

Pause				# invoke the function Pause.

# Prepare to build Stella
 echo '******'
 echo start building Stella
 echo '******'
echo Be sure opacity.inc is what you need, if it is not defined opacitySample.inc is used

PS3='Be sure opacity.inc is what you need, it may be adjusted
 by this script to your model, but *hh toy models need *45* inc files
 hit Enter to see menu again or ctrl-C to stop the script and edit opacity.inc
 enter a choice of opacity*.inc from the above menu to inspect it: '

opacityIncList=($(ls $HOMEStella/src/opacity*.inc |awk '{print $1}'))

select CHOICE in ${opacityIncList[*]} Quit
do
    case "$CHOICE" in
    "") echo Be sure opacity.inc is what you need, hit Enter to see menu again!
	continue
	;;
    Quit) break			# exit the loop
    	;;
    *)  less -X $CHOICE
	;;
    esac
done

if [ ! -e $HOMEStella/src/opacity.inc ]; then
     cp -p $HOMEStella/src/opacitySample.inc $HOMEStella/src/opacity.inc
fi

 echo current directory is:
 cd $HOMEStella/obj
 pwd
 echo '******'
if [ ! -e opacity.inc ] || [ ! -e zone.inc ]; then
   rm *.inc
   ln -s $HOMEStella/src/*.inc .
fi

if [ $BuildNewModel == 1 ]
then
	make -f Stellaf90.mak clean
	make -f Stellaf90.mak eve2
#	make -f Stellaf90.mak evehyd
	echo '******'
	echo '****** eve2.exe created'
	echo start building initial model in Stella format
	echo '******'
	echo current directory is:
	cd $HOMEStella/run/eve/
        Pause
	pwd
	echo '******'
	##################################################################
	# if [ -f $HOMEStella/run/eve/eve.1 ]							 #
	# then															 #
	#    mv $HOMEStella/run/eve/eve.1 $HOMEStella/run/eve/eve.1.prev #
	# fi															 #
	# 																 #
	# sed -e "s/testh/${InputModel}/g" evehead.1 > eve.1			 #
	##################################################################
	echo ls -l evehead.1*
	ls -l evehead.1*
        Pause
        if [ ! -e  evehead.1 ]; then
          cp evehead.1.sample evehead.1
        fi
##	fileEve=${HOMEStella}/run/eve/eve.1
	fileEve=eve.1
	echo ls -l $fileEve
	ls -l $fileEve
        echo fileEve $fileEve
        Pause
	if [ -f $fileEve ]
	then
		line=`sed '2!d' evehead.1  | sed -e "s/testh/${InputModel}/g"`
		echo "Insert to ${fileEve} line: ${line} "
		sed  -i "2i ${line}" $fileEve
	else
		sed -e "s/testh/${InputModel}/g" evehead.1 > $fileEve
	fi
	./eve2.exe
##		./eve2.exe ${InputModel}
#	./xevehyd.exe
fi # for BuildNewModel


if [ "$NewOpacity" == 1 ]
then
# Prepare opacity tables for given model
 echo '******'
 echo start making opacity tables
 echo '******'
 echo current directory is:
 cd $HOMEStella/obj
 pwd
 echo '******'
Pause				# invoke the function Pause.

 case "$Composition" in
      'uniform')
            make -f Stellaf90.mak ronfshb
               ;;
      'mixed')
            make -f rparlnx.mak clean
            make -f rparlnx.mak inner
#            make -f Stellaf90.mak ronfict
               ;;
      'OutUniform')
            make -f Stellaf90.mak ronfoutuni
               ;;
 esac
######################################################
#  echo '******'									 #
#  echo stupid make must be repeated for f90 modules #
# Pause												 #
# 													 #
#  case "$Composition" in							 #
#       'uniform')									 #
#             make -f Stellaf90.mak ronfshb			 #
#                ;;									 #
#       'mixed')									 #
#             make -f Stellaf90.mak ronfict			 #
#                ;;									 #
#       'OutUniform')								 #
#             make -f Stellaf90.mak ronfoutuni		 #
#                ;;									 #
#  esac												 #
######################################################
 echo '******'
 echo current directory is:
 cd $HOMEStella/run/vladsf
 pwd
 echo '******'

if [ ! -f $HOMEStella/run/vladsf/lineatom.dat ]
then
#  ln -s $HOMEStella/../StellaMG/OpenStellaM/vladsf/lineatom.dat .
  ln -s $HOMEStella/run/vladsf/lineatom_may07.dat lineatom.dat
fi  

if [ ! -f $HOMEStella/run/vladsf/yakovlev ]
then
  ln -s $HOMEStella/OpenStellaM/vladsf/yakovlev .
fi  


 echo check that  $HOMEStella/run/vladsf/${InputModel}.{1-6,ab} tables are non-zero
 Pause

# if [ ! -f $HOMEStella/run/vladsf/${InputModel}.ab ] # InputModel opacity table do not exist
# then
#
# echo opacity tables must be computed
# Pause


 fileRnf=${HOMEStella}/run/vladsf/ronfict.1
 if [ -f $fileRnf ]
 then
	line=`sed '2!d' ronfhead.1  | sed -e "s/testh/${InputModel}/g"`
	#	echo "Insert to ${fileEve} line: ${line} "
	sed  -i "2i ${line}" $fileRnf
 else
	 #    mv $fileRnf  $fileRnf.prev
	sed -e "s/testh/${InputModel}/g" ronfhead.1 > $fileRnf
 fi


 if [ -f $HOMEStella/run/vladsf/ronf.log ]
 then
    rm $HOMEStella/run/vladsf/ronf.log
 fi

echo Opacity is ready to start
Pause				# invoke the function Pause.

 echo Opacity is starting, watch
 echo  tail -f $HOMEStella/run/vladsf/ronf.log
 echo  and/or:
 echo  tail -f $HOMEStella/run/vladsf/ronfict1.res

 case "$Composition" in
      'uniform')
          nohup  ./xronfshb.exe >& $HOMEStella/run/vladsf/ronf.log
               ;;
      'mixed')
          nohup mpirun -np 6 ./xinsh.exe >& $HOMEStella/run/vladsf/ronf.log
#           nohup nice +20 mpirun -np 6 ./xinsh.exe >& $HOMEStella/run/vladsf/ronf.log # this does not work in bash
#           nohup  ./xronfict.exe >& $HOMEStella/run/vladsf/ronf.log
               ;;
      'OutUniform')
          nohup  ./xronfoutuni.exe >& $HOMEStella/run/vladsf/ronf.log
               ;;
 esac

# fi # for InputModel opacity table check


 echo Opacity done
fi # for NewOpacity

Pause


if [ ! -e $HOMEStella/res  ]; then
   mkdir $HOMEStella/res
   echo directory $HOMEStella/res created
fi

if [ $RunTTfit == 1 ]
then
 make -f Stellaf90.mak ttfit
 cd $HOMEStella/run/strad
 xttfit.exe
 exit
fi

# Make stella executable
 echo '******'
 echo start making Stella executable
 echo '******'
 echo current directory is:
 cd $HOMEStella/obj
 pwd
 echo '******'
 make -f Stellaf90.mak stella7

 echo '******'
 echo current directory is:
 cd $HOMEStella/run/strad
 pwd
 echo '******'
###########################################################################
# if [ -f $HOMEStella/run/strad/strad.1 ]								  #
# then																	  #
#     mv $HOMEStella/run/strad/strad.1 $HOMEStella/run/strad/strad.1.prev #
# fi																	  #
# 																		  #
#  sed -e "s/run/${run}/g" stradheadopa.1 > qq.1						  #
#  sed -e "s/testh/${InputModel}/g" qq.1 > qqq.1						  #
#  sed -e "s/opa/${OpacityTable}/g" qqq.1 > strad.1						  #
###########################################################################


 fileStrad=${HOMEStella}/run/strad/strad.1
 echo fileStrad $fileStrad
 if [ -f $fileStrad ]
 then
   stradfilesize=$(stat --format=%s $fileStrad)
   echo "$stradfilesize"
   minimumsize=100
   if [ $stradfilesize -le $minimumsize ]; then
     echo strad.1 is small size="$stradfilesize"
     cp ${HOMEStella}/run/strad/strad.1.sample $fileStrad
   fi
 else  
   cp ${HOMEStella}/run/strad/strad.1.sample $fileStrad
 fi

 Pause


 if [ -f $fileStrad ]
 then
	 line=`sed '2!d' stradheadopa.1  | sed -e "s/run/${run}/g" -e "s/testh/${InputModel}/g" -e "s/opa/${OpacityTable}/g"`
	 echo "Insert to ${fileStrad} line: ${line} "
	 sed  -i "2i ${line}" $fileStrad
 else
	 sed -e "s/run/${run}/g" stradheadopa.1 > qq.1
	 sed -e "s/testh/${InputModel}/g" qq.1 > qqq.1
	 sed -e "s/opa/${OpacityTable}/g" qqq.1 > $fileStrad
 fi


 if [ -f $HOMEStella/run/strad/st.log ]
 then
     rm $HOMEStella/run/strad/st.log
 fi

 nohup ./xstella7.exe >& st.log &
 echo Stella is started, watch
 echo tail -f $HOMEStella/run/strad/st.log
