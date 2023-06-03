/*-- T r e f o r   Tuning		 
  --							  by Popolitov V.
**********************************************************************/
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#include "trfgen.h"
#include "trfcode.h"

#define ALIGN_FILE "align.h"

#define    _Do      14
#define    _Od		15
#define    _If		16
#define    _Fi		17
#define    _Then	18
#define    _Else	19
#define    _While	20
#define    _Leave	21
#define    _Iterate 22
#define    _Case	23
#define    _Of		24
#define    _Labcase 25
#define    _Esac	26
#define    _Repeat	27
#define    _Until	28
#define    _Select	29
#define    _Other	30
#define    _End 	31
#define    _Proc	32
#define    _Return	33
#define    _endofTree  36
#define    _OnPrint    36
#define    _OffPrint   36
#define    _Fortran    37
#define    _Trefor	   38
#define    _Pascal	   39
#define    _arbcode    36	 /*  Dummy code for Service word */

  short Aclass[256],Wclass[2][256],Class[256],Tclass[256],
  TCC[256];
  short Slcode[NSW]= {
 _Do,_Od,_If,_Fi,_Then,_Else,_While,_Leave,_Iterate, /*  1 */
 _Of,_Repeat,_Until,_Other, /*	1 */
 _Case,_Select, 		/*	2 */
 _Esac,_End,			/*	3 */
 _Labcase,				/*	4 */
 _Define,_Define,_Define,_Define,/*  5	  _define,_label,_deflist,trace */
 _arbcode,				/*	5	 _outcom */
 _Proc, 				/*	5 */
 _Return,				/*	6 */
 _arbcode,				/*	7 */
 _arbcode,_arbcode, 	/*	8	_include,_includeN */
 _Fortran,				/*	9 */
 _Trefor,				/* 10 */
 _Pascal,_Pascal,_Pascal,	   /* 11	_pascal,_Rexx,_C */
 _arbcode,_arbcode,_arbcode,}; /* 12,13,14	  _onprint,_offprint,_endoftree */
