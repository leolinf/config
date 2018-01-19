-mysql-connector-python-

这是一个与mysqldb实现功能大同小异的驱动由于博客还没有搭建好，所以先用代码管理器记录下：

首先mysqldb想来大家用Python的都比较熟悉了吧，网上实例也比较多了。 今天我就想分享一篇用mysql.connector这个驱动操作数据的实例。

首先说一下linux系统，系统python都自带有mysql.connector这个驱动包的，只有windows环境下需要自己手动安装，可以到官网去下载安装包 链接：https://dev.mysql.com/downloads/connector/python/2.1.html 如果linux想升级也可以下载安装

进入正题：链接数据库 import mysql.connector

建立链接： conn = mysql.connector.connect（user='root',password='***',host='localhost',port=3306,database='test',use_unicode=True,charset='utf8'）与mysqldb 不同的是passwd变成了password，db变成了database 建立游标： cursor = conn.cursor()

接下来就是操作数据库的更新，插入，删除等操作 这里主要列出与mysqldb不同的地方。 #通过这个可以做判断 cursor.execute("select * from table where id = %s",[123])#这里与mysqldb不同，mysqldb是tuple，这里是list row = cursor.fetchone() #更新 cursor.execute("update table set Num=%s where Id = %s",(123,123))#这里和mysqldb没有区别 conn.commit() #插入 cursor.execute("insert into table (matchId,matchNum) values(%s,%s)",[123,123])#这里与mysqldb不同，mysqldb是tuple，这里是list conn.commit() #删除 cursor.cexcute("DELETE FROM books WHERE id = %s" (213,))#这里和mysqldb没有区别 conn.commit()

如有其它疑问可以查看官方文档：http://www.mysqltutorial.org/python-mysql-delete-data/
