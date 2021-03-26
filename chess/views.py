from django.shortcuts import render
import json
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, 'chess/index.html')

class PlayView(View):
    def get(self, request):
        return render(request, 'chess/play.html')

class MoveListView(View):
    def get(self, request):
        print(request.GET['move'])
        context_dict = { 'options' : ['a2a3', 'a2a4', 'b2b3', 'b2b4', 'c2c3', 'c2c4', 'd2d3', 'd2d4', 'e2e3', 'e2e4', 'f2f3', 'f2f4', 'g2g3', 'g2g4', 'h2h3', 'h2h4', 'b1a3', 'b1c3', 'g1f3', 'g1h3']}
        return render(request, 'chess/movelist.html', context_dict)

class MoveUpdateView(View):
    def get(self, request):
        pass