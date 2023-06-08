#!/bin/bash
# a script to remove run files except for *.dat

echo removing $1.* files

for INP in $1.*
do
 echo processing $INP
  if [ $INP = $1.dat ]; then
   echo  $INP preserved
 else
   rm $INP
   echo remove $INP completed
 fi
done
echo process ended, please check "$1.*" files
 
