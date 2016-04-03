from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User,Bet,Ranking
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
    ranking = Ranking.objects.all()
    matchRegistration= MatchRegistration.objects.all()
    ordered = users.order_by('-credits')
    count = 1
    Ranking.objects.all().delete()
    for userRnk in ordered:
        try:
            Ranking.objects.get(user = userRnk)
        except Ranking.DoesNotExist:

            rank = Ranking(user = userRnk,position = count)
            rank.save()
            ranking.order_by('-user.credits')
            count = count +1

    for _user in users:
        if _user.login==user and _user.password==password:
            credito = _user.credits
            return render(request,'bolao/jogos.html',{'user':user,'credito': credito,'matchRegistration':matchRegistration,'ranking':ranking})
    return index(request)

def apostar(request):
    matchRegistration= MatchRegistration.objects.all()
    userCredito =  User.objects.get(login =request.POST.get("user-Credito",""))
    matchID = MatchRegistration.objects.get(id =request.POST.get("match-id",""))
    try:
        check = Bet.objects.get(userBets = userCredito,game = matchID)
        print(check)
    except Bet.DoesNotExist:
        if userCredito.credits > 0.0 :
            bet = Bet(userBets = userCredito,game = matchID)
            bet.save()
            userCredito.credits = userCredito.credits - 5.0
            userCredito.save()

    return render( request,'bolao/jogos.html', {'user':userCredito.login,'credito': userCredito.credits,'matchRegistration':matchRegistration} )