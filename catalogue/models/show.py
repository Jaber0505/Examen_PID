from django.db import models
from django.utils.text import slugify
from catalogue.models import Location

class ShowManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class Show(models.Model):
    slug = models.SlugField(
        "Slug",
        max_length=60,
        unique=True,
        blank=True,
    )
    title = models.CharField("Titre du spectacle", max_length=255)
    description = models.TextField("Description", blank=True)
    poster_url = models.CharField("Affiche (URL)", max_length=255, blank=True, null=True)
    duration = models.PositiveSmallIntegerField("Durée (min)", blank=True, null=True)
    created_in = models.PositiveSmallIntegerField("Année de création")
    
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="shows",
        verbose_name="Lieu"
    )

    bookable = models.BooleanField("Réservable", default=True)

    objects = ShowManager()

    class Meta:
        db_table = "shows"
        verbose_name = "Spectacle"
        verbose_name_plural = "Spectacles"
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(fields=["slug", "created_in"], name="unique_show_slug_year")
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.slug,)
