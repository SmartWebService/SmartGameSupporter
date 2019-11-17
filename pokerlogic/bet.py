import random
from Poker import *


class Player:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.chips = 0
        self.bet_chips = 0
        self.die = False
        self.afterplayer = None
        self.beforeplayer = None

    def set_players(self, before, after):
        self.afterplayer = after
        self.beforeplayer = before

    def set_cards(self, cards):
        self.cards = cards

    def get_cards(self):
        return self.cards

    def get_bet_chips(self):
        return self.bet_chips

    def view_cards(self):
        card_sort(self.cards)
        cards_string = ""
        for card in self.cards:
            if card == self.cards[4]:
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

    def view_dump(self):
        print()
        for card in self.cards:
            print(card, end=' ')
        print()
        print()

    def give_hand(self,player, n):
        tmp = random.sample(self.cards, n)
        for card in tmp:
            self.cards.remove(card)

        playercards = []
        for card in tmp:
            playercards.append(Card(card//13, card%13))
        player.set_cards(playercards)



'''
def one_game(p1, p2, p3, p4):
    carddump = CardDump()
    endgame = False
    while not endgame:

        all_basic_bet(p1, p2, p3, p4)

        all_give_hand(carddump, p1, p2, p3, p4)

        print("p1's cards : ", end='')
        p1.view_cards()
        print("p2's cards : ", end='')
        p2.view_cards()
        print("p3's cards : ", end='')
        p3.view_cards()
        print("p4's cards : ", end='')
        p4.view_cards()

        bet_func(p1, p2, p3, p4)

        PL = [p1, p2, p3, p4]
        a = [[],[]]
        for player in PL:
            if player.is_die():
                continue
            else:
                a[0].append(player.change_point())
                a[1].append(player)
        if len(a[0]) == 1:
            winner = a[1][0]
        else:
            winnerp = max(a[0])
            winner = a[1][a[0].index(winnerp)]

        winner.view_cards()
        print(winner.id, "is win!!")

        for player in PL:
            winner.add_chip(player.bet_chips)
            player.clear()
        print("p1의 현재 칩 : ", p1.get_chip())
        print("p2의 현재 칩 : ",p2.get_chip())
        print("p3의 현재 칩 : ",p3.get_chip())
        print("p4의 현재 칩 : ",p4.get_chip())
        carddump.clear()
        if p1.get_chip() == 0 or p2.get_chip() == 0 or p3.get_chip() == 0 or p4.get_chip() == 0:
            endgame = True
'''

class PokerGame:
    def __init__(self, p1, p2, p3, p4):
        self.nowbet = 1
        self.raisecount = 0
        self.raiseplayer = p1
        self.diecount = 0
        self.allincount = 0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.all_player = [self.p1, self.p2, self.p3, self.p4]
        self.carddump = CardDump()
        self.nowplayer = p1

    def get_nowplayer(self):
        return self.nowplayer

    def next_player(self):
        self.nowplayer = self.nowplayer.afterplayer

    def all_basic_bet(self):
       for player in self.all_player:
           player.basic_bet()

    def all_give_hand(self):
        for player in self.all_player:
            self.carddump.give_hand(player, 5)

    def get_all_bet(self):
        return self.p1.get_bet_chips() + self.p2.get_bet_chips() + self.p3.get_bet_chips() + self.p4.get_bet_chips()

    def give_winner_chips(self, winner):
        if winner.get_chip() == 0:
            for player in self.all_player:
                remainder = player.get_bet_chips() - winner.get_bet_chips()
                if remainder > 0:
                    winner.add_chip(winner.get_bet_chips())
                    player.add_chip(remainder)
                else:
                    winner.add_chip(player.get_bet_chips())
        else:
            winner.add_chip(self.get_all_bet())
        self.clear_game()

    def clear_game(self):
        for player in self.all_player:
            player.clear()
        self.carddump.clear()

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
            pass
        else:
            player.betting(self.nowbet)

    def rais(self, player, chips):
        self.nowbet = chips
        self.raiseplayer = player
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

    def check_break(self, player):
        if self.diecount >= 3 or self.diecount + self.allincount >= 4 or player.afterplayer == self.raiseplayer:
            return True
        else:
            return False

    def check_winner(self):
        PL = [self.p1, self.p2, self.p3, self.p4]
        a = [[], []]
        for player in PL:
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
        for player in self.all_player:
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

    game = PokerGame(p1, p2, p3, p4)
    game.all_basic_bet()
    game.all_give_hand()
    while True:
        string = ""
        print("player {}'s turn, now bet is {}, all bet is {}".format(game.nowplayer.id, game.nowbet, game.get_all_bet()))
        string = input("die - d, raise - r, call, c : ")
        if string != 'd' and string != 'r' and string != 'c':
            continue

        if string == 'd':
            game.die(game.nowplayer)

        elif string == 'r':
            if game.check_all_in(game.nowplayer, game.nowbet):
                print("your chips are less than now betting, you can only do call(all-in) or die")
                continue
            else:
                raise_chip = int(input("how do you raise? : "))
                if game.check_raise(raise_chip):
                    if game.check_all_in(game.nowplayer, raise_chip):
                        print("your chips are less than your raise chips")
                        answer = input("if you want to do all-in raise with {}chips more, enter y : ".format(game.nowplayer.get_chip()))
                        if answer == 'y':
                            game.rais(game.nowplayer, game.nowplayer.get_chip())
                            game.all_in(game.nowplayer)
                        else:
                            continue
                    else:
                        game.rais(game.nowplayer, raise_chip)
                else:
                    continue

        elif string == 'c':
            if game.check_all_in(game.nowplayer, game.nowbet):
                print("your bet chip is less than now betting, do you want all-in?")
                answer = input("if you want all_in, enter y : ")
                if answer == 'y':
                    game.all_in(game.nowplayer)
                else:
                    continue
            else:
                game.call(game.nowplayer)

        if game.check_break(game.nowplayer):
            break

        game.next_player()

    winner = game.check_winner()

    print("winner is {}, the card is {}".format(winner.id, winner.view_cards()))

    print(p1.id, p1.view_cards())
    print(p2.id, p2.view_cards())
    print(p3.id, p3.view_cards())
    print(p4.id, p4.view_cards())

    game.give_winner_chips(winner)

    for player in game.all_player:
        print(player.id, player.get_chip())




            


