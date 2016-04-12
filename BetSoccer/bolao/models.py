# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    id = models.AutoField(primary_key=True,default=None)
    login = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=15,default=123456)
    adm = models.BooleanField(default=False)
    credits = models.FloatField(default=10.0, validators = [MinValueValidator(0.0)])

    def __str__(self):
        return "Login: {}, Crédito: {} ".format(self.login,self.credits)


class MatchRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    homeTeam = models.CharField(max_length=30)
    visitorTeam = models.CharField(max_length=30)
    date = models.CharField(max_length=10)
    hora = models.CharField(max_length=6)
    amountOfCredits = models.FloatField(default=0.0, validators = [MinValueValidator(0.0)])
    message = models.CharField(max_length=300,default="")
    def __str__(self):
        return "Time1: {} X Time2: {}, data: {},hora: {}".format(self.homeTeam,self.visitorTeam,self.date,self.hora)


class MatchResult(models.Model):
    game = models.ForeignKey(MatchRegistration,default=None)
    homeScore = models.IntegerField(blank=False,default=0)
    visitorScore = models.IntegerField(blank=False,default=0)

    def __str__(self):
        return "{}: {} X {} :{} ".format(self.game.homeTeam,self.homeScore,self.visitorScore,self.game.visitorTeam)

class Bet(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(MatchRegistration,on_delete = models.CASCADE,default=None)
    userBets = models.ForeignKey(User,on_delete = models.CASCADE,default=None)
    homeScore = models.CharField(max_length = 2,default = 0)
    visitorScore = models.CharField(max_length = 2,default = 0)

    def __str__(self):
        return "Jogo: {}, Usuário: {} ".format(self.game,self.userBets)

class Ranking(models.Model):
    position = models.IntegerField(default = None,blank=True)
    user = models.ForeignKey(User,blank=True,on_delete = models.CASCADE)

    def __str__(self):
        return "Posição: {} ".format(self.position)

class RegisterBet(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(MatchRegistration,default=None)
    homeTeam = models.CharField(max_length=30)
    visitorTeam = models.CharField(max_length=30)
    date = models.CharField(max_length=10)
    hora = models.CharField(max_length=6)

    def __str__(self):
        return "Time1: {} X Time2: {}, data: {},hora: {}".format(self.homeTeam,self.visitorTeam,self.date,self.hora)
