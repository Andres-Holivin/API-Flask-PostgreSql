from typing import cast
from sqlalchemy.sql import select
from models import *
from app import db
from passlib.hash import pbkdf2_sha256 as sha256
from Schema import *
from flask import jsonify
from sqlalchemy import func,join
class RepositoryUser():
    def seve_to_db(UserModel):
        db.session.add(UserModel)
        db.session.commit()
        return "success"
    def return_all():
        def to_json(UserModel):
            return{
                'userid':UserModel.userid,
                'userimgurl':UserModel.userimgurl,
                'name':UserModel.name,
                'username':UserModel.username,
                'email':UserModel.email,
                'password':UserModel.password,
                'dob':UserModel.dob.strftime('%m/%d/%Y'),
                'create_on':UserModel.create_on.strftime('%m/%d/%Y'),
                'user_in':UserModel.user_in
            }
        return{'userlgamez':list(map(lambda UserModel:to_json(UserModel),UserModel.query.all()))}
    def find_by_username(username):
        return UserModel.query.filter_by(username=username).first()
    def generate_hash(password):
        return sha256.hash(password)
    def verify_hash(password,hash):
        return sha256.verify(password,hash)
    def get_name_by_id(UserId):        
        return [{'name':a.name} for a in UserModel.query.with_entities(UserModel.name).filter_by(userid=UserId).all()]        
class RepositoryRevoke():
    def add(revokedModel):
        db.session.add(revokedModel)
        db.session.commit()
        return "success"
    def is_jti_blacklisted(jti):
        query=RevokedModel.query.filter_by(jti=jti).first()
        return bool(query)

class RepositoryCategory():
    def return_all():
        def to_json(CategoryModel):
            return{
                'categoryid':CategoryModel.categoryid,
                'categoryname':CategoryModel.categoryname,
                'categoryimgurl':CategoryModel.categoryimgurl
            }
        return{'userlgamez':list(map(lambda CategoryModel:to_json(CategoryModel),CategoryModel.query.all()))}
class RepositoryForum():
    def get_all_forum():        
        form=ForumThreadSchema(many=True)
        query=ForumThreadModel.query.all()  
        return jsonify({"Forum":form.dump(query)})
    def get_thread_by_id(ThreadId):
        thread=ForumThreadModel.query.filter_by(threadid=ThreadId).first()
        return thread        
    def insert_forum_thread(ForumThread):
        db.session.add(ForumThread)
        db.session.commit()
        return "success"
    def insert_forum_replay(ForumReplay):
        db.session.add(ForumReplay)
        db.session.commit()
        return "success"
    def getReplayById(ThreadId):
        replay=ForumReplayModel.query.filter_by(threadid=ThreadId).all()
        forumReplay=ForumReplaySchema(many=True)
        return jsonify({"ForumReplay":forumReplay.dump(replay)})
class RepositoryToko:
    def get_all_product_sell():
        productSell=db.session.\
        query(ProductSellModel.id,ProductSellModel.modal,ProductSellModel.harga_jual,ProductSellModel.terjual,ProductNameModel.name)\
        .distinct(ProductSellModel.id).join(ProductNameModel,ProductSellModel.productid==ProductNameModel.id).filter(ProductSellModel.status=='A').all()
        productSellSchemas=ProductSellSchema(many=True)
        return jsonify({"ProductSell":productSellSchemas.dump(productSell)})
    def get_all_product_stock():
        productStock=db.session.\
        query(ProductStockModel.id,ProductStockModel.modal,ProductStockModel.harga_jual,ProductStockModel.jumlah,ProductNameModel.name)\
        .distinct(ProductStockModel.id).join(ProductNameModel,ProductStockModel.productid==ProductNameModel.id).filter(ProductStockModel.status=='A').all()
        productStockSchemas=ProductSellSchema(many=True)
        return jsonify({"ProductSell":productStockSchemas.dump(productStock)})
    def find_product_name_by_name(ProductName):
        return ProductNameModel.query.filter(func.upper(ProductNameModel.name)==(ProductName.upper())).all()
    def find_product_name_by_id(ProductId):
        return ProductNameModel.query.filter_by(id=ProductId).first()
    def find_product_stock_by_id(ProductId):
        return ProductStockModel.query.filter_by(productid=ProductId).first()
    def get_all_product_name():
        productName=ProductNameModel.query.all()
        productNameSchemas=ProductNameSchema(many=True)
        return jsonify({"ProductName":productNameSchemas.dump(productName)})
    def insert_product_name(ProductName):
        try:
            db.session.add(ProductName)
            db.session.commit()
            return 'success'
        except:
            return 'error'
    def insert_product_sell(ProductSell):
        try:
            db.session.query(ProductStockModel).filter(ProductStockModel.productid==ProductSell.productid)\
            .update({ProductStockModel.jumlah:ProductStockModel.jumlah-ProductSell.terjual})
            db.session.add(ProductSell)
            db.session.commit()
            return 'success'
        except:
            db.session.rollback()
            return 'error'
