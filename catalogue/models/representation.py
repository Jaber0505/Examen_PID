from django.db import models
from .show import Show
from .location import Location

MAX_CAPACITY = 100  # valeur globale

class RepresentationManager(models.Manager):
    def get_by_natural_key(self, show_slug, schedule):
        return self.get(show__slug=show_slug, schedule=schedule)

class Representation(models.Model):
    show = models.ForeignKey(
        Show,
        on_delete=models.RESTRICT,
        null=False,
        related_name='representations',
        verbose_name='Spectacle'
    )
    schedule = models.DateTimeField(
        verbose_name='Date et heure',
        help_text="Horaire de la représentation"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.RESTRICT,
        null=False,
        related_name='representations',
        verbose_name='Lieu'
    )

    objects = RepresentationManager()

    def __str__(self):
        return f"{self.show.title} @ {self.schedule.strftime('%Y-%m-%d %H:%M')}"

    def natural_key(self):
        return (self.show.slug, self.schedule)

    natural_key.dependencies = ['catalogue.show', 'catalogue.location']
    
    @property
    def capacity_used(self):
        return sum(item.quantity for item in self.representation_reservations.all())

    @property
    def is_full(self):
        return self.capacity_used >= MAX_CAPACITY

    @property
    def is_expired(self):
        from django.utils import timezone
        return self.schedule < timezone.now()


    class Meta:
        db_table = "representations"
        verbose_name = "Représentation"
        verbose_name_plural = "Représentations"
        constraints = [
            models.UniqueConstraint(
                fields=["show", "schedule"],
                name="unique_show_schedule"
            )
        ]
