from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User
from django.http import HttpResponse

# Create your views here.
global user
global credito
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
    matchRegistration= MatchRegistration.objects.all()
    for _user in users:
        if _user.login==user and _user.password==password:
            credito = _user.credits
            return render(request,'bolao/jogos.html',{'user':user,'credito': credito,'matchRegistration':matchRegistration})
    return index(request)
def apostar(request):
    matchRegistration= MatchRegistration.objects.all()
    userCredito =  User.objects.get(login =request.POST.get("user-Credito",""))
    if userCredito.credits > 0.0 :
        userCredito.credits = userCredito.credits - 5.0
        userCredito.save()

    return render( request,'bolao/jogos.html', {'user':userCredito.login,'credito': userCredito.credits,'matchRegistration':matchRegistration} )