#!/bin/ksh

date=20190207
run=00
lagg=6
couplfr=6
leadtime=30
mem=01

actdate=$(date '+%Y%m%d');
actdate1=$(/home/ms/at/kmcw/bin/datecalc ${actdate} -f -t -1 | cut -c 1-8)

echo $actdate
echo $actdate1

echo $date

if [[ $date == $actdate || $date == $actdate1 ]]
then

   HIST=.FALSE.

else

   HIST=.TRUE.

fi

echo $HIST
