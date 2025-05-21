from django.urls import path
from . import views

app_name = "catalogue"

urlpatterns = [
    # Artists
    path("artist/", views.artist.index, name="artist-index"),
    path("artist/create/", views.artist.create, name="artist-create"),
    path("artist/<int:artist_id>/", views.artist.show, name="artist-show"),
    path("artist/<int:artist_id>/edit/", views.artist.edit, name="artist-edit"),
    path("artist/<int:artist_id>/delete/", views.artist.delete, name="artist-delete"),

    # Types
    path("type/", views.type.index, name="type-index"),
    path("type/create/", views.type.create, name="type-create"),
    path("type/<int:type_id>/", views.type.show, name="type-show"),
    path("type/<int:type_id>/edit/", views.type.edit, name="type-edit"),
    path("type/<int:type_id>/delete/", views.type.delete, name="type-delete"),

    # Localities
    path("locality/", views.locality.index, name="locality-index"),
    path("locality/create/", views.locality.create, name="locality-create"),
    path("locality/<int:locality_id>/", views.locality.show, name="locality-show"),
    path("locality/<int:locality_id>/edit/", views.locality.edit, name="locality-edit"),
    path("locality/<int:locality_id>/delete/", views.locality.delete, name="locality-delete"),

    # Shows
    path("show/", views.show.index, name="show-index"),
    path("show/create/", views.show.create, name="show-create"),
    path("show/<slug:slug>/", views.show.show, name="show-show"),
    path("show/<slug:slug>/edit/", views.show.edit, name="show-edit"),
    path("show/<slug:slug>/delete/", views.show.delete, name="show-delete"),

    # Locations
    path("location/", views.location.index, name="location-index"),
    path("location/create/", views.location.create, name="location-create"),
    path("location/<slug:slug>/", views.location.show, name="location-show"),
    path("location/<slug:slug>/edit/", views.location.edit, name="location-edit"),
    path("location/<slug:slug>/delete/", views.location.delete, name="location-delete"),

    # Prices
    path("price/", views.price.index, name="price-index"),
    path("price/create/", views.price.create, name="price-create"),
    path("price/<int:price_id>/", views.price.show, name="price-show"),
    path("price/<int:price_id>/edit/", views.price.edit, name="price-edit"),
    path("price/<int:price_id>/delete/", views.price.delete, name="price-delete"),
    
    # Reviews
    path("review/<int:review_id>/edit/", views.review.edit, name="review-edit"),
    path("review/<slug:slug>/create/", views.review.create, name="review-create"),
    path("review/<int:review_id>/delete/", views.review.delete, name="review-delete"),

    # Representations
    path('representation/', views.representation.index, name='representation-index'),
    path('representation/<int:id>/', views.representation.show, name='representation-show'),
    path('representation/create/', views.representation.create, name='representation-create'),
    path('representation/edit/<int:id>/', views.representation.edit, name='representation-edit'),
    path('representation/delete/<int:id>/', views.representation.delete, name='representation-delete'),

    # Réservations
    path('reservation/', views.reservation.index, name='reservation-index'),
    path('reservation/<int:id>/', views.reservation.show, name='reservation-show'),
    path("reservation/<int:id>/edit/", views.reservation.edit, name="reservation-edit"),
    path("reservation/<int:id>/delete/", views.reservation.delete, name="reservation-delete"),
    path('reservation//<slug:slug>/create', views.reservation.create, name='reservation-create'),

    # Artist_Types
    path("artist-type/", views.artist_type.index, name="artist-type-index"),
    path("artist-type/create/", views.artist_type.create, name="artist-type-create"),
    path("artist-type/<int:id>/edit/", views.artist_type.edit, name="artist-type-edit"),
    path("artist-type/<int:id>/delete/", views.artist_type.delete, name="artist-type-delete"),

    # Artist_Type_Shows
    path("artist-type-show/", views.artist_type_show.index, name="artist-type-show-index"),
    path("artist-type-show/create/", views.artist_type_show.create, name="artist-type-show-create"),
    path("artist-type-show/<int:id>/edit/", views.artist_type_show.edit, name="artist-type-show-edit"),
    path("artist-type-show/<int:id>/delete/", views.artist_type_show.delete, name="artist-type-show-delete"),
    
    # Representation_Reservation
    path("representation-reservation/", views.representation_reservation.index, name="representation_reservation-index"),
    path("representation-reservation/add/", views.representation_reservation.create, name="representation_reservation-create"),
    path("representation-reservation/<int:id>/", views.representation_reservation.show, name="representation_reservation-show"),
    path("representation-reservation/<int:id>/edit/", views.representation_reservation.edit, name="representation_reservation-edit"),
    path("representation-reservation/<int:id>/delete/", views.representation_reservation.delete, name="representation_reservation-delete"),

    # Route renommée avec un nouveau name pour éviter conflit
    path(
        "representation/<int:representation_id>/tarif/<int:price_id>/reserver/",
        views.representation_reservation.create,
        name="representation_reservation-create-with-price"
    ),

    path(
        "representation/<int:representation_id>/reserver/",
        views.representation_reservation.multi_tarif_create,
        name="representation_reservation-multi-create"
    ),

]
