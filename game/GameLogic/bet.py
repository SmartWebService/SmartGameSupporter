import random
from Poker import *


class Player:
    def __init__(self, user):
        self.user = user
        self.cards = []
        self.chips = 0
        self.bet_chips = 0
        self.die = False
        self.afterplayer = None
        self.beforeplayer = None

    def discard_cards(self, index):
        tmp = self.cards[:]
        for i in index:
            self.cards.remove(tmp[i])

    def set_players(self, before, after):
        self.afterplayer = after
        self.beforeplayer = before

    def set_cards(self, cards):
        self.cards = cards

    def get_cards(self):
        return self.cards

    def add_cards(self, cards):
        self.cards = self.cards + cards

    def get_bet_chips(self):
        return self.bet_chips

    def view_cards(self, sorted=True):
        tmp = self.cards[:]
        if sorted:
            card_sort(tmp)
        cards_string = ""
        for card in tmp:
            if card == tmp[4]:
                cards_string += str(card)
            else:
                cards_string += str(card) + " "
        return cards_string

    def set_chip(self, chips):
        self.chips = chips

    def get_chip(self):
        return self.chips

    def add_chip(self, chips):
        self.chips += chips

    def basic_bet(self):
        self.chips -= 1
        self.bet_chips += 1

    def betting(self, BetChips):
        self.chips -= BetChips
        self.bet_chips += BetChips

    def all_in(self):
        self.bet_chips += self.chips
        self.chips = 0

    def clear(self):
        self.bet_chips = 0
        self.die = False
        self.cards = []

    def do_die(self):
        self.die = True

    def is_die(self):
        return self.die

    def get_type(self):
        cards_type = check_hand(self.cards)
        return(cards_type[0])

    def change_point(self):
        cards_type = check_hand(self.cards)
        return type_tuple.index(cards_type[0])*1000 + cards_type[1].get_point()


