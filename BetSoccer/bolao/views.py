from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User,Bet
from django.http import HttpResponse

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
    matchRegistration= MatchRegistration.objects.all()
    for _user in users:
        if _user.login==user and _user.password==password:
            credito = _user.credits
            return render(request,'bolao/jogos.html',{'user':user,'credito': credito,'matchRegistration':matchRegistration})
    return index(request)
def apostar(request):
    matchRegistration= MatchRegistration.objects.all()
    userCredito =  User.objects.get(login =request.POST.get("user-Credito",""))
    matchID = MatchRegistration.objects.get(id = request.POST.get("match-id",""))

    if userCredito.credits > 0.0 and Bet(userBets = userCredito)== False :
        userCredito.credits = userCredito.credits - 5.0
        userCredito.save()
        bet = Bet(game = matchID,userBets = userCredito)
        bet.save()


    return render( request,'bolao/jogos.html', {'user':userCredito.login,'credito': userCredito.credits,'matchRegistration':matchRegistration} )