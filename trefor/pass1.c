/* PASS 1                                               */
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#include "chargen.h"
#include "trfgen.h"
#include "trfcode.h"
#include "tree.h"
#include "align.h"

#define __TUN__

#if !defined(max) && !defined(NOMAX)
extern max(int,int);
#endif

 void Dtcdia(unsigned char *Diagn,int Ntext,int Param,int *Idiag,int *Retcod);
 //New function introduced by Yaroslav Urzhumov, defined in trefor.c
 FILE *fopenUsingPath(const char *filename, const char *mode);

#define Zero        0
#define WDEBUG
#define NewTree     (*ntr)
/* Lsr - Sr */
#define _Symrdr     SR
/* C2 mc2 */
#define _Symc2      C2
/* C-Cl2 */
#define _Symbol     Cl2
#define _TextC2     text[ltext]=_Symc2;++ltext;CHK(ltext);
#define _TextC2p(parm)     text[ltext]=parm;++ltext;CHK(ltext)
/* --= Nuzhno li eto prisvaivanie : C3=... ? */
#define _TextCC     CHK(ltext+3);C3=_Attention;text[ltext++]=_Attention;text[ltext++]=_Symc2;
#define _TextCCp(parm) CHK(ltext+3);C3=_Attention;text[ltext++]=_Attention;text[ltext++]=parm;
#define _ReadCard   if(fgets((char*)Card,LC*2,Include[Incl00])) { \
            Endin=0;lcard=strlen((char*)Card);while(lcard>0 && \
            (Card[lcard-1]=='\r' || \
		    Card[lcard-1]=='\n' || \
		    Card[lcard-1]=='\t' || \
		    Card[lcard-1]==' ' )) --lcard;} else Endin=1; ++Cardn ;
#define Synonym_header "-- Synonym List --"
/* Common variables for RDR and Anls */
static Integer4 Remlab; /* Work var */
static int Cl2 ;    /* No variable C */
static Character Mark ;   /* marker for include */
static unsigned char Card[LC*2+1],Diagn[35];  /*Buffer for reader & Diagnostics */
static Integer2  LinReq;
static Integer2  Rdr,Anls;             /* Management vars for coroutins */
static int Idiag=0;                    /* Print diag line */
static Integer2 ifn=0;                 /* Current count for fileid*/
static int Incl00=0;
static char FileName[LC],              /* Buffer for filename */
     Fblank[7]={"      "};
/* --= Make ifdef here !!! */
static char DefType[10]="inc      ";
static Integer2 Oldlst[MAXLEVEL],Lsts;  /* statck for print mode */
static char Lstyes='S',Lstno='N';       /* print start , print stop */
static char List=0,Fort=0,Pascal=0,Oldlis[MAXLEVEL],Lists;
/* Variables for RDR */
static int Irdr,Endin=0;
static unsigned int SR;
/* Variables for analize */
static int Nproc=0, /* actual number of procedures */
           Iproc,   /* current number of procedures */
           Ncall=0, /* number of calls */
           Ret[PROCMAX], /* returns */
           Lastc[PROCMAX]; /* last call of procedure */
static int Ndefpr[PROCMAX], /* definition of proc in TABALS */
	    Inr,Rf;
static Integer4 Lalias;
static char Gfound,Wspec,Outcom,Lproc=0,Lcall=0;
static char *Tmess[]={   "TMESSAGE \'<--Leaving  Node ",
                         "TMESSAGE \'-->Entering Node " };
static char Retl[]="RET_",Conl[]=":CONTINUE",Lgoto[]="GOTO";
static char Hcard[LC],Trace,Offtrc='O';
static char Tnode[NODEMAX], /* if '+' then trace of nodes needed */
            Opcon[NODEMAX]; /* ^Trefor regime */
static char Lastch=' ';     /* ANLS variable */
static int Nwords=0,Enter;
static int Jcase=0;         /* counter for case or select */
static Integer ltext,Begnam,Num,Lcase[NCASEMAX],Lalias1;
static Integer2 lslsl,C1,C2,Cc,Cnode,Lnodes;
static char Slsl[LENMAX];
static Integer2 Ncase[NCASEMAX],NCOMEN=0;
static Integer2 S,P,Sclass,Sinit;
static  Integer2 PP[360]={
/*  0, 4, 1,10,28, 2, 2, 2,10,10, 3,10, 2, 2, 2,19,10,10, 3, 0,*/
   0, 4, 1,10,28, 2, 2,36,10,10, 3,10, 2, 2, 2,19,10,10, 3, 0,
 /* 0, 5, 1,10, 3, 2, 6, 2,10,10, 3,10, 2, 2, 2,19,10,10, 3, 0,*/
  0, 5, 1,10, 3, 2, 6,36,10,10, 3,10, 2, 2, 2,19,10,10, 3, 0,
  7, 0, 7, 7, 8, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
 11,11,11,11,11,11,11,11,15,11,11,12, 0,11,11,11,11,11,11,11,
/*  0, 2, 1,10, 3, 2, 2, 2,10,10, 3,10, 2, 2, 2,19,10,10, 3, 0,
   26,26,26,26,13,26,26,26,26,26,26,26,26,26,26,26,26,26,26, 0,*/
    0, 2, 2,10, 3, 2, 2,36,10,10, 3,10, 2, 2, 2,19,10,10, 3, 0,
   26,26,26,26,13,26,26,35,26,26,26,26,26,26,26,26,26,26,26, 0,
 11,11,11,15,11,11,11,11,11,11,11,14,11,11,11,11,11,11,11,11,
 11,11,11,14,11,11,11,11,12,11,11,15,11,11,11,11,11,11,11,11,
 31,34,31,31,17,34,34,31,31,31,31,31,31,18,31,31,31,31,31,31,
/* 11,11,11,11,11,11,11, 11,11,11,11,16,11,11,11,11,11,11,11,11, */ //  orig 11 in 9th col.
 11,11,11,11,11,11,11,11,37,11,11,16,11,11,11,11,11,11,11,11, //for =>
  0, 0, 0, 0,17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,23, 0, 0, 0,
 26,26,26,26,17,26,26,26,26,26,26,26,26,26,26,26,23,26,26,26,
 30,30,30,30,17,30,30,30,25,30,30,30,30,30,30,30,24,30,30,30,
 20, 2, 2,20,20, 2, 2,20,20,20,20,20,20,20,20,20,20,20,20,20,
 22,22,22,22,22,22,22,22,22,22,22,22,21,22,22,22,22,22,22,22,
 11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,27,11,11,
 26,26,26,26,29,26,26,26,26,26,26,26,26,26,26,26,26,26,29,29,
  0,32,32,32,33,32,32,32,32,32,32,32,32,32,32,32,32,32,33,33};
static Integer2 SS[360]={
  1, 2, 3, 4, 0, 5, 5, 6, 7, 8, 1,10, 1, 1, 1,14,15,16, 1, 1,
  1, 2, 3, 4, 0, 5, 1, 6, 7, 8, 1,10, 1, 1, 1,14,15,16, 1, 2,
/*   1, 3, 1(5), 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,from SW to identif*/
  1, 3, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1,
/*  5, 5, 3, 4, 0, 5, 5, 6, 7, 8, 1,10, 1, 1, 1,14,15,16, 1, 5,
  6, 6, 6, 6, 1, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,*/
  1, 5, 5, 4, 0, 5, 5, 6, 7, 8, 1,10, 1, 1, 1,14,15,16, 1, 1,
  6, 6, 6, 6, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
 11, 9,11,11, 1, 9, 9,11,11,11,11,11,13,11,11,11,11,11,11,11,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
 11,11,11,11, 1,11,11,11,11,11,11,11,13,11,11,11,11,11,11,11,
 12,12,12,12, 1,12,12,12,12,12,12,12,13,12,12,12,12,12,12,12,
 11,11,11,11, 1,11,11,11,11,11,11,11,13,11,11,11,11,11,11,11,
  1,14,14, 1, 1,14,14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,11, 1, 1, 1, 1, 1, 1, 1,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
 17,17,17,17, 1,17,17,17,17,17,17,17,17,17,17,17,17,17,17, 1,
 18,18,18,18, 1,18,18,18,18,18,18,18,18,18,18,18,18,18, 1, 1};
