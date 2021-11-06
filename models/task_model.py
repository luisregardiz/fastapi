from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Tasks(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=30, null=False)
    task = fields.CharField(max_length=225, null=False)
    is_completed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField("models.User", related_name="user")


Task_schema = pydantic_model_creator(Tasks, name='Task')
TaskCreate_schema = pydantic_model_creator(Tasks, name="TaskCreate", exclude_readonly=True)