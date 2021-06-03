from flask import Flask
from flask_restful import  Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'something-secret-dont-peoples-know'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt=JWTManager(app)

db_string = "postgresql://avzlqjcgocyiwy:28f06381a58c76cf04d9f77d2188ab921a340fae1d77f43d72751e2f6b22ca5d@ec2-54-159-175-113.compute-1.amazonaws.com:5432/d8ag165a0mhoeg"
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models,repository

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return repository.RepositoryRevoke.is_jti_blacklisted(jti)

import views, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
# api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

api.add_resource(resources.GetAllCategory,'/getAllCategory')