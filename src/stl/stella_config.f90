module stella_config
   use kinds,                           only: dp
   use phys_constants,          only:  p_c
   use cp_files,                  only: open_file, close_file

    implicit none
    private

   character(len=*), parameter, private :: mdl_name = 'stella_config'
   character(len=*), parameter, private :: file_stella_config = 'stella_config.dat'

!! COMMON
    integer, parameter, public :: p_Nvars  = 3                 ! -- 3 - NOCONV,4 - CONV !--NVARS - number of independent variables
!    integer, parameter, public :: p_Nfreq  = 300
    integer, parameter, public :: p_Nfreq  = 100
    integer, parameter, public :: p_default_nums_mu  = 30      !   number of rays by mu
!    integer, parameter, public :: p_Mzon   = 88  !  for W7 Nomoto's model
!    integer, parameter, public :: p_Mzon   = 600 ! for thick layer as Utrobin
!    integer, parameter, public :: p_Mzon   = 100
!    integer, parameter, public :: p_Mzon   = 90
    integer, parameter, public :: p_Mzon   = 300
!    integer, parameter, public :: p_Mzon   = 45  ! for m030307G model
    integer, parameter, public :: p_NYDim  = (p_Nvars+2*p_Nfreq)*p_Mzon
    integer, parameter, public :: p_MaxDer = 4
    integer, parameter, public :: p_NZ     = 3000000
    integer, parameter, public :: p_KOMAX  = 80

    real (kind=dp), parameter, public :: p_wlmax = 50000._dp;! in A
    real (kind=dp), parameter, public :: p_wlmin = 1._dp;! in A
!    real (kind=dp), parameter, public :: p_wlmin = 40._dp;! for Uli, in A

    real (kind=dp), parameter, public :: p_freq_min = p_c / ( p_wlmax * 1.e-8_dp ) ! to A
    real (kind=dp), parameter, public :: p_freq_max = p_c / ( p_wlmin * 1.e-8_dp ) ! to A
    logical, save, public :: EachStepOutput = .false.

!!  URSOS
    logical, save, public :: p_is_ursos_lucy = .false.  ! method: false -> lte, true -> lucy
    logical, save, public :: p_is_ursos_pfsaha = .false. ! method: false -> ground states, true -> call pfsaha
    real(dp), save, public :: p_time_delay_ursos = 0._dp ! time delay to start tday > p_time_delay_ursos
    logical, save, public :: p_is_ursos_saha_only = .true. ! if true => always sahaandd
    logical, save, public :: p_is_drv_numeric = .true.  ! if true => compute derivatives in ursos with numeric method
    logical, save, public :: p_is_drv_numeric_with_Trad = .true.  ! if true => compute derivatives in ursos with numeric method

!!  OPACITY
    logical, save, public :: p_is_opacity_bb = .true.
    logical, save, public :: p_is_opacity_bf = .true.
    logical, save, public :: p_is_opacity_ff = .true.
    logical, save, public :: p_is_opacity_hminus = .true.
    logical, save, public :: p_is_opacity_bf_photocross = .true.  ! if TRUE  use  cross_photo for bf sigma, else gshfdxsec (old)
!    logical, save, public :: p_is_opacity_bb = .false.
!    logical, save, public :: p_is_opacity_bf = .false.
!    logical, save, public :: p_is_opacity_ff = .false.
!    logical, parameter, public :: p_is_van_Regemorter = .true.
    logical, parameter, public :: p_is_van_Regemorter = .false.

!!  LINE ATOM DATA
    character(len=*), parameter, public :: p_dir_chem_data = '../vladsf'
    character(len=*), parameter, public :: p_dir_atom_data = p_dir_chem_data//'/atoms_data'
    character(len=*), parameter, public :: p_FileLineAtom = p_dir_chem_data//'/lineatom.dat'
    character(len=*), parameter, public :: p_FileLineAtomDump = p_dir_chem_data//'/linedata.dump'
    character(len=*), parameter, public :: p_xsecdatadir = p_dir_chem_data//'/yakovlev ';

    integer, parameter, public :: p_atom_source_wmbasic = 1
    integer, parameter, public :: p_atom_source_eastman = 20
    integer, parameter, public :: p_atom_source_kurucz = 30
    integer, parameter, public :: p_atom_source_kurucz_Kurgf2 = 32
