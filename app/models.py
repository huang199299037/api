import pymysql
from config import db_config,args_curl,args_ping,users
from flask_login import UserMixin
from . import db,login_manager


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(64),unique=True,index=True)
    user_passwd = db.Column(db.String(256),index=True)
    user_admin = db.Column(db.Integer)
    @property
    def id(self):
        return self.user_id


class args_ping(db.Model):
    __tablename__ = 'args_ping'
    args_id=db.Column(db.Integer,primary_key=True)
    args_ipversion = db.Column(db.Integer)
    args_url=db.Column(db.String(100))
    args_packagesize=db.Column(db.Integer)
    args_count=db.Column(db.Integer)
    args_timeout=db.Column(db.Integer)


class args_curl(db.Model):
    __tablename__='args_curl'
    args_id=db.Column(db.Integer,primary_key=True)
    args_ipversion=db.Column(db.Integer)
    args_url=db.Column(db.String(45))
    args_timeout=db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def data_query(tables):
    con = pymysql.connect(**db_config)
    cursor = con.cursor()
    if tables == "users":
        try:
            sql = """select * from users"""
            cursor.execute(sql)
        except:
            print("There is no table named users")
            con.rollback()
        row_users = cursor.fetchall()
        user_list=list()
        for i in range(len(row_users)):
            user_dict = dict()
            for j in range(len(users)):
                user_dict[users[j]]=row_users[i][j]
            user_list.append(user_dict)
        return user_list
    elif tables == "args_ping":
        try:
           sql = """select * from args_ping"""
           cursor.execute(sql)
        except:
            print("There is no table named args_ping")
            con.rollback()
        row_ping = cursor.fetchall()
        # con.close()
        ping_list = list()
        for i in range(len(row_ping)):
            ping_dict = dict()
            for j in range(len(args_ping)):
                if j==0:
                    continue
                ping_dict[args_ping[j]] = row_ping[i][j]
            ping_list.append(ping_dict)
        return ping_list

    elif tables == "args_curl":
        try:
             sql = """select * from args_curl """
             cursor.execute(sql)
        except:
            print("There is no table named args_curl")
            con.rollback()
        row_curl = cursor.fetchall()
        # con.close()
        curl_list = []
        for i in range(len(row_curl)):
            curl_dict = {}
            for j in range(len(args_curl)):
                curl_dict[args_curl[j]] = row_curl[i][j]
            curl_list.append(curl_dict)
        return curl_list


def insert_tables(tables,*kwargs):
    con = pymysql.connect(**db_config)
    cursor = con.cursor()
    if tables == "args_curl":
        try:
           sql = "INSERT INTO args_curl VALUES ('%d','%d','%s','%d')" % (0,kwargs[0],kwargs[1],kwargs[2])
           cursor.execute(sql)
           con.commit()
        except:
            con.rollback()
    elif tables == "args_ping":
        try:
             sql = "INSERT INTO args_ping VALUES('%d','%d','%s','%d','%d','%d')" % (0,kwargs[0],kwargs[1],kwargs[2],kwargs[3],kwargs[4])
             cursor.execute(sql)
             con.commit()
        except:
            con.rollback()






