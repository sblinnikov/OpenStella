 /*  Preprocessor of structure program design for FORTRAN.
  Input  file 01 contains the design tree text in punch card (i.e. 80 pos.
  strings) format.
  Output file 02 is the text of resulting program in
  FORTRAN (or C, Rexx etc).
  File 06 - contains the  design tree listing and diagnostics.
  Version for Microsoft Visual C++ cl and Borland bcc32 compilers;
  a timer is defined*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define _MAIN_DEF_
#ifdef __CLDOS__
#include <time.h>
#include <sys/timeb.h>
#endif

#include "chargen.h"
#include "trfgen.h"
#include "tree.h"
#include "align.h"

extern void pass1(int *NewTree,unsigned *cardn);
extern void pass2(void);

#ifndef MAX_FILE_NAME
 #define MAX_FILE_NAME 256
#endif
#if MAX_FILE_NAME<32
  #undef MAX_FILENAME
  #define MAX_FILE_NAME 256
#endif

static char fname[MAX_FILE_NAME],Temp[MAX_FILE_NAME];

static unsigned cardn=0;
static int LTemp;
static int NewTree;
static int Concod,Totcod;
#define Lstchar Lst
int Lst ;

/* if macros max is not defined in stdlib.h (Borland C++ & e.t.c ,
     we use function max(x,y);
  if function is already declared in stdlib , use -DNOMAX in command line */
#if !defined(NOMAX) && !defined(max)
 int max(int x,int y) {
  return x<y?y:x;
 }
#endif


void CheckText(Integer4 ltext){
 if(ltext>=NTEXTMAX){
  fprintf(stderr,"Internal buffer is full,increase const NTEXTMAX\n");
  exit(32);
 }else{
 // fprintf(stderr,"ltext %8d\n",ltext);
    }
}

/* Yaroslav Urzhumov addendum -
 function testing a character to be an empty space
*/
int isBlank(char c)
{if (c==' '||c=='\n'||c=='\t') return 1;
 return 0;
}

int substring(char* dest, char* src,int i1,int i2)
{int k;
 if (!dest || !src) return-1;
 if (i2<=i1) {dest[0]=0;return 0;}
 for(k=i1;k<i2;k++)
 dest[k-i1]=src[k];
 dest[i2-i1]=0;
 return i2-i1;
}


/* Yaroslav
// function deletes "blank" symbols at end of string
*/
void deleteBlank(char* str)
{int i,l=strlen(str);
 char newstr[500];  newstr[0]=0;
//delete whitespaces or newline characters at end
 for(i=l-1;(i>=0)&&isBlank(str[i]);i--){}
 str[i+1]=0;//cut off the string

 //delete whitespaces or newline characters at beginning
 for(i=0;i<strlen(str)&&isBlank(str[i]);i++){}
 substring(newstr,str,i,strlen(str));
 strcpy(str,newstr);

}

/* Yaroslav Urzhumov
 -- simple upgrade of fopen function
This function tries to open the include file in the current directory,
and if it is not found, reads a list of paths from the variable "PATH"
trying to open a file path+filename.

The paths for include search are written in .trfrc (so trf.cfg is not needed
anymore).
Since all uncommented lines in  .trfrc are executed one has to write paths as
comments, e.g.:

# PATH
# ..\src\
# ..\eve\
# ENDPATH

Don't forget to provide slash (file separator) at end of each
pathname! Absence of a slash results in skip of the path (as
an incorrect pathname).

To comment this path out just use one more hash or any special symbol, e.g.
## ..\coll\ #this is a commented path
# @@@ this is also a comment in a pathlist
One can place # PATH ... # ENDPATH list wherever he likes in .trfrc but
only once - the second entry of # PATH will be ignored!
Follow exactly the template (in particular, write exactly
# PATH
but not
#PATH
and not
 # PATH
and not
# path
).

In Urzhumov's version .trfrc (or 'path' file in older version) was looked for
only in the current directory.
Blinnikov allowed the serach for .trfrc in C:\util etc exactly as it is done by
Popolitov in trf.c/trfu.c .

For older version with 'path':
Example "path":

c:\program files\stella\  #full path, Win32 conventions
..\src\                   #relative path from upper directory
.\run\                    #relative path from current directory

Don't leave blanks in the beginning of line. Don't make any comments in "path".
Erroneous pathname will be actually ignored, because the file will not be opened
with such a name.

*/

