from random import *
import time
import core.core

class Bomb:
    hostSocket = None
    room = None                     # 게임을 하고있는 방 객체
    host = None                     # 게임을 하고있는 호스트 유저 객체
    participants = []               # 게임을 하고있는 참가자들의 유저 객체를 가진 리스트
    current_bomb_player = None      # 게임진행중에 폭탄을 현재 가지고 있는 유저객체
    start_time = None               # 게임 시작 시간
    bomb_time = None                # 게임시작시 설정되는 폭탄 랜덤 시간
    beep = False

    def __init__(self, host, participants):  # 새 폭탄돌리기 게임 객체
        print("Started bomb at ", host.room.room_code)
        self.room = host.room
        self.host = host
        self.participants = participants
        self.beep = True

        print(host)
        print(participants)
        print(self.participants)

    def get_timer(self):
        return int(self.bomb_time + self.start_time - time.time())
    
    def get_beep(self):
        b = self.beep
        self.beep = False
        return b


    def get_IoT_data(self):
        data = dict()
        data['opcode'] = "gaming"
        data['room_code'] = self.room.room_code
        data['timer'] = self.get_timer()
        data['beep'] = self.get_beep()
        self.check_bomb()
        return data

    def start_game(self, IoT_code):
        self.room.IoT_code = IoT_code
        self.bomb_time = randint(10, 20)
        first_i = randint(0, len(self.participants)-1)
        self.current_bomb_player = self.participants[first_i]
        self.start_time = time.time()

    def is_user_in_game(self, user):
        self.check_bomb()
        for i in self.participants:
            if i == user:
                return True
        return False

    def push_bomb(self, user):
        if not self.is_end():
            while self.current_bomb_player == user:        # push_bomb요청한 유저가 권한이 있는지 확인(폭탄을 가지고있는 유저만 가능) 또한 랜덤픽했을때 또 자신에게 왔을때 다시 배정을 위해 if대신 while사용
                random_i = randint(0, len(self.participants)-1)
                self.current_bomb_player = self.participants[random_i]
                self.beep = True
            self.check_bomb()

    def get_bomb(self, user):
        if not self.is_end():
            self.check_bomb()
            if self.current_bomb_player == user:
                return True
            else:
                return False
    
    def refresh(self):
        p = []
        index = 0

        for i in range(len(self.participants)):
            this_user = self.participants[i]
            p.append(this_user.nickname)
            if this_user == self.current_bomb_player:
                index = i

        self.check_bomb()
        return p, index
        
    def check_bomb(self):
        if self.get_timer() <= 0:
            self.hostSocket.bomb_bomb()
    
    def is_end(self):
        return self.get_timer() <= 0