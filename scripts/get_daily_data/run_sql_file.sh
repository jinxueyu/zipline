#!/bin/sh

source /home/hadoop/jiangtianyu/oracle/config/init.config

export NLS_LANG="AMERICAN_AMERICA.UTF8"

db_config=$1
source ${db_config}

sql_file=$2

output_file=$3

date=$4

sqlStr=`cat ${sql_file}`
sqlStr=${sqlStr//\$\{code\}/${date}}

echo ${sqlStr}

/home/hadoop/jiangtianyu/oracle/bin/sqluldr2 user=${user}/${pwd}@${host}:${port}/${db} query="${sqlStr}" file=${output_file} head=yes
