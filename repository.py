from models import UserModel,RevokedModel,CategoryModel
from run import db
from passlib.hash import pbkdf2_sha256 as sha256
class RepositoryUser():
    def seve_to_db(UserModel):
        db.session.add(UserModel)
        db.session.commit()
    def return_all():
        def to_json(UserModel):
            return{
                'userid':UserModel.userid,
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

class RepositoryRevoke():
    def add(revokedModel):
        db.session.add(revokedModel)
        db.session.commit()
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
