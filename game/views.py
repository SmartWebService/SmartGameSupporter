from django.shortcuts import render, redirect
import core.core

# Create your views here.
def in_game(request, game_code):
    request_user = core.core.room_manager.get_user_by_sessionKey(request.session.session_key)

    data = dict()
    data['type'] = 1 if request_user.isParticipant else 0
    data['game_code'] = request_user.room.room_code
    data['game_code_sp'] = str(data['game_code'])[:3] + " " + str(data['game_code'])[3:]
    data['username'] = request_user.nickname
    data['sessionKey'] = request.session.session_key


    if request_user.room.selected_game == "RPS":
        if request_user.isParticipant():
            return render(request, 'RPS/RSPuser.html', data)
        else:
            return render(request, 'RPS/RSPhost.html', data)

    elif request_user.room.selected_game == "FIVE_POKER":
        if request_user.isParticipant():
            return render(request, 'five-poker/gamescreen.html', data)
        else:
            return render(request, 'five-poker/ingame.html', data)

    elif request_user.room.selected_game == "indian-poker":
        if request_user.isParticipant():
            return render(request, 'RPS/RSPmain.html', data)
        else:
            return render(request, 'RPS/RSPmain.html', data)
            
    elif request_user.room.selected_game == "Bomb":
        if request_user.isParticipant():
            return render(request, 'Bomb/Bombuser.html', data)
        else:
            return render(request, 'Bomb/Bomb.html', data)

    else:
        return redirect('lobby')