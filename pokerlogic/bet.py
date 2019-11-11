import random
from Poker import *


class Player:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.chips = 0
        self.die = False

    def set_cards(self, cards):
        self.cards = cards

    def get_cards(self):
        return self.cards

    def view_cards(self):
        card_sort(self.cards)
        for card in self.cards:
            print(card, end=' ')
        print()

    def set_chip(self, chips):
        self.chips = chips

    def basic_bet(self):
        self.chips -= 10

    def betting(self, BetChips):
        self.chips -= BetChips

    def do_die(self):
        self.die = True

    def is_die(self):
        return self.die

    def change_point(self):
        cards_type = check_hand(self.cards)
        return type_tuple.index(cards_type[0])*1000 + cards_type[1].get_point()


class Bet:
    def __init__(self, howbet):
        self.howbet = howbet

    def die(self, player):
        player.Die = True

    def call(self,player):
        player.betting(self.howbet)

    def raise_func(self, player, howraise):
        player.betting(howraise)
        self.howbet = howraise


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

        bet = Bet(1)
        raisecount = 0
        allcall = False
        diecouont = 0



        carddump.clear()
        endgame = True




def bet_func(player):




        endgame = True

if __name__ == '__main__':
    p1 = Player(1)
    p2 = Player(2)
    p3 = Player(3)
    p4 = Player(4)


    p1.set_chip(100)
    p2.set_chip(100)
    p3.set_chip(100)
    p4.set_chip(100)


    one_game(p1, p2, p3, p4)


