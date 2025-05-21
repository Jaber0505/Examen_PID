from django.db import models
from catalogue.models import artist, type

class ArtistTypeManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name, type_name):
        return self.get(
            artist__first_name=first_name,
            artist__last_name=last_name,
            type__name=type_name
        )

class ArtistType(models.Model):
    artist = models.ForeignKey(
        "Artist",
        on_delete=models.CASCADE,
        related_name="artiste_type",
        verbose_name="Artiste"
    )
    type = models.ForeignKey(
        "Type",
        on_delete=models.CASCADE,
        related_name="artiste_type",
        verbose_name="Type"
    )

    objects = ArtistTypeManager()

    class Meta:
        db_table = "artiste_type"
        verbose_name = "Association artiste/type"
        verbose_name_plural = "Associations artiste/type"
        constraints = [
            models.UniqueConstraint(fields=["artist", "type"], name="unique_artist_type")
        ]

    def __str__(self):
        return f"{self.artist} – {self.type}"

    def natural_key(self):
        return self.artist.natural_key() + self.type.natural_key()

    natural_key.dependencies = ["catalogue.artist", "catalogue.type"]