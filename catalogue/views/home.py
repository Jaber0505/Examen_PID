from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {
        "is_admin": request.user.is_admin if request.user.is_authenticated else False,
        'title': "Accueil"
    })
