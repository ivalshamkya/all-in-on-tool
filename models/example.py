from datetime import datetime

from bson import ObjectId
from mongoengine import DateField, DateTimeField, IntField, ObjectIdField, StringField

from models.base_model import BaseModel


class Example(BaseModel):
    _id = ObjectIdField(required=False, default=lambda: ObjectId())
    name = StringField(required=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    deleted_at = DateTimeField(default=None)

    meta = {"collection": "examples"}
