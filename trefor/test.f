      implicit real*8(a-h,o-z)
      parameter ( mn = 100 )  
      integer int(mn), sum, x

      write(*,*) 'number of elements'
      read(*,*) n
      write(*,*) 'enter the elements'
      read(*,*) (int(j),j=1,n)

      sum = 0
      do i = 2, n
         do j = 1, i-1
            call product(int(i),int(j),x)
            sum = sum + x
         enddo
      enddo

      write(*,*) 'sum -', sum

      stop
      end

      subroutine product(i,j,x)
      implicit real*8(a-h,o-z)
      integer i,j,x

      x = i*j

      return
      end

