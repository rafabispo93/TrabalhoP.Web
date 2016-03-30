# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    login = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=15,default=123456)
    adm = models.BooleanField(default=False)
    credits = models.FloatField(default=10.0, validators = [MinValueValidator(0.0)])

    def __str__(self):
        return "Nome: {}, Crédito: {} ".format(self.name,self.credits)

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    homeTeam = models.CharField(max_length=30)
    visitorTeam = models.CharField(max_length=30)
    homeScore = models.IntegerField(blank=True,default=0)
    visitorScore = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return "Time1: {} {} X {} Time2: {} ".format(self.homeTeam,self.homeScore,self.visitorScore,self.visitorTeam)

class Bet(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Match,on_delete = models.CASCADE)
    userBets = models.ManyToManyField(User)
    amountBets = models.FloatField()

    def __str__(self):
        return "Jogo: {}, Valor Acumuado: {} ".format(self.game,self.amountBets)
