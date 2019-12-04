from django.shortcuts import render

# Create your views here.
def in_game(request, game_code):
    # return render(request, 'five-poker/gamescreen.html')

    return render(request, 'RPS/RSPmain.html')