from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalogue.models import Price
from catalogue.forms import PriceForm

def index(request):
    prices = Price.objects.all()
    return render(request, "price/index.html", {
        "prices": prices,
        "title": "Liste des tarifs"
    })

def show(request, price_id):
    price = get_object_or_404(Price, pk=price_id)
    return render(request, "price/show.html", {
        "title": f"Tarif : {price.type} – {price.price:.2f} €",
        "price": price,
    })

def create(request):
    form = PriceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tarif créé avec succès.")
            return redirect("catalogue:price-index")
        messages.error(request, "❌ Erreur lors de la création.")

    return render(request, "price/form.html", {
        "form": form,
        "title": "➕ Ajouter un tarif"
    })

def edit(request, price_id):
    price = get_object_or_404(Price, pk=price_id)
    form = PriceForm(request.POST or None, instance=price)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tarif modifié.")
            return redirect("catalogue:price-index")
        messages.error(request, "❌ Erreur lors de la modification.")

    return render(request, "price/form.html", {
        "form": form,
        "title": f"✏️ Modifier : {price}"
    })

def delete(request, price_id):
    price = get_object_or_404(Price, pk=price_id)
    if request.method == "POST":
        price.delete()
        messages.success(request, "🗑 Tarif supprimé.")
        return redirect("catalogue:price-index")

    return render(request, "price/delete.html", {
        "price": price,
        "title": f"🗑 Supprimer : {price}"
    })
