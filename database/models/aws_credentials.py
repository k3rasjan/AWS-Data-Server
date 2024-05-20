from tortoise.models import Model
from tortoise import fields


class AWSCredentials(Model):
    id = fields.IntField(pk=True)
    access_key = fields.TextField()
    secret_key = fields.TextField()
    company = fields.ForeignKeyField(
        "models.Companies", related_name="aws_credentials"
    )

    def __str__(self):
        return f"{self.access_key};{self.secret_key}"
