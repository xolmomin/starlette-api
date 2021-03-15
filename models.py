from tortoise import fields, models


class Contact(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=25)
    phone = fields.CharField(max_length=20)

    def __str__(self) -> str:
        return f"Contact {self.id}: {self.name}"

    class Meta:
        table = "contact"
