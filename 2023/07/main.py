from shared.utils import *


class Hand:
    TYPE_FIVE_OF_A_KIND = 7
    TYPE_FOUR_OF_A_KIND = 6
    TYPE_FULL_HOUSE = 5
    TYPE_THREE_OF_A_KIND = 4
    TYPE_TWO_PAIR = 3
    TYPE_ONE_PAIR = 2
    TYPE_HIGH_CARD = 1

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid

        self.counts = defaultdict(lambda: 0)
        for card in cards:
            self.counts[Hand.value(card)] += 1

        self.resolved_type = Hand.get_type(self.counts)
        self.use_joker_cards = False

    def recount_for_jokers(self):
        self.use_joker_cards = True

        if 'J' not in self.cards:
            return

        self.counts = defaultdict(lambda: 0)
        for card in self.cards:
            self.counts[Hand.value(card, use_joker=True)] += 1

        self.resolved_type = Hand.get_type(self.counts, use_joker=True)

    @staticmethod
    def get_type(counts: Dict[int, int], use_joker=False) -> int:
        return max(Hand.yield_types(counts, use_joker))

    @staticmethod
    def yield_types(counts: Dict[int, int], use_joker=False) -> Iterable[int]:
        j_value = Hand.value('J', use_joker)

        for value, count in counts.items():
            if count == 5:
                yield Hand.TYPE_FIVE_OF_A_KIND

            elif count == 4:
                if use_joker and value != 'J':
                    yield Hand.TYPE_FIVE_OF_A_KIND
                else:
                    yield Hand.TYPE_FOUR_OF_A_KIND

            elif count == 3:
                if use_joker:
                    if counts[j_value] == 1:
                        yield Hand.TYPE_FOUR_OF_A_KIND
                    elif counts[j_value] == 2:
                        yield Hand.TYPE_FIVE_OF_A_KIND
                    elif counts[j_value] == 3 and 2 in counts.values():
                        yield Hand.TYPE_FIVE_OF_A_KIND
                    else:
                        yield Hand.TYPE_FOUR_OF_A_KIND
                else:
                    if 2 in counts.values():
                        yield Hand.TYPE_FULL_HOUSE
                    else:
                        yield Hand.TYPE_THREE_OF_A_KIND

            elif count == 2:
                if use_joker:
                    if counts[j_value] == 2:
                        if list(counts.values()).count(2) == 2:
                            yield Hand.TYPE_FOUR_OF_A_KIND
                        else:
                            yield Hand.TYPE_THREE_OF_A_KIND
                    else:
                        if list(counts.values()).count(2) == 2:
                            yield Hand.TYPE_FULL_HOUSE
                        else:
                            yield Hand.TYPE_THREE_OF_A_KIND
                else:
                    if list(counts.values()).count(2) == 2:
                        yield Hand.TYPE_TWO_PAIR
                    else:
                        yield Hand.TYPE_ONE_PAIR

            else:
                if use_joker:
                    yield Hand.TYPE_ONE_PAIR
                else:
                    yield Hand.TYPE_HIGH_CARD

    @staticmethod
    def value(card, use_joker=False):
        if '2' <= card <= '9':
            return int(card)
        elif card == 'T':
            return 10
        elif card == 'J':
            if use_joker:
                return 1
            else:
                return 11
        elif card == 'Q':
            return 12
        elif card == 'K':
            return 13
        elif card == 'A':
            return 14

    def __lt__(self, other: 'Hand'):
        if self.resolved_type != other.resolved_type:
            return self.resolved_type < other.resolved_type

        for idx, card in enumerate(self.cards):
            m, o = Hand.value(card, use_joker=self.use_joker_cards), Hand.value(other.cards[idx], use_joker=other.use_joker_cards)
            if m != o:
                return m < o

    def __repr__(self):
        return f'H({self.cards}):{self.bid}'


class Day07(Solution):
    hands: List[Hand]

    def setup(self):
        self.hands = list()

        for line in self.input_lines():
            cards, bid = line.split()
            self.hands.append(Hand(cards, int(bid)))

    def part_1(self):
        for rank, hand in enumerate(sorted(self.hands)):
            self.add_result(hand.bid * (rank + 1))

    def part_2(self):
        for hand in self.hands:
            hand.recount_for_jokers()

        for rank, hand in enumerate(sorted(self.hands)):
            self.add_result(hand.bid * (rank + 1))


Day07(__file__).solve()
