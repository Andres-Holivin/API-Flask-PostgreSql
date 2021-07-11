from marshmallow_sqlalchemy import load_instance_mixin
from marshmallow_sqlalchemy import fields
from marshmallow import fields
from marshmallow_sqlalchemy.fields import Nested
from app import *
from models import *

class ForumReplaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ForumReplayModel

class ForumThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ForumThreadModel
    replay=ma.Nested(ForumReplaySchema, many=True)

class ProductNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ProductNameModel
class ProductSellSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields=('id','modal','harga_jual','terjual','name')
class ProductSellSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields=('id','modal','harga_jual','jumlah','name')
    
    