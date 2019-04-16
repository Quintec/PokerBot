from operator import itemgetter, attrgetter, methodcaller
class Card:
    def __init__(self, n, s):
        self.num = n
        self.suit = s
    def to_img_str(self):
        strn = ""
        n=self.num
        if self.num>=2 and self.num<=10:
            strn = str(self.num)
        elif n==1:
            strn = "Ace"
        elif n==11:
            strn = "Jack"
        elif n==12:
            strn = "Queen"
        elif n == 13:
            strn = "King"
        return "/Users/huangl16/Documents/cards/" + strn + "_of_" + self.suit + ".png"
    def __str__(self):
        strn = ""
        n=self.num
        if self.num>=2 and self.num<=10:
            strn = str(self.num)
        elif n==1:
            strn = "Ace"
        elif n==11:
            strn = "Jack"
        elif n==12:
            strn = "Queen"
        elif n == 13:
            strn = "King"
        return strn + " of " + self.suit


class Player:
    def __init__(self, u):
        self.user = u
        self.hand_name = ""
        self.money = 100
        self.bet = 0
        self.hand = []
        self.folded = False
        self.has_moved = False
        self.d_files = []
        self.rank = -1
        self.flush = False
        self.straight = False
        self.royal = False
        self.pairs = 0
        self.three = False
        self.four = False
        self.high = -1
        self.high2 = -1
        self.counts = {}
    def tsa_precheck(self):
        self.hand = sorted(self.hand, key=attrgetter('num'))
        for i in range(1, 14):
            self.counts[i] = 0;
        for h in self.hand:
            self.counts[h.num] += 1;

    def num_string(self, n):
        n = int(n)
        if 2 <= n <= 10:
            return str(n)
        elif n==1 or n==14:
            return "Ace"
        elif n==11:
            return "Jack"
        elif n==12:
            return "Queen"
        elif n == 13:
            return "King"
        
    def highest(self):
        ans = 0
        for h in self.hand:
            if h.num == 1:
                return 14
            ans = ans if ans > h.num else h.num
        return ans

    def rank_hand(self):
        if self.check_flush() and self.check_straight():
            self.high = self.highest()
            self.rank = 9
            if self.highest() == 14:
                self.hand_name = "a royal flush"
            else:
                self.hand_name = "a " + self.num_string(str(self.high)) + " high straight flush"
        elif self.check_four_kind():
            for num, count in self.counts.items():
                if count == 4:
                    self.high = num
            self.rank = 8
            self.hand_name = "four " + self.num_string(str(self.high))
        elif self.check_full_house():
            for num, count in self.counts.items():
                if count == 3:
                    self.high = num
                if count == 2:
                    self.high2 = num
            self.rank = 7
            self.hand_name = "a full house with three " + self.num_string(str(self.high)) + " and two " + str(self.high2)
        elif self.check_flush():
            self.high = self.highest()
            self.rank = 6
            self.hand_name = "a " + self.num_string(str(self.high)) + " high flush"
        elif self.check_straight():
            self.high = self.highest()
            self.rank = 5
            self.hand_name = "a " + self.num_string(str(self.high)) + " high straight"
        elif self.check_three_kind():
            for num, count in self.counts.items():
                if count == 3:
                    self.high = num
            self.rank = 4
            self.hand_name = "three " + self.num_string(str(self.high))
        elif self.check_two_pair():
            for num, count in self.counts.items():
                if count == 2 and self.high2 == -1:
                    self.high2 = num
                elif count == 2 and self.high2 != -1:
                    self.high = num
            self.rank = 3
            self.hand_name = "pairs of " + self.num_string(str(self.high)) + "s and " + self.num_string(str(self.high)) + "s"
        elif self.check_pair():
            for num, count in self.counts.items():
                if count == 2:
                    self.high = num
            self.rank = 2
            self.hand_name = "a pair of " + self.num_string(str(self.high)) + "s"
        else:
            self.high = self.highest()
            self.rank = 1
            self.hand_name = self.num_string(str(self.high)) + " high"
        
            
    def check_flush(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        for s in suits:
            ans = True
            for h in self.hand:
                if not h.suit == s:
                    ans = False
            if ans:
                return True
        return False
    def check_straight(self):
        if self.hand[0].num == 1 and self.hand[1].num == 10 and self.hand[2].num == 11 and self.hand[3].num == 12 and self.hand[4].num == 13:
               return True
        for i in range(1,11):
            ans = True
            for j in range(0,5):
                if not self.hand[j].num == i+j:
                    ans = False
            if ans:
                return True
        return False
    
    def check_four_kind(self):
        return 4 in list(self.counts.values())

    def check_three_kind(self):
        return 3 in list(self.counts.values())

    def check_pair(self):
        return 2 in list(self.counts.values())

    def check_two_pair(self):
        return list(self.counts.values()).count(2) == 2

    def check_full_house(self):
        return self.check_three_kind() and self.check_pair()
