
'''Card Class
        suit와 rank를가지는 클래스
        suit는 카드의 문양, rank는 카드의 숫자
        문양은 낮은 순서대로 0,1,2,3으로 표현(클로버, 하트, 다이아몬드, 스페이드
        숫자는 2부터 A까지 0부터 12로 표현
        getPoint함수는 카드를 비교할 때 사용, 카드숫자가 높울수록, 카드 숫자가 같으면
        문양순서대로 점수가 높다'''

rank_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suit_list = ['C', 'D', 'H', 'S']
type_tuple = ('High Card', 'Pair', 'Two Pair', 'Three Of A Kind', 'Straight', 'Flush',
              'Full House', 'Four Of A Kind', 'Straight Flush')


class Card:

    def __init__(self, suit, rank):
        self.__suit: int = suit
        self.__rank: int = rank

    def get_rank(self):
        return self.__rank

    def get_suit(self):
        return self.__suit

    def get_point(self):
        return (self.__rank + 2)*10 + self.__suit

    def __str__(self):
        return suit_list[self.__suit] + rank_list[self.__rank]




'''CH함수
        카드 다섯장을 담은 리스트를 인자로 받는다
        카드의 패 종류와 종류가 같을때 점수를 결정하는 하이카드를 반환'''


def check_hand(cards):

    straight = False
    flush = False
    Fok = False
    Tok = False
    numPair = 0
    backstraight = False

    card_sort(cards) #카드들을 내림차순으로 정렬

    '''스트레이트 확인'''
    straightCounter = 0
    for i in range(4):
        if cards[i].get_rank() == cards[i+1].get_rank()+1:
            straightCounter += 1
    if straightCounter == 4:
        straight = True
    elif straightCounter == 3 and cards[0].get_rank() == 12 and cards[1].get_rank() == 3:
        straight = True
        backstraight = True

    '''플러시 확인'''
    for i in range(len(cards)):
        if cards[0].get_suit() != cards[i].get_suit():
            break
    else:
        flush = True

    '''같은 숫자 확인'''
    toc = Card(0,0) #페어일 경우 가장높은 카드
    for i in range(len(cards)):
        cnt = 0
        for j in range(0, len(cards)):
            if cards[i].get_rank() == cards[j].get_rank():
                cnt += 1
        if cnt == 2:
            numPair += 1
            if toc.get_point() < cards[i].get_point():
                toc = cards[i]
        elif cnt == 3:
            if toc.get_point() < cards[i].get_point():
                toc = cards[i]
            elif numPair == 2 and not Tok:
                toc = cards[i]
            Tok = True
        elif cnt == 4:
            Fok = True
            if toc.get_point() < cards[i].get_point():
                toc = cards[i]
            break
    numPair /= 2

    highcard = cards[0] if flush or straight else toc

    if  (straight and flush):
        handtype = 'Straight Flush'
        if backstraight:
            highcard = cards[1]
    elif (Fok):
        handtype = 'Four of A Kind'
    elif (numPair == 1 and Tok):
        handtype = 'Full House'
    elif flush:
        handtype = 'Flush'
    elif straight:
        handtype = 'Straight'
        if backstraight:
            highcard = cards[1]
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


def card_sort(cards5):
    for i in range(4):
        for j in range(i+1,5):
            if cards5[i].get_point() < cards5[j].get_point():
                tmp = cards5[i]
                cards5[i] = cards5[j]
                cards5[j] = tmp


if __name__ == '__main__':
    fc = Card(0, 12)
    sc = Card(0, 2)
    tc = Card(1, 1)
    fourc = Card(2, 0)
    fifc = Card(2, 3)
    cards = [fc, sc, tc, fourc, fifc]
    for i in range(5):
        print(cards[i])
    answer = check_hand(cards)
    print(answer[0], answer[1])