int  Refsw[NSW]={
1,1,1,1,1,1,1,1,1,1,1,1,1,
2,2,
3,3,
4,
5,5,5,5,5,5,
6,
7,
8,8,
9,
10,
11,11,11,
12,13,14};
  char *Sword[NSW]={
   "DO","OD","IF","FI","THEN","ELSE",
   "WHILE","LEAVE","ITERATE","OF","REPEAT",
   "UNTIL","OTHER","CASE","SELECT","ESAC",
   "END","","DEFINE","LABEL","DEFLIST","TRACE",
   "OUTCOM","PROC","RETURN","CALL","INCLUDE",
   "INCLUDEN","FORTRAN","TREFOR","PASCAL",
   "REXX","C","ONPRINT","OFFPRINT","ENDOFTREE"};
  short Pslsl[NSW+1];
  char Tslsl[SWMAX*LENMAX];
  unsigned char Letter[]={
	'a','A','b','B','c','C','d','D',  /* English */
	'e','E','f','F','g','G','h','H',
	'i','I','j','J','k','K','l','L',
	'm','M','n','N','o','O','p','P',
	'q','Q','r','R','s','S','t','T',
	'u','U','v','V','w','W','x','X',
	'y','Y','z','Z'};
  char Digits[10]={'1','2','3','4','5','6','7','8','9','0'};
  int Cpoint, Point;
  char Array1[40];
  static char Array2[40];
  main(){
  FILE *pass1,*pass2,*chargen;
	int i;
    int typenum1,typenum2,typenum3;
    char Array3[40];
    pass1=fopen("pass1dep.h","w");
    pass2=fopen("pass2dep.h","w");
    chargen=fopen("chargen.h","w");
	if(pass1!=NULL && pass2!=NULL && chargen!=NULL){
	for(i=0;i<256;++i){
	 Aclass[i]=8;
	 Class[i]=1;
	 Tclass[i]=15;
	 TCC[i]=0;
     Wclass[0][i]=6;
     Wclass[1][i]=6;
	}
    /*1: Prepare Tclass For DTCF1 */
	for(i=0;i<sizeof(Letter);++i) Tclass[Letter[i]]=6 ;
	for(i=0;i<sizeof(Digits);++i) Tclass[Digits[i]]=2 ;
	Tclass[_Question]=6;/* ? */
    Tclass['h']=7;                                  /* Hollerit. */
    Tclass['H']=7;                                  /* Constant */
	Tclass[_S_Blank]=1;
	Tclass[_Underline]=3;
	Tclass[_Apostrophe]=8;
	Tclass[_S_Minus]=18;
	Tclass[_Equal]=12;
	Tclass[_S_Aster]=13;
	Tclass[_Colon]=14;
	Tclass[_Alias]=16; TCC[_Alias]=_Calias; 		/* _ */
	Tclass[_Slash]=17;								/* / */
	Tclass[_S_Semicol]=11; TCC[_S_Semicol]=_Ko; 	/* ; */
	Tclass[_Cr]=20;
    Tclass[_S_Exclam]=11; TCC[_S_Exclam]=_Or;
	Tclass[_Ampersand]=11; TCC[_Ampersand]=_And;	/* & */
	Tclass[_S_GT]=9;  TCC[_S_GT]=_Gt;
	Tclass[_S_LT]=4;  TCC[_S_LT]=_Lt;				/* < */
	Tclass[_S_NE]=10;  TCC[_S_NE]=_Not; 			/* ^ */
	Tclass[_S_L_Br]=11; TCC[_S_L_Br]=_L_Bracket;	/* [ */
	Tclass[_S_R_Br]=11; TCC[_S_R_Br]=_R_Bracket;	/* ] */
	Tclass[_Kt]=5; TCC[_Kt]=_Kt;
	Tclass[_Ky]=5; TCC[_Ky]=_Ky;
                   TCC[0]=1;           /* Why ? */
fprintf(pass1,"static Integer2 Tclass[256]={\n");
for(i=0;i<256;++i)
 fprintf(pass1,"%2d%s%s",Tclass[i],((i!=255)?",":"};"),((i+1)%20?"":"\n"));
fprintf(pass1,"static Integer2 TCC[256]={\n");
for(i=0;i<256;++i)
 fprintf(pass1,"%2d%s%s",TCC[i],((i!=255)?",":"};"),((i+1)%20?"":"\n"));

    /*A: Prepare Aclass For DTCF1 */
    Aclass[_S_Blank]=1;
    Aclass[_Cr]=1;
    Aclass[_Apostrophe]=2;
    Aclass[_S_Quote]=2;
    Aclass[_Kt]=3; Aclass[_Ky]=3;
    Aclass[_Alias]=4;
    Aclass[_Underline]=5;
    for(i=0;i<sizeof(Letter);++i) Aclass[Letter[i]]=5;
    for(i=0;i<sizeof(Digits);++i) Aclass[Digits[i]]=5;
    Aclass[_Question]=5;/* ? */
    Aclass[_S_Minus]=6;
    Aclass[_Comma]=7;
fprintf(pass1,"static Integer2 Aclass[256]={\n");
for(i=0;i<256;++i)
 fprintf(pass1,"%2d%s%s",Aclass[i],((i!=255)?",":"};"),((i+1)%20?"":"\n"));

/*    _Label _Aclass;
	Write(6,_Aclass) (Aclass(i),i=1,256);
	_Aclass: Format( 1X,'INTEGER*2 ACLASS(256)/',
                     16(/1X,16(i2,',')),'/;' ); */
    /*0: Generate Array Up    */
    /*3: Prepare Class  For Dtcf2(Synt) */
     Class[  _Kt      ] = 2;   /* End of Text */
     Class[  _Gt      ] = 3;   /* 3na*i otno6eniy */
     Class[  _Lt      ] = 3;
     Class[  _Ge      ] = 3;
     Class[  _Le      ] = 3;
     Class[  _Ne      ] = 3;
     Class[  _Eq      ] = 3;
     Class[  _And     ] = 3;
     Class[  _Or      ] = 3;
     Class[  _Not     ] = 3;
     Class[  _Do      ] = 4;    /* Slyzebnye clova */
     Class[  _Od      ] = 5;
     Class[  _If      ] = 6;
     Class[  _Fi      ] = 7;
     Class[  _Then    ] = 8;
     Class[  _Else    ] = 9;
     Class[  _While   ] =10;
     Class[  _Leave   ] =11;
     Class[  _Iterate ] =12;
     Class[  _Case    ] =13;
     Class[  _Of      ] =14;
     Class[  _Labcase ] =15;
     Class[  _Esac    ] =16;
     Class[  _Repeat  ] =17;
     Class[  _Until   ] =18;
     Class[  _Select  ] =19;
     Class[  _Other   ] =20;
     Class[  _End     ] =21;
     Class[  _L_Bracket ] =22;
     Class[  _R_Bracket ] =23;
     Class[_Ko]=24;             /* End of Operator */
     Class[_Proc]=25;           /* Procedure */
     Class[_Return]=26;     /* Procedure */
fprintf(pass2,"static Integer2 CLASS[256]={\n");
for(i=0;i<256;++i)
 fprintf(pass2,"%4d%s%s",Class[i],((i!=255)?",":"};"),((i+1)%12?"":"\n"));

/*    _Label _Class;
	Write(6,_Class) (Class(i),i=1,256);
	_Class: Format( 1X,'INTEGER*2  CLASS(256)/',
                    16(/1X,16(I3,',')),'/;' );*/
  /*4: Prepare Wclass  For Dtcf2(Wtr) */
    Wclass[0][_Dt]=5;              /* : */
    Wclass[0][_Cr]=11;
    Wclass[0][_Attention]=2;
    Wclass[0][_S_Blank]=7;
    for(i=0;i<sizeof(Digits);++i)
      Wclass[0][Digits[i]]=1;
    Wclass[1][_Kt]=3;
    Wclass[1][_Ko]=2;
    Wclass[1][_Er]=4;              /* Error */
    Wclass[1][_Fortran]=8;
    Wclass[1][_Trefor ]=9;
    Wclass[1][_Pascal ]=10;
    Wclass[1][_Bcm    ]=12;
    Wclass[1][_Ecm    ]=13;
fprintf(pass2,"static Integer2 WCLASS[2][256]={\n      ");
for(i=0;i<512;++i)
 fprintf(pass2,"%s%2d%s%s%s",(i%256)==0?"{":"",
  Wclass[i/256][i%256],(i==255)?"}":"",((i!=511)?",":"}};"),((i+1)%16?"":"\n      "));

   /* _Label _Wclass;
	Write(6,_Wclass) ((Wclass(i,j),i=1,256),j=1,2);
	_Wclass: Format( 1X,'INTEGER*2 WCLASS(256,2)/',
		     32(/1X,16(i2,',')),'/;'); */
    i=SWMAX;
    /*5: Prepare service word table Tslsl() and pointers Pslsl() */
   { int Kword;
    Kword=0;  /* The first service word begins */
	Point=1;
    Pslsl[Kword]=Point;
    while( Kword < NSW ) {
	Cpoint=strlen(Sword[Kword]);
	Point+=Cpoint;
	++Kword;
	Pslsl[Kword]=Point;
    }
   }
fprintf(pass1,"static Integer2 Pslsl[%3d]={\n",SWMAX+1);
for(i=0;i<=SWMAX;++i)
 fprintf(pass1,"%3d%s%s",(i<NSW)?Pslsl[i]:Pslsl[NSW],
  ((i!=SWMAX)?",":"};"),((i+1)%15?"":"\n"));
fprintf(pass1,"static char Tslsl[%d]={\n",SWMAX*LENMAX);
Point=0;
for(i=0;i<NSW;++i){
 Cpoint=0;
 while(Sword[i][Cpoint]){
  fprintf(pass1,"\'%c\'%s",Sword[i][Cpoint],(Point+1)%16?",":",\n");
  Point++;
  Cpoint++;
 }
}
while(Point<SWMAX*LENMAX){
 fprintf(pass1,"\' \'%s",Point==(SWMAX*LENMAX-1)?"};\n":(Point+1)%16?",":",\n");
 Point++;
}

fprintf(pass1,"static Integer2 Refsw[%d]={\n",SWMAX);
for(i=0;i<SWMAX;++i)
 fprintf(pass1,"%3d%s%s",(i<NSW)?Refsw[i]:Refsw[NSW-1],
  ((i!=SWMAX-1)?",":"};"),((i+1)%15?"":"\n"));
fprintf(pass1,"static Integer2 Slcode[%d]={\n",SWMAX);
for(i=0;i<SWMAX;++i)
 fprintf(pass1,"%3d%s%s",(i<NSW)?Slcode[i]:Slcode[NSW-1],
  ((i!=SWMAX-1)?",":"};"),((i+1)%15?"":"\n"));
fprintf(pass1,"static Integer2 Order[%d]={\n",SWMAX);
for(i=0;i<SWMAX;++i)
 fprintf(pass1,"%3d%s%s",(i<NSW)?i+1:NSW,
  ((i!=SWMAX-1)?",":"};"),((i+1)%15?"":"\n"));

	/*write: Pslsl(), Tslsl() */
 /*    _Label _F_Pslsl, _F_Tslsl,_F_Tslsl1;
	Write(6,_F_Pslsl) ii+1,(Pslsl(i),i=1,_Nsw+1),
					 (Pslsl(_Nsw+1),i=1,ii-_Nsw);
	_F_Pslsl: Format( 1X,'INTEGER*2 PSLSL(',i3,')/',
			 23(/1X,15(i3,',')) );
	Write(6,_F_Tslsl) _SWmax*_Lenmax,(Tslsl(i),i=1,Point-1),
					  (' ',i=1,_SWmax*_Lenmax-Point+1);
	_F_Tslsl: Format( 1X,'_CHARACTER TSLSL(',i4,')/',
		      100(/1X,16('''',A1,'''',',')) );*/

    /*6: Prepare service word code table Slcode(), Refsw(), Order() */


/*    _Label _F_Refsw,_F_Slcode,_F_Order;
	Write(6,_F_Refsw) ii,(Refsw(i),i=1,_Nsw),
						 (Refsw(_Nsw),i=1,ii-_Nsw);
	Write(6,_F_Slcode)ii,(Slcode(i),i=1,_Nsw),
						 (Slcode(_Nsw),i=1,ii-_Nsw);
	Write(6,_F_Order) ii,(I,i=1,_Nsw),
						 (_Nsw,i=1,ii-_Nsw);
	_F_Refsw: Format( 1X,'INTEGER*2 REFSW(',i3,')/',23(/1X,15(i3,',')) );
	_F_Slcode:Format( 1X,'INTEGER*2 SLCODE(',i3,')/',23(/,1X,15(i3,',')) );
    _F_Order: Format( 1X,'INTEGER*2 ORDER(',i3,')/',23(/,1X,15(i3,',')) );*/
  fflush(pass1);
  fflush(pass2);
  fclose(pass1);
  fclose(pass2);
  pass1=NULL;
  pass2=NULL;
  { char *type;
    int len;
  fprintf(chargen,"#ifndef Character\n#define Character char\n#endif\n");
  fprintf(chargen,"#ifndef Integer4\n#define Integer4 ");
  if(sizeof(int)==4){
    type="int";
    typenum1=1;
  } else
  if(sizeof(unsigned)==4){
    type="unsigned";
    typenum1=2;
  } else
  if(sizeof(long)==4){
    type="long";
    typenum1=3;
  } else
  if(sizeof(unsigned long)==4){
    type="unsigned long";
    typenum1=4;
  } else
  if(sizeof(short)==4){
    type="short";
    typenum1=5;
  } else
  if(sizeof(unsigned short)==4){
    type="unsigned short";
    typenum1=6;
  } else {
   fprintf(stderr,"I don\'t find integer type with sizeof == 4\n");
   exit(1);
  }
  fprintf(chargen,"%s\n#endif\n",type);
  fprintf(chargen,"#ifndef Integer2\n#define Integer2 ");
  if(sizeof(int)==2){
    type="int";
    typenum2=1;
  } else
  if(sizeof(unsigned)==2){
    type="unsigned";
    typenum2=2;
  } else
  if(sizeof(long)==2){
    type="long";
    typenum2=3;
  } else
  if(sizeof(unsigned long)==2){
    type="unsigned long";
    typenum2=4;
  } else
  if(sizeof(short)==2){
    type="short";
    typenum2=5;
  } else
  if(sizeof(unsigned short)==2){
    type="unsigned short";
    typenum2=6;
  } else {
   fprintf(stderr,"I don\'t find integer type with sizeof == 2\n");
   exit(1);
  }
  fprintf(chargen,"%s\n#endif\n",type);
  len=sizeof(size_t);
  fprintf(chargen,"#ifndef Integer\n#define Integer ");
  if(sizeof(int)>=len){
    type="int";
    typenum3=1;
  } else
  if(sizeof(unsigned)>=len){
    type="unsigned";
    typenum3=2;
  } else
  if(sizeof(long)>=len){
    type="long";
    typenum3=3;
  } else
  if(sizeof(unsigned long)>=len){
    type="unsigned long";
    typenum3=4;
  } else
  if(sizeof(short)>=len){
    type="short";
    typenum3=5;
  } else
  if(sizeof(unsigned short)>=len){
    type="unsigned short";
    typenum3=6;
  } else {
   fprintf(stderr,"Warning ! I don\'t find integer type "
                  "with sizeof >= sizeof(size_t)\n");
   type="int";
    typenum3=1;
  }
  fprintf(chargen,"%s\n#endif\n",type);
  fflush(chargen);
  fclose(chargen);
  { int Yn=0;
    FILE *align;
    do {
     fprintf(stderr,"\n\nTrying to test alignment\npress Y for continue\n"
     "or N for exit\n"
     "\t1.If program hangs , continue make process.\n"
     "\t2.If program continue with many system error (Bus error,\n"
     "\t  segmentation error,allignment error (f.e. DEC-ALPHA)),\n"
     "\t  run this program again and answer \'N\' to question above\n"
     "\t3.Program executes Ok - continue make process\n");
     Yn=getchar();
     } while(!(Yn=='Y' || Yn=='y' || Yn=='N' || Yn=='n' || Yn==EOF ));
    align=fopen("align.h","w");
    if(align){
    fprintf(align,"/* The alignment is required for this machine */\n"
                  "#ifndef ALLIGN\n#define ALLIGN\n#endif");
    fflush(align);
    fclose(align);
    if(Yn=='Y' || Yn=='y'){ int i;
     int type_int=1;
     unsigned type_uint=2;
     short type_s=3;
     unsigned short type_us=4;
     long type_long=5;
     unsigned long type_ulong=6;
     fprintf(stderr,"Testing allignment of Integer4\n");
     fflush(stderr);
     for(i=0;i<32;++i){
      switch(typenum1){
       case 1:
        *(int*)&Array1[i]=type_int;
        *(int*)&Array2[i]=type_int;
        *(int*)&Array3[i]=type_int;
        break;
       case 2:
        *(unsigned*)&Array1[i]=type_uint;
        *(unsigned*)&Array2[i]=type_uint;
        *(unsigned*)&Array3[i]=type_uint;
        break;
       case 3:
        *(long*)&Array1[i]=type_long;
        *(long*)&Array2[i]=type_long;
        *(long*)&Array3[i]=type_long;
        break;
       case 4:
        *(unsigned long*)&Array1[i]=type_ulong;
        *(unsigned long*)&Array2[i]=type_ulong;
        *(unsigned long*)&Array3[i]=type_ulong;
        break;
       case 5:
        *(short*)&Array1[i]=type_s;
        *(short*)&Array2[i]=type_s;
        *(short*)&Array3[i]=type_s;
       break;
       case 6:
        *(unsigned short*)&Array1[i]=type_us;
        *(unsigned short*)&Array2[i]=type_us;
        *(unsigned short*)&Array3[i]=type_us;
        break;
      }
     }
     fprintf(stderr,"Integer4 Ok!\n");
     fprintf(stderr,"Testing allignment of Integer2\n");
     fflush(stderr);
     for(i=0;i<32;++i){
      switch(typenum2){
       case 1:
        *(int*)&Array1[i]=type_int;
        *(int*)&Array2[i]=type_int;
        *(int*)&Array3[i]=type_int;
        break;
       case 2:
        *(unsigned*)&Array1[i]=type_uint;
        *(unsigned*)&Array2[i]=type_uint;
        *(unsigned*)&Array3[i]=type_uint;
        break;
       case 3:
        *(long*)&Array1[i]=type_long;
        *(long*)&Array2[i]=type_long;
        *(long*)&Array3[i]=type_long;
        break;
       case 4:
        *(unsigned long*)&Array1[i]=type_ulong;
        *(unsigned long*)&Array2[i]=type_ulong;
        *(unsigned long*)&Array3[i]=type_ulong;
        break;
       case 5:
        *(short*)&Array1[i]=type_s;
        *(short*)&Array2[i]=type_s;
        *(short*)&Array3[i]=type_s;
       break;
       case 6:
        *(unsigned short*)&Array1[i]=type_us;
        *(unsigned short*)&Array2[i]=type_us;
        *(unsigned short*)&Array3[i]=type_us;
        break;
      }
     }
     fprintf(stderr,"Integer2 Ok!\n");
     fprintf(stderr,"Testing allignment of Integer\n");
     fflush(stderr);
     for(i=0;i<32;++i){
      switch(typenum3){
       case 1:
        *(int*)&Array1[i]=type_int;
        *(int*)&Array2[i]=type_int;
        *(int*)&Array3[i]=type_int;
        break;
       case 2:
        *(unsigned*)&Array1[i]=type_uint;
        *(unsigned*)&Array2[i]=type_uint;
        *(unsigned*)&Array3[i]=type_uint;
        break;
       case 3:
        *(long*)&Array1[i]=type_long;
        *(long*)&Array2[i]=type_long;
        *(long*)&Array3[i]=type_long;
        break;
       case 4:
        *(unsigned long*)&Array1[i]=type_ulong;
        *(unsigned long*)&Array2[i]=type_ulong;
        *(unsigned long*)&Array3[i]=type_ulong;
        break;
       case 5:
        *(short*)&Array1[i]=type_s;
        *(short*)&Array2[i]=type_s;
        *(short*)&Array3[i]=type_s;
       break;
       case 6:
        *(unsigned short*)&Array1[i]=type_us;
        *(unsigned short*)&Array2[i]=type_us;
        *(unsigned short*)&Array3[i]=type_us;
        break;
      }
     }
     fprintf(stderr,"Integer Ok!\n");
    align=fopen(ALIGN_FILE,"w");
    if(align){
    fprintf(align,"/* The alignment is required for this machine */\n"
                  "#ifdef ALLIGN\n#undef ALLIGN\n#endif");
    fflush(align);
    fclose(align);
    } else fprintf(stderr,"Can\'t open for writing %s\n",ALIGN_FILE);

    }
    } else fprintf(stderr,"Can\'t open for writing %s\n",ALIGN_FILE);
  }


  }
 } else {
  fprintf(stderr,"Can not open file for writing\n");
 }
 if(pass1) fclose(pass1);
 if(pass2) fclose(pass2);
 return 0;
}

