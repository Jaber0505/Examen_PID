from django.db import models

class TypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Type(models.Model):
    name = models.CharField("Nom", max_length=60, help_text="Nom du type de rôle")

    objects = TypeManager()

    class Meta:
        db_table = "types"
        verbose_name = "Type"
        verbose_name_plural = "Types"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_type_name")
        ]

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)
