from random import *
# from  game.GameLogic import *
import game.GameLogic.RPS
import game.GameLogic.Bomb
# import game.GameLogic.bet

class RoomManager:
    room_list = []
    all_users = []

    def __str__(self):
        return ",".join(list(map(str, self.room_list)))

    def new_room(self, room_host=None):
        is_picked = False
        while not is_picked:
            pick_code = randint(100000, 999999)
            is_picked = True

            for room in self.room_list:
                if room.room_code == pick_code:
                    is_picked = False
                    break
        
        # new_room = Room(pick_code, room_host)
        new_room = Room(pick_code)
        self.room_list.append(new_room)
        return new_room

    def get_room(self, room_code):
        room_code = int(room_code)
        for i in self.room_list:
            if i.room_code == room_code:
                return i
        return None

    def del_room(self, room):
        self.room_list.remove(room)
    
    def add_user(self, user):
        self.all_users.append(user)

    def get_user_by_sessionKey(self, key_sessionKey):
        for i in self.all_users:
            if i.sessionKey == key_sessionKey:
                return i
        return None

    def get_room_by_iot_code(self, IoT_code):
        for i in self.room_list:
            if i.IoT_code == IoT_code:
                return i
        return None


class Room:
    room_code = None            # 방코드 (int)
    selected_game = None        # 선택된게임의 String
    game_obj = None             # 게임객체
    room_host = None            # 호스트의 User객체
    room_participants = []      # 유저객체들의 리스트
    IoT_code = None             # IoT 디바이스 코드


    def __init__(self, room_code, room_host=None):
        self.room_code = room_code
        self.room_host = room_host
        self.room_participants = []

    def __str__(self):
        return str(self.room_code) + ",".join(list(map(str, self.room_participants)))

    def add_user(self, user):
        self.room_participants.append(user)
        user.room = self
    
    def set_room_host(self, host_obj):
        self.room_host = host_obj
        host_obj.room = self

    def num_of_participants(self):
        return len(self.room_participants)

    def is_in_game(self):
        if self.selected_game == None:
            return False
        else:
            return True
    
    def start_game(self, selected_game):
        self.selected_game = selected_game
        if selected_game == "RPS":
            self.game_obj = game.GameLogic.RPS.RPS(self.room_host, self.room_participants)
        elif selected_game == "FIVE_POKER":
            pass
            # self.game_obj = game.GameLogic.bet.PokerGame(self.room_participants[0], self.room_participants[1], self.room_participants[2], self.room_participants[3])
        elif selected_game == "Bomb":
            self.game_obj = game.GameLogic.Bomb.Bomb(self.room_host, self.room_participants)


class User:
    room = None
    nickname = None
    sessionKey = None
    # socketObject = None

    def __init__(self, sessionKey, nickname=None):
        print("__init__", sessionKey)
        self.sessionKey = sessionKey
        self.nickname = nickname


    def delete(self):
        if self.isParticipant:
            self.room.room_participants.remove(self)


    def __str__(self):
        if self.isParticipant():
            return self.nickname
        else:
            return str(self.room.room_code) + "'s host"

    def isParticipant(self):
        if self.nickname == None:
            return False
        else:
            return True
    


global room_manager
room_manager = RoomManager()