!    integer, parameter, public :: p_atom_source_default = p_atom_source_kurucz
!    integer, parameter, public :: p_atom_source_default = p_atom_source_wmbasic
    integer, save, public :: p_atom_source_default = p_atom_source_eastman
    logical, save, public :: p_is_opacity_const = .false.  !  false  true
    logical, save, public :: p_is_Fe_add = .false.  !  false  true
    logical, save, public :: p_is_only_eastman_opacity = .false.  !  false  true

    integer, parameter, public :: p_opacity_qfactor_Znscat = -1  ! use 0 or less for qfactor = 1 forall Zn
    real(kind=dp), parameter, public :: p_global_qfactor = 1.00_dp

!    logical, save, public :: p_is_fluor_opacity = .true.  !  false  true
    logical, save, public :: p_is_fluor_opacity = .false.   !  false  true
!    logical, save, public :: p_is_fluor_branching = .true.  !  false  true
    logical, save, public :: p_is_fluor_branching = .false.  !  false  true
!    logical, save, public :: p_is_fluor_branching_aprox_enable = .true.  !  false  true
    logical, save, public :: p_is_fluor_branching_aprox_enable = .false.  !  false  true

!!  Isotopes
    character(len=4), save, dimension(1), public :: p_isotope_chains = (/'Ni56'/)
!    character(len=4), save, dimension(2), public :: p_isotope_chains = (/'Ni56','Fe52'/)
!   character(len=4), save, dimension(2), public :: p_isotope_chains = (/'Ni56','Cr48'/)  todo the correct order to xni-file
!    character(len=4), save, dimension(3), public :: p_isotope_chains = (/'Ni56','Fe52','Cr48'/)
    logical, save, public :: p_chain_is_eng_positrons = .true.  !  false  true
    logical, save, public :: p_chain_is_load_abn = size(p_isotope_chains) > 1
    real(kind=dp), parameter, public::  p_gamma_kappa0 = 0.05 ! 0.05_dp;  !



!!  TRANSFER EQUATION
    real(kind=dp), parameter, public::  p_T_rad_lim_min = 1.5e3_dp;  ! 4.e3_dp; ! 2.e3_dp; ! 1.5e3_dp;
    logical, save, public :: p_is_te_lucy = .false.  !  false  true
    logical, save, public :: p_is_fluor_te = .false.  !  false  true
    logical, save, public :: p_is_difmat_Teng = .true.  !  false  true
!    logical, save, public :: p_is_fluor_te = .true.  !  false  true
    logical, save, public :: p_is_HOLDFR = .true.  !  if .true., HOLDFR  is always true

!!  OUTPUT
    logical, parameter, public :: p_is_write_vtk = .false.
    logical, parameter, public :: p_is_write_silo = .false.

!! RUN CONTROL
    logical, save, public :: p_is_main_cycle_over = .false.

    public :: stl_general_write, stl_general_set
    public :: stl_general_kurucz_data_mode2str

 contains

!-------------------------------------------------------------------------
  subroutine stl_general_set(file)
    character(len=*), intent(in), optional ::  file
    character(len=*), parameter ::  subrtn_name = 'stl_general_set' &
                                       , fullPathSubrtn = mdl_name//'.'//subrtn_name
    integer :: unit_number
    logical :: exists
    character(len=80) ::  file_settings

    ! namelist/stl_ursos/p_is_ursos_saha_only, p_is_ursos_lucy, p_is_ursos_pfsaha

    ! namelist/stl_opacity/p_is_opacity_bb, p_is_opacity_bf, p_is_opacity_ff, p_is_opacity_bf_photocross &
    !                    , p_is_only_eastman_opacity, p_is_fluor_opacity, p_is_fluor_branching, p_is_fluor_branching_aprox_enable


    ! namelist/stl_transfer/p_is_te_lucy, p_is_fluor_te, p_is_difmat_Teng

    ! namelist/stl_atom_data/p_atom_source_default