FILE *fopenUsingPath(const char *filename, const char *mode)
{      FILE* attempt=fopen(filename,mode);
       char* retVal;
       FILE* pathInfo;
#ifndef BUFFER_SIZE
 #define BUFFER_SIZE 1024
#endif
  #define RCFILENAME ".trfrc"
char *rcpath[]= {
#ifndef __MSDOS__
		    "/usr/bin",
                    "/usr/local/bin",
                    "/usr/local/lib",
                    "/var/trf"
#else
 		    "c:\\util\\",
 		    "c:\\utils\\"
#endif
                };
#define rcpathsize  (sizeof(rcpath)/sizeof(rcpath[0]))
#ifdef __MSDOS__
/* system() prototype */
#include <process.h>
#else
extern char **environ;
#endif

  int i,j;
  char buffer[BUFFER_SIZE];
  FILE *in;
       char* pathStart="# PATH";//change the comment starting pathlist
       char* pathEnd="# ENDPATH";//the comment with ends up pathlist
       if (attempt) return attempt;// open is OK in this folder


  *buffer=0;
  /* prepare commands for compilation by trefor and fortran */
  if((in=fopen(RCFILENAME,"r"))==NULL){
   i=0;
#ifndef __MSDOS__
   while(environ[i]){
    if(strlen(environ[i])>5 &&
     (!memcmp(environ[i],"home=",5) || !memcmp(environ[i],"HOME=",5)))
    {
     for(j=5;*(environ[i]+j)!=0 && j<BUFFER_SIZE+4-sizeof(RCFILENAME);++j)
      buffer[j-5]=*(environ[i]+j);
     buffer[j-5]=0;
     if(strlen(buffer)>0 && buffer[strlen(buffer)-1]!='/')
       strcat(buffer,"/");
     strcat(buffer,RCFILENAME);
     in=fopen(buffer,"r");
     #ifdef DEBUG
      fprintf(stderr,"Trying %s\n",buffer);
     #endif
     break;
    }
    else { ++i;}
   }
#endif
   if(in==NULL){
    for(i=0;i<rcpathsize;++i){
     if(strlen(rcpath[i])<BUFFER_SIZE-sizeof(RCFILENAME)){
     strcpy(buffer,rcpath[i]);
     if(strlen(buffer)>0 && buffer[strlen(buffer)-1]!='/')
       strcat(buffer,"/");
     strcat(buffer,RCFILENAME);
     in=fopen(buffer,"r");
     #ifdef DEBUG
      fprintf(stderr,"Trying %s\n",buffer);
     #endif
     if(in!=NULL)
      break;
     }
    }
   }

  }
       pathInfo=fopen(buffer,"r");//search for pathlist in trf config file
#ifdef DEBUG
        fprintf(stderr,"pathInfo .trfrc %s\n",buffer);
#endif

       if (pathInfo==NULL) return NULL; //now you can honestly exit

       {char path[200];
        retVal= (char*)pathInfo;
        //Find the beginning of pathlist appended to this directory

        while(retVal!=NULL)
        { path[0]=0;
         retVal=fgets(path,200,pathInfo);
         deleteBlank(path);
         if (strcmp(path,pathStart)) continue;
         else break;
        }

        // Start reading pathlist
        while(retVal!=NULL && attempt==NULL)
        {
         path[0]=0;
         retVal=fgets(path,200,pathInfo);
         deleteBlank(path);
         if (strlen(path)<1) continue;//retry reading from the pathfile
         if (!strcmp(path,pathEnd)) break;
         path[0]=' ';
         deleteBlank(path);
         strcat(path,filename);
         attempt=fopen(path,mode);
        }//endwhile
        fclose(pathInfo);
        return attempt;
       }

}

/*
 fopenUsingPath() is used in trefor.c (to open .trf) and pass.c (to open .inc)
*/



