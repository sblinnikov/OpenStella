module stl_units

  use kinds,                only: dp
  use math_constants,        only: p_pi
  use phys_constants,        only: p_cg, p_rsol, p_cms, p_k, p_h
  implicit none

  private
     
  character(len=*), parameter, private :: mdl_name = 'stl_units' 
  public :: write_stl_units
  public :: s2w, sub_s2w, sub_drv_Stella2World
  public :: w2s, sub_w2s, sub_drv_World2Stella
  public :: s2w_drv, w2s_drv
  
  public :: p_utp, p_urho, p_ueu, p_upu            
  public :: p_ulgr, p_upurs, p_ulgpu, p_ulgeu, p_upc &
            , p_ulgtp, p_ulgpl, p_ulgtm, p_ulgp &
            , p_uv, p_ulge, p_uepri, p_utime, p_ur, p_up, p_upi &  
            , p_ue_cgs, p_uei, p_iurs, p_urs, p_um, p_um4pi
       
        real (kind=dp), parameter :: p_ulgr  = 1.4000000000d+01
        real (kind=dp), parameter :: p_upurs = 1.0000000000d+07
        real (kind=dp), parameter :: p_ulgpu = 7.0000000000d+00 
        real (kind=dp), parameter :: p_ulgeu = 1.3000000000d+01
        real (kind=dp), parameter :: p_upc   = 3.0856775807d+18
        real (kind=dp), parameter :: p_utp   = 1.0000000000d+05 
        real (kind=dp), parameter :: p_urho  = 1.0000000000d-06
!         real (kind=dp), parameter :: p_ln_10 = log(10.d0)

              
        real (kind=dp), parameter :: p_ulgtp = log10(p_utp)
        real (kind=dp), parameter :: p_ulgpl = log10(p_urho)
        real (kind=dp), parameter :: p_ulgtm = -(log10(4.d0*p_pi*p_cg)+p_ulgpl)/2.d0
        real (kind=dp), parameter :: p_ulgp  = p_ulgpl+2.d0*(p_ulgr - p_ulgtm)
        real (kind=dp), parameter :: p_ulgv  = (p_ulgr - p_ulgtm)
        real (kind=dp), parameter :: p_uv    = 10.d0**p_ulgv
        real (kind=dp), parameter :: p_ulge  = 2.d0*(p_ulgr-p_ulgtm)
        real (kind=dp), parameter :: p_uepri = 4.d0*p_pi*10.d0**(p_ulgpl+3.d0*p_ulgr+p_ulge-50.d0)
        real (kind=dp), parameter :: p_utime = 10.d0**p_ulgtm
        real (kind=dp), parameter :: p_ur    = 10.d0**p_ulgr
        real (kind=dp), parameter :: p_up    = 10.d0**(p_ulgp - p_ulgpu)
        real (kind=dp), parameter :: p_upu    = 10.d0**p_ulgpu != 1.0000E+07
        real (kind=dp), parameter :: p_upi   = 1.d0/p_up
        real (kind=dp), parameter :: p_ue_cgs    = 10.d0**(p_ulge) ! from cgs to stella
        real (kind=dp), parameter :: p_ue_urs    = 10.d0**(p_ulge - p_ulgeu) ! from ursos to stella
        real (kind=dp), parameter :: p_ueu    = 10.d0**p_ulgeu  ! = 1.0000E+13 ursos in CGS
!!!        real (kind=dp), parameter :: p_ueu    = 10.d0**p_ulgeu  ! = 1.0000E+13 ursos in CGS
        real (kind=dp), parameter :: p_uei   = 1._dp / p_ue_cgs
        real (kind=dp), parameter :: p_iurs  = log10( 10.d0**p_ulgr / p_rsol )
        real (kind=dp), parameter :: p_urs   = 10.d0**p_iurs
        real (kind=dp), parameter :: p_um    = p_urho*p_ur**3.d0 / p_cms ! != UM (stella) = 5.0277E+02
        real (kind=dp), parameter :: p_um4pi    = 4.d0*p_pi*p_um ! == UM (old stella) = 6.3179E+03 
        real (kind=dp), parameter :: p_urm   = p_ur/p_rsol
        real (kind=dp), parameter :: p_ufreq   = p_k * p_utp / p_h;
  
  contains

