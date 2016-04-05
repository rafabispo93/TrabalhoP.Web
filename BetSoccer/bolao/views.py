from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User,Bet,Ranking,RegisterBet
from django.http import HttpResponse

# Create your views here.

def index(request):
    matchResult= MatchResult.objects.all()
    betResult = Bet.objects.all()
    matchRegistration= MatchRegistration.objects.all()
    for match in matchResult: #para cada resultado testar se alguem acertou o placar,criar no match register a quantidade apostada nele, colocar no def apostar aumentar esse campo
        try:
            betWinner = Bet.objects.filter(homeScore = match.homeScore,visitorScore = match.visitorScore)
            betWinnerCount = Bet.objects.filter(homeScore = match.homeScore,visitorScore = match.visitorScore).count
            for x in betWinner:
                cred = User.objects.get(id = betWinner.userBets.id)
                cred.credits = cred.credits + (betWinner.game.amountOfCredits / betWinnerCount)
                cred.save()
                Bet.objects.get(game = x.game).delete()
        except Bet.DoesNotExist:
            print()
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
            try:
                RegisterBet.objects.get(game = match).delete()
            except RegisterBet.DoesNotExist:
                print()
        except MatchResult.DoesNotExist:
            register = RegisterBet(id = match.id,homeTeam = match.homeTeam,visitorTeam = match.visitorTeam,date = match.date,hora = match.hora,game = match)
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

    except Bet.DoesNotExist:
        if userCredito.credits > 0.0 :
            bet = Bet(userBets = userCredito,game = matchID,homeScore = request.POST.get("homeScore"+str(matchID.id),"") , visitorScore = request.POST.get("visitorScore"+str(matchID.id),""))
            bet.save()
            userCredito.credits = userCredito.credits - 5.0
            userCredito.save()
            matchID.amountOfCredits = matchID.amountOfCredits + 5.0
            matchID.save()

    for match in matchRegistration:
        try:
            MatchResult.objects.get(game = match)
        except MatchResult.DoesNotExist:
            register = RegisterBet(id = match.id,homeTeam = match.homeTeam,visitorTeam = match.visitorTeam,date = match.date,hora = match.hora,game = match)
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