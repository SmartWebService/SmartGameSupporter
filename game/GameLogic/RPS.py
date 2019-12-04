from random import *
import core.core


class Player():
    RPS_container = None
    user = None

    def __init__(self, user):
        self.user = user
    
    def setRPS(self, RPS_container):
        self.RPS_container = RPS_container


class RPS:
    host = None
    participants = []
    players = []

    def __init__(self, host, participants):  # 새 가위바위보 게임 객체
        print("Started RPS at ", host.room.room_code)
        self.host = host
        self.participants = participants
        self.participants_to_player()

    def participants_to_player(self):
        for participant in self.participants:
            self.players.append(Player(participant))
    
    def playRPS_set(self, user, RPS_container):
        for player in self.players:
            if player.user == user:
                player.setRPS(RPS_container)
        
    def decision(self):
        host_pick = randint(0,2)
        R_players = []
        P_players = []
        S_players = []

        for player in self.players:
            if player.RPS_container == 'R':
                R_players.append(player)
            elif player.RPS_container == 'P':
                P_players.append(player)
            elif player.RPS_container == 'S':
                S_players.append(player)
            
