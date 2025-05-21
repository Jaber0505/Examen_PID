from django.db import models

class ArtistManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)

class Artist(models.Model):
    first_name = models.CharField("Prénom", max_length=60)
    last_name = models.CharField("Nom", max_length=60)
    
    troupe = models.ForeignKey(
        "catalogue.Troupe",
        on_delete=models.PROTECT,
        related_name='artists',
        null=True,
        blank=True,
        verbose_name="Troupe"
    )
    
    def troupe_name(self):
        if self.troupe:
            return self.troupe.name
        return "Non affilié"

    objects = ArtistManager()

    class Meta:
        db_table = "artists"
        verbose_name = "Artiste"
        verbose_name_plural = "Artistes"
        ordering = ["last_name", "first_name"]
        constraints = [
            models.UniqueConstraint(fields=["first_name", "last_name"], name="unique_artist_name")
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def natural_key(self):
        return (self.first_name, self.last_name)