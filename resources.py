from flask.json import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import null
from models import *
from datetime import datetime
from repository import *
from flask import jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt)

parser = reqparse.RequestParser()

class Home(Resource):
    def get(self):
        return jsonify({"name":"hello"})
class UserRegistration(Resource):
    def post(self):
        parser.add_argument('Name',required ="true")
        parser.add_argument('Username',required ="true")
        parser.add_argument('Email',required ="true")
        parser.add_argument('Password',required ="true")
        parser.add_argument('DOB',required ="true")
        data = parser.parse_args() 
        if(RepositoryUser.find_by_username(data['Username'])):
            return {'message':"UserName {} already exists".format(data['Username'])}
        else:
            new_user=UserModel(
                name=str(data['Name']),
                username=str(data['Username']),
                userimgurl='-',
                email=str(data['Email']),
                password=RepositoryUser.generate_hash(str(data['Password'])),
                dob=datetime.strptime(data['DOB'],'%d/%m/%Y').date(),
                create_on=datetime.now(),
                user_in=str(data['Name'])
            )
            try:
                RepositoryUser.seve_to_db(new_user)
                access_token=create_access_token(identity=data['Username'])
                # refresh_token=create_refresh_token(identity=data['Username'])
                return{
                    'message':'user was created',
                    'access_toke':access_token,
                    # 'refresh_toke':refresh_token
                    }
            except Exception  as e:
                return{'message':"something wrong"},500

class UserLogin(Resource):
    def post(self):
        parser.add_argument('Username',required ="true")
        parser.add_argument('Password',required ="true")
        data = parser.parse_args()
        current_user=RepositoryUser.find_by_username(data['Username'])
        if not current_user:
            return{"message":"Username {} doesn't exist".format(data['Username'])}
        try:
            if RepositoryUser.verify_hash(data['Password'],current_user.password):
                access_token=create_access_token(identity=data['Username'])
                # refresh_token=create_refresh_token(identity=data['Username'])
                return{                
                    'userId':current_user.userid,
                    'name':current_user.name,
                    'message':'Login in as {}'.format(current_user.username),
                    'access_token':access_token,
                    # 'refresh_token':refresh_token
                    }
            else:
                return {'message':'Wrong credentials'}
        except:
            return {'message':'Wrong credentials'}
      
class UserLogoutAccess(Resource):
    @jwt_required()
    def post(self):
        jti=get_jwt()['jti']
        try:
            revoked_token=RevokedModel(jti=jti)
            RepositoryRevoke.add(revoked_token)
            return {'message':'Access token has been revoked'}
        except Exception as e:
            return {'message':e},500
      
# class UserLogoutRefresh(Resource):
#     @jwt_required(refresh=True)
#     def post(self):
#         jti=get_jwt()['jti']
#         try:
#             revoked_token=RevokedModel(jti=jti)
#             return {'message':'Access token has bee n revoked'}
#         except Exception as e:
#             return {'message':e},500
      
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        access_token=create_access_token(identity=current_user) 
        return {'access_token':access_token}
      
class AllUsers(Resource):
    def get(self):
        return RepositoryUser.return_all()
      
class SecretResource(Resource):
    @jwt_required()
    def get(self):
        return {'answer': '42'}

class GetAllCategory(Resource):
    def get(self):
        return RepositoryCategory.return_all()
class GetForum(Resource):
    def get(self):        
        return RepositoryForum.get_all_forum()
class InsertThread(Resource):
    def post(self):
        parser.add_argument('UserId',required ="true")
        parser.add_argument('Title',required ="true")
        parser.add_argument('Description',required ="true")
        data=parser.parse_args()
        User_name=RepositoryUser.get_name_by_id(data['UserId'])
        thread=ForumThreadModel(
            userid=int(str(data['UserId'])),
            title=str(data['Title']),
            description=str(data['Description']),
            interested=0,
            create_on=datetime.now(),
            user_in=User_name[0]['name'],            
        )
        return RepositoryForum.insert_forum_thread(thread)
class InsertReplay(Resource):
    def post(self):
        parser.add_argument('ThreadId',required="true")
        parser.add_argument('UserId',required="true")
        parser.add_argument('Description',required="true")
        data=parser.parse_args()
        User_name=RepositoryUser.get_name_by_id(data['UserId'])
        thread=RepositoryForum.get_thread_by_id(data['ThreadId'])
        Replay=ForumReplayModel(
            userid=data['UserId'],
            description=data['Description'],
            create_on=datetime.now(),
            user_in=User_name[0]['name'],
            replayName=thread
        )
        return RepositoryForum.insert_forum_replay(Replay)
