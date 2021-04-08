from django.contrib import admin
from chess.models import Tournament, Game, Move, AccountPage

# Register your models here.

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    
class GameAdmin(admin.ModelAdmin):
    list_display = ('time', 'player_white', 'player_black', 'tournament')

class MoveAdmin(admin.ModelAdmin):
    list_display = ('game', 'move_id', 'square_from', 'square_to', 'captured_piece')

# Register your models here.

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Move, MoveAdmin)
admin.site.register(AccountPage)
