from tortoise import fields
from tortoise.models import Model


class File(Model):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField("models.User", related_name="files")
    filename = fields.CharField(max_length=255)
    description = fields.TextField(default="")
    content = fields.BinaryField(null=True)

    class Meta:
        table = "files"