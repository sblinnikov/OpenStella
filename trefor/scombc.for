      PROGRAMSCOMB 
C On entry 
C    X(1:N) - the array of N real elements 
C    M - integer > 0 
C         On exit 
C           SUM is the sum of products of all combinations of M 
C           different elements of X 
C         * 
C: variables description * 
C------- '<--Entering Node %_Var:' 
      Implicitreal*8(a-h,o-z) 
      Parameter(NDIM=10000) 
C- maximum dimension of arrays
      Real*8X(NDIM),SUM,PRODCT
      IntegerK(NDIM),I,M,N,L 
C------- '<--Leaving  Node %_Var:' 
C: input N, M, and the values of X(1:N) * 
C------- '<--Entering Node %_Input:' 
      Write(0,*)'Enter the array length N'
      READ(5,*)N 
      Write(0,*)'Enter the number of elements in product M' 
      READ(5,*)M 
      Write(0,*)'Enter the array X(1:N)' 
      READ(5,*)(X(I),I=1,N) 
C------- '<--Leaving  Node %_Input:' 
C abstract variable  SET  - the ordered set of indexes K(I):
C           K(1) < K(2) < ... < K(M) 
C         Statement QS:  SUM is the sum of products 
C                   X(K(I)) for all  { K(I) }==SET <= SET(CURRENT) * 
C: make  QS  true for  SET==SET(INITIAL) * 
C------- '<--Entering Node %1:' 
      SUM=1.D0 
C- !!! 
      DO32757I=1,M 
      K(I)=I 
      SUM=SUM*X(I) 
32757 CONTINUE 
C------- '<--Leaving  Node %1:' 
32754 IF(.NOT.( 
C:  SET ^= SET(FINAL) * 
     *K(1).NE.N+1-M 
C- If K(1)==N+1-M all the K(I) reach their final value 
     *))GOTO32753 
C: find next  SET  keeping QS invariant * 
C------- '<--Entering Node %3:' 
C: find new  SET , i.e. new { K(I) } * 
C------- '<--Entering Node %3A:' 
C concrete presentation of  SET: 
C          K(I) - array of integer  M  elements * 
      I=M 
32751 IF(.NOT.(K(I).EQ.N+I-M))GOTO32750 
      I=I-1 
      GOTO32751 
32750 CONTINUE 
      K(I)=K(I)+1 
C The next loop is valid only for Fortran-77 
C       since for  m==1  Fortran-66  executes Do-loop L=1,0 * 
      DO32748L=1,M-1 
      K(I+L)=K(I)+L 
32748 CONTINUE 
C------- '<--Leaving  Node %3A:' 
C: put in PRODCT the product of X(K(I)) * 
C------- '<--Entering Node %3B:' 
      PRODCT=1.D0 
      DO32745I=1,M
      PRODCT=PRODCT*X(K(I)) 
32745 CONTINUE 
C------- '<--Leaving  Node %3B:' 
      SUM=SUM+PRODCT 
C------- '<--Leaving  Node %3:' 
     * 
      GOTO32754 
32753 CONTINUE 
C- Here  SET==SET(FINAL) and QS==.TRUE., that is 
C- sum contains all needed products of X(K(I)) 
      WRITE(0,*)' N=',N,'   M=',M,'   SUM=',SUM
      END 
