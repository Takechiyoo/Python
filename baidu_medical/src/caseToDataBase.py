# -*- coding: utf-8 -*-
import pandas as pd
import MySQLdb
import os

# Test
path = r'D:\tutorial\data'

error_count = 0

files = os.listdir(path)
for name in files:
    data = pd.DataFrame()
    filename = os.path.join(path, name)
    try:
        data = pd.read_csv(filename, sep = '\t', header = None)
        data = data.transpose()
        #print data
        data = data.ix[:, [0,1,2,4,8,12,13,14]].drop([0])
    except:
        error_count += 1
        print filename
    print data.columns
    conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '920129', db = 'baidu', use_unicode=1, charset = 'utf8')
    try:
        data.to_sql(con = conn, name = 'dataframe_test', if_exists = 'append', flavor = 'mysql', index = False)
        conn.commit()
    except Exception, e:
        print e
        print "error!"
        conn.rollback()
    print "success!"

conn.close()

print error_count
print "hello world"