static Integer2 RFF[360]={
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
  0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
  0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
/*  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, */ //orig
  0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, // for => removed *
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0,
  0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static  Integer2 PPind[10]={1,0,0,3,6,2,4,5,3,0},
                 SSind[10]={0,2,1,0,1,2,0,0,0,2};
 static Integer2 Ip7,Lp7,Cind[LC];
 static Integer Jp7,KP7,Ipw,i;

#ifndef __TUN__
static Integer2 Tclass[256]={
 5, 5,15,15,15,15,15,15,15,15,15,15,15,20,15,15,15,15,15,15,
/*15,15,15,15,15,15,15,15,15,15,15,15, 1,15,15,15,15,15,11, 8,*/
15,15,15,15,15,15,15,15,15,15,15,15, 1, 8,15,15,15,15,11, 8,
15,15,13,15,15,18,15,17, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,14,11,
 4,12, 9, 6,16, 6, 6, 6, 6, 6, 6, 6, 7, 6, 6, 6, 6, 6, 6, 6,
 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,11,15,11,10, 3,15, 6, 6, 6,
 6, 6, 6, 6, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
 6, 6, 6,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,
15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15};
static Integer2 TCC[256]={
 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,12, 0, 0, 0, 0,11, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,35,
 6, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,66, 0,67,13, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static Integer2 Refsw[ 64]={
  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,
  3,  3,  4,  5,  5,  5,  5,  5,  5,  6,  7,  8,  8,  9, 10,
 11, 11, 11, 12, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
 14, 14, 14, 14},
Slcode[ 64]={
 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 27, 28, 30, 23, 29,
 26, 31, 25,  3,  3,  3,  3, 36, 32, 33, 36, 36, 36, 37, 38,
 39, 39, 39, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
 36, 36, 36, 36},
Order[ 64]={
  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
 31, 32, 33, 34, 35, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
 36, 36, 36, 36},
Pslsl[ 65]={
  1,  3,  5,  7,  9, 13, 17, 22, 27, 34, 36, 42, 47, 52, 56,
 62, 66, 69, 69, 75, 80, 87, 92, 98,102,108,112,119,127,134,
140,146,150,151,158,166,175,175,175,175,175,175,175,175,175,
175,175,175,175,175,175,175,175,175,175,175,175,175,175,175,
175,175,175,175,175};
static char  Tslsl[1024]={
'D','O','O','D','I','F','F','I','T','H','E','N','E','L','S','E',
'W','H','I','L','E','L','E','A','V','E','I','T','E','R','A','T',
'E','O','F','R','E','P','E','A','T','U','N','T','I','L','O','T',
'H','E','R','C','A','S','E','S','E','L','E','C','T','E','S','A',
'C','E','N','D','D','E','F','I','N','E','L','A','B','E','L','D',
'E','F','L','I','S','T','T','R','A','C','E','O','U','T','C','O',
'M','P','R','O','C','R','E','T','U','R','N','C','A','L','L','I',
'N','C','L','U','D','E','I','N','C','L','U','D','E','N','F','O',
'R','T','R','A','N','T','R','E','F','O','R','P','A','S','C','A',
'L','R','E','X','X','C','O','N','P','R','I','N','T','O','F','F',
'P','R','I','N','T','E','N','D','O','F','T','R','E','E',' '};
static Integer2 Aclass[256]={
 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 8, 2, 8, 8, 8, 8, 2,
 8, 8, 8, 8, 7, 6, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8,
 8, 8, 8, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8, 8, 8, 5, 8, 5, 5, 5,
 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
 5, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8};

#else
#include "pass1dep.h"
#endif
static unsigned char Diagn2[35];
 static Integer2 Ipk1,Cpk1;
 static char Erhead,Foundk,Found,Found7,Refnfn=0;
 static Integer2 Areq,Enhead,Path,RPath,Nhead;
 static Integer2 Ison,Cson;
/* Variables for alias */
 static Integer2 Sals,Pals,C3,Iclass, /* Variables for ALIASes */
	   Lroot,Pos,Alsrf;
 static Integer4  Ltxdef,Ltextd;   /* Position of Alias definition beginning */
/* @Character Posald(4); Equivalence (Posald(1),Ltextd); */
/* static Integer2 Cl3; /*Equivalence (cl3(1),c3); */
static char  Root[LC],Droot[]="Z00000",
            SQuote,SQuote2,OSrdr;   /*  -- " , Old Symbol RDR*/
static char Defr=0;         /* Deflist root is used ? */
 static Integer2 PPals[88]={ /*--Blank ' KY,KT @ L_D  -  ,  Others */
  1,  9,  9,  2,  9,  0,  9,  9,
  3,  3,  9,  4,  5,  4,  4,  4,
  1,  7,  9,  0,  0,  0,  0,  0,
  6,  0,  6,  0,  0,  0,  0,  0,
  0,  8,  6,  0,  0,  0,  0,  0,
  1,  9,  9,  2,  9,  0,  9,  9,
  10, 10, 10, 10,  5, 10, 10, 10,
  1,  9,  9, 11, 12,  0,  9,  9,
  1,  9,  9,  2, 12,  0,  9,  9,
  1,  9,  9,  2,  9,  0,  1,  9,
  13, 13, 13, 13,  5, 13, 13, 13};
static  Integer2 SSals[88]={ /*Blank ' KY,KT @ L_D  -  ,  Others*/
  1,  0,  0,  2,  0,  1,  0,  0,
  3,  5,  0,  4,  2,  4,  4,  4,
  3,  5,  0,  4,  4,  4,  4,  4,
  1,  4,  0,  4,  4,  4,  4,  4,
  5,  5,  0,  5,  5,  5,  5,  5,
  6,  0,  0,  7,  0,  6,  0,  0,
  6,  0,  0,  0,  7,  6,  6,  0,
  8,  0,  0, 11,  9,  8,  0,  0,
 10,  0,  0, 11,  9, 10,  0,  0,
 10,  0,  0, 11,  0, 10, 10,  0,
 10,  0,  0,  0, 11, 10, 10,  0};
/* Other variables */
static int Numsw=NSW;  /* Number of service words (can be increased at run time)*/

unsigned ToUpper(unsigned ch){
 if(islower(ch)) return _toupper(ch);
 else return ch ;
}

int Memcmp(const char *first,const char *second,size_t len){
 size_t i;
 int res;
 if(len==0) return 0;
 for(i=0;i<len;++i){
  res=ToUpper((unsigned char)*first++)-ToUpper((unsigned char)*second++);
  if(res) break;
 }
 return res;
}

static void GetServiceWord(void){
 Lp7=-1; Found7=0; /* -- Lp7 - popjd*ovyy nomep cl.clova */
 while( Lp7<Numsw && !Found7) {  /* Numsw - Number of Service Words */
     ++Lp7;
     if( lslsl==(Pslsl[Lp7+1]-Pslsl[Lp7])){
	/*1: Check Service Word, SET Found7=.true. if found */
	  KP7=Pslsl[Lp7]-1;
	  Found7=(lslsl==0)?1:!Memcmp(Slsl+1,Tslsl+KP7,lslsl);
     }
 }
 Lp7=Order[Lp7]-1;  /* SERVICE WORD order Number */
 Ip7=Refsw[Lp7];  /* SERVICE WORD Group Number */
}

static void  NumRetrt(void){
   Ipw=6;
    while( Inr ) {
     --Ipw;
     Retrt[Ipw]=Inr%10+'0';
     Inr=Inr/10;
    }
}

static void TRACE(void){
  C2=_Calias; _TextCC;
  C3=Alsprc;
#ifndef ALLIGN
  *((Integer2*)&text[ltext])=C3;
#else
  memcpy((char*)(text+ltext),(char*)(&C3),2);
#endif
  ltext=ltext+2;
  CHK(ltext);
  strcpy((char*)(text+ltext),Tmess[Enter]);ltext+=strlen(Tmess[Enter]);CHK(ltext);
  memcpy((char*)(text+ltext),Hcard,Nhead);ltext+=Nhead;CHK(ltext);
  text[ltext++]=_Apostrophe;CHK(ltext);
  C2=_Ecm; _TextCC; C2=_Ko; _TextCC;
}

static void ReadProfileWord(int  *j ) {
  unsigned char *card=&Card[*j];
  while(*card==' ' || *card=='\t') ++card;
  if(*card==_Underline) ++card;
  lslsl=0;
  while( (*card!=' ' && *card!='\t' && *card!=0 &&*card!='\n')
    && lslsl< LENMAX ){
    Slsl[lslsl]=ToUpper(*card);
    ++lslsl;
    ++card;
  }
  *j += card-&Card[*j];
}

static void ReadProfile(void){
  int i,j ;
  FILE *profile;
  if((profile=fopen("profile.trf","r"))!=NULL){
    i=NSW;
    for(;;){
      if(fgets((char*)Card,LC,profile)){
       if(i==NSW) fprintf(Include[LISTING],"%s\n",Synonym_header);
       j=0;  /* Pointer in CARD */
       ReadProfileWord(&j);

       if( Card[j]==' ' || Card[j]=='\t') {
	GetServiceWord(); /*  Find TREFOR Service word */
	 if( Found7 ) {

            /*3: Select Synonym stripped Word from Card */
            ReadProfileWord(&j);
	    ++i; /* Define SYNONYM for LP7-th TREFOR service word */
	    Pslsl[i+1]=Pslsl[i]+lslsl; Order[i]=Lp7;
        memcpy(&Tslsl[Pslsl[i]-1],Slsl,lslsl);
            fprintf(Include[LISTING],"%s\n",Card);
            continue;
         }
            fprintf(Include[LISTING],"%s\n",Card);
            fprintf(stderr,"%s\n",Card);
       }
      } else break ;
    }
    Numsw=i;   /* The number of Service Word Set */
    fclose(profile);
  }
}

static int Llind;

static  void Down(void){
 int IPS;
 /*0: PROCEDURA Down - ISHODJ I3 TEKUQEGO Path (PUTI B DEREVE) I
      Glind (MECTO B 3AGOLOVKE U3LA) PRODLIT@ Path I Glind
      HA ODIN LOKAL@NYY INDEKS.  SOHRANJT@ INVARIANT
      Q2331: LIBO Erhead = .False. I Glind SOSTAVLJET POSLED.LOK.IND.
      PO PUTI DO VER6INY Path , LIBO Erhead = .True. */
 S=Sinit; Llind=0;  /*  Length of Loc. index */
 while (S!=0 ){
   Enhead=Enhead+1;_Symbol=ToUpper(Card[Enhead]);
   /*0: One step of automat */;
     /*1: Get in Iclass Lexic class of C , in P - Number of Program */
 switch(_Symbol){
   case _Point :  Iclass=3 ; break ;
   case _Underline : Iclass=2 ; break ;
   case _Colon: case _Equal :    Iclass=4 ;break;
   case _S_Blank : Iclass=5 ; break ;
   default : Iclass=1 ; break ;
 }
 IPS=(S-1)*5+Iclass-1;P=PPind[IPS];S=SSind[IPS];
     /*2: Perform program number P */
  switch( P ) {
        case 1 : Llind=1; Cind[Llind]=Cl2 ; break ;
        case 2 :Llind=Llind+1; Cind[Llind]=Cl2 ; break;
        case 3 :Enhead=Enhead-1;break;
        case 4 :Sinit=2;break;
	case 5 :Sinit=1;break;
        case 6 :Llind=0;break;
  }

 }
 if( Llind!=0 ) {
    /*1: Find Son to Path with Local Index Cind() and Add it to Path,
        if the Son is not found then set  Erhead=.True. */
 /*  Ison - number of Son node */
 /*  Cson - a number of unexamined Son nodes */
 Ison=Ason[Path]; Cson=Nofson[Path]; Erhead=1;
 while (Cson>0 && Erhead ){
   if( Llind==Plind[Ison+1]-Plind[Ison]  ){
      Ip7=0;Erhead=0;Jp7=Plind[Ison];
      while( Ip7<Llind && !Erhead ) {
        if(Lind[Jp7+Ip7]!=Cind[Ip7+1]) Erhead=1;
        Ip7++;
      }
      if( !Erhead ) {
        /*1: Add Node Ison to Path */
        Path=Ison ;

      }
   }
   Ison=Ison+1; Cson=Cson-1;
 }

   Llind=0 ;
 }

}


extern int Lst;  /* in trefor.c */

void pass1(int NewTree,unsigned *cardn);

void pass1(int NewTree,unsigned *cardn){
/*first passage */
int lcard;
int Cardn=0,Ndef,Ips,isamp,Ipk2;
  List=1;Fort=0;Pascal=0; Incl00=0; /* Init */
  Diagn[34]=0;
  NewTree=0; /* Numsw=@Nsw; init in declaration */
  /* read profile */
  ReadProfile();
  Rdr=1;Anls=1;
  goto Lab2000;
  Lab1000: switch(Rdr){
   case 1 : goto Lab1001;
   case 2 : goto Lab1002;
   case 3 : goto Lab1003;
   default : fprintf(stderr,"Internal Error Rdr not in [1,2,3](=%d)\n",Rdr);
  }
  Lab1001:;
       /*2: Body of Coroutine RDR. Get symbol by symbol output text
            or symbols KY (End_of_Node), KT (End_of_Text).
            After KY begins next card. Print Listing of Program */
 Endin=0;
 while(!Endin){
  _ReadCard ;
  while( Endin==0 && (Card[0] != _Percent || NCOMEN != 0) ){
     /*3: Transfer Card to Anls by symbol  */
     Irdr=0;
     Card[lcard]=_Cr;lcard++; /* Imitate Car. Ret */
     if(Fort && (Card[0]==_S_C || *Card==_S_Aster)) {
           _Symrdr=_S_Minus; Alsrf=1; /*  To imitate '--' */
     Rdr=2; goto Lab2000;
     }
     while( Irdr < lcard) {
      _Symrdr=Card[Irdr];  /*  To second byte of SR */
      Rdr=2;goto Lab2000;
      Lab1002: Irdr++;  /* Resume ANLS */
     }
     Card[lcard-1]=0;    /*  delete Carriage Return */
     /* --lcard;            /*  --=2 add in Beta-trefor ??? Why */
     /*4: Print Card to Listing */
     switch(Idiag){
      default : if(List && Lst==1)
       fprintf(Include[LISTING]," %4d%c%s\n",Cardn,Mark,Card);
       break;
      case 1 :                           /* Information */
    fprintf(Include[LISTING]," %4d%c%s %s\n",Cardn,Mark,Card,Diagn);Idiag=0;break;
      case 2 :                           /* serious error */
	fprintf(stderr," %4d%c%s %s\n",Cardn,Mark,Card,Diagn);Idiag=0;
        fprintf(Include[LISTING]," ->Error %s %s\n",Card,Diagn);
        break;
      case 3 :                           /* Warning */
    fprintf(Include[LISTING]," %4d%c%s %s\n",Cardn,Mark,Card,Diagn);
    fprintf(stderr," %4d%c%s %-34s\n",Cardn,Mark,Card,Diagn);Idiag=0;break;
     }
     _ReadCard;
  }
 /*5: Transfer to ANLS symbol @KY and print HEADER or @KT */
  if( Endin==0 ) {
    SR=_Ky; Rdr=3; goto Lab2000;
    Lab1003: ;  /*  Resume ANLS */
    /*1: Print Header of Node from Card, Diagn, Cardn */
      /*1: Fill the line of the Header with Minuses  */
      memset(Card+lcard,_S_Minus,LC-lcard-1);
      Card[LC-1]=0;
      fprintf(Include[LISTING]," %4d%c%s %-34s\n",Cardn,Mark,Card,Diagn);
      if(Idiag>0) {
       fprintf(stderr," %4d%c%s %-34s\n",Cardn,Mark,Card,Diagn);
        Idiag=0;
      }
  } else if( Incl00==0 ) {
   SR=_Kt; goto Lab2000;
  } else {
   List=Oldlis[Incl00];Lst=Oldlst[Incl00];
   fclose(Include[Incl00]);
   Incl00-- ; Cardn--;
   Endin=0;
   fprintf(Include[LISTING],"====>   Level( %1d )\n",Incl00);
   if(Incl00==0) Mark=_S_Blank;
  }
 }

 Lab2000:
 switch(Anls){
   case 1 : goto Lab2001;
   case 2 : goto Lab2002;
   case 3 : goto Lab2003;
   case 4 : goto Lab2004;
   case 5 : goto Lab2005;
   case 6 : goto Lab2006;
   case 7 : goto Lab2007;
   case 8 : goto Lab2008;
   case 9 : goto Lab2009;
 }
 Lab2001:;
 /*3: Body of Coroutine ANLS, construct Tree, coding spec. sym */
   /*1: Modeling situation after succesful analysis of root header
        Node and reading 1-st symbol of the node text */
   Mark=_S_Blank;
   Lind[1]=_Percent;
   Cnode=1;    /*   Number of current Node */
   Lnodes=2;   /*   Number of 1-st free line in NODES */
   ltext=0;    /*   Number of 1-st free byte of Text */
   Atext[1]=1; Ason[1]=2; Nofson[1]=0; Headln[1]=0;
   Plind[1]=1; /*   Local index pointer for ROOT NODE */
   Plind[2]=2; /*   Local index pointer for the first requested node */
   Clind=2;    /*   Counter for Local Indeces Lind() */
   Tnode[1]=_S_Minus;
   Trace=_S_Minus; Outcom=0;
   Opcon[1]=_S_Minus;
   Defr=0;
   Alspre[1]=0;
   Alsprc=0;
   Alsrf=0;
   Sals=0;
   Calias=1;   /*  current free position in ALIAS NAMES */
   Palias[1]=1;
   Ndef=NDEF0;   /*  Current alias number */
   Wspec=0;
   Lastch=_S_Blank;
   Anls=2; goto Lab1000;
   Lab2002: ;  /*  Resume RDR */
     while( SR != _Kt) {

      /*2: Pass through the text from the current symbol until @KT or KY,
           Analyse the text of Node */
        S=1;
        while( S ) {
          if( Sals ) {
             if( Alsrf==1 ) {
                Talfin[Ndef]=ltext;Ndef++;
                Alsrf=0; _Symrdr=OSrdr;
             }
             Lab2008: ;  /*  Return from RDR */
             /*ALD: Alias definition accumulation */
             /*1: Get in Iclass Lexic alias class of SR ,
                  in Pals - Number of Program */
             Iclass=Aclass[SR]; /* --= Corrected here SR+1 and -1 added */
             Ips=(Sals-1)*8+Iclass-1; Pals=PPals[Ips]; Sals=SSals[Ips];
             /*2: Perform program number Pals */
             switch(Pals){
              case 1 : Anls=8; goto Lab1000;  /*  Resume RDR, Return to 2008 */
              case 2 : Alpred[Ndef]=Alsprc; Alsprc=Ndef;
                   Anls=8; goto Lab1000;  /*  Resume RDR, Return to 2008 */
                case 3 : Palias[Ndef+1]=Calias; Talbeg[Ndef]=ltext;
                   if(Iclass==2) SQuote=_Symrdr;  /*  store open quote */
                   Anls=8; goto Lab1000;  /*  Resume RDR, Return to 2008 */
                case 4 : Palias[Ndef+1]=Calias; Talbeg[Ndef]=ltext; break ;
                case 5 : Nalias[Calias]=ToUpper(SR);++Calias;
                   Anls=8; goto Lab1000;  /*  Resume RDR, Return to 2008 */
                case 6 : OSrdr=_Symrdr;_Symrdr=_S_Blank; Alsrf=1;break;
                case 7 : SQuote=_Symrdr;
                   Anls=8; goto Lab1000;  /*  Resume RDR, Return to 2008 */
                case 8 : if( SQuote==_Symrdr ){
                          OSrdr=_S_Blank;
                          _Symrdr=_S_Blank; Sals=1; Alsrf=1;
			 } break ;
                case 9 :  _P9: Ltextd=ltext;  /*  EQU. POSALD */
                      #ifndef ALLIGN
                        *(Integer4*)&text[Ltxdef]=ltext;
                      #else
                       memcpy((char*)(text+Ltxdef),(char*)(&ltext),4);
                      #endif
                         if( Lproc )
                           S=14;
                         else
                           S=1;
                         if(Fort && _Symrdr==_S_Semicol) _Symrdr=_S_Blank ;
                         break;
                case 10 :  Palias[Ndef+1]=Calias; Talbeg[Ndef]=ltext;
                    /*Lab: Generate next LABEL, Define TALFIN(ndef) */
                     Remlab=Llab;  /*  Generate Num. Label */
                     for(isamp=1;isamp<=5;++isamp){
                      C2=Remlab/10000;
                      Remlab=(Remlab%10000)*10;C2=C2+'0';
		      _TextC2;
                     }
                     --Llab;  /*  Next Label */
                     Talfin[Ndef]=ltext;

                     ++Ndef;
		    if( Lproc ) { int i;
                      Sals=0;
                      /*proc:   begin of procedure */
                      /* send @ret_procname to NALIAS and define it as RETRT//Nproc */
		      for( i=0;i<4;++i) { Nalias[Calias]=Retl[i]; ++Calias ; }
		      i=Palias[Ndef-1];
		      while( i<Palias[Ndef]) {
			 Nalias[Calias]=Nalias[i];
			 ++Calias; ++i;
                      }
                      Ndefpr[Nproc]=Ndef-1;
                      Palias[Ndef+1]=Calias;
                      Talbeg[Ndef]=ltext; Alpred[Ndef]=Alsprc;
                      Inr=Nproc;
		      NumRetrt();
                      if( Ipw>3 )   /* --= IPW isprawit'  na -1 */
			 for( i=3;i<Ipw;++i) Retrt[i]='0' ;

		      for(i=0;i<6;++i) text[ltext+i]=Retrt[i]; ltext+=6;
                      CHK(ltext);
                      Alsprc=Ndef; Talfin[Ndef]=ltext;
                      ++Ndef;
                      if (Nc1st[Nproc]==0 ){
                          Nc1st[Nproc]=CALLMAX-1; Retlab[CALLMAX-1]=Llab; /*  fictitious call */
                      }
                    }
                    if(Sals==0) goto _P9;
                    break;
                case 11 :
                    for( Lroot=0;Lroot<6;++Lroot) Root[Lroot]=Droot[Lroot];
                    Lroot=5;/* --= or 6 ? */
                    Alpred[Ndef]=Alsprc; Alsprc=Ndef; Defr=1;
                    Anls=8; goto Lab1000;
                case 12 : ++Lroot; Root[Lroot]=_Symrdr;break;
                case 13 : Palias[Ndef+1]=Calias; Talbeg[Ndef]=ltext;
                      /*Defl: Generate next IDENTIFIER from _Deflist, Define
                              TALFIN(ndef) */
                      /*1: Send Root into TEXT */
                      for(Pos=0;Pos < Lroot;++Pos){
                          text[ltext]=Root[Pos];
                          ++ltext;
                      }
                      CHK(ltext);
                      if( Sals!=0 || Defr ) {
                        Pos=Lroot;
                        _Symc2=Root[Pos];  /*  C2 */
                        while( C2=='9' && Pos>1 ) {
                          Root[Pos]='0';
                          --Pos;
                          _Symc2=Root[Pos];
                        }
                        if (C2>='0' && C2<'9') {
                          ++C2; Root[Pos]=_Symc2;
                        } else {
                          /* --= ??? Call Dtcdia(Diagn,15,Zero,&Idiag,&Retcod);*/
                          Sals=0;  /*  Break Deflist */
                        }
                    }
                    Talfin[Ndef]=ltext;


                    ++Ndef;
                    if( Sals==0 && Defr ){
                      Defr=0;
                      for(Lroot=0;Lroot<5;++Lroot) Droot[Lroot]=Root[Lroot];
                    }
                    goto _P9;
             }
           }
          /*2: One step of Automat: the class of symbol SR put into SCLASS,
               possible symbol for recoding into CC, get S, P, RF from
               arrays SS, PP, RFF. Execute program number P, if RF
               read the next symbol into SR */
      /*1: Put the class of symbol SR into SCLASS, possible symbol
           for recoding into CC */
       Sclass=Tclass[SR];Cc=TCC[SR];
      /*2: Get S, P, RF from arrays SS, PP, RFF */
       Ips=(S-1)*NCLASS+Sclass-1;P=PP[Ips];S=SS[Ips];Rf=RFF[Ips];
      /*3: Execute program number P */
	switch(P){
         case 1 : /*1: Clear SLSL */
          lslsl=0;
          break;
         case 2 : /*2: Put C in TEXT */
       text[ltext]=SR; ++ltext; CHK(ltext);break;
         case 3 : /*3: Put CC in TEXT */
	  _TextCCp(Cc); break;
         case 4 : /*4: begin accumulating of Number in NUM, put C in TEXT */
	  Num=SR-'0'; _TextC2p(SR) ; break;
         case 5 : /*5: accumulate of Number in NUM, put C in TEXT */
	  Num=Num*10+SR-'0';  _TextC2p(SR); break;
         case 6 : /*6: Put C and NUM next symbols in TEXT ( the LAST of them
              remains in C). If KY or KT - message like P13 and RF */
           /*  SR='H', NUM - Length of Hollerit. const */
           while( Num>0 && SR!=_Kt && SR!=_Ky ) {
	     _TextC2p(SR);
             Anls=4; goto Lab1000;  /*  RESUME RDR */
             Lab2004: --Num ;
           }
           if( SR==_Kt || SR==_Ky ) {
             Rf=1;
             fprintf(Include[LISTING],"Char. constant not completed\n");
             /*  PE4AT@ ' HE 3AVER6ENA TEKCT.KOHCT. */
             Retcod=3;
             fprintf(stderr,"Char. constant not completed\n");
	   } else { _TextC2p(SR); }  break;
         case 7 : _P7:;
          /*7: Put SPECcod of service word in SLSL, TEXT, message if ERROR */
	 GetServiceWord();
	 if( Found7 )  {
	   C2=Slcode[Lp7];   /* Code of service word */
	    switch(Ip7){
		   case 1 :  _TextCC;break;
		   case 2 :  _TextCC;
		    Jcase=Jcase+1;Ncase[Jcase]=0;     /*  Case,Select */
		    Lcase[Jcase]=ltext;++ltext; /*  Reserve Byte */
		    break;
		   case 3 :  _TextCC;         /*  Esac,end */
                    if( Jcase>0 )  {
		       C2=Ncase[Jcase];text[Lcase[Jcase]]=_Symc2;
                       --Jcase;
                    } else {
		       Dtcdia(Diagn,9,Zero,&Idiag,&Retcod);
                     } break;
		   case 4 :  _TextCC;++Ncase[Jcase];break;
                   case 5 :  if( Sals==0 ) { int Ip77;
                      Ip77=Lp7-18+1;
		      switch(Ip77){
        /* define */ case 1: _TextCC; Sals=1; Ltxdef=ltext;
                          ltext=ltext+4;break;
        /* label */  case 2: _TextCC; Sals=6; Ltxdef=ltext;
                          ltext=ltext+4;break;
	/* deflist */case 3: _TextCC; Sals=8; Ltxdef=ltext;
                          ltext=ltext+4; Lroot=0;break;
        /* trace */  case 4: _TextCC; Sals=3;  Ltxdef=ltext; ltext=ltext+4;
                 Dtcdia(Diagn,13,Zero,&Idiag,&Retcod);
                             Trace=_S_Plus; Alpred[Ndef]=Alsprc; Alsprc=Ndef;
			     {int i;
			       for(i=0;i<8;++i,++Calias)
				 Nalias[Calias]=Tmess[0][i];
			     }
			    Palias[Ndef+1]=Calias; Talbeg[Ndef]=ltext;break;
	    /* outcom */ case 5: Outcom=1;
	      Dtcdia(Diagn,14,Zero,&Idiag,&Retcod); break;
	    /* proc   */ case 6: _TextCC; ++Nproc;
			       C2=Nproc; /*  TWO BYTES after @PROC = Nproc */
			       #ifndef ALLIGN
                    *(Integer2*)&text[ltext]=C2;
			       #else
                    memcpy((char*)(text+ltext),(char*)(&C2),2);
                   #endif
                   ltext+=2;
                   CHK(ltext);
			       _TextCCp(_Ko); Lproc=1;
			       _TextCCp(_Define);
			       Sals=6; Ltxdef=ltext; ltext+=4;
		      }
		    } else {
	      Dtcdia(Diagn,16,Zero,&Idiag,&Retcod);
		    } break ;
		   case 6 :  _TextCCp(_Ko); _TextCC; break ;/*  _Return */
		   case 7 :  Lcall=1; break;   /*  _Call */
		   case 8 :  if( Incl00<MAXLEVEL )  {    /*  Able to open new level ? */
		      S=18;Lists=List;ifn=0;Nwords=0;Lastch=_S_Blank;
                      if( Lp7==(27-1) ){
                         Lsts=Lst;
                     } else {
                         Lsts=0;
                      }
                   } else {
             Dtcdia(Diagn,18,Zero,&Idiag,&Retcod);
                    } break;
		   case 9 : _TextCC;
                   Fort=1;Pascal=0;   /*  _Fortran */
                   Tclass[';']=15; TCC[';']=0;
                   Tclass[_Alias]=16; Aclass[_Alias]=4; TCC[_Alias]=_Calias;
                   Tclass[_S_Number]=15; Aclass[_S_Number]=8;TCC[_S_Number]=0;
                   Tclass['-']=18;  /*  Restore Minus class */
                   Aclass['-']=6;   /* --=2 */
                   Tclass[_Cr]=19; TCC[_Cr]=_Ko;
                   Tclass[_S_Blank]=15;
                   PP[2*NCLASS+2-1]=7; SS[2*NCLASS+2-1]=1; RFF[2*NCLASS+2-1]=1;
                   PP[14*NCLASS+17-1]=22; SS[14*NCLASS+17-1]=1; RFF[14*NCLASS+17-1]=1; /*--=2*/
                   /* --= ???? What it is */
                   /*F: Restore special signs and related programs */
                     TCC[_S_GT]=_Gt;
                     TCC[_S_LT]=_Lt;
                     Tclass[_S_NE]=10;
                     Tclass[_Ampersand]=11;
                     Tclass[_Equal]=12; /*--?*/
                     Tclass[_S_Exclam]=11;
                     Tclass[_S_L_Br]=11;
                     Tclass[_S_R_Br]=11;
                     Tclass['H']=7;
                     Tclass['h']=7;
                     PP[12+9*NCLASS-1]=16;
                     PP[9 +3*NCLASS-1]=15;RFF[9 +3*NCLASS-1]=0;  /*-- <>  */
                     PP[12+6*NCLASS-1]=14;RFF[12+6*NCLASS-1]=0;  /*-- >=  */
		     PP[12+3*NCLASS-1]=12;RFF[12+3*NCLASS-1]=0;  /* -- <= */
		     break;
		   case 10:  _TextCC;
                    Fort=0;Pascal=0;  /*  _Trefor */
                    Tclass[_Alias]=16; Aclass[_Alias]=4; TCC[_Alias]=_Calias;
                    Tclass[_S_Number]=15; Aclass[_S_Number]=8; TCC[_S_Number]=0;
                     Tclass[_S_Semicol]=19;TCC[_S_Semicol]=_Ko;
                    Tclass[_S_Minus]=18;  /*  Restore Minus class */
                      Tclass[_Cr]=20; TCC[_Cr]=0;
                    Tclass[_S_Blank]=1;
                    PP[2*NCLASS+2-1]=0; SS[2*NCLASS+2-1]=3; RFF[2*NCLASS+2-1]=0;
                    PP[14*NCLASS+17-1]=22; SS[14*NCLASS+17-1]=1; 
                    RFF[14*NCLASS+17-1]=1; /*--=2*/
                  Aclass[_S_Minus]=6;   /* --=2 */
                  
                    /*T: Restore special signs and related programs */
                     TCC[_S_GT]=_Gt;
                     TCC[_S_LT]=_Lt;
                     Tclass[_S_NE]=10;
                     Tclass[_Ampersand]=11;
                     Tclass[_Equal]=12; /*--?*/
                     Tclass[_S_Exclam]=11;
                     Tclass[_S_L_Br]=11;
                     Tclass[_S_R_Br]=11;
                     Tclass['H']=7;
                     Tclass['h']=7;
                     PP[12+9*NCLASS-1]=16;
                     PP[9 +3*NCLASS-1]=15;RFF[9 +3*NCLASS-1]=0;  /*-- <>  */
                     PP[12+6*NCLASS-1]=14;RFF[12+6*NCLASS-1]=0;  /*-- >=  */
		     PP[12+3*NCLASS-1]=12;RFF[12+3*NCLASS-1]=0;  /* -- <= */
		     break;
		   case 11:  _TextCC;
                    Fort=0;Pascal=1;Outcom=0;  /*  _Pascal */
                     Tclass[_S_Semicol]=15;TCC[_S_Semicol]=0;
                   if( Lp7!=(33-1) )  {      /*  Do not Change @ for _C  --? */
                      Tclass[_Alias]=15; Aclass[_Alias]=8;TCC[_Alias]=0;
                      Tclass[_S_Number]=16; Aclass[_S_Number]=4;
                      TCC[_S_Number]=_Calias;
                    }
                    Tclass[_S_Minus]=18;  /*  Restore Minus class */
                    Tclass[_Cr]=19; TCC[_Cr]=_Ko;
                    Tclass[_S_Blank]=15;
                    PP[14*NCLASS+17-1]=22; SS[14*NCLASS+17-1]=1;  /*--=2*/ 
                    RFF[14*NCLASS+17-1]=1; /*--=2*/
                    Aclass[_S_Minus]=6;   /* --=2 */
                    PP[2*NCLASS+2-1]=7; SS[2*NCLASS+2-1]=1; RFF[2*NCLASS+2-1]=1;
                   /*P: Define special signs for PAscal and change programs *>;*/
                     TCC[_S_GT]=0;
                     TCC[_S_LT]=0;
                     Tclass[_S_NE]=15;
                     Tclass[_Ampersand]=15;
                     Tclass[_Equal]=15; /* ? */
                     Tclass[_S_Exclam]=15;
                     Tclass[_S_L_Br]=15;
                     Tclass[_S_R_Br]=15;
                     Tclass['H']=6;
                     Tclass['h']=6;
                     PP[12+9*NCLASS-1]=11;
                     PP[9 +3*NCLASS-1]=11;RFF[9 -1+3*NCLASS]=1;  /*  <> */
                     PP[12+6*NCLASS-1]=11;RFF[12-1+6*NCLASS]=1;  /*  >= */
                     PP[12+3*NCLASS-1]=11;RFF[12-1+3*NCLASS]=1;  /*  <= */
                    if( Lp7==(33-1) )  {      /*  For _C  redefine Minus */
                      Tclass[_S_Minus]=15; /*  Rest */
                      Aclass[_S_Minus]=8 ;
                      Tclass['/']=17; /* --=2 */
                      PP[14*NCLASS+17-1]=27; SS[14*NCLASS+17-1]=1;  /*--=2*/ 
                      RFF[14*NCLASS+17-1]=0; /*--=2*/
                    } break;
	   case 12:  List=1 ; Dtcdia(Diagn,21,Zero,&Idiag,&Retcod);break;
		   case 13:  List=0 ; Dtcdia(Diagn,19,Zero,&Idiag,&Retcod);break;
		   case 14:  Endin=1;NewTree=1;   /*  _Endoftree */
                    Dtcdia(Diagn,17,Zero,&Idiag,&Retcod);
            fprintf(Include[LISTING]," %4d%c   %s %-34s\n",Cardn,Mark,Card,Diagn);
                    SR=_Kt; goto Lab2000;
            }
	 } else {
	      text[ltext]=_Underline;++ltext;
          CHK(ltext);
	      memcpy(text+ltext,Slsl+1,lslsl);
	      ltext+=lslsl;
          CHK(ltext);
	  /*    Dtcdia(Diagn,20,Zero,&Idiag,&Retcod); */ /*  Wng Unknown service word !!! */
	  }

	  break;
	 case 8 : /*8: Message:'Service word  not complete'*/
	  if( lcard==LC ) {
	   fprintf(Include[LISTING],"Service word in danger\n");
           fprintf(stderr,"Service word in danger\n");
           Retcod=max(Retcod,2);
          }
          goto _P7;
	 case 9 : /*9: add Letter to SLSL */
          if( lslsl<LENMAX ) {    /*  Lenmax - max. length of service word */
           ++lslsl;Slsl[lslsl]= /* --=2 ToUpper*/(SR); /*  accum. service word */
      } else Dtcdia(Diagn,1,Zero,&Idiag,&Retcod);
          break;
	 case 10: /*A: If CC^=0, Then C1=CC, Else C1=SR */
          if( Cc!=0 ) {
            C1=Cc; Wspec=1;
          } else {
            C1=SR; Wspec=0;
           }
          break;
	 case 11: /*B: Put C1 in text */
          C2=C1; if( Wspec )  {  _TextCC; Wspec=0;
                 } else {  _TextC2 ; }
          break;
	 case 12: /*C: Put cod of <= in text */
          _TextCCp(_Le);
          break;
	 case 13: /*D: Message:'Character constant do not complete'*/
             fprintf(Include[LISTING],"Char. constant not completed\n");
             fprintf(stderr,"Char. constant not completed\n");
             Retcod=3;
          break;
	 case 14: /*E: Put cod of >= in text */
	  _TextCCp(_Ge);break;
	 case 15: /*F: Put cod of ^= in text */
          _TextCCp(_Ne); break;
	 case 16: /*G: Put cod of == in text */
	  _TextCCp(_Eq);break;
	 case 17: if( SR==_Ky && NCOMEN!=0 ){
            if( Outcom ) {
              S=12;
            } else {
              S=11;
             }
         } else {
	     Clind=max(Clind-Llind,2); Llind=0;
             /*H: Message:'Request or comment do not complete'*/
             fprintf(Include[LISTING],"Request or comment not closed\n");
             fprintf(stderr,"Request or comment not closed\n");
             Retcod=3;
          } break;
	 case 18: if( Outcom ){
	   C2=_Bcm; _TextCC; S=12;
          }
	 LinReq=Cardn; break;
	 case 19:  /*  Symbol @ */
         if( Lcall ) {
             /*call: after _call */
           Begnam=ltext; /*  begin of procedure name */
         } else {
            /*  Put CC (TRFCODE-@Calias) and Alsprc ( 2 Bytes ) to text */
            C2=Cc; _TextCC;
           if( Sals==0 ) {
              C2=Alsprc;
              #ifndef ALLIGN
               *(Integer2*)&text[ltext]=C2;
              #else
               memcpy((char*)(text+ltext),(char*)(&C2),2);
              #endif
              ltext+=2;
              CHK(ltext);
            }
         }
	 Lalias1=ltext;  break; /* --=? */
	 case 20:  /*  Put @KA ( End of Alias ) to text */
	   if(Lproc){
	    /*head: complete HEAD of procedure */
            Ipw=Talbeg[Ndef-2];
            memcpy(text+ltext,text+Ipw,5);ltext+=5;
            memcpy(text+ltext,Conl,9);ltext+=9;
            _TextCCp(_Ko);
            Lproc=0;
	   } else if( Lcall){
            text[ltext]=_S_Blank;++ltext;
            CHK(ltext);
            /*retc: complete call and return after call */
              /*  after @Procname */
             ++Ncall;
	     Iproc=-1; Found7=0; Lalias=ltext-Begnam-1;
             while( Iproc< Nproc && !Found7) {
            ++Iproc; i=Ndefpr[Iproc];
	       if( Lalias==Palias[i+1]-Palias[i] ){
                  /*1: set Found7=.true. if Procname==Nalias() */
		    Jp7=0; Found7=1; KP7=Palias[i];
		    while( (Jp7<Lalias) && Found7 ) {
		      Jp7=Jp7+1;
		      Found7=ToUpper(text[Begnam+Jp7-1])==Nalias[KP7]; /* ? */
                      ++KP7;
                    }
               }
             } /*  Iproc number of procedure needed or Iproc==Nproc */
             if( Found7 )  {
               ++Ret[Iproc];
               if( Ret[Iproc]==1 )  {
                  Nc1st[Iproc]=Ncall;
               } else {
		  i=Lastc[Iproc]; Nextc[i]=Ncall;
               }
               Lastc[Iproc]=Ncall;
               /*2: Send into TEXT 'RETRT'//'value of Iproc',
                    the symbol '=', value of RET(IPROC), @KO,
                    GOTO 'Label of procname' @ko,
                    Llab:continue@ko */
                  KP7=Ndefpr[Iproc]+1;
                  Ipw=Talbeg[KP7];
                  memcpy(text+Begnam,text+Ipw,6);ltext=Begnam+6;
                  text[ltext]=_Equal; ++ltext;
                  CHK(ltext);
                  Inr=Ret[Iproc];
                  NumRetrt();
		  for(i=Ipw;i<6;++i){
		   _TextC2p(Retrt[i]);
                  }
                  _TextCCp(_Ko);
                  if( Fort )  {
                     memcpy(text+ltext,Fblank,6);ltext+=6;
                  }
                  memcpy(text+ltext,Lgoto,4);ltext+=4;
                  CHK(ltext);
                  Jp7=Ndefpr[Iproc]; KP7=Talbeg[Jp7];
                  memcpy(text+ltext,text+KP7,5);ltext+=5;
                  _TextCCp(_Ko);
                  Remlab=Llab;     /*  Generate Num. Label */
                  for(isamp=1;isamp<=5;++isamp){
                       C2=Remlab/10000;
                       Remlab=(Remlab%10000)*10;C2=C2+'0';
                       _TextC2;
                    }
                  memcpy(text+ltext,Conl,9) ; ltext+=9; /*  :CONTINUE; */
                  _TextCCp(_Ko);

               Retlab[Ncall]=Llab; --Llab;
             } else {
               Dtcdia(Diagn,23,Zero,&Idiag,&Retcod);
             }
             Lcall=0;


           } else {
          /*UPalias: go backward and capitalize alias name *>; /* --? */
            { Integer i;
                 for(i=Lalias1;i<ltext;++i) text[i]=ToUpper(text[i]);
            }
              text[ltext]=_S_Blank;++ltext;
              CHK(ltext);
           }
           break ;
	 case 21: ++NCOMEN;
         if( Outcom ) {
            if( NCOMEN==1 ) {
              C2=_Bcm; _TextCC;
             }
            S=12;
          } break;
	 case 22:  if( NCOMEN==0 ) {         /*  C1 --> text */
              C2=C1; _TextC2
          } else {
             if( Outcom ) {
               S=12 ;
             } else {
               S=11 ;
             }
           } break;
	 case 23:  if(NCOMEN!=0) S=15;
          if( Outcom ) {
            text[ltext]=_Symrdr;++ltext;
            CHK(ltext);
           } break ;
	 case 24:
            if( NCOMEN!=0 ) {
              --NCOMEN;
              if( NCOMEN==0 ) {
                 S=1;
                 if( Outcom ) {
                    C2=_Ecm; _TextCC;
                 }
               }
             } break;
	 case 25:  if( NCOMEN==0 ) {
             S=1;
             if( Outcom ) {
                C2=_Ecm; _TextCC;
              }
          } else {
            if(Outcom) S=12;
           }
          if( Llind != 0 ) {
          /*K: Include the Request with local index from Lind
                  beginning in Plind(Lnodes) of the length LLIND
                  into the TREE. Send control code @TR into text *>*/;

 /*1: If among the son nodes to the Node Cnode there exists
      Loc.index=Cind() Then Foundk=.True., Else  Foundk=.False. */
 Ipk1=Ason[Cnode]; Cpk1=Nofson[Cnode]; Foundk=0; /*  INT Ipk1,Cpk1 */
 Ipk2=Plind[Lnodes];
 Llind=Clind-Ipk2;  /*  Length of current Node Local index */
   while( Cpk1>0 && !Foundk) {
    if( Llind==Plind[Ipk1+1]-Plind[Ipk1] ) {
      Ip7=0;Foundk=1;Jp7=Plind[Ipk1];
      while( Ip7<Llind && Foundk ){
       if(Lind[Jp7+Ip7]!=Lind[Ipk2+Ip7]) Foundk=0;
       Ip7++;
      }
    } ;
    Ipk1=Ipk1+1; Cpk1=Cpk1-1;
   }

 if( Foundk )  {
   /*2: Diagn: Local Index Repeated */
   Dtcdia(Diagn,2,Zero,&Idiag,&Retcod);
   Clind=Clind-Llind;

 } else {
   /*3: Add to NODES New String, Increase Cnode.Nofson .
 Put code @Tr (request) to Text */
 if( Trace==_S_Plus ) {
   Tnode[Lnodes]=_S_Plus;
 } else {
   Tnode[Lnodes]=_S_Minus;
  } ;
 if( (Fort || Pascal) && Card[Irdr+1]!=_Cr ) {
   Opcon[Lnodes]=_S_Plus;
 } else {
   Opcon[Lnodes]=_S_Minus;
  }
 Headln[Lnodes]=LinReq; Atext[Lnodes]=0;
 Alspre[Lnodes]=Alsprc; /*  current alias predecessor */
 Ason[Lnodes]=0; Nofson[Lnodes]=0;
 Lnodes=Lnodes+1;
 Plind[Lnodes]=Clind; Nofson[Cnode]=Nofson[Cnode]+1;
 C2=_Tr; _TextCC ;
  }
 Llind=0;

           } break;
     case 26:  text[ltext]=_Symrdr;++ltext; CHK(ltext);/*  not changed */
          break ;
	 case 27:  /*  Ada comment */
	  if(NCOMEN==0) {
           if(Fort) Alsrf=0; /* --=2 */
           if( Outcom && (Sals==0  ||  Sals==5)) {
              C2=_Bcm; _TextCC; S=17;  /*  Begin of comment */
              if(!Fort) Rf=1;
           } else {
             if( (Pascal || Fort) && Irdr!=1 ) {
               C2=_Ko; _TextCC;
             }
             Irdr=lcard;
           }
          } else {
             if( Outcom ) 
              S=12 ;
             else
              S=11 ;  
          }
          break ;
	 case 28:  if( Tnode[Cnode]==_S_Plus ){
             Enter=0; TRACE();  /* 'Leaving Node' Hcard(1:Pos(':')) */
             }
             C2=Cc;_TextCC ; break ;
	 case 29:  if(  SR==_Cr ){
             C2=_Ecm; _TextCC; S=1 ;    /*  End of ADA comment */
          } else {
             text[ltext]=_Symrdr;++ltext; CHK(ltext); /*  not changed */
           } break ;
	 case 30:  if( Outcom ){
            if( S!=13) S=12;
             text[ltext]=_Symrdr;++ltext;CHK(ltext);
            } break;
	 case 31:  Clind=max(Clind-Llind,2);
          if( Outcom ) {
            C2=_Bcm; _TextCC; S=12;
            Irdr-=Llind+1; /*  restore Irdr */
           }
          Llind=0; break ;
	 case 32:
          /*P: accumulate FileName - Fileid for Include , count Nwords */
         if(_Symrdr==_S_Semicol) { S=1; goto _P33 ; } else
         if( Lastch==_S_Blank && _Symrdr!=_S_Blank )
           {Nwords=Nwords+1;Lastch=_Symrdr;
            ifn=ifn+1;
            #ifdef unix
             FileName[ifn]=SR;
            #else
             FileName[ifn]=ToUpper(SR);
            #endif
            } else
         if( Lastch==_S_Blank && _Symrdr==_S_Blank) { Lastch=_Symrdr ;}
         else {Lastch=_Symrdr; ifn=ifn+1;
            #ifdef unix
             FileName[ifn]=SR;
            #else
             FileName[ifn]=ToUpper(SR);
            #endif
                  
         }

          break;
	 case 33:  _P33:;
          /*R: Open new include Level, Check Fileid *>*/
          /*extension: Does FileName complete ?  DOS */
    { int L;
    L=ifn;
    FileName[L+1]=0;
    while( L>1 && FileName[L] != _Point && FileName[L] != DIR_DELIMITER ) --L;
    if( FileName[L]==_Point && L == ifn) {
        strcpy(FileName+1+ifn,"inc");
        #ifdef _DEBUG_TRF_
        printf("Include = %s\n",FileName+1);
        #endif
        ifn=ifn+3;
    }else if (FileName[L]==DIR_DELIMITER ||  L==1 ) {
        strcpy(FileName+1+ifn,".inc");ifn=ifn+4;
        #ifdef _DEBUG_TRF_
        printf("Include = %s\n",FileName+1);
        #endif
    }
    }
    //old one if((Include[Incl00+1]=fopen(FileName+1,"r"))==NULL){  /*  Include Failed */
    if((Include[Incl00+1]=fopenUsingPath(FileName+1,"r"))==NULL){  /*  Include Failed */
     memset(FileName,_S_Blank,ifn);
     Dtcdia(Diagn,12,Zero,&Idiag,&Retcod);
    } else {
     memset(FileName,_S_Blank,ifn);
     Incl00++;   /*  new Level */
     Oldlis[Incl00]=List;Oldlst[Incl00]=Lst; /*  Save prt_mode */
       List=Lists;Lst=Lsts;   /*  Define New prt_mode */
       Irdr=lcard; Rf=1;
       Anls=9;goto Lab1000; /*  Rdr prints card and diagn */
       Lab2009: ;
       fprintf(Include[LISTING],"====>   Level( %1d )\n", Incl00); Mark=_S_Plus;
    }
          break;
         case 34:
         Lind[Clind]=ToUpper(SR); Clind=Clind+1; Llind=Llind+1;
          break;
         case 35: 
          if (SQuote2== _Symrdr /* --=22 ? */ ) S=1 ;
           text[ltext]= _Symrdr ; ++ltext; CHK(ltext); break;
         case 36:
          SQuote2=_Symrdr; text[ltext]= _Symrdr ; ++ltext; CHK(ltext); break;
         case 37: // for =>
         /*B: Put C1 in text */
          C2=C1; if( Wspec )  {  _TextCC; Wspec=0;
                 } else {  _TextC2 ; }
       text[ltext]=SR; ++ltext; CHK(ltext);
       break;
        
      }


      if( max(Rf,Alsrf)==0 ) {
        Anls=3; goto Lab1000; Lab2003:;  /*  Resume Rdr */
      }
    }
    /*3: Beginning from Card find 1-st correct header or @KT.
           If Header then Process it, Obtain in C 1-st symbol of text of
           Node or @KT, in Cnode - Number of Node of this Node */
 /* VAR: FOUND,Erhead,Areq,Enhead,Path,RPath,Diagn2(30)-CM%2B */
 /* Logical Found- PRI3NAK TOGO,4TO NAYDEN TEKCT U3LA POSLE
   PRAVIL@NOGO 3AGOLOVKA, CHARACTER Diagn2 - Diagnostic Messages  */
 if( Opcon[Cnode]==_S_Plus )  {
      _Symbol=text[ltext-3];
    if( _Symbol==_Ko )  {    /*  delete @KO */
      text[ltext-3]=text[ltext-1]; /*  here @KY or @KT */
      ltext=ltext-2 ;
    }
 }
 Found=0;
 while(!Found && (SR != _Kt ) ){
   /*1: PROANALI3IROVAT@ TEKCT OPREDELJEMOGO GLOB.INDEKSA B Card.
        ESLI OH NEPRAVIL@NYY , TO Erhead = .True. ,
        INA4E , ESLI OH KON4AETSJ HA ':' , TO DOFORMIROVAT@ COOTB.
        ELEMENT NODES , SDELAT@ EGO TEKUQIM U3LOM , POLU4IT@ B Areq
        HOMEP STROKI TREBOVANIJ HA ETOT U3EL B NODES,
        FOUND=.True.,Erhead=.False.
        ESLI OH KON4AETSJ HA '=',TO POLU4IT@ B Areq HOMEP STROKI
        TREBOVANIJ HA ETOT U3EL , FOUND=Erhead=.False. */
 /* INT Path - Path in Tree from ROOT NODE until Node with Global index
    from Card finishing at symbol C Number Enhead.
    INT Enhead - current position in Card. See %2B
    Condition  Q2331:
    Glind - some left piece of Global index from Header in Card
    Path  - some path from Root Node in NODES
    such that:
       Either Erhead = .False. and Glind is a Sequence of Local
       indeces on the way to Path , or
       Erhead = .True. (Error in Header).
       The Path includes all elements of NODES from Root to the element
       of NODES with Global index Glind  */
 /*2: Make Q2331 .True. when Glind is empty and Path=Root */
 Enhead=0; Path=1; Erhead=0; Sinit=1;/*  Initial state in DOWN */
 /*  Glind is empty */

 while (!Erhead & /*3: Glind is not all defined Global index */
  ( Card[Enhead+1]!=_Colon && Card[Enhead+1]!=_Equal )

  ){
   /*4: Add to Glind next symbol of Header for Q2331 invariant */
 Down(); Lab2331:;
 }
     if( !Erhead ) {
    /*5: Obtain in Areq number of Line with Request  */
      Areq=Headln[Path];

    if(Card[Enhead+1]==_Colon /*6: Defined Global index is finished by ':' */){
       Found=1;
       /*7: Complete formation of element of NODES number Path
            and make it current Node */
   if( Atext[Path]==0 ) {
     Atext[Path]=ltext; Ason[Path]=Lnodes;
     Nofson[Path]=0; Headln[Path]=Cardn; Cnode=Path;
     Alsprc=Alspre[Path];
     Trace=Tnode[Path];
     _Symbol=ToUpper(Card[Enhead+2]); /*  Up control character */
     if(_Symbol==Offtrc) Tnode[Path]=_S_Minus;
     if(_Symbol==Lstno)  List=1;
     if(_Symbol==Lstyes) List=1;
     if( Trace==_S_Plus && _Symbol!=Offtrc ) {
       Nhead=Enhead+2;
       memcpy(Hcard,Card,Nhead);
       Enter=1; TRACE(); /*  'Entering Node ',Card(1:Pos(':')) */
     } ;
   } else {
     Gfound=1; Erhead=1;
   }
  }
  }


   if( Erhead ) {
      /*2: B Diagn:'HET TREB.HA U3EL';B Diagn2:'TEKCT HE ANALI3IR.'*/
      Dtcdia(Diagn2,5,Zero,&Idiag,&Retcod);
 if( Gfound )  {
   Dtcdia(Diagn,22,Headln[Path],&Idiag,&Retcod);
   Gfound=0; Found=0;
 } else {
   Dtcdia(Diagn,3,Zero,&Idiag,&Retcod);
  }
   } else {
      /*4: B Diagn 'U3EL 3ATREBOVAN B CTPOKE',Areq */
       Dtcdia(Diagn,4,Areq,&Idiag,&Retcod);
      if( Found ) {
        /*5: POLU4IT@ B SR PERVYY SIMVOL TEKCTA U3LA */
       Anls=5; goto Lab1000; Lab2005: ;   /*  RESUME RDR */
      } else {
        /*6: PROANALI3IROVAT@ OPREDELJWQIY GLOB.INDEKS
             ESLI OH PRAVIL@NYY , TO SVJ3AT@ OPREDELJEMYY U3EL
             C TEKCTOM I NASLEDNYMI U3LAMI K OPREDELJWQEMU ,
	     PODGOTOVIT@ B Diagn2 SOOBQENIE OB ETOY SVJ3I.
	     ESLI OH NEPRAVIL@NYY , TO PODGOTOVIT@ B Diagn2 SOOBQ.
             OB O6IBKE. */
 RPath=Path; /*  Store Path of Defined Global Index */
 /*  Now  Path is the part of Path from Root to Request for Node  with */
 /*  Defining Global index , Glind is the part of Defining Global index */
 /*  Invariant Q2336 as Q2331, but instead of Defined - Defining. */
 /*2: SDELAT@ Q2336 ISTINNYM PRI PUSTOM Glind I Path=KOREN@ */
 Enhead=Enhead+1; Path=1; Sinit=1; /*  Initial state in DOWN */

 while ( !Erhead && Card[Enhead+1]!=_Colon /*3: Glind is not completed */ ) {
   /*4: RAS6IRIT@ Glind PRI INVARIANTNOM Q2336 */
 Down(); Lab2336:;
 }
 if( !Erhead ) {
   /*5: ESLI OPREDELJWQIY GLOB.INDEKS UKA3YVAET HA RA3RABOTANNYY U3EL ,
        TO B NODES DLJ OPREDELJEMOGO GLOB.INDEKSA OSTAVIT@ LOK.INDEKS
        I Headln EGO ZE , Atext, Ason I Nofson - OPREDELJWQEGO , I
	PODGOTOVIT@ B Diagn2 SOOBQENIE 'RA3RABOTKA U3LA B CTPOKE' Headln1,
        GDE Headln1 - V3JTO I3 NODES DLJ OPREDELJWQEGO U3LA ,
	INA4E - B Diagn2 :' HE RA3RAB. U3EL I3 STROKI' Headln1 */
 Areq=Headln[Path];
 _Symbol=ToUpper(Card[Enhead+2]);  /*  Up control character */
 if(_Symbol==Lstno)  List=0;
 if(_Symbol==Lstyes) List=1;
 if( Atext[Path]!=0 )  {   /*  Node is Ready */
   Atext[RPath]=Atext[Path]; Ason[RPath]=Ason[Path];
   Nofson[RPath]=Nofson[Path]; Headln[RPath]=Cardn;
   Dtcdia(Diagn2,6,Areq,&Idiag,&Retcod);
 } else {
   Dtcdia(Diagn2,7,Areq,&Idiag,&Retcod);
   Refnfn=1;
  }
 } else {
    /*6: Diagn2: reference to unrequested Node */
    Dtcdia(Diagn2,8,Zero,&Idiag,&Retcod);Refnfn=1;
 }
      }
   }
   if( !Found )  {
     /*3: Return to RDR (Rdr Prints  Card & Diagn).
	  Then Prints Diagn2, pass by RDR until @ky or @KT */
 Anls=6; goto Lab1000; Lab2006:;   /*  RESUME RDR */
 fprintf(Include[LISTING],"%-34s\n",Diagn2);
 if(Refnfn) fprintf(stderr,"%-34s\n",Diagn2);
 Refnfn=0;
 while( (SR!=_Kt)&&(SR!=_Ky) ) {
   Anls=7; goto Lab1000; Lab2007: ; /*  RESUME RDR */
 }
   }
 }


     }

    /* return */
    *cardn=Cardn;
    Nbyte=ltext; Nodtot=Lnodes-1;

     return;
   }
/* END */
