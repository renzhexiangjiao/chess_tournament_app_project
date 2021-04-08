from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tournament(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField()
    participants = models.ManyToManyField(User)
    
    def __str__(self):
        return self.name

class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    
    time = models.DateTimeField()
    player_white = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='player_white')
    player_black = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='player_black')
    
    def __str__(self):
        return self.player_white.username + ' vs ' + self.player_black.username

class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    move_id = models.PositiveIntegerField()
    square_from = models.CharField(max_length=2)
    square_to = models.CharField(max_length=2)
    captured_piece = models.IntegerField(default=0)

    class Meta:
        unique_together = ('move_id', 'game')

    def save(self, *args, **kwargs):
        existing_ids = Move.objects.filter(game=self.game).order_by('-move_id').values_list('move_id', flat=True)
        if existing_ids:
            self.move_id = existing_ids[0] + 1
        else:
            self.move_id = 0
        super(Move, self).save(*args, **kwargs)

    def __str__(self):
        return self.square_from + self.square_to

class AccountPage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    winRate = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    wonGame = models.IntegerField(default=0)
    lostGame = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username