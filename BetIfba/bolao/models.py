# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    login = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(min_lenght=5,max_length=15)
    adm = models.BooleanField(default=false)
    credits = models.FloatField(default=10.0, validators = [MinValueValidator(0.0)])

    def __str__(self):
        return "Nome: "+self.name._str_()+"Créditos: "+self.credits._str_()

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    homeTeam = models.CharField(max_length=30)
    visitorTeam = models.CharField(max_length=30)
    homeScore = models.IntegerField()
    visitorScore = models.IntegerField()

    def __str__(self):
        return "Time1: "+self.homeTeam._str_()+"Placar: "+self.homeScore._str_()+" X "+self.visitorScore._str_()+"Time2: "+self.visitorTeam._str_()

class Bet(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Match,on_delete = models.CASCADE)
    userBets = models.ManyToManyField(User)
    amountBets = models.FloatField()

    def __str__(self):
        return "Jogo: "+self.game._str_()+"Valor acumulado: "+self.amountBets._str_()