!!*** *************************************************************************
!!****s* stl_units/sub_s2w  *
!!
!!   NAME
!!     sub_s2w
!!
!!   FUNCTION
!!     Convert from stella units to world's units
!!
!!   ARGUMENTS
!!      - rho     !  stella density
!!      - time    !  stella time
!!      - mass    !  stella mass
!!      - lenght  !  stella lenght
!!      - press   !  stella pressure
!!      - T    !  stella temperature
!!
!!   AUTHOR
!!      Baklanov
!!
!!   MODIFICATION HISTORY
!!    created  07.2006
!!
!!   SOURCE
!!***************************************************************************
  
  elemental subroutine sub_s2w(rho, time, mass &
                                , lenght, press, E_urs, E, T, v, freq ) 
    real(kind=dp), intent(inout), optional  :: rho, time, mass &
                                        ,lenght, press, E_urs, E, T, v, freq
    
    if ( present ( rho )  ) rho = s2w(rho=rho)
    if ( present ( time ) ) time =  s2w(time=time) !  time * p_utime
    if ( present ( mass ) ) mass =  s2w(mass=mass) ! mass * p_um4pi
    if ( present ( lenght)) lenght =  s2w(lenght=lenght) ! lenght * p_ur    
    if ( present ( press )) press =  s2w(press=press) ! press * p_upu    
    if ( present ( T ) ) T =  s2w(T=T) !  T * p_utp     
    if ( present ( E_urs )  ) E_urs =   s2w(E_urs=E_urs) ! erg * p_ueu
    if ( present ( E )  ) E =   s2w(E=E) ! erg * p_ueu
    if ( present ( v )  )   v =  s2w(v=v) !  v * p_uv
    if ( present ( freq )  )   freq =  s2w(freq=freq) !  v * p_uv
  end subroutine sub_s2w
 
 !***************************************************************************  
      
elemental  function s2w(rho, time, mass &
                                , lenght, press, E_urs, E, T, v, freq ) result(res)
 
    real(kind=dp), intent(in), optional  :: rho, time, mass &
                                        ,lenght, press, E_urs, E, T, v, freq
    real(kind=dp) :: res    
    
    if ( present ( rho ) )    res  = rho * p_urho;
    if ( present ( time ) ) res = time * p_utime
    if ( present ( T ) )      res = T * p_utp    
    if ( present ( mass ) ) res = mass * p_um4pi    
    if ( present ( lenght ) ) res = lenght * p_ur    
    if ( present ( press ) )  res = press * p_upu         
    if ( present ( E_urs ) )    res = E_urs * p_ueu    
    if ( present ( E ) )        res = E * p_ue_cgs
    if ( present ( v ) )      res = v * p_uv    
    if ( present ( freq ) )   res = freq * p_ufreq
    
  end function s2w

!***************************************************************************  
elemental  function w2s(rho, time, mass &
                                , lenght, press, E_urs, E, T, v, freq ) result(res)
 
    real(kind=dp), intent(in), optional  :: rho, time, mass &
                                        ,lenght, press, E_urs, E, T, v, freq
    real(kind=dp) :: res    
    
    if ( present ( rho ) )    res = rho / p_urho    
    if ( present ( time ) ) res = time / p_utime    
    if ( present ( T ) )      res = T / p_utp    
    if ( present ( mass ) ) res = mass / p_um4pi    
    if ( present ( lenght ) ) res = lenght / p_ur
    if ( present ( press ) ) res = press / p_upu
    if ( present ( E_urs ) )  res = E_urs / p_ueu
    if ( present ( E ) )  res = E / p_ue_cgs
    if ( present ( v ) )    res = v / p_uv
    if ( present ( freq ) ) res = freq / p_ufreq
    
  end function w2s
  
elemental  subroutine sub_w2s(rho, time, mass &
                                , lenght, press, E_urs, E, T, v, freq ) 
    real(kind=dp), intent(inout), optional  :: rho, time, mass &
                                        ,lenght, press, E_urs, E, T, v, freq

    if ( present ( rho ) )           rho = w2s(rho=rho)
    if ( present ( time ) )     time = w2s(time=time)
    if ( present ( mass ) )     mass = w2s(mass=mass)
    if ( present ( lenght ) ) lenght = w2s(lenght=lenght)
    if ( present ( press ) )   press = w2s(press=press)
    if ( present ( T ) )               T = w2s(T=T)
    if ( present ( E_urs ) )       E_urs = w2s(E_urs=E_urs)
    if ( present ( E ) )       E = w2s(E=E)
    if ( present ( v ) )           v = w2s(v=v)
    if ( present ( freq ) )     freq = w2s(freq=freq)
  end subroutine sub_w2s
 
 !***************************************************************************  
elemental  subroutine sub_drv_World2Stella(PT, PPl, ET_urs, EPl, XePl, XeT, d_dt)
    real(kind=dp), intent(inout), optional  :: PT, PPl, ET_urs, EPl, XePl, XeT, d_dt
    
	if ( present ( PT ) )  PT = w2s_drv( PT = PT)
	if ( present ( PPl) )  PPl= w2s_drv( PPl = PPl )
	if ( present ( ET_urs ) )  ET_urs = w2s_drv( ET_urs = ET_urs )
	if ( present ( EPl) )  EPl= w2s_drv( EPl = EPl )
