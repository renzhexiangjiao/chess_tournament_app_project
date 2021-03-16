from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tournament(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    
    time = models.CharField(max_length=20)
    player_white = models.CharField(max_length=30)
    player_black = models.CharField(max_length=30)
    
    def __str__(self):
        return self.time

class Move(models.Model):
    moveId = models.IntegerField(default=1)
    square_from = models.IntegerField(default=0)
    square_to = models.IntegerField(default=0)
    
    def __str__(self):
        return self.moveId

class AccountPage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    winRate = models.DecimalField(max_digits=3, decimal_places=1)
    wonGame = models.IntegerField(default=0)
    lostGame = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username