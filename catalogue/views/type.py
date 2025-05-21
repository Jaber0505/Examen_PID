from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from catalogue.models.type import Type
from catalogue.forms.type_form import TypeForm

def index(request):
    types = Type.objects.all()
    return render(request, "type/index.html", {
        "types": types,
        "title": "Liste des types",
    })

def show(request, type_id):
    type_obj = get_object_or_404(Type, pk=type_id)
    return render(request, "type/show.html", {
        "type": type_obj,
        "title": f"Type : {type_obj.name}",
    })

def create(request):
    if request.method == "POST":
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Le type a été ajouté avec succès.")
            return redirect("catalogue:type-index")
        else:
            messages.error(request, "❌ Une erreur est survenue. Veuillez vérifier le formulaire.")
    else:
        form = TypeForm()

    return render(request, "type/form.html", {
        "form": form,
        "title": "➕ Ajouter un type",
    })

def edit(request, type_id):
    type_obj = get_object_or_404(Type, pk=type_id)

    if request.method == "POST":
        form = TypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Le type a été modifié avec succès.")
            return redirect("catalogue:type-show", form.instance.id)
        else:
            messages.error(request, "❌ Une erreur est survenue lors de la modification.")
    else:
        form = TypeForm(instance=type_obj)

    return render(request, "type/form.html", {
        "form": form,
        "title": f"✏️ Modifier : {type_obj.name}",
    })

def delete(request, type_id):
    type_obj = get_object_or_404(Type, pk=type_id)

    if request.method == "POST":
        type_obj.delete()
        messages.success(request, "🗑 Le type a été supprimé avec succès.")
        return redirect("catalogue:type-index")

    return render(request, "type/delete.html", {
        "type": type_obj,
        "title": f"🗑 Supprimer : {type_obj.name}",
    })
