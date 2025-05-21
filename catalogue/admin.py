from django.contrib import admin
from .models import Artist, Type, Locality, Show, Location, Price, Representation, Review, Reservation, RepresentationReservation

admin.site.register(Price)
admin.site.register(Show)
admin.site.register(Artist)
admin.site.register(Type)
admin.site.register(Locality)
admin.site.register(Location)
admin.site.register(Representation)
admin.site.register(Review)
admin.site.register(Reservation)
admin.site.register(RepresentationReservation)