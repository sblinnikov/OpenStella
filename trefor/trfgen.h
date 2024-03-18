#ifndef __TRFGEN__
#define __TRFGEN__

/* --     Length of array TEXT integer*4 */
#define NTEXTMAX    2400000 
/* --     Maximum number of Nodes */
#define NODEMAX     2048
/* --     Maximum number of loc. index buffer */
#define LINDMAX     8192
/* --     Upper count for alias names */
#define NDEFMAX     2048
/* --     Buffer for alias names */
#define LDEFMAX     30000
/* --     N of embedded Do-constructions */
#define NDOMAX      64
/* --     N of embedded Case-constructions */
#define NCASEMAX    200
/* --     N of embedded States for DTCF2 */
#define NSTATEMAX   256
/* --     N of Intrinsic Trefor service words */
#define NSW         36
/* --     Maximum length of a service word */
#define LENMAX      16
/* --     Maximum N of all service words */
#define SWMAX       64
/* --     Trefor truncating position */
#define LC          256
/* --     Output truncating position */
#define LCOUT       72
/* --     Lexic classes for DTCF1 */
#define NCLASS      20
/* --     Highest include level */
#define MAXLEVEL     5
/* -- */
#define NDEF0        1
/* --     Maximum depth of NODES STACK */
#define STNODE       500
/* --     Maximum depth of ALIAS STACK */
#define STALS        200
/* --     loc. of literal byte in logical eq. */
#define EQBYTE       1
/* --     Maximum number of procedures */
#define PROCMAX     32
/* --     Maximum number of procedure calls */
#define CALLMAX     256
/* -- Symbol continuation for PASCAL etc... */
#define _S_CONTINUATION  ' '

#endif

