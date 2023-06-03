#ifndef __TREE__
#define __TREE__

#ifdef __WIN32__
#define __MSDOS__  "I work under WinNT but want to leave this code"
#endif
//Under Windows  _WINT_T is usually defined

#ifdef __MSDOS__
#define CURRENT_DIR      ".\\"
#define DIR_DELIMITER   '\\'
#define sDIR_DELIMITER  "\\"
#define COLON_IN_NAME   0
#define NULL_FILE       "NUL"
#define FOR_EXTENTION   "for"
#define LST_EXTENTION   "lst"
/* for time function */
#include <dos.h>
#else
#ifdef unix
#define CURRENT_DIR      "./"
#define DIR_DELIMITER   '/'
#define sDIR_DELIMITER  "/"
#define COLON_IN_NAME   1
#define NULL_FILE       "/dev/null"
#define FOR_EXTENTION   "f"
#define LST_EXTENTION   "lst"
/* for time function */
#include <time.h>
#else
 #error "Operation system is not defined"
#endif
#endif


#ifndef _MAIN_DEF_
 #define EXTERN extern
#else
 #define EXTERN
#endif
#ifdef __MSDOS__
 #if defined(__TURBOC__) || defined(__TSC__)
  #define ___far far
 #else
  #if defined (__ZTC__) || defined(__MSC__)
   #define ___far _far
  #else define ___far
  #endif
 #endif
#else
 #define ___far
#endif
//Works under Borland C++ in Windows
#ifdef __WIN32__
 #ifdef ___far
 #undef ___far
 #endif
#define ___far
#endif

#ifdef POINTER

EXTERN unsigned char  *text /*[NTEXTMAX-1000] */;
 /* The following 9 arrays form the structure of variable NODES: */
EXTERN  Integer2   (*Lind),       /* Local indeces of nodes */
       (*Plind),      /* Local index pointer */
       (*Ason),       /* Address of Son nodes */
       (*Nofson),     /* Number of Son nodes */
       (*Headln),     /* Number of Tree line where node head is kept */
       (*Alspre);     /* alias predecessor in given node */
EXTERN  Integer2 (*Alpred), /* alias predecessor */
	   Alsprc,              /* current alias predecessor */
	   Calias,              /* current free position in ALIAS NAMES */
       (*Palias);  /* pointer to beginning of i-th alias name */
/* _Integer  Nc1st,  /* first call of procedure */
/*           Nextc,  /* next call of procedure */
/*           Retlab; /* buffer for return labels */
EXTERN  Integer2 (*Nc1st),(*Nextc),(*Retlab);
EXTERN  Integer  (*Atext);       /* Addresses of Node texts */
/*Integer Talbeg,               /* pointer to beginning of i-th alias def. in TEXT */
/*        Talfin;               /* pointer to next position after end */
/*                              /*  i-th alias def. in TEXT */
EXTERN  Integer      (*Talbeg),(*Talfin);

#else

EXTERN unsigned char ___far text[NTEXTMAX];
 /* The following 9 arrays form the structure of variable NODES: */
EXTERN  Integer2  ___far Lind[ LINDMAX],       /* Local indeces of nodes */
	   Plind[NODEMAX],      /* Local index pointer */
	   Ason[NODEMAX],       /* Address of Son nodes */
	   Nofson[NODEMAX],     /* Number of Son nodes */
	   Headln[NODEMAX],     /* Number of Tree line where node head is kept */
	   Alspre[NODEMAX];     /* alias predecessor in given node */
EXTERN  Integer2 ___far Alpred[NDEFMAX],               /* alias predecessor */
	   Alsprc,              /* current alias predecessor */
	   Calias,              /* current free position in ALIAS NAMES */
	   Palias[NDEFMAX];              /* pointer to beginning of i-th alias name */
/* _Integer  Nc1st,  /* first call of procedure */
/*           Nextc,  /* next call of procedure */
/*           Retlab; /* buffer for return labels */
EXTERN  Integer2 Nc1st[PROCMAX],Nextc[CALLMAX],Retlab[CALLMAX];
EXTERN  Integer ___far Atext[NODEMAX];       /* Addresses of Node texts */
/*Integer Talbeg,               /* pointer to beginning of i-th alias def. in TEXT */
/*        Talfin;               /* pointer to next position after end */
/*                              /*  i-th alias def. in TEXT */
EXTERN  Integer      Talbeg[NDEFMAX],Talfin[NDEFMAX];
#endif

EXTERN  Integer4 Numerr,Llab,Clind,Ndef,Nbyte,Nodtot;
EXTERN int Retcod
#ifdef _MAIN_DEF_
=0
#endif
;


EXTERN Character Nalias[LDEFMAX];             /* NAMES of aliases */

EXTERN  Character Retrt[7]
#ifdef _MAIN_DEF_
= {'I','6','R',' ',' ',' ',' '}
#endif
;

#define MAXINCLUDE 6
 #ifdef MAXFILE
 #undef MAXFILE
 #endif
#define MAXFILE    (MAXINCLUDE+2)
#define OUTPUT     (MAXINCLUDE)
#define LISTING    (MAXINCLUDE+1)
EXTERN FILE *Include[MAXFILE];

EXTERN void CheckText(Integer4 ltext);
#define CHK(parm)  CheckText(parm)

extern unsigned ToUpper(unsigned);

#endif
