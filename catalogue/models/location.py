from django.db import models

class LocationManager(models.Manager):
    def get_by_natural_key(self, slug, website):
        return self.get(
            slug=slug,
            website=website
        )

class Location(models.Model):
    slug = models.SlugField("Slug", max_length=60, unique=True, help_text="Identifiant unique dans l'URL")
    designation = models.CharField("Désignation", max_length=100, help_text="Nom du lieu (ex : Théâtre Royal)")
    address = models.CharField("Adresse", max_length=255, help_text="Rue et numéro complet")
    
    locality = models.ForeignKey(
        "catalogue.Locality",
        on_delete=models.RESTRICT,
        related_name="locations",
        verbose_name="Localité"
    )

    website = models.CharField("Site web", max_length=255, blank=True, null=True)
    phone = models.CharField("Téléphone", max_length=30, blank=True, null=True)

    objects = LocationManager()

    class Meta:
        db_table = "locations"
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"
        ordering = ["designation"]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "website"],
                name="unique_location_slug_website"
            )
        ]

    def __str__(self):
        return f"{self.designation} ({self.slug})"

    def natural_key(self):
        return (self.slug, self.website)

    natural_key.dependencies = ['catalogue.locality']
