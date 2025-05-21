from django.db import models

class PriceManager(models.Manager):
    def get_by_natural_key(self, type, price):
        return self.get(type=type, price=price)

class Price(models.Model):
    type = models.CharField(
        "Type de tarif",
        max_length=30,
        help_text="Ex : Enfant, Étudiant, Senior"
    )
    price = models.DecimalField(
        "Montant (€)",
        max_digits=10,
        decimal_places=2,
        help_text="Prix du billet (ex : 12.00)"
    )
    start_date = models.DateField("Début de validité")
    end_date = models.DateField("Fin de validité")

    objects = PriceManager()

    class Meta:
        db_table = "prices"
        verbose_name = "Tarif"
        verbose_name_plural = "Tarifs"
        ordering = ["type"]
        constraints = [
            models.UniqueConstraint(
                fields=["type", "price", "start_date", "end_date"],
                name="unique_price_type_date_range"
            )
        ]

    def __str__(self):
        return f"{self.type} – {self.price:.2f} €"

    def natural_key(self):
        return (self.type, str(self.price))

    natural_key.dependencies = []
