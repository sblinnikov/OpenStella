/*****************************************************************************
 *     trf - invoke trefor,fortran
 *     return code:
 *       0 - OK
 *       1 - error in parameters
 *****************************************************************************/
//#define DDEBUG
#include <stdio.h>

#include <string.h>
/* exit(), memory allocation */
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#ifdef DDEBUG
#ifdef _MSDOS_
#include <conio.h>
#endif
#endif

#ifdef _MSDOS_
/* system() prototype */
#include <process.h>
#else
extern char **environ;
#endif

#ifndef BUFFER_SIZE
#define BUFFER_SIZE 1024
#endif
#if BUFFER_SIZE<32
#error "BUFFER_SIZE is so small"
#endif
#ifndef RCFILENAME
#ifdef _MSDOS_
#define RCFILENAME "trf.cfg"
#else
#define RCFILENAME ".trfrc"
#endif
#endif
#ifndef COMP_NAME_SIZE
#define COMP_NAME_SIZE 128
#endif
#ifndef DEFCOMPILER
#define DEFCOMPILER "trefor"
#endif
#ifndef DEFFORTRAN
#define DEFFORTRAN "f77"
#endif
#ifndef DELIMITER
#define DELIMITER ':'
#endif

#define MIN0LEN(a,b) ((strlen(a)<strlen(b))?0:strlen(b))

int treforReturnCode;

