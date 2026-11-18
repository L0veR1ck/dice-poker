import random
from abc import ABC, abstractmethod
from typing import Literal, cast

type Dice = Literal[1, 2, 3, 4, 5, 6]


class Dices:
    dices: list[Dice]
    rethrown: int

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Use {cls.__name__}.{cls.throw.__name__}")

    @staticmethod
    def throw(rng: random.Random | None = None) -> Dices:
        if rng is None:
            rng = random.Random()

        dices = object.__new__(Dices)
        dices.rethrown = 0
        dices.dices = [cast(Dice, rng.randint(1, 6)) for _ in range(5)]
        dices.dices.sort()

        return dices

    def rethrow(self, mask: int, rng: random.Random | None = None):
        """mask = 0b10000 means that the fifth dice must be rethrown"""
        assert 0b00000 <= mask <= 0b11111

        if rng is None:
            rng = random.Random()

        self.rethrown += 1
        for i in range(5):
            if mask & (1 << i):
                self.dices[i] = cast(Dice, rng.randint(1, 6))

        self.dices.sort()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.dices})"


type Score = int


class BaseCombination(ABC):
    score: Score
    x2: bool

    @abstractmethod
    def matches(self, dices: Dices) -> bool: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.score})"


class SchoolCombination(BaseCombination):
    def matches(self, dices: Dices) -> bool:
        return True


class Aces(SchoolCombination):
    def __init__(self, count: int):
        self.count = count
        self.score = 1 * (count - 3)


class Twos(SchoolCombination):
    def __init__(self, count: int):
        self.count = count
        self.score = 2 * (count - 3)


class Threes(SchoolCombination):
    def __init__(self, count: int):
        self.count = count
        self.score = 3 * (count - 3)


class Fours(SchoolCombination):
    def __init__(self, count: int):
        self.count = count
        self.score = 4 * (count - 3)


class Fives(SchoolCombination):
    def __init__(self, count: int):
        self.count = count
        self.score = 5 * (count - 3)


class Sixes(SchoolCombination):
    def __init__(self, count: int):
        self.count = count
        self.score = 6 * (count - 3)


class Pair(BaseCombination):
    def __init__(self, value: Dice, x2: bool = False):
        self.value = value
        self.x2 = x2

        self.score = value * 2
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return dices.dices.count(self.value) >= 2


class Set(BaseCombination):
    def __init__(self, value: Dice, x2: bool = False):
        self.value = value
        self.x2 = x2

        self.score = value * 3
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return dices.dices.count(self.value) >= 3


class TwoPairs(BaseCombination):
    def __init__(self, values: set[Dice], x2: bool = False):
        assert len(values) == 2

        self.values = values
        self.x2 = x2

        self.score = sum(values) * 2
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        value1, value2 = self.values
        return dices.dices.count(value1) >= 2 and dices.dices.count(value2) >= 2


class SmallStraight(BaseCombination):
    def __init__(self, x2: bool = False):
        self.x2 = x2

        self.score = 15
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return dices.dices == [1, 2, 3, 4, 5]


class LargeStraight(BaseCombination):
    def __init__(self, x2: bool = False):
        self.x2 = x2

        self.score = 20
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return dices.dices == [2, 3, 4, 5, 6]


class Quads(BaseCombination):
    def __init__(self, value: Dice, x2: bool = False):
        self.value = value
        self.x2 = x2

        self.score = value * 4
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return dices.dices.count(self.value) >= 4


class FullHouse(BaseCombination):
    def __init__(self, pair_dice: Dice, trio_dice: Dice, x2: bool = False):
        assert pair_dice != trio_dice

        self.value1 = pair_dice
        self.value2 = trio_dice
        self.x2 = x2

        self.score = pair_dice * 2 + trio_dice * 3
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return dices.dices.count(self.value1) >= 2 and dices.dices.count(self.value2) >= 3


class Poker(BaseCombination):
    def __init__(self, value: Dice, x2: bool = False):
        self.value = value
        self.x2 = x2

        self.score = 50 + value * 5
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return dices.dices.count(self.value) == 5


class Chance(BaseCombination):
    def __init__(self, dices: Dices, x2: bool = False):
        self.value = dices
        self.x2 = x2

        self.score = sum(dices.dices)
        if x2:
            self.score *= 2

    def matches(self, dices: Dices) -> bool:
        return True


class NoCombination(BaseCombination):
    def __init__(self):
        self.score = 0

    def matches(self, dices: Dices) -> bool:
        return True
