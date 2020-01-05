#!/usr/bin/env bash

startdate=${1}
enddate=${2}

curr="${enddate}"
while true
do
    if [ ${curr} -lt ${startdate} ] ; then
        break
    fi
    #echo ${curr}
    ## ---- next can replace by any cmd begin
    result=`sh /opt/applications/script/check_trade_date/check_date.sh ${curr}`
    echo ${curr}SS${result}
    ## ---- next can replace by any cmd end
    curr=$( date +%Y%m%d --date "$curr -1 day" )
done