char *rcpath[]= {
#ifndef _MSDOS_
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

typedef struct {
  char *LineName,*optionON,*optionOFF;
  int Active;
  char command[COMP_NAME_SIZE];
  char *HelpText;
} cell;

#ifndef MAXACTIONS
#define MAXACTIONS 20
#endif

cell Actions[MAXACTIONS]= { {"TREFOR","","",1,"trefor %t . 1",""},
  {"EDITOR","e","ne",0,"joe %t",""},
  {"VIEWER","v","nv",0,"less %l",""},
  {"COMPILER","f","nf",1,"f77 %p %f",""},
  {"DELLISTING","nl","l",1,"rm %l",""},
  {"DELSOURCE","ns","s",0,"rm %f",""},
};
int NumActions=5; /* TREFOR , EDITOR and FORTRAN are known default */

#ifndef RULE_LEN
#define RULE_LEN 32
#endif

typedef struct {
  char Letter;
  char Rule[RULE_LEN];
  char Contents[COMP_NAME_SIZE];
} letters;

#ifndef MAXLETTER
#define MAXLETTER 26
#endif
letters Letters[MAXLETTER] =  {
  { '2',"",""}, /* trefor file name tag */
  { '1',"",""}, /* options */
  { 'n',"%2%3%3%3%7",""}, /* trefor file name tag */
  { 't',"%n.trf",""}, /* trefor file name */
  { 'f',"%n.f",""}, /* fortran file name */
  { 'l',"%n.lst",""}, /* listing file name*/
  { 'p',"%1",""},  /* options after trf-option before trf-name*/
  { 'o',"%n.o",""}  /* object file name*/
};
int LetterMin=2,LetterMax=8;

#ifndef LABEL_LEN
#define LABEL_LEN 8
#endif
typedef struct {
  int code;
  unsigned rc;
  char Label[LABEL_LEN];
} Exec ;

#ifndef MAXEXECUTE
#define MAXEXECUTE 64
#endif

#define E_LABEL     (-1)
#define E_RCEQ      (-2)
#define E_RCLT      (-3)
#define E_RCGT      (-4)
#define E_RCLE      (-5)
#define E_RCGE      (-6)
#define E_EXIT      (-7)
#define E_STOP      (-8)

Exec Execute[MAXEXECUTE]={
  {0,0,""},		/* RUN TREFOR 		*/
  {E_RCGT,4,"ERROR"},	/* if rc>4 goto ERROR 	*/
  {E_RCLT,4,"WARN"},	/* if rc<4 goto WARN 	*/
  {2,0,""},		/* RUN FORTRAN 		*/
  {E_RCGE,0,"EXIT"},	/* goto EXIT 		*/
  {E_LABEL,0,"ERROR"},  /* label ERROR 		*/
  {E_LABEL,0,"WARN"},   /* label WARN 		*/
  {1,0,""},		/* RUN EDITOR		*/
  {E_LABEL,0,"EXIT"},	/* label EXIT		*/
  {3,0,""},		/* Delete listing	*/
  {E_EXIT,0,""}
};
int MaxExecute=11;

#ifndef MAXOPTCHARS
#define MAXOPTCHARS 10
#endif
#if (MAXOPTCHARS)<5
#define MAXOPTCHARS 10
#endif
static int MaxOptchars=1,OptChars[MAXOPTCHARS]={'-'};


void Usage(){
  fprintf(stderr,"Usage:\n\ttrf -[[n]f][[n]s][[n]l][[n]e] [compiler-option] filenames\n");
  exit(1);
}

void SayAndExit(int rc,char *message){
  fprintf(stderr,"Error:%d, %s\n", rc, message);
  exit(rc);
}

char *SkipSpace(char *pnt){
  while(isspace(*pnt)) ++pnt;
  return pnt;
}

void ProcessOptchars(char *pnt){
  while(MaxOptchars<MAXOPTCHARS && *pnt){
    if(!iscntrl(*pnt) && !isspace(*pnt)){
      OptChars[MaxOptchars++]=*pnt;
    }
    ++pnt;
  }
}

int IsOptChar(char Opt){
  int i;
  for(i=0;i<MaxOptchars;++i){
    if(OptChars[i]==Opt) return 1;
  }
  return 0;
}

void ProcessExec(FILE *in,char *buffer){
  char *pnt;
  int i,len;
  MaxExecute=0;
  while(fgets(buffer,BUFFER_SIZE,in)!=NULL  && MaxExecute<MAXEXECUTE-1 ){
#ifdef DDEBUG
    fprintf(stderr,"%s",buffer);
#endif
    pnt=SkipSpace(buffer);
    if(*pnt=='\0' || *pnt=='\n' || *pnt=='!' || *pnt=='%' || *pnt=='#')
      continue; /* comment */
    if(*pnt==':'){    /* label */
      ++pnt;
      pnt=SkipSpace(pnt);
      for(i=0;i<LABEL_LEN-1 && *pnt;++i,++pnt){
        if(isalpha(*pnt)){
          (Execute[MaxExecute].Label)[i]=*pnt;
        }
        else
          break;
      }
      (Execute[MaxExecute].Label)[i]=0;
      Execute[MaxExecute].code=E_LABEL;
      ++MaxExecute;
      continue;
    }
    len=MIN0LEN(pnt,"RCEQ0");
    if(len && !memcmp(pnt,"RC",2)){
      int gotoOK=0;
      if(!memcmp(pnt+2,"EQ",2)){
        gotoOK=1;
        Execute[MaxExecute].code=E_RCEQ;
      }
      if(!memcmp(pnt+2,"GT",2)){
        gotoOK=1;
        Execute[MaxExecute].code=E_RCGT;
      }
      if(!memcmp(pnt+2,"GE",2)){
        gotoOK=1;
        Execute[MaxExecute].code=E_RCGE;
      }
      if(!memcmp(pnt+2,"LT",2)){
        gotoOK=1;
        Execute[MaxExecute].code=E_RCLT;
      }
      if(!memcmp(pnt+2,"LE",2)){
        gotoOK=1;
        Execute[MaxExecute].code=E_RCLE;
      }
      if(gotoOK){ int rcc;char *tmp;
        pnt+=4;
        pnt=SkipSpace(pnt);
        rcc=(int)strtol(pnt,&tmp,10);
        if(tmp!=pnt ||(tmp==pnt && *pnt=='0' && ++tmp)){  /* ++tmp to skip 0 */
          Execute[MaxExecute].rc=rcc;
          pnt=tmp;
          pnt=SkipSpace(pnt);
          for(i=0;i<LABEL_LEN-1 && *pnt;++i,++pnt){
            if(isalpha(*pnt))
              (Execute[MaxExecute].Label)[i]=*pnt;
            else
              break;
          }
          (Execute[MaxExecute].Label)[i]=0;
          MaxExecute++;
        } else fprintf(stderr,"Error in %s:BAD rc code(rc==%d) in RC.. command:%s|%s|%s\n"
            "errno=%d\n",
            RCFILENAME,rcc,buffer,pnt,tmp,errno);
        continue;
      }
    }/* test GOTO */
    len=MIN0LEN(pnt,"NOP");
    if(len && !memcmp(pnt,"NOP",len) && (isspace(*(pnt+len)) || *(pnt+len)==0))
      continue;
    len=MIN0LEN(pnt,"STOP");
    if(len && !memcmp(pnt,"STOP",len) && (isspace(*(pnt+len)) || *(pnt+len)==0)){
      Execute[MaxExecute].code=E_STOP;
      continue;
    }
    for(i=NumActions-1;i>=0;--i){ char *tmp;
      tmp=Actions[i].LineName;
      len=MIN0LEN(pnt,tmp);
      if(len && !memcmp(pnt,tmp,len) && (isspace(*(pnt+len)) || *(pnt+len)==0)){
        Execute[MaxExecute].code=i;
        MaxExecute++;
        break;
      }
    }
    if(i<0){
      fprintf(stderr,"Error in %s:Unknown command in EXECUTE:%s\n",RCFILENAME,pnt);
    }
  } /* main loop */
  Execute[MaxExecute++].code=E_EXIT;
  return;
}

void ProcessOption(char *buffer){
  int i,ibeg,iend,flag;
  if(NumActions<MAXACTIONS){
    ibeg=0;
    Actions[NumActions].LineName=NULL;
    for(i=ibeg,flag=0;i<BUFFER_SIZE && (buffer[i]!='\0' && buffer[i]!='\n');++i){
      if(buffer[i]==DELIMITER){
        flag=1;
        break;
      }
    }
    if(flag){
      iend=i;
      if((Actions[NumActions].LineName=(char*)malloc(strlen(buffer)+2))==NULL){
        SayAndExit(2,"Not enough memory");
      }
      for(i=ibeg;i<iend;++i)
        (Actions[NumActions].LineName)[i-ibeg]=buffer[i];
      /*(Actions[NumActions].LineName)[i-ibeg]='=';   ++i;*/
      (Actions[NumActions].LineName)[i-ibeg]=0;
      Actions[NumActions].optionON=Actions[NumActions].LineName+iend+1-ibeg;
      ibeg=iend+1;
      for(i=ibeg,flag=0;i<BUFFER_SIZE && (buffer[i]!='\0' && buffer[i]!='\n');++i){
        if(buffer[i]==DELIMITER){
          flag=1;
          break;
        }
      }
      if(flag){
        iend=i;
        for(i=ibeg;i<iend;++i)
          (Actions[NumActions].optionON)[i-ibeg]=buffer[i];
        (Actions[NumActions].optionON)[i-ibeg]=0;
        Actions[NumActions].optionOFF=Actions[NumActions].optionON+iend+1-ibeg;
        ibeg=iend+1;
        for(i=ibeg,flag=0;i<BUFFER_SIZE && (buffer[i]!='\0' && buffer[i]!='\n');++i){
          if(buffer[i]==DELIMITER){
            flag=1;
            break;
          }
        }
        if(flag){
          iend=i;
          for(i=ibeg;i<iend;++i)
            (Actions[NumActions].optionOFF)[i-ibeg]=buffer[i];
          (Actions[NumActions].optionOFF)[i-ibeg]=0;
          Actions[NumActions].HelpText=NULL;
          ibeg=iend+1;
          if(!memcmp(buffer+ibeg,"ON:",3)) i=1;
          else if(!memcmp(buffer+ibeg,"OFF:",4))i=0;
          else flag=0;
          Actions[NumActions].Active=i;
        }
      }
    }
    if(!flag){
      fprintf(stderr,"Error in OPTION:line %s\n",buffer);
      if(Actions[NumActions].LineName)
        free(Actions[NumActions].LineName);
    }
    else
      ++NumActions;
  } else {
    fprintf(stderr,"Number of OPTION is big (bigger %d)."
        "Increase MAXACTIONS and recompile program\n",MAXACTIONS);
  }
  return;
}

void ProcessLetter(char *buffer){
  int flag=0,i,ibeg,iend;
  if(LetterMax<MAXLETTER){
    if(isalpha(buffer[0]) && buffer[1]==':'){
      ibeg=2;
      Actions[NumActions].LineName=NULL;
      for(i=ibeg,flag=0;i<BUFFER_SIZE && (buffer[i]!='\0' && buffer[i]!='\n');++i){
        if(buffer[i]==DELIMITER){
          flag=1;
          break;
        }
      }
      if(flag){
        iend=i;
        for(i=ibeg;i<iend && (i-ibeg)<RULE_LEN;++i)
          (Letters[LetterMax].Rule)[i-ibeg]=buffer[i];
        (Letters[LetterMax].Rule)[i-ibeg]=0;
        Letters[LetterMax].Letter=buffer[0];
      }
    }
    if(flag)
      ++LetterMax;
    else
      fprintf(stderr,"Error in LETTER:line %s\n",buffer);

  } else {
    fprintf(stderr,"Number of LETTER is big (bigger %d)."
        "Increase MAXLETTER and recompile program\n",MAXLETTER);
  }
  return;
}

void ProcessRC(FILE *in,char *buffer){
  int i,flag,len;
  char *pnt;
  while(fgets(buffer,BUFFER_SIZE,in)!=NULL){
#ifdef DDEBUG
    fprintf(stderr,"%s",buffer);
#endif
    pnt=SkipSpace(buffer);
    if(*pnt=='\0' || *pnt=='\n' || *pnt=='!' || *pnt=='%' || *pnt=='#')
      continue; /* comment */

    len=MIN0LEN(pnt,"EXECUTION");
    if(len && !memcmp(pnt,"EXECUTION",len) &&
        (isspace(*(pnt+len)) || *(pnt+len)=='0' ))
    {
      ProcessExec(in,buffer);
      break;
    }
    if(!memcmp(pnt,"OPTION",6) && (isspace(*(pnt+6)) || *(pnt+6)=='=')){
      pnt=SkipSpace(pnt+6);
      if(*pnt=='='){
        ++pnt;
        ProcessOption(SkipSpace(pnt));
      }
      continue;
    }
    if(!memcmp(pnt,"LETTER",6) && (isspace(*(pnt+6)) || *(pnt+6)=='=')){
      pnt=SkipSpace(pnt+6);
      if(*pnt=='='){
        ++pnt;
        pnt=SkipSpace(pnt);
        ProcessLetter(pnt);
      }
      continue;
    }
    if(!memcmp(pnt,"OPTCHAR",7) && (isspace(*(pnt+7)) || *(pnt+7)=='=')){
      pnt=SkipSpace(pnt+7);
      if(*pnt=='='){
        ++pnt;
        pnt=SkipSpace(pnt);
        ProcessOptchars(pnt);
      }
      continue;
    }
    for(i=NumActions-1,flag=0;i>=0;--i){
      len=MIN0LEN(pnt,Actions[i].LineName);
      if(len && !memcmp(pnt,Actions[i].LineName,len) &&
          (isspace(*(pnt+len)) || *(pnt+len)=='='))
      {
        pnt=SkipSpace(pnt+len);
        if(*pnt=='='){
          pnt=SkipSpace(pnt+1);
          strcpy(Actions[i].command,pnt);
          flag=1;
        }
        break;
      }
    }
    if(!flag)
      fprintf(stderr,"Error in %s,unknownm command in line %s\n",
          RCFILENAME,buffer);
  }
}


void ProcessTrfOption(char *string){
  int i,flag,len;
  ++string ; 	/*skip '-'	*/
  while(*string && *string!=' ' && *string!='\t'){
    for(i=NumActions-1,flag=0;i>=0 && flag==0 ;--i){
#ifdef DDEBUG
      fprintf(stderr,"Option %c test in %s:ON=%s,OFF=%s!%s!\n",
          *string,Actions[i].LineName,Actions[i].optionON,Actions[i].optionOFF,
          (Actions[i].Active)?"Active":"Passive");
#endif
      len=MIN0LEN(string,Actions[i].optionON);
      if(len && !memcmp(string,Actions[i].optionON,len)){
        Actions[i].Active=1;
        flag=1;
      }
      else {
        len=MIN0LEN(string,Actions[i].optionOFF);
        if(len && !memcmp(string,Actions[i].optionOFF,len)){
          Actions[i].Active=0;
          flag=1;
        }
      }
    }
    if(flag)
      string+=len;
    else {
      fprintf(stderr,"Unknown trf option:-%c\n",*string);
      ++string;
    }
  }
}

void PrepareLetter(void){
  int i,j;
  char *pin,*pintmp,*pout,*poutend;
  for(i=2;i<LetterMax;++i){
    pin=Letters[i].Rule;
    pout=Letters[i].Contents;
    poutend=pout+COMP_NAME_SIZE-1;
    while(*pin && pout<poutend){
      if(*pin!='%'){
        *pout++=*pin++;
      } else {
        switch(*++pin){
          case 0: break ;
          case '%': *pout++=*pin++; break;
          case '3': if(pout>Letters[i].Contents && isalpha(*(pout-1))) --pout;++pin;break;
          case '4': if(pout>Letters[i].Contents && isdigit(*(pout-1))) --pout;++pin;break;
          case '5': if(pout>Letters[i].Contents && isspace(*(pout-1))) --pout;++pin;break;
          case '6': if(pout>Letters[i].Contents && isprint(*(pout-1))) --pout;++pin;break;
          case '7': if(pout>Letters[i].Contents && *(pout-1)=='.') --pout;++pin;break;
          default:
                      for(j=i-1;j>=0;--j){
                        if(*pin==Letters[j].Letter){
                          pintmp=Letters[j].Contents;
                          while(*pintmp && pout<poutend)
                            *pout++=*pintmp++;
                          break;
                        }
                      }
                      if(j<0) fprintf(stderr,"Error in LETTER processing:LETTER %%%c"
                          " reffer to unknown LETTER %%%c\n",
                          Letters[i].Letter,*pin);
                      ++pin;break;
        }
      }	/* prepare letter			*/
    } 	/* end of current letter		*/
    *pout=0;
#ifdef DDEBUG
    fprintf(stderr,"Letter %%%c Rule %s Contents %s\n",
        Letters[i].Letter,Letters[i].Rule,Letters[i].Contents);
#endif
  } 	/* end if for through all letters	*/
}

#ifndef MAXLOOPS
#define MAXLOOPS 1024
#endif

void DoExecution(){
  int psw=0,buf,rc=0,loop;
  for(loop=0;psw<MAXEXECUTE && loop<MAXLOOPS;loop++){
    buf=Execute[psw].code;
    if(buf>=0){
      if(buf<NumActions){
        int size=0,i;
        char bufchar,*pointer,*pin1,*pin2,*buffer;
#ifdef DDEBUG
        fprintf(stderr,"Action %d:%s",buf,Actions[buf].command);
#endif
        /* calculate size of string */
        if(Actions[buf].Active){
          size=strlen(Actions[buf].command)+7; /* -== (must be 0) I have no time to count exactly */
          pointer=strchr(Actions[buf].command,'%');
          while(pointer!=NULL){
            bufchar=*++pointer;
            for(i=LetterMax;i>1;--i)
              if(Letters[i].Letter==bufchar){
                size+=strlen(Letters[i].Contents)-2;
                break;
              }
            pointer=strchr(pointer,'%');
          }
          buffer=(char*)malloc(size+1);
          if(buffer==NULL)
            SayAndExit(2,"No memory for command line to start new process");
          pointer=buffer;
          pin1=Actions[buf].command;
          while(*pin1 && pointer<buffer+size){
            if(*pin1!='%'){
              *pointer++=*pin1++;
            }
            else {
              switch(*++pin1){
                case 0 : break;
                case '%' : *pointer++='%';++pin1;break;
                default :
                           for(i=LetterMax;i>1;--i)
                             if(Letters[i].Letter==*pin1){
                               pin2=Letters[i].Contents;
                               while(*pin2 && pointer<buffer+size)
                                 *pointer++=*pin2++;
                               break;
                             }
                           if(i==1)
                             fprintf(stderr,"Warning: Unknown LETTER %%%c in command %s%s\n",
                                 *pin1,Actions[buf].LineName,Actions[buf].command);
                           ++pin1;
              }
            }
          }
          *pointer=0;
#ifdef DDEBUG
          fprintf(stderr,"Execute %s\n",buffer);
#endif
          rc=system(buffer);

          if(rc && ((rc & 0xff)==0)) /* if 8 LSB equal 0 */
            rc=(unsigned)rc>>8;

#ifdef DDEBUG
          fprintf(stderr,"RC=%d\n",rc);
#endif
          if(!strcmp(Actions[buf].LineName,"TREFOR"))
            treforReturnCode = rc;

          free(buffer);
        }
      }
      ++psw;
    } else {
      int gotoOK=0;
      switch(buf){
        case E_LABEL :  break;
        case E_EXIT : return ;
        case E_STOP : exit(3) ; /* was 3 */
        case E_RCEQ : if(rc==Execute[psw].rc) gotoOK=1;break;
        case E_RCLE : if(rc<=Execute[psw].rc) gotoOK=1;break;
        case E_RCGE : if(rc>=Execute[psw].rc) gotoOK=1;break;
        case E_RCGT : if(rc>Execute[psw].rc) gotoOK=1;break;
        case E_RCLT : if(rc<Execute[psw].rc) gotoOK=1;break;
        default: /* --= */ break;
      }
      if(gotoOK){
        for(gotoOK=0;gotoOK<MaxExecute;++gotoOK){
#ifdef DDEBUG
          fprintf(stderr,"  Label seek %s:in line %d command %d label %s\n"
              "  rc=%d ,in execution array=%d\n" ,
              Execute[psw].Label,gotoOK,Execute[gotoOK].code,
              Execute[gotoOK].Label,rc,Execute[gotoOK].rc);
          rc=0;
#endif

          if(Execute[gotoOK].code==E_LABEL &&
              !strcmp(Execute[psw].Label,Execute[gotoOK].Label)){
            psw=gotoOK;
            break;
          }
        }
        if(gotoOK==MaxExecute) ++psw;
      } else ++psw;
#ifdef DDEBUG
      fprintf(stderr,"Language after:in line %d\n",psw);
#endif
    }
  }
  if(loop==MAXLOOPS) fprintf(stderr,"Execution stopped (perpetual loop)"
      ", check your %s or increase MAXLOOPS const\n",RCFILENAME);
}

main(int argc,char **argv){
  treforReturnCode = 0;
  int i,j;
  char buffer[BUFFER_SIZE];
  FILE *in;
  if(argc<2)
    Usage();
  *buffer=0;
  /* prepare commands for compilation by trefor and fortran */
  if((in=fopen(RCFILENAME,"r"))==NULL){
    i=0;
#ifndef _MSDOS_
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
#ifdef DDEBUG
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
#ifdef DDEBUG
          fprintf(stderr,"Trying %s\n",buffer);
#endif
          if(in!=NULL)
            break;
        }
      }
    }

  }
  if(in==NULL){
    /* No default action */
  } else {
#ifdef DDEBUG
    fprintf(stderr,"Opened %s\n",buffer);
#endif
    ProcessRC(in,buffer);
#ifdef DDEBUG
    fprintf(stderr,".trfrc is processed\n");
#endif
    fclose(in);
  }
  if( argv[1][0]=='-') {
    ProcessTrfOption(argv[1]);
    i=2;
  } else i=1;
  j=0; /* 0 - wait fortran options , 1 wait file name */
  (Letters[1].Contents)[0]=0;
  for(;i<argc;++i){
    if(IsOptChar(argv[i][0])){
      if(j){
        strcat(Letters[1].Contents," ");
        strcat(Letters[1].Contents,argv[i]);
      } else {
        strcpy(Letters[1].Contents,argv[i]);
        j=1;
      }
    } else {
      strcpy(Letters[0].Contents,argv[i]);
      PrepareLetter();
      DoExecution();
      j=0;
    }
  }
  return (treforReturnCode);
}