int main(int argc,char **argv){
    Integer4 nodall,Ntrees,inbyte,iconcd;
    unsigned Ttime,CPUtime,Btime;
    char DateTime[40];
/* filename path '1'  */
 /***************** Date and time *************************/

#ifdef __CLDOS__
  time_t ltime;
  struct tm *TimeBeg,*TimeEnd,*Date;
  struct _timeb tstruct;
  time( &ltime ); // gets ltime
  TimeBeg=localtime( &ltime ); // transforms to tm struct
  Date=localtime( &ltime );
  sprintf(DateTime,"Date %02d/%02d/%02d  Time %02d:%02d:%02d",
  Date->tm_mday,Date->tm_mon,Date->tm_year,
  TimeBeg->tm_hour,TimeBeg->tm_min,TimeBeg->tm_sec);
  _ftime( &tstruct );
  Btime=(tstruct.time)*1000+( tstruct.millitm );
#else
#ifdef __MSDOS__
  struct time TimeBeg,TimeEnd;
  struct date Date;
   gettime(&TimeBeg);
   getdate(&Date);
   sprintf(DateTime,"Date %02d/%02d/%04d  Time %02d:%02d:%02d",
    Date.da_day,Date.da_mon,Date.da_year,TimeBeg.ti_hour ,TimeBeg.ti_min,
    TimeBeg.ti_sec);
#else
#ifdef unix
   time_t TimeBeg,TimeEnd;
   time(&TimeBeg);
   strcpy(DateTime,asctime(localtime(&TimeBeg)));
#endif
#endif
#endif
 /****************** Open file ****************************/
      if(argc<2) return (28); //no filename provided
// Yaroslav Urzhumov
// In the future one may place here a set of file opening trials
// Try first in the current dir, then in the list of directories given in a special file
// (".trfrc", for example) or in the trf option:
// trf  -I virtualpathname1,vpn2,vpn3 filename.trf
// The first opportunity does not require any modifications in trf-options processing

      Include[0]=fopenUsingPath(argv[1],"r");


      if(Include[0]==NULL) //retry in different directory if path options are provided
         exit(28); //  file not found
      if(argc<3)
	strcpy(Temp,CURRENT_DIR);
      else
	strcpy(Temp,argv[2]);
      if(argc<4)
	Lstchar='1';
      else
	Lstchar=argv[3][0];
      Lstchar=Lstchar=='1'?1:0;
      LTemp=strlen(Temp);
	if (
      #if !(COLON_IN_NAME)
	Temp[LTemp-1]!=':' &&
      #endif
	Temp[LTemp-1]!=DIR_DELIMITER ) {
	  LTemp++;
	  strcat(Temp,sDIR_DELIMITER);
	}
	strcpy(fname,Temp);
	{int i;
	   i=strlen(argv[1])-1;
	   while(i>=0  && argv[1][i] != '.'  ) --i;
	   if(i>=0){
	     memcpy(fname+LTemp,argv[1],i+1);
	     memcpy(Temp+LTemp, argv[1],i+1);
         strcpy(fname+LTemp+i+1,LST_EXTENTION);
         strcpy(Temp+LTemp+i+1,FOR_EXTENTION);
	   }
	}
	Include[OUTPUT]=fopen(Temp,"w");
	if(Include[OUTPUT]==NULL){
	 fprintf(stderr,"Cannot open output file %s\n",Temp);
	 exit(28);
	}
	if ( Lstchar==1 )
	   Include[LISTING]=fopen(fname,"w");
	else
	   Include[LISTING]=fopen(NULL_FILE,"w");
	if(Include[LISTING]==NULL){
	 fprintf(stderr,"Cannot open output file %s\n",Temp);
     return 28;
	}
#ifdef POINTER
 text=(unsigned char *)malloc((size_t)NTEXTMAX);
 /* Local indeces of nodes */
 Lind=(Integer2*)malloc((LINDMAX+5*NODEMAX+2*NDEFMAX+2*CALLMAX+PROCMAX)*sizeof(Integer2));
 Atext=(Integer*)malloc((NODEMAX+2*NDEFMAX)*sizeof(Integer)); /*Addresses of Node texts */
 if(!text || !Lind || !Atext) {
   fprintf(stderr,"Not enough memory for compiler buffer\n");
   return 28;
 }
 memset((void*)text,0,NTEXTMAX);
 memset((void*)Lind,0,(LINDMAX+5*NODEMAX+2*NDEFMAX+2*CALLMAX+PROCMAX)*sizeof(Integer2));
 memset((void*)Atext,0,(NODEMAX+2*NDEFMAX)*sizeof(Integer) );
 Plind=Lind+LINDMAX;           /* Local index pointer */
 Ason=Plind+NODEMAX;           /* Address of Son nodes */
 Nofson=Ason+NODEMAX;          /* Number of Son nodes */
 Headln=Nofson+NODEMAX;        /* Number of Tree line where node head is kept */
 Alspre=Headln+NODEMAX;        /* alias predecessor in given node */
 Alpred=Alspre+NODEMAX;        /* alias predecessor */
 Palias=Alpred+NDEFMAX;        /* pointer to beginning of i-th alias name */
 Nc1st=Palias+NDEFMAX;         /* first call of procedure */
 Nextc=Nc1st+PROCMAX;          /* next call of procedure */
 Retlab=Nextc+CALLMAX;         /* buffer for return labels */
 Talbeg=Atext+NODEMAX;         /* pointer to beginning of i-th alias def. in TEXT */
 Talfin=Talbeg+NDEFMAX;        /* pointer to next position after end */
#endif

 Numerr=0;Retcod=1;
 cardn=0;nodall=0; Ttime=0;iconcd=0;inbyte=0; Ntrees=0;
 fprintf(Include[LISTING],
 "=================================================="
 "======================================================================\n"
 " Version 5.2.3 (May 2009)   C Trefor  %s   File compiled \"%s\"\n"
 "======================================================================"
 "==================================================\n",DateTime,argv[1]);
#ifdef WITH_LOGO
 fprintf(stderr,"C TREFOR (ver 5.2.3) compiling file: \"%s\"\n"
     "Copyright (c) Weinstein et al. 1983-2009.\n",
     argv[1]);
#endif

 do {
    /* Llab=32757; */
   Llab=9999;
   Ndef=NDEF0;
   Ntrees=Ntrees+1;
 #ifdef _DEBUG_TRF_
   printf("Before pass1\n");
 #endif
   pass1(&NewTree,&cardn); /*  PERVYY PROHOD */
 #ifdef _DEBUG_TRF_
   printf("Before pass2\n");
 #endif
   pass2(); /*  VTOROY PROHOD */
 #ifdef _DEBUG_TRF_
   printf("After pass2\n");
 #endif
    switch( Retcod ) {
	  case 1 :  Concod=0 ; break;
	  case 2 :  Concod=4 ; break;
	  case 3 :  Concod=8 ; break;
    }
#ifdef __CLDOS__
   _ftime( &tstruct );
   CPUtime = (tstruct.time)*1000+( tstruct.millitm );
   CPUtime = CPUtime - Btime;
#else
#ifdef __MSDOS__
 gettime(&TimeEnd);
 CPUtime=(((TimeEnd.ti_hour-TimeBeg.ti_hour)*60+
           (TimeEnd.ti_min -TimeBeg.ti_min ))*60+
           (TimeEnd.ti_sec -TimeBeg.ti_sec ))*100+
           (TimeEnd.ti_hund-TimeBeg.ti_hund);
#else
 #ifdef unix
  time(&TimeEnd);
  CPUtime=(TimeEnd-TimeBeg)*100;
 #else
  CPUtime=0;
 #endif
#endif
#endif
 if(Numerr != 0 ) fprintf(Include[LISTING] ,
    " ====>> Count of Trefor syntaxis errors: \'%3d \n" , Numerr);
 if( NewTree || Ntrees>1) {
   fprintf(Include[LISTING],
   " ========================== Trefor compiling time(sec) %u.%03u\n"
   "     Length of compressed text(bytes) - %d"
   "  Condition code = %d       "
   "     Number of nodes -  %4d\n"
   " ==============================================================="
   ,CPUtime/1000u,CPUtime%1000u,Nbyte,Concod,Nodtot);
 }
  nodall=nodall+Nodtot;Ttime=Ttime+CPUtime;inbyte=inbyte+Nbyte;
  iconcd=max(iconcd,Concod); /* -- Total condition code */
  Totcod=max(Totcod,Retcod); /* -- Total return code    */
  TimeBeg=TimeEnd;
 }  while(NewTree) ;
 #ifdef POINTER
  free(text);
  free(Lind);
  free(Atext);
 #endif
 /********************** Print footer *******************************/
 fprintf(Include[LISTING],
 "=================================================="
 "======================================================================\n"
 #ifdef __MSDOS__
 " Number of Trees Compiled -%3ld        "
 "Total Trefor compiling time(sec)  - %4u.%02u     "
 " Total number of nodes -%6ld\n"
 " Highest Condition code=%6ld       "
 " Total Length of compressed text(bytes): %ld "
 " Count for Local indeces: %6ld\n"
 " (c) Copyright  Weinstein et al. 1983-2009\n"
 #else
  #ifdef unix
 " Number of Trees Compiled -%3d        "
 "Total Trefor compiling time(sec)  - %4u.%03u\n     "
 " Total number of nodes -%6d\n"
 " Highest Condition code=%6d       "
 " Total Length of compressed text(bytes): %d "
 " Count for Local indeces: %6d\n"
 " (c) Copyright  Weinstein et al. 1983-2009\n"
  #else
   "Don't know sizeof(Integer4)\n"
  #endif
 #endif
 "=================================================="
 "======================================================================\n"
#ifdef __CLDOS__
 ,Ntrees,(unsigned)(Ttime/1000u),Ttime%1000u,nodall,iconcd,inbyte,Clind);
#else
 ,Ntrees,(unsigned)(Ttime/100u),Ttime%100u,nodall,iconcd,inbyte,Clind);
#endif
 fclose(Include[OUTPUT]);
  if(Lstchar==1)
   fclose(Include[LISTING]);
  fclose(Include[0]);
 switch (Totcod ){
      case 1 : return 0 ;
      case 2 : return 4 ;
      case 3 : return 8 ;
 }
 return 0;
}

