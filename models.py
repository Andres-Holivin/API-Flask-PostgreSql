from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
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
    # thread=db.relationship('ForumThreadModel',foreign_keys='ForumReplayModel.threadid')
    # thread=db.relationship("ForumThreadModel",back_populates='replay' )
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
    
    
