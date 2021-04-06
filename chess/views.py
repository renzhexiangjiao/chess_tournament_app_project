from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from . import gamerules

class IndexView(View):
    def get(self, request):
        return render(request, 'chess/index.html')

class PlayView(View):
    def get(self, request):
        context_dict = {'perspective': 0}
        return render(request, 'chess/play.html', context_dict)

class MoveListView(View):
    def get(self, request):
        print(request.GET['move'])
        context_dict = { 'options' : gamerules.legal_moves(gamerules.starting_board_state) }
        return render(request, 'chess/movelist.html', context_dict)

class MoveUpdateView(View):
    def get(self, request):
        return HttpResponse('Hello')