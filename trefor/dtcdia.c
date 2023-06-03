#include <string.h>
#include <stdlib.h>

/*#include "chargen.h"*/
/*#include "trfgen.h"*/

#if !defined(max) && !defined(NOMAX)
extern max(int,int);
#endif


 static char *Ttext[] = {
   "Error in service word             ",
   "Local index repeated              ",
   "   The node is not requested      ",
   "   The node requested in line    *",
   "   Text ignored until the node end",
   "   Its  design begins in line    *",
   "No design for node from line     *",
   "Reference to nonexistent node     ",
   "Case or Select not opened.        ",
   "Alias not identified              ",
   "Unrecognizable symbol in Fileid.  ",
   "Unable to open include file.      ",
   "Caution: TREFOR TRACE active!     ",
   "Caution: COMMENTS will be output! ",
   "Deflist basis is too short        ",
   "Forbidden alias definition        ",
   "Current tree completed.           ",
   "Include level e xceeds max.level! ",
   "Print full listing forced.        ",
   "Warning:Unknown service word !!!  ",
   "Print full listing started.       ",
   "   Node head already in line     *",
   "Procedure not found               "
   };

 void Dtcdia(unsigned char *Diagn,int Ntext,int Param,int *Idiag,int *Retcod);

 void Dtcdia(unsigned char *Diagn,int Ntext,int Param,int *Idiag,int *Retcod){
   int I5,J5,K5;

   /*3:PERESLAT@ TEKCT HOMEP NTEXT DLINOY 34 BAYTA I3 TTEX B DIAGN*/
   memcpy((char*)Diagn,Ttext[Ntext-1],strlen(Ttext[Ntext-1]));

   if( Diagn[33]=='*' )  {
     /*4: OTREDAKTIROVAT@ PARAM B PRAVYY KONEC DIAGN */
	Diagn[33]='0'; /*'0'*/ I5=Param; J5=33;
	while( I5!=0 ){
	  /*1: POSLEDWW CIFRU I5 B DIAGN(J5); UMEN@6IT@ I5 B 10 RA3 */
	    K5=I5/10; K5=I5-K5*10+'0'; /*POSL.CIFRA + '0' */
	    Diagn[J5]=K5;  I5=I5/10 ;
	  J5=J5-1 ;
	}
   }
   switch( Ntext ){
	  case 0 : *Idiag=1 ; break ;
	  case 1 : *Retcod=3;*Idiag=2 ; break ;
	  case 2 : *Retcod=3;*Idiag=2 ; break ;
	  case 3 : *Retcod=max(*Retcod,2);*Idiag=3 ; break ;
	  case 5 : *Idiag=1; break ;
	  case 7 : *Retcod=max(*Retcod,2);*Idiag=2; break ;
	  case 8 : *Retcod=max(*Retcod,2);*Idiag=2; break ;
	  case 9 : *Retcod=3;*Idiag=2; break ;
	  case 10: *Retcod=3;*Idiag=2; break ;
	  case 11: *Retcod=3;*Idiag=2; break ;
	  case 12: *Retcod=max(*Retcod,2);*Idiag=2; break ;
	  case 13: *Idiag=3; break ;
	  case 14: *Idiag=3; break ;
	  case 15: *Retcod=3;*Idiag=2; break ;
	  case 16: *Retcod=3;*Idiag=2; break ;
	  case 17: *Idiag=3; break ;
	  case 18: *Idiag=2;*Retcod=3; break ;
	  case 19: *Idiag=1; break ;
	  case 20: *Idiag=1;*Retcod=max(*Retcod,2); break ;
	  case 21: *Idiag=1; break ;
	  case 22: *Idiag=2;*Retcod=3; break ;
	  case 23: *Idiag=2;*Retcod=3; break ;
	  default: break;
   }
}

