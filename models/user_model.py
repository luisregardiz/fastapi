from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields
from config.auth import pwd_context



class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, null=False)
    email = fields.CharField(max_length=128, null=False, unique=True)
    first_name = fields.CharField(max_length=60, null=False)
    last_name = fields.CharField(max_length=60, null=True)
    password_hash = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)



User_Pydantic = pydantic_model_creator(User, name='User', exclude=["password_hash"])
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)