!    namelist/stl_isotope_data/p_isotope_chains, p_chain_is_eng_positrons
    namelist/stl_isotope_data/p_chain_is_eng_positrons

    ! namelist/stl_run_control/p_is_main_cycle_over

    file_settings = file_stella_config
    if ( present(file) ) file_settings = file

    write(*,'(a)') repeat("-", 32);
    write(unit=*,FMT="(T2,A,T61,A)") 'Read STELLA settings from: ', file_settings

    !    write (unit=*,FMT="(T2,A,T41,L)") subrtn_name//": p_is_main_cycle_over = ", p_is_main_cycle_over


     inquire(file=trim(file_settings),exist=exists)

     if( exists ) then  ! read from file
        call open_file(file_settings,unit_number=unit_number)
    !    read(unit_number,stl_ursos)
     !   read(unit_number,stl_opacity)
      !  read(unit_number,stl_transfer)
       ! read(unit_number,stl_atom_data)
        read(unit_number,stl_isotope_data)
        !read(unit_number,stl_run_control)
        call close_file(unit_number)

        !
        ! the rules of dependences
        if ( p_is_ursos_saha_only ) then
           p_is_ursos_lucy = .false.
        endif

        if( .not.p_is_ursos_lucy ) p_is_te_lucy = .false.;

        if( p_is_opacity_const ) then
           p_is_only_eastman_opacity = .false.
           p_is_fluor_opacity = .false.
           p_is_opacity_bb = .false.
           p_is_opacity_bf = .false.
           p_is_opacity_ff = .false.
        endif

        if( p_is_only_eastman_opacity ) p_is_fluor_opacity = .false.;
        p_is_fluor_te = p_is_fluor_te .and. p_is_fluor_opacity
        p_is_fluor_branching = p_is_fluor_opacity .and. p_is_fluor_branching
        p_is_fluor_branching_aprox_enable = p_is_fluor_branching_aprox_enable .and. p_is_fluor_branching
     else
        write(*,'(/a,a,a)') fullPathSubrtn, ': No file: ',file_settings
        write(*,'(a,a/)') fullPathSubrtn, ': Used the default parameters '
     endif

  end subroutine stl_general_set
! -------------------------------------------------------------------------
  elemental function stl_general_kurucz_data_mode2str(method) result(res_str)
    integer, intent(in)  :: method
    character(len=9)  :: res_str

    res_str = "ERROR"

    select case(method)
      case(p_atom_source_wmbasic)
         res_str = "WMbasic"
      case(p_atom_source_kurucz)
         res_str = "KURUCZ"
      case(p_atom_source_eastman)
         res_str = "EASTMAN"
    end select
  end function stl_general_kurucz_data_mode2str

