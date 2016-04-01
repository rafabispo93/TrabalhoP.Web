from django.shortcuts import render
from .models import Match,User

# Create your views here.

def index(request):
    match= Match.objects.all()
    return render(request, 'bolao/index.html', {'match':match})
def bolao(request):
    match= Match.objects.all()
    return render(request, 'bolao/jogos.html', {'match':match})
def login(request):
    user = request.POST.get("username", "")
    password = request.POST.get("password", "")
    users = User.objects.all()

    for _user in users:
        if _user.login==user and _user.password==password:
            return bolao(request)
    return index(request)