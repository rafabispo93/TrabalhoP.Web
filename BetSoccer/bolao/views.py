from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User

# Create your views here.

def index(request):
    matchResult= MatchResult.objects.all()
    matchRegistration= MatchRegistration.objects.all()
    return render(request, 'bolao/index.html', {'matchResult':matchResult,'matchRegistration':matchRegistration})
def bolao(request):
    matchRegistration= MatchRegistration.objects.all()
    return render(request, 'bolao/jogos.html', {'matchRegistration':matchRegistration})
def login(request):
    user = request.POST.get("username", "")
    password = request.POST.get("password", "")
    users = User.objects.all()

    for _user in users:
        if _user.login==user and _user.password==password:
            return bolao(request)
    return index(request)