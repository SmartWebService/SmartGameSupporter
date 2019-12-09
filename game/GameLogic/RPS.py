from random import *
import core.core


class Player():
    RPS_container = None
    user = None

    def __init__(self, user):
        self.user = user
    
    def setRPS(self, RPS_container):
        self.RPS_container = RPS_container
    
    def __str__(self):
        return self.user.nickname


class RPS:
    host = None
    participants = []
    players = []

    def __init__(self, host, participants):  # 새 가위바위보 게임 객체
        print("Started RPS at ", host.room.room_code)
        self.host = host
        self.participants = participants
        self.participants_to_player()

        print(host)
        print(participants)
        print(self.participants)
        print(self.players)

    def participants_to_player(self):
        for participant in self.participants:
            self.players.append(Player(participant))

    def is_user_in_game(self, user):
        for i in self.participants:
            if i == user:
                return True
        return False
    
    def playRPS_set(self, user, RPS_container):
        for player in self.players:
            if player.user == user:
                player.setRPS(RPS_container)
    
    def get_participants_and_containers(self):
        p = []
        c = []

        for player in self.players:
            p.append(player.user.nickname)
            c.append(player.RPS_container)
        
        return p, c
        
    def decision(self, host_container):
        # host_pick = randint(0,2)
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
        
        print("host container", host_container)
        if host_container == "R":
            self.players = P_players
        elif host_container == "P":
            self.players = S_players
        elif host_container == "S":
            self.players = R_players

        self.participants = []

        print("R_players")
        for i in R_players:
            print(i)

        print("P_players")
        for i in P_players:
            print(i)

        print("S_players")
        for i in S_players:
            print(i)
        
        print("here")
        for i in self.players:
            print(i)
        
        


        
        for i in self.players:
            self.participants.append(i.user)
            
        return R_players, P_players, S_players
            
