/*  BUGS:
>        1.  _leave or _iterate all -- here all is not UPed (ALL)
>            variable VARLV !!! Tue  03-09-1993  01:17:29
>   Fixed 07-10-1995 20:21
> */

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define   _Wcard       if(fprintf(Include[OUTPUT],"%s\n",Outcard)==EOF){ fprintf(stderr,"Writing error (disk full\?)\n");Retcod=3;exit(28);}
#define   _Werror      fprintf(Include[OUTPUT],"CERROR(%4d) Syntactical or Alias error\n", Chln );Retcod=3;

#include "chargen.h"
#include "trfgen.h"
#include "trfcode.h"
#include "align.h"

#define __TUN__

#if !defined(max) && !defined(NOMAX)
extern max(int,int);
#endif


 /*  Variables for Tree of program */
 /*C: variables for WTR */
 static char  Savcar[15]={"               "}, Symcon={_S_CONTINUATION};
static Integer2 /*I34,/* Lnold,--=C */ Wcl,Icont=1;
/*static Integer4 Wln; --=C */
static Integer2 WP,Plst[66]={0,
           1,  0, 0,  3, 3,  2, 2, 10, 11, 12, 17, 13, 0,
           0,  4, 4,  4, 5,  4, 5,  4, 4,  4, 17,  4, 3,
	   9,  6, 6,  8, 9,  9, 9, 10, 11, 12, 17, 14, 0,
           0, 15, 6,  0, 0,  0, 0,  0, 0,  0, 17,  0, 6,
           0, 15, 6,  0, 0,  0, 0,  0, 0,  0, 17,  0, 16};
static Integer2 Wpos=LC,Wstate,Wst[66]={0,
	   2,   1,   0,   1,   1,  3, 3,1, 1, 1,1, 4, 1,
	   2,   1,   0,   1,   3,  1, 3,1, 1, 1,2, 4, 1,
	   3,   1,   0,   3,   3,  3, 3,1, 1, 1,3, 5, 3,
	   4,   4,   0,   4,   4,  4, 4,4, 4, 4,4, 4, 1,
	   5,   5,   0,   5,   5,  5, 5,5, 5, 5,5, 5, 3};
#ifdef __TUN__
#include "pass2dep.h"
#else
static Integer2 WCLASS[2][256]={{
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,11, 2, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
       6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6},{
       3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 2, 6, 8, 9,10, 6,12,13, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 4, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	   6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6}};
static Integer2  CLASS[256]={
   2,   1,   1,   1,   1,   3,   3,   3,   3,   3,   3,   3,
   3,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
  14,  15,  16,  17,  18,  19,  20,  21,  25,  26,   1,  24,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,  22,  23,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,
   1,   1,   1,   1};
#endif
static char /*WDIA[]={"C  TRF000  Syntactical or Alias error  "},  /*  %344324 */
    Fortio[]={"C-->Fortran section begins....         "},  /*  %3443A */
    Trefio[]={"C-->Trefor  section begins....         "},  /*  %3443A */
    Pascio[]={"(*  Pascal  section begins....       *)"}; /*  %3443A */
 /*B: variable for SYNT */
/*   NIZE SIMVOLOM ; OBO3NA4EN SPECKOD @KO (KONEC OPERATORA): */
 Integer2 Ioutlt,Jprog,Out[23][6]={  /*  TXTS */
  16, 1, 0, 0, 0, 0,                /*   1:  IF(.NOT.( */
  16,-1,15, 0, 0, 0,                /*   2:  DO */
   2,-1, 0, 0, 0, 0,                /*  3:  .GT. */
  14,-1, 0, 0, 0, 0,  /*  14a        -- 4:  .LT. */
  16,-3,17, 0, 0, 0,  /*  10a,18a    -- 5:  .GE. */
  12,-1,16, 0, 0, 0,                /*  6:  .LE. */
  16,-1, 0, 0, 0, 0,  /*   8a        -- 7:  .NE. */
  17,-2,17, 0, 0, 0,                /*  8:  .EQ. */
  14,-2,16,-1,17, 0,                /*  9:  .AND. */
  14,-1,16,-2,17, 0,  /*  10         -- 10:  .OR. */
  18,-1, 0, 0, 0, 0,                /*  11:  .NOT. */
  19, 0, 0, 0, 0, 0,  /*  13a        -- 12:  ))GOTO */
  -1,20, 0, 0, 0, 0,                /*  13:  :CONTINUE */
  16,-1,17, 0, 0, 0,                /*  14:  ;GOTO */
  16, 0, 0, 0, 0, 0,  /*  15         -- 15:  :IF(.NOT.( */
  12,-2,16, 0, 0, 0,                /*  16:  ; */
  -1,17, 0, 0, 0, 0,                /*  17:  :CONTINUE; */
  14,-1,16, 0, 0, 0,                /*  18:  GOTO */
  16,-2,17, 0, 0, 0,                /*  19:  GOTO( */
  12,-1,16,-2,17, 0,  /*  20         -- 20:  , */
  16,-3,13, 0, 0, 0,                /*  21:  ), */
  12,-1, 0, 0, 0, 0,                /*  22:  : */
   0, 0, 0, 0, 0, 0};               /*  23    THIS LINE CANNOT BE USED */
