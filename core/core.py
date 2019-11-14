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


    def del_room(self, room):
        self.room_list.remove(room)


class Room:
    room_code = None
    selected_game = None
    room_host = None
    room_participants = []

    def __init__(self, room_code, room_host):
        self.room_code = room_code
        self.room_host = room_host

    def __str__(self):
        return room_code

    def add_user(self, user):
        self.room_participants.append(user)
        user.room = self


class User:
    room = None
    nickname = None
    socketObject = None

    def __init__(self, nickname):
        self.nickname = nickname
    
    def __str__(self):
        return self.nickname
    