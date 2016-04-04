from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User,Bet,Ranking,RegisterBet
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
    registerBet = RegisterBet.objects.all()
    Ranking.objects.all().delete()

    for match in matchRegistration:
        try:
            MatchResult.objects.get(game = match)
        except MatchResult.DoesNotExist:
            register = RegisterBet(id = match.id,homeTeam = match.homeTeam,visitorTeam = match.visitorTeam,date = match.date,hora = match.hora)
            register.save()
    count = 1
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
            return render(request,'bolao/jogos.html',{'user':user,'credito': credito,'registerBet':registerBet,'ranking':ranking})
    return index(request)

def apostar(request):
    scoreHome = request.POST.get("homeScore", "")
    scoreVisitor = request.POST.get("visitorScore", "")
    matchRegistration= MatchRegistration.objects.all()
    userCredito =  User.objects.get(login =request.POST.get("user-Credito",""))
    matchID = MatchRegistration.objects.get(id =request.POST.get("match-id",""))
    users = User.objects.all()
    ranking = Ranking.objects.all()
    ordered = users.order_by('-credits')
    registerBet = RegisterBet.objects.all()
    Ranking.objects.all().delete()

    try:
        check = Bet.objects.get(userBets = userCredito,game = matchID)
        print(check)
    except Bet.DoesNotExist:
        if userCredito.credits > 0.0 :
            bet = Bet(userBets = userCredito,game = matchID,homeScore = scoreHome, visitorScore = scoreVisitor)
            bet.save()
            userCredito.credits = userCredito.credits - 5.0
            userCredito.save()

    for match in matchRegistration:
        try:
            MatchResult.objects.get(game = match)
        except MatchResult.DoesNotExist:
            register = RegisterBet(id = match.id,homeTeam = match.homeTeam,visitorTeam = match.visitorTeam,date = match.date,hora = match.hora)
            register.save()
    count = 1
    for userRnk in ordered:
        try:
            Ranking.objects.get(user = userRnk)
        except Ranking.DoesNotExist:
            rank = Ranking(user = userRnk,position = count)
            rank.save()
            ranking.order_by('-user.credits')
            count = count +1

    return render( request,'bolao/jogos.html', {'user':userCredito.login,'credito': userCredito.credits,'registerBet':registerBet,'ranking':ranking} )