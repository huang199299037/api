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

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class args_curl(db.Model):
    __tablename__='args_curl'
    args_id=db.Column(db.Integer,primary_key=True)
    args_ipversion=db.Column(db.Integer)
    args_url=db.Column(db.String(45))
    args_timeout=db.Column(db.Integer)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Map(db.Model):
    __tablename__ = 'map'
    map_id = db.Column(db.Integer,primary_key=True, nullable=False)
    map_desc = db.Column(db.String(255))
    map_ofid = db.Column(db.Integer,nullable=False)
    map_ofname = db.Column(db.String(255),nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))









