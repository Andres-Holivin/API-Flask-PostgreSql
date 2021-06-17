from models import *
from app import db
from passlib.hash import pbkdf2_sha256 as sha256
from Schema import *
from flask import jsonify
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
        form=ForumThreadSchema()
        query=ForumThreadModel.query.all()
        x=form.dump(query)
        x=[]
        for a in range(len(query)):
            x.append(form.dump(query[a]))        
        return jsonify({"Forum":x})
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
    def getReplayById():
        # replay=ForumReplayModel.query.filter_by(threadid=ThreadId).all()
        replay=ForumReplayModel.query.all()
        forumReplay=ForumReplaySchema()
        x=[]
        for a in range(len(replay)):
            x.append(forumReplay.dump(replay[a]))
        return jsonify({"ForumReplay":x})