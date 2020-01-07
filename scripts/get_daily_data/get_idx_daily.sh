while read e ; do
    echo ${e}
    sh run_sql_file.sh config/testDB_eastmoney.config sql/get_one_idx.sql daily/${e}.csv ${e:0:6}
done < ${1}