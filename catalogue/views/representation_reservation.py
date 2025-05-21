from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from catalogue.models import Representation, Reservation, RepresentationReservation, Price
from catalogue.forms import RepresentationReservationForm, MultiTarifReservationForm

@login_required
def index(request):
    reservations = RepresentationReservation.objects.select_related(
        "representation__show", "price", "reservation__user"
    )
    return render(request, "representation_reservation/index.html", {
        "representation_reservations": reservations,
        "title": "Liste des réservations par tarif"
    })

@login_required
def show(request, id):
    item = get_object_or_404(RepresentationReservation, id=id)
    return render(request, "representation_reservation/show.html", {
        "item": item,
        "title": f"Détail réservation - {item}"
    })

@login_required
def create(request, representation_id, price_id):
    representation = get_object_or_404(Representation, id=representation_id)
    price_choisi = get_object_or_404(Price, id=price_id)

    # Créer ou récupérer une réservation pour cet utilisateur
    reservation, _ = Reservation.objects.get_or_create(
        user=request.user,
        representation=representation,
        defaults={"booking_date": timezone.now()}
    )

    form = RepresentationReservationForm(
        request.POST or None,
        initial={"price": price_choisi}
    )

    if request.method == "POST" and form.is_valid():
        rr = form.save(commit=False)
        rr.representation = representation
        rr.reservation = reservation
        rr.price = price_choisi
        rr.save()
        return redirect("catalogue:representation-show", representation.id)

    return render(request, "representation_reservation/form.html", {
        "form": form,
        "representation": representation,
        "title": f"Réserver au tarif {price_choisi.type}"
    })

@login_required
def edit(request, id):
    item = get_object_or_404(RepresentationReservation, id=id)
    representation = item.representation

    form = RepresentationReservationForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        updated_rr = form.save(commit=False)

        # recalcul avec nouvelle quantité
        future_total = representation.capacity_used - item.quantity + updated_rr.quantity
        if future_total > 100:
            messages.error(request, "❌ Modification impossible : dépassement de la capacité.")
        else:
            updated_rr.save()
            messages.success(request, "✅ Réservation mise à jour.")
            return redirect("catalogue:representation_reservation-show", item.id)

    return render(request, "representation_reservation/form.html", {
        "form": form,
        "item": item,
        "title": "✏️ Modifier la réservation"
    })

@login_required
def delete(request, id):
    item = get_object_or_404(RepresentationReservation, id=id)
    if request.method == "POST":
        item.delete()
        messages.success(request, "🗑 Réservation supprimée.")
        return redirect("catalogue:representation-show", item.representation.id)

    return render(request, "representation_reservation/delete.html", {
        "item": item,
        "title": f"🗑 Supprimer la réservation"
    })

@login_required
def multi_tarif_create(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)
    prices = Price.objects.all()

    if request.method == "POST":
        form = MultiTarifReservationForm(request.POST, available_prices=prices)
        if form.is_valid():
            # Créer la réservation principale
            reservation, _ = Reservation.objects.get_or_create(
                user=request.user,
                representation=representation,
                defaults={"booking_date": timezone.now()}
            )

            created_count = 0
            for price in prices:
                quantity = form.cleaned_data.get(f"quantity_{price.id}", 0)
                if quantity and quantity > 0:
                    RepresentationReservation.objects.create(
                        reservation=reservation,
                        representation=representation,
                        price=price,
                        quantity=quantity
                    )
                    created_count += 1

            if created_count > 0:
                messages.success(request, "✅ Réservation enregistrée.")
            else:
                messages.warning(request, "Aucun tarif sélectionné.")
            return redirect("catalogue:representation-show", representation.id)
    else:
        form = MultiTarifReservationForm(available_prices=prices)

    return render(request, "representation_reservation/multi_tarif_form.html", {
        "form": form,
        "representation": representation,
        "title": f"Réserver plusieurs tarifs pour « {representation.show.title} »"
    })