/*static Integer2 Crko; --=C */
/*static char lcrko[2];
 Equivalence (Crko,Lcrko);*/
 static char TXTS[61]={':','I','F','(','.','N','O','T','.','(',
		      'D','O','.','G','T','.','L','T','.','G',
		      'E','.','L','E','.','N','E','.','E','Q',
		      '.','A','N','D','.','O','R','.',')',')',
		      'G','O','T','O',':','C','O','N','T','I',
		      'N','U','E','$','G','O','T','O','(',')',','};
 Integer2 TBEG[22]={ 2,11,13,16,19,22,25,28,31,35,
		     5,39,45,54,1,54,45,55,55,61,60,45};
 Integer2 TLNG[22]={9,2,4,4,4,4,4,4,5,4,
		    5,6,9,5,10,1,10,4,5,1,2,1};   /* %3315 */
 Integer4 Remlab,LabSel,CurLab;  /*  %3312 */
 Integer2 Sclass,Spred,Cstack,Sprog,Nsel,Nc,Icase,Nproc;   /*  %331 */
 Integer2 Sprg[390]={
 /*    WA DO IF TH EL WH WD CS RP UN SL OT WDU PROC A[ */
       5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,  5,   5,/*  REST */
       5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,  5,   5,/*  KT */
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  4,   4,/*  <>^=... */
       3, 3, 0, 3, 3,18, 3, 3, 3, 0, 3, 3, 0,  3,   3,/*  _DO */
       0, 8, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0,  0,   0,/*  _OD */
       1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0,  1,   1,/*  _ if */
       0, 0, 0,13,13, 0, 0, 0, 0, 0, 0, 0, 0,  0,   0,/*  _ fi */
       0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,   0,/*  _ then */
       0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,   0,/*  _ else */
       2, 2, 0, 2, 2, 0, 2, 2, 2, 0, 2, 2, 0,  2,   2,/*  _WHILE */
       0,11, 0,11,11, 0,11,11,11, 0,11,11, 0,  0,   0,/*  _LEAVE */
       0,12, 0,12,12, 0,12,12,12, 0,12,12, 0,  0,   0,/*  _ITERATE */
      14,14, 0,14,14, 0,14,14,14, 0,14,14, 0, 14,  14,/*  _CASE */
       0, 0, 0, 0, 0, 0, 0,17, 0, 0, 0, 0, 0,  0,   0,/*  _OF */
       0, 0, 0, 0, 0, 0, 0,15, 0, 0, 1, 0, 0,  0,   0,/*  _LABELS */
       0, 0, 0, 0, 0, 0, 0,13, 0, 0, 0, 0, 0,  0,   0,/*  _ESAC */
      19,19, 0,19,19, 0,19,19,19, 0,19,19, 0, 19,  19,/*  _REPEAT */
       0, 0, 0, 0, 0, 0,23, 0,23, 0, 0, 0, 0,  0,   0,/*  _UNTIL */
      24,24, 0,24,24, 0,24,24,24, 0,24,24, 0, 24,  24,/*  _SELECT */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,21, 0, 0,  0,   0,/*  _OTHER */
       7, 7, 7, 7, 7, 7, 7,13, 7, 7,13,13, 7,  7,   7,/*  _END */
       0,17,31,17,17,30,17, 0,21, 0,31,21, 0,  0,   0,/*  [ */
      32, 8, 0,13,13, 0,10, 0,20, 0,25,21, 0, 32,  29,/*  ] */
       5, 5, 5, 5, 5, 5, 5, 5, 5,27, 5, 5,26,  5,   5,/*  KO */
      28,28, 0,28,28, 0,28,28,28, 0,28,28, 0, 28,  28,/*  _PROC */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16,  0};/*  _RETURN */
 /*    WA DO IF TH EL WH WD CS RP UN SL OT WDU PROC A[ */
 Integer2 Cstk[390]={
 /*    WA DO IF TH EL WH WD CS RP UN SL OT WDU PRC A[ */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  REST */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  KT */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  <>^=... */
       2, 2, 0, 2, 2, 7, 2, 2, 2, 0, 2, 2, 0,  2, 2,/*  _DO */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _OD */
       3, 3, 0, 3, 3, 0, 3, 3, 3, 0, 3, 3, 0,  3, 3,/*  _ if */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ fi */
       0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ then */
       0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ else */
       6, 6, 0, 6, 6, 0, 6, 6, 6, 0, 6, 6, 0,  6, 6,/*  _WHILE */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _LEAVE */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ITERATE */
       8, 8, 0, 8, 8, 0, 8, 8, 8, 0, 8, 8, 0,  8, 8,/*  _CASE */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _OF */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _LABELS */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ESAC */
       9, 9, 0, 9, 9, 0, 9, 9, 9, 0, 9, 9, 0,  9, 9,/*  _REPEAT */
       0, 0, 0, 0, 0, 0,13, 0,10, 0, 0, 0, 0,  0, 0,/*  _UNTIL */
      11,11, 0,11,11, 0,11,11,11, 0,11,11, 0, 11,11,/*  _SELECT */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,12, 0, 0,  0, 0,/*  _OTHER */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _END */
       0, 0, 4, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  [ */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  ] AS */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  KO */
      14,14, 0,14,14, 0,14,14,14, 0,14,14, 0, 14,14,/*  _PROC */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,0};/*  _RETURN */
 /*    WA DO IF TH EL WH WD CS RP UN SL OT WDU PRC A[ */
 Integer2 Sprd[390]={
 /*    WA DO IF TH EL WH WD CS RP UN SL OT WDU PRC A[ */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  REST */
       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  2, 2,/*  KT */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  <>^=... */
       1, 1, 0, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0,  1, 1,/*  _DO */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _OD */
       1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0,  1, 1,/*  _ if */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ fi */
       0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ then */
       0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ else */
       1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0,  1, 1,/*  _WHILE */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _LEAVE */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ITERATE */
       3, 3, 0, 3, 3, 0, 3, 3, 3, 0, 3, 3, 0,  3, 3,/*  _CASE */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _OF */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _LABELS */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _ESAC */
       1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0,  1, 1,/*  _REPEAT */
       0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0,  0, 0,/*  _UNTIL */
       3, 3, 0, 3, 3, 0, 3, 3, 3, 0, 3, 3, 0,  3, 3,/*  _SELECT */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0,  0, 0,/*  _OTHER */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  _END */
       0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  [ AS ; */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,/*  ] */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,  0, 0,/*  KO */
       1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0,  1, 1,/*  _PROC */
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0};/*  _RETURN */
 /*    WA DO IF TH EL WH WD CS RP UN SL OT WDU PRC A[ */
static Integer2 Blab,Numtxt=0;
static Integer2 ITXT,CTXT;        /*   %33142 */
 static char Foundo;
 static ALL[3]={'A','L','L'},VARLV[LC];              /*   %3344B */
static Integer2 LoopSt[NDOMAX],Leave[NDOMAX],Pvardo[NDOMAX],
	   Iter[NDOMAX],State[NSTATEMAX],Labs[NSTATEMAX],
	   Ssptr,Sloop,Cvardo;
 static Integer2 Stproc[PROCMAX],Cproc,i2,i3;
 static char VARDO[NDOMAX];
 static Integer2 Ido=0;
 static Integer2 Lcurdo=0;
 /*1: Common variables for coroutines COMPS,SYNT,WTR */

 static unsigned Integer2 Cs,Sw, /*  SIMVOLY D/OBMENA COMPS-SYNT,SYNT-WTR; */
    Chln;     /*  TEKUQIY HOMEP STROKI 3AGOLOVKA U3LA */
 static Integer2 Comps,Synt,RetWtr; /*  UPRAVLJWQIE PEREMENNYE SOPROGRAMM */
 static Integer2 Spec; /*  1 for ordinary , 2 for special trefor symbols */
 static Integer4  Posold; /*  old position in Outcard */
 static Integer2 Wdig;  /*  for coding the digits */
 static  char Outcard[LC+2];
 static  char Blank6[]="      " ;
 static  char Fort, /*  Fortran format I/O */
              Waitbr; /*  Wait left bracket in if( _while _select */
 /*A: variables for Comps */
 static Integer4 Cnsymb,Pnsymb[STNODE];
 static unsigned Integer2 Cason,Csymb,Pason[STNODE],Psptr;
 static Integer2 Ilind,Nlind,Nind,Reqln;
 /*static Integer2 CKY;*/
 static char Lindt[LC];
 /*Z: variables for ALIAS */
 static Integer4 Ltextd;
 static Integer4  Lalias,
           Pathal;
 static Integer4  Csals,
           Cdef,      /*  Current ALIAS wanted number */
           Cndef,     /*  Current ALIAS definition number */
           Csdef,      /*  work var */
           Stals,      /*  open alias stack */
           Tstals,
           Stpal[STALS],  /*  stack for Pathal */
           Stdefa[STALS], /*  stack for Cdef */
           Jp7,Kp7;
 static char Alias[LC];
 static char Founda,Recals;
 static int Isprog,Nloop,Ncall,ISTATE;

#include "tree.h"

#define CallOutLT(lab) OutLTret=lab; goto OutLT ; LabOutLT##lab: ;
#define Case(lab)      case lab : goto LabOutLT##lab ;
static OutLTret;

/*	Clear remnant & output CARD */
void static Putcard(void){
  if( Posold>=Wpos )
    memset(Outcard+Wpos,' ',Posold-Wpos+1);
  Posold=Wpos-1;
//seb  Outcard[Wpos+1]=0;
  Outcard[Wpos]=0;
  _Wcard;
  Wpos=0;
}

void pass2();

void pass2(){
   /*3: VTOROY PROHOD. PO TREE POSTROIT@ VYHODNOY TEKCT HA FORTRANE*/
 Comps=1; Synt=1;  /*  _NEW(Comps)(Synt) */
 RetWtr=2;    /*  Return from WRITER TO Synt */
 Spec=1; Wpos=0;
 #ifdef _DEBUG_TRF_
 {
 FILE *aa;
 aa=fopen("b.b","w");
 fwrite(text,40000U,1,aa);
 fclose(aa);
 }
 #endif
 Fort=0;
 /* Crko=_Cr; --=C */
 memset(Outcard,' ',LC);
 TXTS[53]=_Cr;
 goto LabWriter_init;
 LabComps:
  switch(Comps){
   case 1 : goto Lab2001 ;
   case 2 : goto Lab2002 ;
   case 3 : goto Lab2003 ;
  }
 Lab2001:;
   /*2:SOPROGRAMMA Comps. SOBIRAET DEREVO TREE B TEKCT STRUKTURIROVAN.
       FORTRANA, VYDAET POSIMVOL@NO B Synt, B KONCE VYDAET @Kt */
 /* VAR VYDTEKST, PUT@ (Cnsymb,Cason,Csymb,MCSYM,
     PNSYMB(@Stnode),Pason(@Stnode) Psptr - CM.%3A).
     VAR CNODINF - INFORMACIJ O SOSTOJNII PROSMOTRA TEKUQEGO U3LA.
     VAR PATHSTACK - CTEK INFORMACII O SOSTOJNII PROSMOTRA U3LOV
       HA PUTI OT TEKUQEGO K KORNW.
     INT Cnsymb - HOMEP PERVOGO PODLEZAQEGO PROSMOTRU SIMVOLA.
     INT*2 Cason,Csymb - INDEKS PERVOGO PODLEZAQEGO PROSMOTRU NASLEDNOGO
    U3LA , 3NA4ENIE SIMVOLA, HA KOTORYY UKA3YVAET PUT@.
     USLOVIE Q32:
       PUT@ RA3RE3AET DEREVO TEKCTOB HA DVE POLOVINY .
       LEVAJ i3 NIH SOOTVETSVUET TEKSTU , VYDANNOMU B VYDTEKST,
       A PUT@ UKA3YVAET HA PERVYY SIMVOL i3 PRAVOY POLOVINY. */
 /*2: SDELAT@ Q32 ISTINNYM PRI PUT@,UKA3.HA 1-Y SIMV.KORNEVOGO U3LA*/
 Cnsymb=0; Cason=2; Chln=0; Psptr=0;
 Csymb=text[0];/* ML.BAYT Csymb */
 while( /*3: PUT@ HE UKA3YVAET HA @Ky KORNEVOGO U3LA*/
   Psptr!=0 || Csymb!=_Attention || text[Cnsymb+1]!=_Ky
 ) {
   /*4: UMEN@6IT@ POLOVINU DEREVA SPRAVA OT PUT@ PRI INV Q32 */
 if( Csymb==_Attention)  {
    Cnsymb=Cnsymb+1; Csymb=text[Cnsymb];/*  Next symbol in Csymb */
    switch( Csymb ) {
          default : Cs=Csymb; Comps=2; RetWtr=2; goto LabSynt;
          case 1 :
            /*KY: VYYTI i3 U3LA,T.K. OH HE KORNEVOY(i3-3A 3AGOL.CIKLA) */
 /*  U3EL HE KORNEVOY, SLED.Psptr^=0 */
 Cnsymb=Pnsymb[Psptr]; Cason=Pason[Psptr]+1; Psptr=Psptr-1;
 /*1: VOSSTANOVIT@ Chln */
 if( Psptr==0 ) {  Chln=0 ; }
 else { Chln=Pason[Psptr]; Chln=Headln[Chln]; }
          break;
          case 2 :
	      /*TR: OBRABOTAT@ TREBOVANIE,TO EST@ NA4AT@ OBRABOTKU
              NASLEDNOGO U3LA,ILI VYDAT@ SOOBQENIE OB EGO OTSUTSTVII*/
 if( Atext[Cason]==0 )  {
   /*1: VYDAT@ DIAGNOSTIKU, ISPOL@3UJ(LIND I Headln)(Cason) */
 /*  INT Ilind,Reqln; LOG Slind(@EqByte):=:Ilind.  CM %3A */
 Reqln=Headln[Cason]; Nlind=Plind[Cason]; Nind=0;
 while( Nlind+Nind<Plind[Cason+1] && Nind<LC ) {
    Ilind=Lind[Nlind+Nind];
    Nind=Nind+1;
    Lindt[Nind]=Ilind;
 }
 fprintf(stderr," No design for the NODE requested in"
    " line:%4d Node number:%3d  with local index: ",Reqln,Cason);
 fprintf(Include[LISTING]," No design for the NODE requested in"
    " line:%4d Node number:%3d  with local index: ",Reqln,Cason);
 {int i;
     for(i=1;i<=Nind;++i)
        {
         fputc(Lindt[i],stderr);
         fputc(Lindt[i],Include[LISTING]);
	}
  }
 fprintf(stderr," \n");
 fprintf(Include[LISTING]," \n");
 Retcod=max(Retcod,2);

   Cason=Cason+1;
 } else {
   /*2: Cnsymb I Cason B CTEK,B Chln-Headln(Cason),B Cnsymb I Cason ADR:
    0-GO SIMVOLA I 1-GO NASL.U3LA K U3LU,TREBOVANIE HA K-RYY DOSTIGN.*/
 Chln=Headln[Cason]; Psptr=Psptr+1;
 Pnsymb[Psptr]=Cnsymb; Pason[Psptr]=Cason;
 Cnsymb=Atext[Cason]-1; Cason=Ason[Cason];

  }
          break;
          case 3 :
                /*DEF: Skip over _define region according to 4 bytes after
                @define, which keep address of the transition in the
                TEXT */
  #ifndef ALLIGN
    Ltextd=*(Integer4 *)&text[Cnsymb+1];
  #else
    memcpy((char*)(&Ltextd),(char*)(text+Cnsymb+1),4);
  #endif
  Cnsymb=Ltextd-1; /*  Posald equ. Ltextd */
          break;
          case 4 :
               /*ALS: Process alias Name, i.e. find it in alias table TABALS
                and construct ALIAS TREE with all its SONs */
  /* Var INT Pathal
  Log Founda  - found alias
     Invariant Q_ALS: ( Founda &
       Pathal divides the tree of alias generated text into 2 parts:
       Left part corresponds to output text,
       Pathal points to 1-st symbol of the right part ) or ^Founda */
 /*1: make Q_ALS true, when Pathal points to 1-st symbol of definition
      of the root alias and Cnsymb points to the ENDSIGN of this alias */
  Recals=0;  /*  Recursion in Alias */
  /*1: Accumulate alias name ALIAS() */
  #ifndef ALLIGN
   Alsprc=*(Integer2 *)&text[Cnsymb+1];
  #else
    memcpy((char*)(&Alsprc),(char*)(text+Cnsymb+1),2);
  #endif
   Cnsymb+=2;
  Lalias=0;
  Cnsymb=Cnsymb+1; Csymb=text[Cnsymb];
  while( Csymb!=_S_Blank && Lalias < LC ){
    Lalias=Lalias+1; Alias[Lalias]=Csymb;
    Cnsymb=Cnsymb+1; Csymb=text[Cnsymb];
  }

  /*2: Scan TABALS upward using ALPRED and find Cdef of ALIAS in
       TABALS, then Founda=1 else Founda=0 */
 Csdef=Alsprc; Founda=0;
 while( Csdef > 0 && !Founda ) {
   Cdef=Csdef;
   if( Lalias==Palias[Cdef+1]-Palias[Cdef])  {
       /*1: SET Founda=1 IF ALIAS()=Nalias() */
   /*Jp7=-1; Founda=1;*/
   Kp7=Palias[Cdef];
   Founda=!memcmp(Alias+1,Nalias+Kp7,Lalias);
              /* while (Jp7<Lalias) & Founda ){
                Jp7=Jp7+1;
                if(Alias[Jp7]!=Nalias(Kp7)) Founda=0;
                 Kp7=Kp7+1;
                } */
    }
   Csdef=Alpred[Cdef];
 }

  if( Founda ) {
    Stals=0;   /*  open alias stack */
    Cndef=Cdef;   /*  current Ndef */
    Pathal=Talbeg[Cndef];
   } ;

 while( (Stals!=0 || Pathal!=Talfin[Cndef] /*2:Pathal does not point to TALFIN (of the root alias)*/)
 && Founda ) {
     /*3: reduce the part of alias tree to the right of Pathal for
          invariant  Q_ALS */
    Csals=text[Pathal];

       if(Pathal==Talfin[Cndef] ) {
       /*1: return from alias */
 Cndef=Stdefa[Stals];
 Pathal=Stpal[Stals];
 Stals=Stals-1;

       } else
       if( Csals==_Attention )   { Pathal=Pathal+1;
                                 Csals=text[Pathal];
                                 if( Csals==_Calias )   {
                                  /*2:process son of current alias*/
  /*1: Accumulate alias name ALIAS() */
  Lalias=0;
  Pathal++; Csymb=text[Pathal];
  while( Csymb!=_S_Blank && Lalias < LC ){
    Lalias=Lalias+1; Alias[Lalias]=Csymb;
    Pathal=Pathal+1; Csymb=text[Pathal];
  }
  /*2: Scan TABALS upward using ALPRED and find Cdef of ALIAS in
       TABALS, then Founda=1 else Founda=0 */
 Csdef=Alsprc; Founda=0;
 while( Csdef > 0 && !Founda ) {
   Cdef=Csdef;
   if( Lalias==Palias[Cdef+1]-Palias[Cdef])  {
       /*1: SET Founda=1 IF ALIAS()=Nalias() */
   /*Jp7=-1; Founda=1;*/ Kp7=Palias[Cdef];
    Founda=!memcmp(Alias+1,&Nalias[Kp7],Lalias);
            /* while( (Jp7<Lalias) && Founda ){
              Jp7=Jp7+1;
              if(ALIAS[Jp7]!=Nalias[Kp7]) Founda=0;
              Kp7=Kp7+1;
             } */
   }
   Csdef=Alpred[Cdef];
 }
  if( Founda )  {
    /*3: put Pathal and Cndef into stack, Cndef:=Cdef,
  Pathal:= zeroth symbol of alias number Cdef */
  Stals=Stals+1;
  Stpal[Stals]=Pathal;
  Stdefa[Stals]=Cndef;
  Cndef=Cdef;
  Pathal=Talbeg[Cndef]-1;
  /*Rec: test on recursion in alias definition */
  Tstals=Stals; Recals=0;
   while ( Tstals>0 && !Recals ){
     if( Stdefa[Tstals]==Cdef ) {
       Recals=1; Founda=0;
     }
     Tstals=Tstals-1;
   }
  }

                                 } else {
                                  Cs=Csals;Comps=3;RetWtr=2;goto LabSynt;
                                  }
   }
       else {  Sw=Csals;Comps=3;RetWtr=1;goto LabWriter ; }

Lab2003:; Pathal=Pathal+1;

 }
 if( !Founda )  {
   /*4: error message: in node CNODE alias not found */
 if( Recals )  {
   fprintf(Include[LISTING],"In NODE beginning in line:%d recursion in ALIAS @%s\n",Chln,
    Alias+1);
   fprintf(stderr,"In NODE beginning in line:%d recursion in ALIAS @%s\n",Chln,
    Alias+1);
 } else {
   fprintf(stderr,"In NODE beginning in line:%d not defined ALIAS @%s\n",Chln,
    Alias+1);
   fprintf(Include[LISTING],"In NODE beginning in line:%d not defined ALIAS @%s\n",Chln,
    Alias+1);
  }
 Comps=2; RetWtr=2; goto LabPerror; /*  return through Synt */
  }

	  break;
    }
  } else {
    Sw=Csymb; Comps=2; RetWtr=1;goto LabWriter;
  }
 Lab2002: ;
 /*3: PEREYTI K SLED.SIMVOLU B TEKCTE TEKUQEGO U3LA */
 Cnsymb=Cnsymb+1; Csymb=text[Cnsymb];
 }
 Cs=_Kt;
 goto LabSynt; /*  RESUME Synt -VO3VRATA HE BUDET */
 LabSynt:;
  switch(Synt){
   case 1 : goto Lab3001 ;
   case 2 : goto Lab3002 ;
   case 3 : goto Lab3003 ;
   case 4 : goto Lab3004 ;
   case 5 : goto Lab3005 ;
   case 6 : goto Lab3006 ;
   case 7 : goto Lab3007 ;
   case 8 : goto Lab3008 ;
   default : goto Lab3001 ;
  }

   /********************* _proc outlt ************************************/
   OutLT:;
   Ioutlt=1; Numtxt=Out[Jprog][0];
   while( Numtxt!=0 ){
     if( Numtxt>0 ) {
        /*txt: output txt(Numtxt) */
       ITXT=TBEG[Numtxt-1]-1; CTXT=TLNG[Numtxt-1];  /*  Outtxt */
       while( CTXT>0 ) {
          Sw=TXTS[ITXT];Synt=4; goto LabWriter;
          Lab3004:; /*  RESUME WTR */
          CTXT=CTXT-1; ITXT=ITXT+1;
       }

     } else {
        /*lab: output Labs(Ssptr)+Numtxt+1 */
       int Ilab;
       Ilab=0; Remlab=Labs[Ssptr]+Numtxt+1;
       while( Ilab < 5 ){
         Ilab=Ilab+1;Sw=Remlab/10000;
         Remlab=(Remlab%10000)*10;Sw=Sw+'0';
         Synt=3; goto LabWriter;
         Lab3003: ;   /*  RESUME WTR */
       }

      }
     Numtxt=Out[Jprog][Ioutlt]; Ioutlt++;
   }
   switch(OutLTret){
    Case(1);Case(2);Case(3);Case(4);Case(5);Case(6);Case(7);Case(8);Case(9);
    Case(10);Case(11);Case(12);Case(13);Case(14);Case(15);Case(16);Case(17);
    Case(18);Case(19);Case(20);Case(21);Case(22);Case(23);Case(24);Case(25);
    Case(26);Case(27);Case(28);Case(29);Case(30);Case(31);Case(32);Case(33);
    Case(34);Case(35);Case(36);Case(37);Case(38);Case(39);
    default : fprintf(stderr,"Error in OutLT %d\n",OutLTret);exit(1);
   }
/********************* end of _proc outlt ************************************/
 Lab3001: ;
   /*3: SOPROGRAMMA Synt. POLU4AET TEKCT i3 Comps,ANALI3IRUET TEKCT
        HA STRUKTURIROVANNOM FORTRANE. RAS6IRJET KOHCTPUKCII
        _WHILE,if(,_DO,_ITERATE,_LEAVE,_CASE,_OF,_ESAC,_REPEAT,_UNTIL,
        [,] I SPECKODY OTNO6ENIY. VYDAET FORTRAN
        C RA3DELITELJMI METKI I OPERATORA(':' I @Ko).
        B KONCE VYDAET @Kt */
 /*1: PEREMENNYE I PROCEDURY DLJ Synt */
 /*  CTEK:State(@nstatemax),Labs(@nstatemax),Ssptr; */
 /*  PEREMENNAJ Llab DLJ GENERACII METOK; */
 /*  PEREMENNYE DLJ ABTOMATA: Sclass,Spred,Cstack,Sprog.  CM.%3B */
 /*2: USTANOVIT@ NA4AL@NOE SOSTOJNIE CTEKA I DR.PEREMENNYH */
       Ssptr=1; State[1]=1; /*  State: INITIAL */
       Cvardo=1;
       Pvardo[1]=1;
       Ido=0;
       Cproc=0;
 while( State[Ssptr] != 0 /*3:HA VER6INE CTEKA HE SOSTOJNIE @KT */ ) {
   Synt=2; goto LabComps;
   Lab3002:;  /*  RESUME Comps */
   /*4: TAKT RABOTY Synt C VHODNYM SIMVOLOM Cs */
      /*1: POLU4IT@ B Sclass KLASS SIMVOLA Cs */
      Sclass=CLASS[Cs];
 /*2: RASPAKOVAT@ KLETKU TSYNT,COOTB.COCT.HA CTEKE I KLASSU Sclass,
      B PEREMENNYE Spred,Cstack,Sprog */
      Isprog=(Sclass-1)*15+State[Ssptr]-1;
      Sprog=Sprg[Isprog];Cstack=Cstk[Isprog];Spred=Sprd[Isprog];
 /*3: VYPOLNIT@ PODPROG.,COOTB.Spred, ISPOL@3UJ Cstack */
      switch( Spred ){
        case 1 : /*1: PORODIT@ 3 METKI, 3ANESTI IH I Cstack HA VER6INU CTEKA */
            Ssptr=Ssptr+1; State[Ssptr]=Cstack;
            Labs[Ssptr]=Llab; Llab=Llab-3; break;
        case 2 : State[Ssptr]=Cstack;  /*  3AMENA STEKOVOGO SOSTOJNIJ */ break;
        case 3 : Ssptr=Ssptr+1; State[Ssptr]=Cstack; break ;
      }
 /*4: VYPOLNIT@ CEMAHT. PODPROG. Sprog */
 switch( Sprog ) {
     default:
     LabPerror:;/*0:output B WTR SPECKOD @Er, Spec=2 */
        Sw=_Er;Numerr=Numerr+1;Synt=5;Spec=2; goto LabWriter;
       case 1 : /*1: output ";IF(.NOT.(", wait L_Bracket  */
	Jprog=0; CallOutLT(1); Waitbr=1; if(Fort) Plst[33]=20;
	 break;
	   case 2 : /*2: process WHILE: loop stack,
			output ";LAB1:IF(.NOT.(", wait L_Bracket  */
			Ido=Ido+1; LoopSt[Ido]=Ssptr; Leave[Ido]=0; Iter[Ido]=0;
			Pvardo[Ido+1]=Cvardo;
	    Jprog=1; CallOutLT(2); Waitbr=1; if(Fort) Plst[33]=20; break;
	   case 3 : /*3: process DO: output"DO LAB1", prepare Pvardo(),Vardo() */
			Ido=Ido+1; LoopSt[Ido]=Ssptr; Leave[Ido]=0; Iter[Ido]=0;
	    Jprog=2; CallOutLT(3);
	    Cnsymb=Cnsymb+1; Sw=text[Cnsymb];
	    while( isalnum(Sw) ) /* Digit or Letter */ {
	       VARDO[Cvardo]=ToUpper(Sw); /* --=2 Add ToUpper */ 
	       Cvardo=Cvardo+1;
	       Synt=8; goto LabWriter;
	       Lab3008:   Cnsymb=Cnsymb+1; Sw=text[Cnsymb];
			}
			Pvardo[Ido+1]=Cvardo;
	    Cnsymb=Cnsymb-1; /*  repeat last symbol in @Comps; */
			break;
       case 4 : /*4: output TXST(Cs-2) where Cs-2 is the code for
			relation or logical operation */
	    Jprog=22; Out[Jprog][0]=Cs-2; CallOutLT(4); break;
       case 5 : /*5: output Cs, set Spec=2 */
	    Sw=Cs; Synt=5; Spec=2; goto LabWriter;  /*  RESUME WTR */
	   case 6 : /*6:output(TEXT(12),LAB1,TEXT(16)) */
	    Jprog=5; CallOutLT(5) ; Waitbr=0; if(Fort) Plst[33]=9; break;
	   case 7 : /*7:output(@Er,@KT) */
	    Synt=6; Sw=_Er; Numerr=Numerr+1; Spec=2; goto LabWriter;
	    Lab3006: Synt=5; Sw=Cs; Spec=2; goto LabWriter;
	   case 8 : /*8:output(TEXT(16),LAB1,TEXT(13)); */
	    Jprog=6; CallOutLT(6);
	    Jprog=7;
			if( Leave[Ido]!=0 ) {		 /*  Do current Loop */
	      Out[Jprog][1]=-2;        /*  contain _Leave ? */
			} else {
	      Out[Jprog][1]=0;      /*  No */
			}
			Cvardo=Pvardo[Ido]; Ido=Ido-1;
			CallOutLT(7);
			Ssptr=Ssptr-1; break ;
	   case 9 : /*9:output(TEXT(14),LAB2,TEXT(16),LAB1,TEXT(17)); LAB1:=LAB2 */
	    Jprog=8; CallOutLT(8);
			Labs[Ssptr]=Labs[Ssptr]-1;
			break;
	   case 10: /*10:output(TEXT(14),LAB1);LAB2:CONTINUE */
	    if( Iter[Ido]!=0 )  {    /*  Generate Lab3:Continue; */
		Jprog=4; CallOutLT(9);
			}
	    Jprog=9; CallOutLT(10);
			Cvardo=Pvardo[Ido]; Ido=Ido-1; Ssptr=Ssptr-1;break;
	   case 11: /*11: process LEAVE   */
			Blab=1;   /*  Set Flag for LAB2 */
			Lab5051:
	     if(Ido==0) goto LabPerror;
	     Jprog=10;
			 /*1: GET VARLV, Lcurdo - LENGTH OF VARLV */
		  Cnsymb=Cnsymb+1; Cs=text[Cnsymb];
				  Lcurdo=0;
		  while( isalnum(Cs) ) {
					 Lcurdo=Lcurdo+1;
		     Cs=ToUpper(Cs); /* --=2 add ToUpper */
		     VARLV[Lcurdo]=Cs;
		     Cnsymb=Cnsymb+1; Cs=text[Cnsymb];
				  }
	    Cnsymb=Cnsymb-1;
	     if(  Lcurdo==0 ) { Nloop=Ido ;} /*  Current Loop Level */
	     else if( Lcurdo==3 && VARLV[1]==ALL[0] && VARLV[2]==ALL[1]
			     && VARLV[3]==ALL[2] ) { Nloop=1; } /*  Leave all */
			 else {
				 /*2: FIND NLoop: GOTO @Perror if not found */
	    Nloop=-1; Foundo=0;
	    while( Nloop<Ido && !Foundo ) {
		 Nloop=Nloop+1;
		 if( Pvardo[Nloop+1]-Pvardo[Nloop]==Lcurdo ) {
		     Jp7=0;Foundo=1; Kp7=Pvardo[Nloop];
		     while ( Jp7<Lcurdo && Foundo ) {
			 Jp7=Jp7+1;
			 if(VARLV[Jp7]!=VARDO[Kp7]) Foundo=0;
			 Kp7=Kp7+1;
					 }
				  }
			}
			if( !Foundo )  {
			  fprintf(Include[LISTING]," In NODE beginning in line:%4d LEAVE or ITERATE "
			      "failed for: ",Chln);
			  fprintf(stderr," In NODE beginning in line:%4d LEAVE or ITERATE "
			      "failed for: ",Chln);
			  { int i; for(i=1;i<Lcurdo;++i) {
		 fputc(VARLV[i],Include[LISTING]);
		 fputc(VARLV[i],stderr);
				}
		 fputc('\n',Include[LISTING]);
		 fputc('\n',stderr);
			  }
			  goto LabPerror ;
			 }

			 }
	     Sloop=LoopSt[Nloop];  /*  State of found Loop, Integer */
	     if( Blab==1 ){
	       Leave[Nloop]=Nloop; /*  Stack for _Leave */
			 } else {
	       Iter[Nloop]=Nloop;  /*  Stack for _Iterate */
	       if(State[Sloop]==2) Blab=0;  /*  Exception done for DO LOOP */
	     }
	     Ssptr++; Labs[Ssptr]=Labs[Sloop]-Blab;
			 CallOutLT(11);
	     Ssptr--; break;
	   case 12: /*12: process ITERATE */
			 Blab=2;	/*	Set Flag for LAB3 */
			 goto Lab5051;	  /*  Entry to Find Nloop to be Iterated */
	   case 13:
	     Jprog=13; CallOutLT(12); Ssptr=Ssptr-1; break;
	   case 14: /*D: P14: INICIALI3ACIJ CASE */
	     Cnsymb=Cnsymb+1; Csymb=text[Cnsymb];Nc=Csymb;/*  NCASE */
	     Jprog=11; CallOutLT(13);
             CurLab=Llab;Icase=0;
             Llab=Llab-Nc;
             Ssptr=Ssptr+2*Nc;   /*  TOP of CASE stack */
             State[Ssptr]=Cstack;Labs[Ssptr]=Llab;  Ssptr--;
             Jprog=12;
             while( Icase<Nc ) {
	       State[Ssptr]=Cstack;Labs[Ssptr]=CurLab;
               if(Icase==Nc-1) Out[Jprog][1]=21;
			   CallOutLT(14);
               CurLab=CurLab-1; Ssptr=Ssptr-1;
               State[Ssptr]=Cstack;Labs[Ssptr]=Llab;   Ssptr=Ssptr-1;
               Icase=Icase+1;
			 }
             Out[Jprog][1]=20;
             Ssptr=Ssptr+2*Nc+1;  /*  TOP of CASE stack */
             Llab=Llab-1; break;
	   case 15: /*E: P15: output ;GOTOLABST;LABST: */
             Jprog=3; CallOutLT(15);
			 Ssptr=Ssptr-1;
             Jprog=13; CallOutLT(16);
			 Ssptr=Ssptr-1; break ;
	   case 16: /*T: P16: [19],retlab....[21],Lab1,[16] */
             Nproc=Stproc[Cproc]; Cproc=Cproc-1;
             Ncall=Nc1st[Nproc];
             Jprog=11; CallOutLT(38);
             Ssptr++;
	     Jprog=12;
             while( Ncall!=0 ) {
               Labs[Ssptr]=Retlab[Ncall];
               if(Nextc[Ncall]==0) Out[Jprog][1]=21;
			   CallOutLT(17);
               Ncall=Nextc[Ncall];
			 }
             Out[Jprog][1]=20;
             Ssptr--;
	      i2=6;
	      while( Nproc!=0 ) {
		i2=i2-1;
		Wdig=(Nproc%10)+'0';
		Retrt[i2]=Wdig;
		Nproc=Nproc/10;
			  }
	     if( i2>3 ) {
	       for( i3=3;i3<i2;++i3) Retrt[i3]='0';
			 }
	     i2=0;
	      while( i2<6 ) {
		Sw=Retrt[i2];
		i2=i2+1;
		Synt=7; goto LabWriter;
				Lab3007:;
			  }
             Jprog=13; CallOutLT(18);
			 Ssptr=Ssptr-1; break;
	   case 17: /*F: P17: output ;(TEXT[16]) */
            Jprog=14; CallOutLT(19);
            if(Fort) Numtxt=16;break;/*here 16 is a dummy to clear Outcard(1:6)*/
	   case 18: /*18: output [12],LAB2,[16] */
            Jprog=15; CallOutLT(20); Waitbr=0;if(Fort) Plst[33]=9; break;
	   case 19: /*K: P19: output LAB1,[17] */
			Ido=Ido+1;LoopSt[Ido]=Ssptr;Leave[Ido]=0;Iter[Ido]=0;
			Pvardo[Ido+1]=Cvardo;
	    Jprog=16; CallOutLT(21); break;
	   case 20: /*L: P20: output [14],LAB1,[16] */
			if( Iter[Ido]!=0 ) {
             Jprog=4; CallOutLT(22);
			}
            Jprog=17; CallOutLT(23);
            Jprog=18;
			if( Leave[Ido]!=0 ) {	  /*  Do current Loop */
              Out[Jprog][1]=-2;        /*  contain _Leave ? */
			} else {
              Out[Jprog][1]=0;         /*  No */
			}
			Cvardo=Pvardo[Ido]; Ido=Ido-1;
			CallOutLT(24);
			Ssptr=Ssptr-1; break;
       case 21: if(Fort) Numtxt=16 ; break ; /*  here 16 is a dummy to clear Outcard(1:6) */
	   case 22: /*M: P22: output [12],DALEE KAK P10 */
            Jprog=19; CallOutLT(25);
			Cvardo=Pvardo[Ido]; Ido=Ido-1; Ssptr=Ssptr-1;break;
	   case 23: /*N: P23: output ;,DALEE KAK P1 */
			if( Iter[Ido]!=0 ) {	/*	Generate Lab3 */
             Jprog=20; CallOutLT(26);
			}
            Jprog=0; CallOutLT(27);break;
	   case 24: /*24: INICIALI3ACIJ SELECT */
            Cnsymb=Cnsymb+1; Csymb=text[Cnsymb];Nsel=Csymb;/*  Nsel */
            LabSel=Llab-Nsel; CurLab=LabSel; /*  Bottom of Select-Stack */
            Labs[Ssptr]=CurLab;State[Ssptr]=Cstack;
            { int ISEL ;
            for(ISEL=1;ISEL<=Nsel;++ISEL){
              CurLab=CurLab+1;
              Ssptr=Ssptr+1;State[Ssptr]=Cstack;Labs[Ssptr]=CurLab;
              Ssptr=Ssptr+1;State[Ssptr]=Cstack;Labs[Ssptr]=LabSel;
              Ssptr=Ssptr+1;State[Ssptr]=Cstack;Labs[Ssptr]=CurLab;
			}
            }
            Llab=LabSel-1;
            Jprog=14; CallOutLT(39);break;
       case 25: /*P: SNJT@ CTEK,;GOTO LabSel */
			Ssptr=Ssptr-1;
	    Jprog=3; CallOutLT(28);
			Ssptr=Ssptr-1;
            Jprog=13; CallOutLT(29);
			Ssptr=Ssptr-1;break;
	   case 26: /*R:  ; after _While _Do _Until  */
            Jprog=19; CallOutLT(30);
			Cvardo=Pvardo[Ido]; Ido=Ido-1; Ssptr=Ssptr-1;break;
	   case 27: /*27: close UNTIL */
            Jprog=21; CallOutLT(31);
            Jprog=18;
			if( Leave[Ido]!=0 ) {	/*	Do current Loop */
              Out[Jprog][1]=-2;     /*  contain _Leave ? */
			} else {
              Out[Jprog][1]=0;      /*  No */
			}
			Cvardo=Pvardo[Ido]; Ido=Ido-1;
			CallOutLT(32);
			Ssptr=Ssptr-1; break;
       case 28: /*28: decode Nproc ,[14], Lab1,[16] */
			#ifndef ALLIGN
	     Csymb=*(Integer2 *)(text+Cnsymb+1);
			#else
             memcpy((char*)(&Csymb),(char*)(text+Cnsymb+1),2);
			#endif
	    Cnsymb+=2;
            Nproc=Csymb;/*  Nproc */
            Cproc=Cproc+1; Stproc[Cproc]=Nproc;  /*  stack for procedures */
            Jprog=17; CallOutLT(33); break;
       case 29: Jprog=0; CallOutLT(34); Ssptr=Ssptr-1; break;
       case 30: /*30: define the State for '[' after _While */
			if(Fort) Plst[33]=9;
            if( Waitbr && Outcard[5]==_S_Blank && Wpos==15 ) {
			   /*  '[' immediately after _while */
               /*_Do Ipos=1,8; Outcard(6+Ipos)=TXTS(45+Ipos) _Od;*/
               memcpy(Outcard+6,TXTS+45,8);
               Posold=max(Posold,14); Wpos=14; /*  for WTR */
               Jprog=14; CallOutLT(35);
               if(Fort) Numtxt=16; /*  here 16 is a dummy to clear Outcard(1:6) */
               State[Ssptr]=6;  /*  change WD back into WH */
               Ssptr=Ssptr+1; State[Ssptr]=15; /*  After [ */
			} else {
               Jprog=15; CallOutLT(36);
               if(Fort) Numtxt=16 ; /*  here 16 is a dummy to clear Outcard(1:6) */
			}
			Waitbr=0;	break ;
       case 31: /*31: define the State for '[' after if( or '_' in _Select */
			if(Fort) Plst[33]=9;
            if( Waitbr && Outcard[5]==_S_Blank && Wpos==15 )  {
			   /*  '[' immediately after if(  or  _ */
               Posold=max(Posold,14);                  /* --= ??? 15 or 14 */
               Wpos=6; Wstate=1;/*  for WTR */
               if(Cstack==4) State[Ssptr]=3;  /*  change TH back into IF */
               Ssptr=Ssptr+1; State[Ssptr]=15; /*  After [ */
			} else {
               Jprog=5; CallOutLT(37);
               if(Fort) Numtxt=16 ; /*  here 16 is a dummy to clear Outcard(1:6) */
			}
			Waitbr=0; break;
	   case 32: /*32: process ']' in fort regime */
			if( Fort )	{
	       Sw=_S_R_Br; Synt=5; goto LabWriter;
			} else {
               goto LabPerror;
			}

 }


   Lab3005: ;
 }

 LabWriter_init: ;
/*4:VYDAET OPERATORY FORTRANA POSTRO4NO, RASPOLAGAET METKI, PRI3NAKI
       PRODOLZENIJ. B KOLONKAH 73:80 STAVIT HOMEP STROKI 3AGOLOVKA U3LA,
       i3 TEKCTA KOTOROGO SGENERIROVAN 1-Y SIMVOL OPERATORA */
 Wstate=1;      /* NA4AL@NOE COCT. ABTOMATA */
 /*Lnold=-1; --=C */
 Posold=0;
 Icont=1;
 while( Wstate !=0 ){
   /*4: TAKT RABOTY ABTOMATA */
    if(RetWtr==1) goto LabComps;
	else goto LabSynt ;
    LabWriter: ; /*  RESUME Synt */
	/*2: Get Writer variables WSTATE,WR,Wp */
    Wcl=WCLASS[Spec-1][Sw];
    LabKO: ISTATE=(Wstate-1)*13+Wcl;
    WP=Plst[ISTATE];Wstate=Wst[ISTATE];
	/*3: VYPOLNIT@ DEYSTVIJ B SOOTVETSTVII C PLIST */
  switch( WP ) {
		  case 1 : break ;
          case 2 : memcpy(Outcard,Blank6,6); Wpos=6 ; break ;
		  case 3 : _Werror ;  break;
		  case 4 : _Werror;  Putcard(); break;
          case 5 : while( Wpos<5 ) {
                     Outcard[Wpos]=_S_Blank; Wpos=Wpos+1;
				   }
                   Sw=_S_Blank; break;
		  case 6 : Putcard();break;
          case 7 : /*_Do I344=1,5; Outcard(i344)=@S_Blank; _Od; */
		   memcpy(Outcard,"     *",6); Wpos=6;break;
	  case 8 : _Werror;
                   /*_Do I344=Wpos,@Lc; Outcard(i344)=@S_Blank; _Od;*/
                   memset(Outcard+Wpos,' ',LC-Wpos);
		   Wpos=LCOUT; break;
	  case 9 : if(Wpos==LCOUT) goto Lab16;
		   break;
		  case 10: /*  Fortran */
				  Icont=1; Fort=1;
				  Plst[1]=1;Wst[1]=2;
				  Plst[2]=18;
				  Plst[6]=19;
				  Plst[7]=0; Wst[7]=1;
				  Plst[15]=6; Plst[19]=9; Wst[19]=3;
		  fprintf(Include[OUTPUT],"%s\n",Fortio); /* chanal 8 */
				  break;
		  case 11: /*  Trefor */
				  Icont=1; Fort=0;
				  Plst[1]=1;Wst[1]=2;
				  Plst[2]=0;
		  Plst[6]=2; Plst[7]=Plst[6];
				  Wst[7]=3;
				  Plst[15]=4; Plst[19]=4; Wst[19]=1;
		  fprintf(Include[OUTPUT],"%s\n",Trefio); /* chanal 8 */
				  break;
		  case 12: /*  Pascal */
				  Icont=2; Fort=0;
				  Plst[1]=0; Wst[1]=3;
				  Plst[2]=18;
		  /*_Do i=73,80 [ Outcard(i)=@S_Blank ];*/
		  memset(Outcard+LCOUT,' ',8);
				  Plst[6]=Plst[1]; Plst[7]=Plst[6];
				  Wst[7]=1; break;
		  case 13:
		  Outcard[0]=_S_C; Wpos=1; break;
	  case 14: if( Waitbr && Wpos==16 ) {
					 Icont=3;
		     /*_Do i=1,15; Savcar(i)=Outcard(i) _od*/
		     memcpy(Savcar,Outcard,15);
				   } else {
					 Waitbr=0; Putcard();
		   }
		   Outcard[0]=_S_C; Wpos=1;break;
		  case 15:
				   Putcard();
		   Outcard[0]=_S_C; Wpos=1;break;
		  case 16: Lab16:;
		   switch( Icont ) {
			case 1 : Putcard();
			/*_Do I344=1,5; Outcard(i344)=@S_Blank; _Od;*/
			memcpy(Outcard,"     *",6); Wpos=6; break;
			case 2 :Wdig=Outcard[LC-1]; Outcard[LC-1]=Symcon;
			Putcard();
			Outcard[0]=Wdig;Wpos=1; break;
			case 3 :Putcard();
		       /*_do i=1,15; Outcard(i)=Savcar(i) _od;*/
		       memcpy(Outcard,Savcar,15);
		       Icont=1; Wpos=15; break;
		   } break ;
		  case 17: Wcl=2; Spec=2; goto LabKO;
	  case 18: Wpos=0;  break;/*  New HLN for pascal is needed here */
		  case 19:
	  if( Numtxt>0 ) {  /*  text came from Synt */
	      memcpy(Outcard,Blank6,6);
	      Wpos=6; Numtxt=0;
	  } break ;
	  case 20: Spec=2 ; break ; /*  for Fortran format I/O after if( _While _Select */
  }
    switch( Spec ){
	case 1 :Outcard[Wpos]=Sw; Wpos=Wpos+1 ; break ;
	case 2 :Spec=1 ; break ;
	}
 }

}

