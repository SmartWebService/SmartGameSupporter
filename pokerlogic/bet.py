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

    def view_cards(self):
        card_sort(self.cards)
        for card in self.cards:
            if card == self.cards[4]:
                print(card)
            else:
                print(card, end=' ')

    def set_chip(self, chips):
        self.chips = chips

    def get_chip(self):
        return self.chips

    def add_chip(self, chips):
        self.chips += chips

    def basic_bet(self):
        self.chips -= 10

    def betting(self, BetChips):
        self.chips -= BetChips
        self.bet_chips += BetChips

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


def one_game(p1, p2, p3, p4):
    carddump = CardDump()
    endgame = False
    while not endgame:
        p1.basic_bet()
        p2.basic_bet()
        p3.basic_bet()
        p4.basic_bet()

        carddump.give_hand(p1, 5)
        carddump.give_hand(p2, 5)
        carddump.give_hand(p3, 5)
        carddump.give_hand(p4, 5)

        print("p1's cards : ", end='')
        p1.view_cards()
        print(p1.change_point())
        print("p2's cards : ", end='')
        p2.view_cards()
        print(p2.change_point())
        print("p3's cards : ", end='')
        p3.view_cards()
        print(p3.change_point())
        print("p4's cards : ", end='')
        p4.view_cards()
        print(p4.change_point())
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

        carddump.clear()
        endgame = True


def bet_func(p1, p2, p3, p4):
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


    one_game(p1, p2, p3, p4)


