from django.db import models

class RepresentationReservationManager(models.Manager):
    def get_by_natural_key(self, representation_slug, reservation_id, price_type):
        return self.get(
            representation__show__slug=representation_slug,
            reservation__id=reservation_id,
            price__type=price_type
        )

class RepresentationReservation(models.Model):
    representation = models.ForeignKey(
        "catalogue.Representation",
        on_delete=models.CASCADE,
        related_name="representation_reservations",
        verbose_name="Représentation"
    )
    reservation = models.ForeignKey(
        "catalogue.Reservation",
        on_delete=models.CASCADE,
        related_name="representation_items",
        verbose_name="Réservation"
    )
    price = models.ForeignKey(
        "catalogue.Price",
        on_delete=models.RESTRICT,
        related_name="representation_usages",
        verbose_name="Tarif"
    )
    quantity = models.PositiveSmallIntegerField(
        "Quantité",
        help_text="Nombre de places réservées à ce tarif"
    )

    objects = RepresentationReservationManager()

    def __str__(self):
        return f"{self.reservation} - {self.representation} - {self.price.type} x{self.quantity}"

    def natural_key(self):
        return (
            self.representation.show.slug,
            self.reservation.id,
            self.price.type
        )

    natural_key.dependencies = [
        "catalogue.representation",
        "catalogue.reservation",
        "catalogue.price"
    ]

    class Meta:
        db_table = "representation_reservations"
        verbose_name = "Détail de réservation"
        verbose_name_plural = "Détails de réservations"
        unique_together = ("representation", "reservation", "price")
