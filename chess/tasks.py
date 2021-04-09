from background_task import background
import chess.models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from random import shuffle, choice
from collections import defaultdict

@background(schedule=60)
def schedule_games(tournament_id):
    try:
        tournament = chess.models.Tournament.objects.get(id=tournament_id)
        participants = list(tournament.participants.values_list('id', flat=True))
        shuffle(participants)
        n = len(participants)

        if n <= 1:
            print("Tournament " + tournament.name + " is cancelled due to lack of participants.")
        elif n == 2: # only one game is played in a 2-participant tournament
            game = chess.models.Game()
            game.tournament = tournament
            game.time = timezone.now()
            game.player_white = User.objects.get(id=participants[0])
            game.player_black = User.objects.get(id=participants[1])
            game.save()
            decide_winner(tournament_id, defaultdict(int), schedule=timedelta(minutes=20, seconds=15))
        else:
            if n % 2 == 1:
                participants.insert(n//2, None)
                n += 1

            pairings = []
            pivot = participants[0]
            rest = participants[1:]
            n_rounds = min(n-1, 6) # max 6 rounds in a tournament

            for i in range(n_rounds): 
                pairings.append(list(zip([pivot]+rest[:n//2-1], rest[:n//2-2:-1])))
                rest.insert(0, rest.pop())

            byes = defaultdict()
            swapped = lambda x:(x[1],x[0])

            for i, _round in enumerate(pairings):
                for j, pair in enumerate(_round):
                    if choice([0,1]):
                        _round[j] = swapped(pair)
                    if None in pair:
                        byes[pair[0] or pair[1]] += 1
                    else:
                        game = chess.models.Game()
                        game.tournament = tournament
                        game.time = timezone.now() + timedelta(minutes=20*i)
                        game.player_white = User.objects.get(id=_round[j][0])
                        game.player_black = User.objects.get(id=_round[j][1])
                        game.save()
            
            decide_winner(tournament_id, byes, schedule=timedelta(minutes=20*n_rounds, seconds=15))
    except chess.models.Tournament.DoesNotExist:
        pass

@background(schedule=60)
def decide_winner(tournament_id, byes):
    try:
        tournament = chess.models.Tournament.objects.get(id=tournament_id)

    except chess.models.Tournament.DoesNotExist:
        pass