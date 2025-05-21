from django.db import models

class Troupe(models.Model):
    name = models.CharField("Nom de la troupe", max_length=60, unique=True)
    logo_url = models.CharField("URL du logo", max_length=255)

    class Meta:
        db_table = "troupes"
        verbose_name = "Troupe"
        verbose_name_plural = "Troupes"
        ordering = ["name"]

    def __str__(self):
        return self.name
