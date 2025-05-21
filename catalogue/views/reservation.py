from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from catalogue.models import Representation, Reservation, RepresentationReservation, Price
from catalogue.forms import ReservationForm, RepresentationReservationForm
from account.decorators import role_required

@login_required
def create(request, slug):
    representation = get_object_or_404(Representation, show__slug=slug)
    authorized_prices = list(representation.show.prices.all())

    RepresentationReservationFormSet = formset_factory(RepresentationReservationForm, extra=0, can_delete=False)
    initial_data = [{'price': price, 'quantity': 0} for price in authorized_prices]

    # Bloquer les réservations si expirée ou complète
    if representation.is_expired:
        messages.error(request, "Cette représentation est déjà passée.")
        return redirect("catalogue:representation-show", representation.id)
    if representation.is_full:
        messages.error(request, "Cette représentation est complète.")
        return redirect("catalogue:representation-show", representation.id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        formset = RepresentationReservationFormSet(request.POST)

        if Reservation.objects.filter(user=request.user, representation=representation).exists():
            form.add_error(None, "Vous avez déjà une réservation pour cette séance.")
        elif form.is_valid() and formset.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.representation = representation
            reservation.save()

            total_places = 0
            for form_item in formset:
                price = form_item.cleaned_data.get('price')
                quantity = form_item.cleaned_data.get('quantity')

                if price not in authorized_prices:
                    form.add_error(None, "Tarif non autorisé.")
                    reservation.delete()
                    break

                if quantity and quantity > 0:
                    RepresentationReservation.objects.create(
                        reservation=reservation,
                        price=price,
                        quantity=quantity,
                        representation=representation
                    )
                    total_places += quantity

            if total_places == 0:
                reservation.delete()
                form.add_error(None, "Veuillez réserver au moins une place.")
            elif not form.errors:
                reservation.update_status()  # important pour le statut
                return redirect('catalogue:reservation-show', id=reservation.id)
    else:
        form = ReservationForm()
        formset = RepresentationReservationFormSet(initial=initial_data)

    return render(request, 'reservation/create.html', {
        'representation': representation,
        'form': form,
        'formset': formset,
        'title': f"Réserver pour {representation.show.title} - {representation.schedule.strftime('%d/%m/%Y %H:%M')}"
    })

@login_required
def index(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('representation__show')
    return render(request, 'reservation/index.html', {
        'reservations': reservations,
        'title': "🎟️ Mes réservations"
    })

@login_required
def show(request, id):
    reservation = get_object_or_404(Reservation, id=id, user=request.user)
    items = reservation.representation_items.select_related('price').all()
    return render(request, "reservation/show.html", {
        "reservation": reservation,
        "items": items,
        "title": f"Réservation #{reservation.id} – {reservation.representation.show.title}"
    })


@login_required
def edit(request, id):
    reservation = get_object_or_404(Reservation, pk=id, user=request.user)
    representation = reservation.representation

    RepresentationReservationFormSet = formset_factory(RepresentationReservationForm, extra=0, can_delete=False)

    # Récupère tous les prix (à adapter selon ta logique métier)
    authorized_prices = list(Price.objects.all())

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        formset = RepresentationReservationFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            total_places = 0
            reservation = form.save(commit=False)

            # Supprime les anciens items liés à la réservation
            reservation.representation_items.all().delete()

            for item_form in formset:
                price = item_form.cleaned_data.get('price')
                quantity = item_form.cleaned_data.get('quantity')

                if price and price in authorized_prices and quantity and quantity > 0:
                    RepresentationReservation.objects.create(
                        reservation=reservation,
                        price=price,
                        quantity=quantity,
                        representation=representation
                    )
                    total_places += quantity

            if total_places == 0:
                messages.error(request, "Veuillez réserver au moins une place !")
            else:
                reservation.save()
                reservation.update_status()
                messages.success(request, "Réservation modifiée avec succès.")
                return redirect('catalogue:reservation-show', id=reservation.id)
    else:
        form = ReservationForm(instance=reservation)
        initial_data = [
            {
                'price': item.price.pk,
                'quantity': item.quantity,
            }
            for item in reservation.representation_items.all()
        ]
        formset = RepresentationReservationFormSet(initial=initial_data)

        # Préremplit le champ display_price si tu l’utilises dans le form
        for form_item, item in zip(formset.forms, reservation.representation_items.all()):
            form_item.initial['display_price'] = f"{item.price.type} – {item.price.price:.2f} €"

    return render(request, 'reservation/form.html', {
        'form': form,
        'formset': formset,
        'title': f"Modifier la réservation #{reservation.id}",
        'representation': representation,
        'reservation': reservation
    })

@role_required("Admin")
@login_required
def delete(request, id):
    reservation = get_object_or_404(Reservation, id=id, user=request.user)

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Réservation supprimée avec succès.")
        return redirect("catalogue:reservation-index")

    return render(request, "reservation/delete.html", {
        "reservation": reservation,
        "representation": reservation.representation,
        "title": f"Supprimer la réservation #{reservation.id}",
    })
