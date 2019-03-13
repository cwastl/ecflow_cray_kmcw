#!/bin/ksh

date=20190312
curdate=$(date +%Y%m%d)
sname=claef

echo $curdate $date

if [ ${date} -eq ${curdate} ]
then

   echo "Everything ok"

else

   echo "date wrong - set suite"  ${sname} "complete" 

fi

