from django.shortcuts import render, redirect
import json
from .consumers import *
from .bcolor import bcolors
import core.core
from django.http import HttpResponse, JsonResponse

# Create your views here.
def lobby(request):
    # return render(request, 'lobby.html')
    return render(request, 'main.html')


def new(request):
    # core.core.room_manager
    request.session['type'] = 0
    request.session['game_code'] = core.core.room_manager.new_room(request.session.session_key).room_code
    print("New room created: ", str(request.session['game_code']))
    return redirect('room/' + str(request.session['game_code']))


def join(request):
    if request.method == "GET":
        return render(request, 'join.html')

    elif request.method == "POST":
        request.session['type'] = 1
        request.session['game_code'] = request.POST.get('game_code')
        request.session['username'] = request.POST.get('username')
        return redirect('room/' + str(request.session['game_code']))


def room(request, game_code):
    # core.core.room_manager
    if str(game_code) == str(request.session['game_code']):              # 정상 접근인지 확인 (주소인자는 사용자 편의를 위해 표시하지만 잘못된 URL로 접근시 차단)
        if request.session['type'] == 1:                                 # 참가자일때
            print(bcolors.YELLOW + "HTTP: participant", request.session['game_code'], request.session['username'] + bcolors.ENDC)
            
            data = dict()
            data['type'] = request.session['type']
            data['game_code'] = request.session['game_code']
            data['game_code_sp'] = str(data['game_code'])[:3] + " " + str(data['game_code'])[3:]
            data['username'] = request.session['username']
            data['sessionKey'] = request.session.session_key

            myroom = core.core.room_manager.get_room(int(request.session['game_code']))
            if myroom == None:
                print("no room: ", request.session['game_code'])
                return redirect('lobby')                        # 없는 방에 들어온경우

            # user = User(request.session.session_key, request.session['username'])
            # myroom.add_user(user) # 유저 추가는 소켓중심으로? -> 계속적으로 연결체크
            else:
                return render(request, 'create.html', data)

        elif request.session['type'] == 0:                  # 호스트일때
            print(bcolors.YELLOW + "HTTP: host", str(request.session['game_code']) + bcolors.ENDC)
            
            data = dict()
            data['type'] = request.session['type']
            data['game_code'] = request.session['game_code']
            data['game_code_sp'] = str(data['game_code'])[:3] + " " + str(data['game_code'])[3:]
            data['sessionKey'] = request.session.session_key
            
            return render(request, 'create.html', data)
                                             
    return redirect('lobby')                                # 비정상 접근 -> 홈으로


def index(request):
    return render(request, 'lobby.html', {})


def api_iot(request, device_code):
    room = core.core.room_manager.get_room_by_iot_code(device_code)
    if room == None:
        data = dict()
        data["opcode"] = "error"
        data["des"] = "can not find room or not yet started"
        return JsonResponse(data, json_dumps_params = {'ensure_ascii': True})
    else:
        data = room.game_obj.get_IoT_data()
        print("IoT send data", data)
        return JsonResponse(data, json_dumps_params = {'ensure_ascii': True})