import pymysql

def shujuku(sql):
    db=pymysql.connect(
                user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
                password="123456",
                host='localhost',
                database='fenci',
                port=3306,
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
                )
    cursor=db.cursor()
    try:
        cursor.execute(sql)
        datas=cursor.fetchall()
        print(datas)
        if datas:
            return datas
        else:
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return 0
    finally:
        db.close()

if __name__ == '__main__':
    # sql="create table teacher(id int not null auto_increment primary key,name varchar(255),age int,score int(100)) engine=InnoDB  default charset=utf8"
    # sql='show tables'
    # sql='insert into student(id,name,age) values(1,"张三",98),(2,"李四",56)'
    # sql="select * from student"
    sql="create TABLE lyb(id int UNSIGNED not null auto_increment PRIMARY KEY,nikename VARCHAR(255) not NULL,info text not NULL,data datetime not NULL) ENGINE=INNODB DEFAULT CHARSET=utf8mb4"
    data=shujuku(sql)
    print(data)