!-------------------------------------------------------------------------
   subroutine stl_general_write(output_unit)
    integer, intent(in)                      :: output_unit

    character(len=*), parameter ::  subrtn_name = 'stl_general_write' &
                                       , fullPathSubrtn = mdl_name//'.'//subrtn_name

          write (unit=output_unit,FMT="(/A)")"-----------------------------------------------------------"
          write (unit=output_unit,FMT="(A/)")"  General settings  "
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_main_cycle_over = ", p_is_main_cycle_over
          ! write (unit=output_unit,FMT="(A,I9)") "  p_Nvars = ", p_Nvars
          ! write (unit=output_unit,FMT="(A,I9)") "  p_KOMAX = ", p_KOMAX
          ! write (unit=output_unit,FMT="(/A)")"---------------------  SPACE  -------------------"
          ! write (unit=output_unit,FMT="(T2,A,T31,I9)") "p_Mzon  = ",p_Mzon
          ! write (unit=output_unit,FMT="(T2,A,T31,I9)") "p_NYDIM  = ", p_NYDIM
          write (unit=output_unit,FMT="(/A)")"---------------------  SPECTRA  -------------------"
          ! write (unit=output_unit,FMT="(T2,A,T31,I5)") "p_Nfreq  = ", p_Nfreq
          write (unit=output_unit,FMT="(T2,A,T31,1pe12.5)") "p_wlmin  = ", p_wlmin
          write (unit=output_unit,FMT="(T2,A,T31,1pe12.5)") "p_wlmax  = ", p_wlmax
          write (unit=output_unit,FMT="(T2,A,T31,1pe12.5)") "p_freq_min  = ", p_freq_min
          write (unit=output_unit,FMT="(T2,A,T31,1pe12.5)") "p_freq_max  = ", p_freq_max
          ! write (unit=output_unit,FMT="(/A)")"---------------------  URSOS  -------------------"
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_ursos_lucy  = ", p_is_ursos_lucy
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_ursos_pfsaha  = ", p_is_ursos_pfsaha
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_ursos_saha_only  = ", p_is_ursos_saha_only
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_drv_numeric  = ", p_is_drv_numeric
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_drv_numeric_with_Trad  = ", p_is_drv_numeric_with_Trad
          ! write (unit=output_unit,FMT="(T2,A,T31,1pE12.4)") "p_time_delay_ursos  = ", p_time_delay_ursos
          write (unit=output_unit,FMT="(/A)")"---------------------  OPACITY  -------------------"
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_opacity_bb  = ", p_is_opacity_bb
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_opacity_bf  = ", p_is_opacity_bf
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_opacity_ff  = ", p_is_opacity_ff
          write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_Fe_add  = ", p_is_Fe_add
          write (unit=output_unit,FMT="(T2,A,T31,1pE12.4)") "p_global_qfactor  = ", p_global_qfactor
          write (unit=output_unit,FMT="(T2,A,T31,I4)") "p_opacity_qfactor_Znscat  = ", p_opacity_qfactor_Znscat
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_opacity_hminus  = ", p_is_opacity_hminus
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_opacity_bf_photocross  = ", p_is_opacity_bf_photocross
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_opacity_const  = ", p_is_opacity_const
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_only_eastman_opacity  = ", p_is_only_eastman_opacity
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_fluor_opacity = ", p_is_fluor_opacity
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_fluor_branching = ", p_is_fluor_branching

          write (unit=output_unit,FMT="(/A)")"---------------------  ISOTOPES  -------------------"
          write (unit=output_unit,FMT="(T2,A,T31,3(1x,A))") "p_isotope_chains  = ", p_isotope_chains
          write (unit=output_unit,FMT="(T2,A,T31,L)") "p_chain_is_eng_positrons  = ", p_chain_is_eng_positrons

          write (unit=output_unit,FMT="(/A)")"---------------------  ISOTOPES  & ENERGY SOURCES  -------------------"
          write (unit=output_unit,FMT="(T2,A,T31,3(1x,A))") "p_isotope_chains  = ", p_isotope_chains
          write (unit=output_unit,FMT="(T2,A,T31,L)") "p_chain_is_eng_positrons  = ", p_chain_is_eng_positrons
          write (unit=output_unit,FMT="(T2,A,T31,1pe12.5)") "p_gamma_kappa0  = ", p_gamma_kappa0

          write (unit=output_unit,FMT="(/A)")"---------------------  TRANSFER  -------------------"
          ! write (unit=output_unit,FMT="(T2,A,T31,1pe12.5)") "p_T_rad_lim_min  = ", p_T_rad_lim_min
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_te_lucy  = ", p_is_te_lucy
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_fluor_te       = ", p_is_fluor_te
          ! write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_difmat_Teng  = ", p_is_difmat_Teng
          write (unit=output_unit,FMT="(T2,A,T31,L)") "p_is_HOLDFR  = ", p_is_HOLDFR

          ! write (unit=output_unit,FMT="(/A)")"---------------------  LINE ATOM DATA  -------------------"
          ! write (unit=output_unit,FMT="(T2,A,T31,A)") "p_dir_chem_data  = ", p_dir_chem_data
          ! write (unit=output_unit,FMT="(T2,A,T31,A)") "p_FileLineAtom  = ", p_FileLineAtom
          ! write (unit=output_unit,FMT="(T2,A,T31,A)") "p_FileLineAtomDump       = ", p_FileLineAtomDump
          ! write (unit=output_unit,FMT="(T2,A,T31,A)") "p_dir_atom_data  = ", p_dir_atom_data
          ! write (unit=output_unit,FMT="(T2,A,T31,A)") "p_xsecdatadir  = ", p_xsecdatadir
          ! write (unit=output_unit,FMT="(T2,A,T31,A)")"p_atom_source_default  = ", &
          !                                     stl_general_kurucz_data_mode2str(p_atom_source_default)
          write (unit=output_unit,FMT="(/A)")"-----------------------------------------------------------"
          write (unit=output_unit,FMT="(/A)")" "

    end subroutine stl_general_write
end module  stella_config

