from django.db import models
from catalogue.models import Show, ArtistType

class ArtistTypeShowManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name, type_name, show_slug):
        return self.get(
            artist_type__artist__first_name=first_name,
            artist_type__artist__last_name=last_name,
            artist_type__type__name=type_name,
            show__slug=show_slug
        )

class ArtistTypeShow(models.Model):
    artist_type = models.ForeignKey(
        "ArtistType",
        on_delete=models.CASCADE,
        related_name="shows",
        verbose_name="Artiste + Type",
    )
    show = models.ForeignKey(
        "Show",
        on_delete=models.CASCADE,
        related_name="artiste_type_links",
        verbose_name="Spectacle",
    )

    objects = ArtistTypeShowManager()

    class Meta:
        db_table = "artiste_type_show"
        verbose_name = "Participation artistique"
        verbose_name_plural = "Participations artistiques"
        constraints = [
            models.UniqueConstraint(fields=["artist_type", "show"], name="unique_artist_type_show")
        ]

    def __str__(self):
        return f"{self.artist_type} dans « {self.show.title} »"

    def natural_key(self):
        return self.artist_type.natural_key() + (self.show.slug,)

    natural_key.dependencies = ["catalogue.artisttype", "catalogue.show"]
