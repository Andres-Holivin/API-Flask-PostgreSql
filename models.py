from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship,validates
import sqlalchemy.dialects.postgresql as postgresql
import uuid
class UserModel(db.Model):
    __tablename__='userlgamez'
    userid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(255))
    userimgurl=db.Column(db.String(255))
    username=db.Column(db.String(255)) 
    email=db.Column(db.String(255))
    password=db.Column(db.String(255))
    dob=db.Column(db.DateTime)
    create_on=db.Column(db.Date)
    user_in=db.Column(db.String(255))
class RevokedModel(db.Model):
    __tablename__='revoked_token'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    jti=db.Column(db.String(255))
class CategoryModel(db.Model):
    __tablename__='category'
    categoryid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    categoryname=db.Column(db.String(255))
    categoryimgurl=db.Column(db.String(255))
class ForumReplayModel(db.Model):
    __tablename__='forumreplay'
    replayid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    threadid=db.Column(db.Integer,db.ForeignKey('forumthread.threadid'))
    userid=db.Column(db.Integer,db.ForeignKey('userlgamez.userid'))
    description=db.Column(db.String(255))    
    create_on=db.Column(db.Date)
    user_in=db.Column(db.String(255))
class ForumThreadModel(db.Model):
    __tablename__='forumthread'
    threadid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    userid=db.Column(db.Integer,ForeignKey('userlgamez.userid'))
    title=db.Column(db.String(255))
    description=db.Column(db.String(255))
    interested=db.Column(db.Integer)    
    create_on=db.Column(db.Date)
    user_in=db.Column(db.String(255))
    replay = db.relationship("ForumReplayModel",backref='replayName')    
class ProductNameModel(db.Model):
    __tablename__='productname'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(255))
    date_in=db.Column(db.Date)
    date_up=db.Column(db.Date)
    status=db.Column(db.String(255))
class ProductSellModel(db.Model):
    __tablename__='productsell'
    id=db.Column(postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True)
    productid=db.Column(db.Integer,ForeignKey('productname.id'))
    modal=db.Column(db.Float)
    harga_jual=db.Column(db.Float)
    terjual=db.Column(db.Float)
    date_in=db.Column(db.Date)
    date_up=db.Column(db.Date)
    status=db.Column(db.String(255))

class ProductStockModel(db.Model):
    __tablename__='productstock'
    id=db.Column(db.String(255),primary_key=True,default=uuid.uuid4)
    productid=db.Column(db.Integer,ForeignKey('productname.id'))
    modal=db.Column(db.Float)
    harga_jual=db.Column(db.Float)
    jumlah=db.Column(db.Float)
    date_in=db.Column(db.Date)
    date_up=db.Column(db.Date)
    status=db.Column(db.String(255))