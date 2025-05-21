from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalogue.forms.review_form import ReviewForm
from catalogue.models import Review, Show

@login_required
def create(request, slug):
    show = get_object_or_404(Show, slug=slug)

    if Review.objects.filter(user=request.user, show=show).exists():
        messages.info(request, "ℹ️ Vous avez déjà laissé un avis pour ce film.")
        return redirect("catalogue:show-show", show.slug)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.show = show
            review.save()
            messages.success(request, "✅ Avis ajouté avec succès.")
            return redirect("catalogue:show-show", show.slug)
        messages.error(request, "❌ Erreur lors de la soumission de l’avis.")
    else:
        form = ReviewForm()

    return render(request, "review/form.html", {
        "form": form,
        "title": "📝 Donner un avis",
        "show": show,
    })

@login_required
def edit(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Avis modifié.")
            return redirect("catalogue:show-show", review.show.slug)
        messages.error(request, "❌ Erreur lors de la modification.")
    else:
        form = ReviewForm(instance=review)

    return render(request, "review/form.html", {
        "form": form,
        "title": "✏️ Modifier mon avis",
        "show": review.show,
    })

@login_required
def delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == "POST":
        show_slug = review.show.slug
        review.delete()
        messages.success(request, "🗑 Avis supprimé.")
        return redirect("catalogue:show-show", show_slug)

    return render(request, "review/delete.html", {
        "review": review,
        "title": "🗑 Supprimer l’avis",
    })
