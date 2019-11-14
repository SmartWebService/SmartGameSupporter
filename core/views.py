from django.shortcuts import render

# Create your views here.
def lobby(request):
    return render(request, 'lobby.html')


def host(request):
    room_code = 111111
    return render(request, 'room-host.html', {'room_code': request.session['user']})

def participant(request):
    if request.method == "POST":
        request.session['game_code'] = request.POST.get('game_code')
        request.session['username'] = request.POST.get('username')
        request.session['user'] = 1
    return render(request, 'join.html')