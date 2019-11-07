
'''Card Class
        suit와 rank를가지는 클래스
        suit는 카드의 문양, rank는 카드의 숫자
        문양은 낮은 순서대로 0,1,2,3으로 표현(클로버, 하트, 다이아몬드, 스페이드
        숫자는 2부터 A까지 0부터 12로 표현
        getPoint함수는 카드를 비교할 때 사용, 카드숫자가 높울수록, 카드 숫자가 같으면
        문양순서대로 점수가 높다'''

Srank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
Ssuit = ['CLOVER', 'HEART', 'DIAMOND', 'SPADE']
class Card:

    def __init__(self, suit, rank):
        self.__suit = suit
        self.__rank = rank

    def getRank(self):
        return self.rank

    def getSuit(self):
        return self.suit

    def getPoint(self):
        return self.rank*10+self.suit

    def __str__(self):
        return Ssuit[self.suit]+Srank[self.rank]


'''CH함수
        카드 다섯장을 담은 리스트를 인자로 받는다
        카드의 패 종류와 종류가 같을때 점수를 결정하는 하이카드를 반환'''
def CheckHand(cards):

    straight = False
    flush = False
    Fok = False
    Tok = False
    numPair = 0
    handtype = ''

    CardSort(cards) #카드들을 내림차순으로 정렬

    '''스트레이트 확인'''
    straightCounter = 0
    for i in range(4):
        if cards[i].getRank() == cards[i+1].getRank()+1:
            straightCounter += 1
    if straightCounter == 4:
        straight = True
    elif straightCounter == 3 and cards[0].getRank() == 14:
        straight= True

    '''플러시 확인'''
    for i in range(5):
        if cards[0].getSuit() != cards[i].getSuit():
            break
    else:
        flush = True

    '''같은 숫자 확인'''
    toc = Card(0,0) #페어일 경우 가장높은 카드
    for i in range(5):
        cnt = 0
        for j in range(0, 5):
            if cards[i].getRank() == cards[j].getRank():
                cnt += 1
        if cnt == 2:
            numPair += 1
            if toc.getPoint() < cards[i].getPoint():
                toc = cards[i]
        elif cnt == 3:
            if toc.getPoint() < cards[i].getPoint():
                toc = cards[i]
            elif numPair == 2and Tok == False:
                toc = cards[i]
            Tok = True
        elif cnt == 4:
            Fok = True
            if toc.getPoint() < cards[i].getPoint():
                toc = cards[i]
            break
    numPair /= 2

    highcard = cards[0] if flush or straight else toc

    if  (straight and flush):
        handtype = 'StraightFlush'
    elif (Fok):
        handtype = 'Four of A Kind'
    elif (numPair == 1 and Tok):
        handtype = 'Full House'
    elif flush:
        handtype = 'Flush'
    elif straight:
        handtype = 'straight'
    elif Tok:
        handtype = 'Three Of A Kind'
    elif numPair == 2:
        handtype = 'Two Pair'
    elif numPair == 1:
        handtype = 'Pair'
    else:
        handtype = 'High Card'
        highcard = cards[0]

    return handtype, highcard


'''카드패 정렬 함수'''

def CardSort(cards5):
    for i in range(4):
        for j in range(i+1,5):
            if cards5[i].getPoint() < cards5[j].getPoint():
                tmp = cards5[i]
                cards5[i] = cards5[j]
                cards5[j] = tmp

class Dealer:
    pass

class Player:
    def Player(self, id):
        self.id = id

    def setCards(self, cards):
        self.cards = cards

    def setChip(self, chips):
        self.chips = chips

if __name__ == '__main__':
    fc = Card(0, 8)
    sc = Card(0, 10)
    tc = Card(1, 8)
    fourc = Card(2, 10)
    fifc = Card(2, 12)
    cards = [fc, sc, tc, fourc, fifc]
    for i in range(5):
        print(cards[i])
    answer = CheckHand(cards)
    print(answer[0], answer[1])

