from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.UUIDField(pk=True)
    user = fields.CharField(max_length=255)


class Product(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    code = fields.CharField(max_length=255)


