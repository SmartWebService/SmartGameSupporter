from random import *

class RoomManager:
    room_list = []

    def new_room(self, room_host):
        is_picked = False
        while not is_picked:
            pick_code = randint(100000, 999999)
            is_picked = True

            for room in self.room_list:
                if room.room_code == pick_code:
                    is_picked = False
                    break
        
        new_room = Room(pick_code, room_host)
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


class Room:
    room_code = None            # 방코드 (int)
    selected_game = None        # 게임객체
    room_host = None            # 호스트의 세션키
    room_participants = []      # 유저객체들의 리스트

    def __init__(self, room_code, room_host):
        self.room_code = room_code
        self.room_host = room_host

    def __str__(self):
        return str(self.room_code) + ",".join(list(map(str, self.room_participants)))

    def add_user(self, user):
        self.room_participants.append(user)
        user.room = self


class User:
    room = None
    nickname = None
    # socketObject = None

    def __init__(self, sessionKey, nickname):
        self.sessionKey = sessionKey
        self.nickname = nickname


    def delete(self):
        self.room.room_participants.remove(self)


    def __str__(self):
        return self.nickname
