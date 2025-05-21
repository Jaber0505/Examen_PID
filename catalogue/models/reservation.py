from django.db import models
from django.contrib.auth import get_user_model

from .representation import Representation

User = get_user_model()
MAX_CAPACITY = 100  # ou à importer depuis settings si besoin

class ReservationManager(models.Manager):
    def get_by_natural_key(self, username, representation_slug, schedule):
        return self.get(
            user__username=username,
            representation__show__slug=representation_slug,
            representation__schedule=schedule
        )

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("ouverte", "Ouverte"),
        ("complète", "Complète"),
        ("expirée", "Expirée"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="reservations",
        verbose_name="Utilisateur"
    )
    representation = models.ForeignKey(
        Representation,
        on_delete=models.RESTRICT,
        related_name="reservations",
        verbose_name="Représentation"
    )
    booking_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de réservation"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ouverte",
        verbose_name="Statut"
    )

    objects = ReservationManager()

    class Meta:
        db_table = "reservations"
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        unique_together = ("user", "representation")
        ordering = ["-booking_date"]

    def __str__(self):
        return f"{self.user.username} → {self.representation} ({self.status})"

    def total_places_reserved(self):
        return sum(item.quantity for item in self.items.all())

    def update_status(self):
        if self.representation.is_expired:
            self.status = "expirée"
        elif self.representation.capacity_used >= MAX_CAPACITY:
            self.status = "complète"
        else:
            self.status = "ouverte"
        self.save()

    def natural_key(self):
        return (
            self.user.username,
            self.representation.show.slug,
            self.representation.schedule,
        )
    
    natural_key.dependencies = ['account.user', 'catalogue.representation']
