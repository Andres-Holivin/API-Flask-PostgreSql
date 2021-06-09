from marshmallow_sqlalchemy import load_instance_mixin
from marshmallow_sqlalchemy.fields import Nested
from run import *
from models import *

class ForumReplaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ForumReplayModel
        load_instance=True

class ForumThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ForumThreadModel    
        # load_instance=True    
    replay=ma.Nested(ForumReplaySchema, many=True)
    