!     if ( present ( XePl) )  XePl= XePl   * p_urho
    if ( present ( XeT) )  XeT= w2s_drv( XeT = XeT )
    if ( present ( d_dt) )  d_dt= w2s_drv( d_dt=d_dt )
  end subroutine sub_drv_World2Stella
 
 !***************************************************************************  
elemental  subroutine sub_drv_Stella2World(PT, PPl, ET_urs, EPl, XeT, d_dt)
    real(kind=dp), intent(inout), optional  :: PT, PPl, ET_urs, EPl, XeT, d_dt
    
    if ( present ( PT ) )  PT = s2w_drv(PT=PT)    ! PT  * p_upu / p_utp
    if ( present ( PPl) )  PPl= s2w_drv(PPl=PPl)    !PPl * p_upu / p_urho
    if ( present ( ET_urs ) )  ET_urs = s2w_drv(ET_urs=ET_urs)    !ET_urs  * p_ueu / p_utp
    if ( present ( EPl) )  EPl= s2w_drv(EPl=EPl)    !EPl * p_ueu
    if ( present ( XeT) )  XeT = s2w_drv(XeT=XeT)    !XeT / p_utp
    if ( present ( d_dt) )   d_dt = s2w_drv(d_dt=d_dt)    !XeT / p_utp
  end subroutine sub_drv_Stella2World

 !***************************************************************************  

elemental  function w2s_drv(ET, PT, PPl, ET_urs, EPl, XePl, XeT, d_dt ) result(res)
    real(kind=dp), intent(in), optional  :: ET;
    real(kind=dp), intent(in), optional  :: PT, PPl, ET_urs, EPl, XePl, XeT, d_dt
    real(kind=dp) :: res    
    
    if ( present ( PT ) )   res = PT  / p_upu * p_utp;
    if ( present ( PPl ) )  res = PPl / p_upu * p_urho;     
    if ( present ( ET ) )   res = ET  / p_ue_cgs * p_utp;    
    if ( present ( ET_urs ) )   res = ET_urs  / p_ueu * p_utp;    
    if ( present ( EPl ) )  res = EPl / p_ueu; ! * p_urho;    
    if ( present ( XePl ) ) res = XePl; ! * p_urho; 
    if ( present ( XeT ) )  res = XeT  * p_utp;
    if ( present ( d_dt ) )   res = d_dt * p_utime;
             
  end function w2s_drv 
 
 !***************************************************************************  

elemental  function s2w_drv(ET, PT, PPl, ET_urs, EPl, XePl, XeT, d_dt ) result(res)
    real(kind=dp), intent(in), optional  :: ET;
    real(kind=dp), intent(in), optional  :: PT, PPl, ET_urs, EPl, XePl, XeT, d_dt
    real(kind=dp) :: res    
    
    if ( present ( PT ) )    res = PT  * p_upu / p_utp;     
    if ( present ( PPl ) )   res = PPl * p_upu / p_urho;    
    if ( present ( ET ) )    res = ET  * p_ue_cgs / p_utp;    
    if ( present ( ET_urs ) )    res = ET_urs  * p_ueu / p_utp;    
    if ( present ( EPl ) )   res = EPl * p_ueu;! / p_urho;;    
    if ( present ( XePl ) )  res = XePl; !  / p_urho;
    if ( present ( XeT ) )   res = XeT  / p_utp;
    if ( present ( d_dt ) )   res = d_dt / p_utime;
             
  end function s2w_drv 
 
 !***************************************************************************  
  subroutine write_stl_units(output_unit)
  	integer, intent(in) :: output_unit
  	character(len=*), parameter ::  subrtn_name = 'write_stl_units' &
                                       , fullPathSubrtn = mdl_name//'.'//subrtn_name
	  write (unit=output_unit,fmt="(/A)")&
	    "**************  STELLA UNITS  *******************************"
	  write (unit=output_unit,fmt="(A/)") "*** stella units"
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_ur = ',p_ur
      write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_um = ', p_um
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_utime = ',p_utime
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_uv = ',p_uv
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_urho = ',  p_urho
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_utp = ',p_utp
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_upu = ', p_upu
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_ue_cgs = ', p_ue_cgs
!	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_ue = ', p_ue
	  write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_ueu = ', p_ueu
      write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_ufreq = ', p_ufreq
      write (unit=output_unit,fmt="(T5,A,T25,1pE12.4)")'p_um4pi = ', p_um4pi
	  write (unit=output_unit,fmt="(/A)")&
	    "************************************************************"
  end subroutine write_stl_units
end module stl_units

!******************************************************************************