class CardDump:
    def __init__(self):
        self.clear()

    def clear(self):
        self.cards = {}
        self.cards = set()
        for i in range(52):
            self.cards.add(i)

    def get_len(self):
        return len(self.cards)

    def view_dump(self):
        print()
        for card in self.cards:
            print(card, end=' ')
        print()
        print()

    def draw(self, n):
        tmp = random.sample(self.cards, n)
        for card in tmp:
            self.cards.remove(card)

        playercards = []
        for card in tmp:
            playercards.append(Card(card//13, card%13))
        return playercards


class PokerGame:
    def __init__(self, host, participants):
        self.nowbet = 1
        self.raisecount = 0
        self.callcount = 0
        self.diecount = 0
        self.allincount = 0
        self.players = []
        self.host = host
        self.participatns = participants
        self.participants_to_players(participants)
        self.reload_player()
        self.carddump = CardDump()
        self.nowplayer = self.players[0]

    def participants_to_players(participants):
        for player in participants:
            self.players.append(Player(player))

    def reload_player(self):
        self.players[0].set_players(self.players[3], self.players[1])
        self.players[1].set_players(self.players[0], self.players[2])
        self.players[2].set_players(self.players[1], self.players[3])
        self.players[3].set_players(self.players[2], self.players[0])

    def get_nowplayer(self):
        return self.nowplayer

    def next_player(self):
        self.nowplayer = self.nowplayer.afterplayer

    def all_basic_bet(self):
       for player in self.players:
           player.basic_bet()

    def all_give_hand(self):
        for player in self.players:
            self.all_give_hand(player)

    def give_hand(self, player):
        playercards = self.carddump.draw(5)
        player.set_cards(playercards)

    def change_hand(self, player, index):
        playercards = self.carddump.draw(len(index))
        player.discard_cards(index)
        player.add_cards(playercards)

    def get_all_bet(self):
        return self.p1.get_bet_chips() + self.p2.get_bet_chips() + self.p3.get_bet_chips() + self.p4.get_bet_chips()

    def give_winner_chips(self, winner):
        if winner.get_chip() == 0:
            for player in self.players:
                remainder = player.get_bet_chips() - winner.get_bet_chips()
                if remainder > 0:
                    winner.add_chip(winner.get_bet_chips())
                    player.add_chip(remainder)
                else:
                    winner.add_chip(player.get_bet_chips())
        else:
            winner.add_chip(self.get_all_bet())

    def clear_game(self):
        for player in self.players:
            player.clear()
        self.carddump.clear()
        self.reload_player()

    def all_in(self, player):
        player.beforeplayer.afterplayer = player.afterplayer
        player.afterplayer.beforeplayer = player.beforeplayer
        player.all_in()
        self.allincount += 1

    def die(self, player):
        player.beforeplayer.afterplayer = player.afterplayer
        player.afterplayer.beforeplayer = player.beforeplayer
        player.do_die()
        self.diecount += 1

    def call(self, player):
        if self.nowbet >= player.get_chip():
            print('error')
        else:
            player.betting(self.nowbet)
            self.callcount += 1

    def rais(self, player, chips):
        self.nowbet = chips
        self.callcount = 0
        self.call(player)

    def check_all_in(self, player, chip):
        if chip >= player.get_chip():
            return True
        else:
            return False

    def check_raise(self, chips):
        if self.raisecount >= 3 or self.nowbet >= chips:
            return False
        else:
            return True

    def check_break(self):
        if self.diecount >= 3 or self.diecount + self.callcount + self.allincount >= 4:
            return True
        else:
            return False

    def check_winner(self):
        a = [[], []]
        for player in self.players:
            if player.is_die():
                continue
            else:
                a[0].append(player.change_point())
                a[1].append(player)

        if len(a[0]) == 1:
            winner = a[1][0]
        else:
            winner = a[1][a[0].index(max(a[0]))]
        return winner

    def check_endgame(self):
        for player in self.players:
            if player.get_chip() == 0:
                return True
        return False





'''def bet_func(p1, p2, p3, p4):
    nowbet = 1
    nowplayer = p1
    raisecount = 0
    raiseplayer = None
    diecount = 0
    while nowplayer != raiseplayer:
        if raiseplayer == None:
            raiseplayer = nowplayer
        print("{}님, 현재 베팅 금액은 {}칩 입니다".format(nowplayer.id, nowbet))
        b = input("input die : d, raise : r, call : c  what you want? : ")
        if b == 'd':
            if raiseplayer == nowplayer:
                raiseplayer = None
            nowplayer.beforeplayer.afterplayer = nowplayer.afterplayer
            nowplayer.afterplayer.beforeplayer = nowplayer.beforeplayer
            nowplayer.do_die()
            nowplayer = nowplayer.afterplayer
            diecount += 1
            if diecount >= 3:
                break
        elif b == 'c':
            if nowbet >= nowplayer.get_chip():
                print("you are all in")
                nowplayer.betting(nowplayer.get_chip())
                nowplayer.beforeplayer.afterplayer = nowplayer.afterplayer
                nowplayer.afterplayer.beforeplayer = nowplayer.beforeplayer
                if nowplayer == raiseplayer:
                    raiseplayer = None
            else:
                nowplayer.betting(nowbet)
            nowplayer = nowplayer.afterplayer
        elif b == 'r':
            if raisecount >= 3:
                print("raisecount is 3, you can't raise")
                continue
            else:
                raisemoney = int(input("how much do you raise?"))
                if raisemoney <= nowbet:
                    print("your raise chip is less than now bet, please raise more than {}".format(nowbet))
                    continue
                elif raisemoney >= nowplayer.get_chip():
                    print("your raise chips is more than you have, you all in")
                    raisemoney = nowplayer.get_chip()
                    nowplayer.betting(nowplayer.get_chip())
                    nowplayer.beforeplayer.afterplayer = nowplayer.afterplayer
                    nowplayer.afterplayer.beforeplayer = nowplayer.beforeplayer
                    raiseplayer = None
                    nowplayer = nowplayer.afterplayer
                    raisecount += 1
                else:
                    nowbet = raisemoney
                    nowplayer.betting(nowbet)
                    raiseplayer = nowplayer
                    nowplayer = nowplayer.afterplayer
                    raisecount += 1
        else:
            print("please input only 'c', 'd' or 'r'")
            if raiseplayer == nowplayer:
                raiseplayer == None'''

def onebetting(game:PokerGame):
    while True:
        string = ""
        NP = game.get_nowplayer()
        print("player {}'s turn, now bet is {}, all bet is {}".format(NP.id, game.nowbet, game.get_all_bet()))
        print(NP.view_cards(False))
        string = input("die - d, raise - r, call, c : ")
        if string != 'd' and string != 'r' and string != 'c':
            continue

        if string == 'd':
            game.die(NP)

        elif string == 'r':
            if game.check_all_in(NP, game.nowbet):
                print("your chips are less than now betting, you can only do call(all-in) or die")
                continue
            else:
                raise_chip = input("how do you raise? : ")
                try:
                    raise_chip = int(raise_chip)
                except(ValueError):
                    print("please input number")
                    continue
                if game.check_raise(raise_chip):
                    if game.check_all_in(NP, raise_chip):
                        print("your chips are less than your raise chips")
                        answer = input("if you want to do all-in raise with {}chips more, enter y : ".format(NP.get_chip()))
                        if answer == 'y':
                            game.rais(NP, NP.get_chip())
                            game.all_in(NP)
                        else:
                            continue
                    else:
                        game.rais(NP, raise_chip)
                else:
                    continue

        elif string == 'c':
            if game.check_all_in(NP, game.nowbet):
                print("your bet chip is less than now betting, do you want all-in?")
                answer = input("if you want all_in, enter y : ")
                if answer == 'y':
                    game.all_in(NP)
                else:
                    continue
            else:
                game.call(NP)

        if game.check_break():
            break

        game.next_player()

if __name__ == '__main__':
    p1 = Player(1)
    p2 = Player(2)
    p3 = Player(3)
    p4 = Player(4)

    p1.set_players(p4, p2)
    p2.set_players(p1, p3)
    p3.set_players(p2, p4)
    p4.set_players(p3, p1)


    p1.set_chip(100)
    p2.set_chip(100)
    p3.set_chip(100)
    p4.set_chip(100)

    print("all player's basic chips is 100")

    game = PokerGame(p1, p2, p3, p4)

    print('all basic beted')
    game.all_basic_bet()
    game.all_give_hand()
    onebetting(game)
    '''while True:
        string = ""
        NP = game.get_nowplayer()
        print("player {}'s turn, now bet is {}, all bet is {}".format(NP.id, game.nowbet, game.get_all_bet()))
        print(NP.view_cards(False))
        string = input("die - d, raise - r, call, c : ")
        if string != 'd' and string != 'r' and string != 'c':
            continue

        if string == 'd':
            game.die(NP)

        elif string == 'r':
            if game.check_all_in(NP, game.nowbet):
                print("your chips are less than now betting, you can only do call(all-in) or die")
                continue
            else:
                raise_chip = input("how do you raise? : ")
                try:
                    raise_chip = int(raise_chip)
                except(ValueError):
                    print("please input number")
                    continue
                if game.check_raise(raise_chip):
                    if game.check_all_in(NP, raise_chip):
                        print("your chips are less than your raise chips")
                        answer = input("if you want to do all-in raise with {}chips more, enter y : ".format(NP.get_chip()))
                        if answer == 'y':
                            game.rais(NP, NP.get_chip())
                            game.all_in(NP)
                        else:
                            continue
                    else:
                        game.rais(NP, raise_chip)
                else:
                    continue

        elif string == 'c':
            if game.check_all_in(NP, game.nowbet):
                print("your bet chip is less than now betting, do you want all-in?")
                answer = input("if you want all_in, enter y : ")
                if answer == 'y':
                    game.all_in(NP)
                else:
                    continue
            else:
                game.call(NP)

        if game.check_break(NP):
            break

        game.next_player()'''

    for player in game.players:
        if not player.is_die():
            index = []
            print("player {}, which card do you want to change? \n(nothing is -1, your card is {})".format(player.id, player.view_cards(False)))
            while True:
                try:
                     a = int(input())
                except(ValueError):
                    print("please input number")
                    continue
                cardin = [1,2,3,4,0]
                if a in cardin and a not in index:
                    index.append(a)
                elif a == -1:
                    break
                else:
                    print("please input 0~4, if you do not want to change, input -1")
            game.change_hand(player, index)
    game.next_player()
    onebetting(game)

    winner = game.check_winner()

    print("winner is {}, the card is {}".format(winner.id, winner.view_cards()))
    print()

    game.give_winner_chips(winner)

    for player in game.players:
        print("player {}'s card : {}\n{}, remain chips : {}".format(player.id, player.view_cards(),
                                                                   player.get_type(), player.get_chip()))
        print()

    game.clear_game()


            


