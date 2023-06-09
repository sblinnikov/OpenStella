!-----------------------------------------------------------------------------!
!   CP2K: A general program to perform molecular dynamics simulations         !
!   Copyright (C) 2000  CP2K developers group                                 !
!-----------------------------------------------------------------------------!
!!****** cp2k/kinds [1.0] *
!!
!!   NAME
!!     kinds
!!
!!   FUNCTION
!!     Defines the basic variable types
!!
!!   AUTHOR
!!     Matthias Krack
!!
!!   MODIFICATION HISTORY
!!     Adapted for CP2K by JGH
!!
!!   NOTES
!!     Data type definitions; tested on:
!!         - IBM AIX xlf90
!!         - SGI IRIX  f90
!!         - CRAY T3E  f90
!!         - DEC ALPHA f90
!!         - NAG_F90
!!         - SUN
!!         - HITACHI
!!
!!   SOURCE
!******************************************************************************

MODULE kinds

  IMPLICIT NONE

  PRIVATE
  PUBLIC :: sp, dp, isp, idp, dp_size, sp_size, int_size
  PUBLIC :: default_string_length, default_path_length
  public :: print_kind_info

! #if __SGL
!   INTEGER, PARAMETER :: sp = SELECTED_REAL_KIND ( 6, 30 )
!   INTEGER, PARAMETER :: dp = SELECTED_REAL_KIND ( 6, 30 )
!   ! we rely on this (libraries) but do not check this
!   INTEGER, PARAMETER :: dp_size  = 4,&
!                         int_size = BIT_SIZE(0)/8,&
!                         sp_size  = 4
! #else
  INTEGER, PARAMETER :: sp = SELECTED_REAL_KIND ( 6, 30 )
  INTEGER, PARAMETER :: dp = SELECTED_REAL_KIND ( 14, 200 )
  ! we rely on this (libraries) but do not check this
  INTEGER, PARAMETER :: dp_size  = 8,&
                        int_size = BIT_SIZE(0)/8,&
                        sp_size  = 4
!#endif

  ! The result is a scalar of type default integer.
  ! The result has a value equal to the value of the
  ! kind parameter of the integer data type that
  ! represents all values n in the range of values n with -10p < n < 10p.
  INTEGER, PARAMETER :: isp = SELECTED_INT_KIND (8)
  INTEGER, PARAMETER :: idp = SELECTED_INT_KIND (18)
  ! because 10**19 is bigger than 2**63

  INTEGER, PARAMETER :: default_string_length=80
  INTEGER, PARAMETER :: default_path_length=250

!!*****
!******************************************************************************

CONTAINS

!******************************************************************************
!!****** kinds/print_kind_info [1.0] *
!!
!!   NAME
!!     print_kind_info
!!
!!   SYNOPSIS
!!     Subroutine print_kind_info(iw)
!!       Integer, Intent (IN):: iw
!!     End Subroutine print_kind_info
!!
!!   FUNCTION
!!     Print informations about the used data types.
!!
!!   AUTHOR
!!     Matthias Krack
!!
!!   MODIFICATION HISTORY
!!     Adapted by JGH for Cp2k
!!
!!   SOURCE
!******************************************************************************

SUBROUTINE print_kind_info ( iw )


    INTEGER, INTENT(IN)                      :: iw

!------------------------------------------------------------------------------

  WRITE ( iw, '( /, T2, A )' ) 'DATA TYPE INFORMATION:'

  WRITE ( iw, '( /,T2,A,T79,A,2(/,T2,A,T75,I6),3(/,T2,A,T67,E15.8) )' ) &
       'REAL: Data type name:', 'dp', '      Kind value:', KIND ( 0.0_dp ), &
       '      Precision:', PRECISION ( 0.0_dp ), &
       '      Smallest non-negligible quantity relative to 1:', &
       EPSILON ( 0.0_dp ), &
       '      Smallest positive number:', TINY ( 0.0_dp ), &
       '      Largest representable number:', HUGE ( 0.0_dp )
  WRITE ( iw, '( /,T2,A,T79,A,2(/,T2,A,T75,I6),3(/,T2,A,T67,E15.8) )' ) &
       '      Data type name:', 'sp', '      Kind value:', KIND ( 0.0_sp ), &
       '      Precision:', PRECISION ( 0.0_sp ), &
       '      Smallest non-negligible quantity relative to 1:', &
       EPSILON ( 0.0_sp ), &
       '      Smallest positive number:', TINY ( 0.0_sp ), &
       '      Largest representable number:', HUGE ( 0.0_sp )
  WRITE ( iw, '( /,T2,A,T72,A,4(/,T2,A,T61,I20) )' ) &
       'INTEGER: Data type name:', '(default)', '         Kind value:', &
       KIND ( 0 ), &
       '         Bit size:', BIT_SIZE ( 0 ), &
       '         Largest representable number:', HUGE ( 0 )
  WRITE ( iw, '( /,T2,A,T72,A,4(/,T2,A,T61,I20) )' ) &
       '      Data type name:', 'isp', '      Kind value:', KIND ( 0_isp ), &
       '         Bit size:', BIT_SIZE ( 0_isp ), &
       '      Largest representable number:', HUGE ( 0_isp )
  WRITE ( iw, '( /,T2,A,T72,A,/,T2,A,T75,I6,/ )' ) &
       'LOGICAL: Data type name:', '(default)', &
       '         Kind value:', KIND ( .TRUE. )
  WRITE ( iw, '( /,T2,A,T72,A,/,T2,A,T75,I6,/ )' ) &
       'CHARACTER: Data type name:', '(default)', &
       '           Kind value:', KIND ( 'C' )

END SUBROUTINE print_kind_info

!!*****
!******************************************************************************

END MODULE kinds

!******************************************************************************
