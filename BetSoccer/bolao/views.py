from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User,Bet,Ranking,RegisterBet

from django.db.models import F
from .indexUtil import IndexUtil
from .login import Login
from .aposta import Aposta

# Create your views here.

def index(request):
    matchResult = MatchResult.objects.all()
    bet = IndexUtil()
    bet.betWinRight()
    bet.betWinOther()
    print(matchResult)
    return render(request, 'bolao/index.html', {'matchResult':matchResult,'matchRegistration':bet.matchRegistration})
def login(request):
    user = request.POST.get("username", "")
    password = request.POST.get("password", "")

    log = Login(user,password)
    log.organizeLogin()
    if log.organizeLogin() ==1:
        return render(request,'bolao/jogos.html',{'user':log.user,'credito': log.credito,'registerBet':log.registerBet,'ranking':log.ranking})

    else:
        return index(request)


def apostar(request):
    userCredito =  User.objects.get(login =request.POST.get("user-Credito",""))
    matchID = MatchRegistration.objects.get(id =request.POST.get("match-id",""))
    Ranking.objects.all().delete()

    aposta = Aposta(request.POST.get("user-Credito",""),request.POST.get("match-id",""))
    aposta.apostarRefresh()
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
            mssg = MatchRegistration.objects.get(id =matchID.id)
            mssg.message = "Já realizou aposta"
            mssg.save()



    return render( request,'bolao/jogos.html', {'user':userCredito.login,'credito': userCredito.credits,'registerBet':aposta.registerBet,'ranking':aposta.ranking,'message':matchID.message} )