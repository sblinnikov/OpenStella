module string_tools
  use kinds, only: dp
  implicit none
  private

  character(len=*), parameter, private :: mdl_name = 'string_tools'

  public :: num2str, a2s

  interface num2str
     module procedure int2str
     module procedure dbl2str
  end interface num2str

  interface a2s
     module procedure ai2s
     module procedure ad2s
  end interface a2s
contains

  !!*** *************************************************************************
  !!****s* string_tools/a2s  *
  !!
  !!   NAME
  !!     a2s
  !!
  !!   FUNCTION
  !!     Converts an integer or double array into a string of requested length
  !!
  !***************************************************************************
  function ai2s(a, sep, fmt) ! result(res)
    integer, dimension(:), intent(in) :: a
    character(len=*), intent(in), optional :: sep
    character(len=*), intent(in), optional :: fmt
    character(:), allocatable :: ai2s
    character(9999) :: tmp
    character(22) :: s
    character(:), allocatable :: lsep, lfmt
    integer :: i

    if (present(sep)) then
       lsep = sep
    else
       lsep = " "
    endif
    if (present(fmt)) then
       lfmt = "("//fmt//")"
    else
       lfmt = '(I0)'
    endif

    tmp = ""
    do i = 1, size(a)
       write(s,fmt=lfmt)  a(i)
       if ( i == 1 ) then
          tmp = s
       else
          tmp = trim(tmp)//lsep//s
       endif
    enddo
    ai2s = trim(tmp)
  end function ai2s

  !-------------------------------------------------------
  function ad2s(a, sep, fmt) ! result(res)
    real(dp), dimension(:), intent(in) :: a
    character(len=*), intent(in), optional :: sep
    character(len=*), intent(in), optional :: fmt
    character(:), allocatable :: ad2s
    character(9999) :: tmp
    character(22) :: s
    character(:), allocatable :: lsep, lfmt
    integer :: i

    if (present(sep)) then
       lsep = sep
    else
       lsep = " "
    endif
    if (present(fmt)) then
       lfmt = "("//trim(fmt)//")"
    else
!       lfmt = '(1p,e8.3)'
       lfmt = '(1pe10.3)'
    endif

!    write(*, '(/A," sep: ", A, " fmt:", A, " len(a)=", I3)') 'a2d:',  lsep, lfmt, size(a)

    tmp = ""
    do i = 1, size(a)
       write(s,fmt=lfmt)  a(i)
       if ( i == 1 ) then
          tmp = s
       else
          tmp = trim(tmp)//lsep//s
       endif
    enddo
!    write(*,*) trim(tmp)
    ad2s = trim(tmp)
    return
  end function ad2s
  
  !!*** *************************************************************************
  !!****s* string_tools/int2str  *
  !!
  !!   NAME
  !!     int2str
  !!
  !!   FUNCTION
  !!     Converts an integer `i` into a character string of requested length,
  !!     pre-pending zeros if necessary.
  !!
  !!        - i      !! integer to convert to string
  !!        - length !! desired length of string
  !!
  !!   See  https://github.com/wavebitscientific/datetime-fortran/blob/914d21e497a29a85c9ac6ec8c269aeada244d285/src/lib/mod_datetime.f90
  !***************************************************************************
  pure function int2str(i,length) result(res)
    integer,intent(in) :: i, length
    character(len=length) :: res
    character(len=2)      :: string
    
    write(unit=string,fmt='(I2)')length
    write(unit=res,fmt='(I'//string//'.'//string//')')i
  end function int2str
  
  pure function dbl2str(i,length) result(res)
    real*8,intent(in) :: i
    integer,intent(in) :: length
    character(len=length) :: res
    character(len=2)      :: s1, s2
    
    write(unit=s1,fmt='(I2)')max(10,length)
    write(unit=s2,fmt='(I2)')max(2,length-min(length,7))
    write(unit=res,fmt='(1pE'//s1//'.'//s2//')')i
  end function dbl2str
  
end module string_tools


