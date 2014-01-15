
import MySQLdb
db=MySQLdb.connect(host='localhost',user='root',passwd='rapero04',db='ejemplo')
cursor=db.cursor()
sql='select *from distros'
cursor.execute(sql)
resultado=cursor.fetchall()
for registro in resultado:
    print registro[0] , ' | ' , registro[1] ," | " , registro[2]

