from collections import Counter

from env.game import (
    Aces,
    BaseCombination,
    Chance,
    Dices,
    Fives,
    Fours,
    FullHouse,
    LargeStraight,
    NoCombination,
    Pair,
    Poker,
    Quads,
    Set,
    Sixes,
    SmallStraight,
    Threes,
    TwoPairs,
    Twos,
)


def get_all_possible_combinations(dices: Dices) -> list[BaseCombination]:
    result = [
        Aces(dices.dices.count(1)),
        Twos(dices.dices.count(2)),
        Threes(dices.dices.count(3)),
        Fours(dices.dices.count(4)),
        Fives(dices.dices.count(5)),
        Sixes(dices.dices.count(6)),
        Chance(dices),
        NoCombination(),
    ]

    if dices.dices == [1, 2, 3, 4, 5]:
        result.append(SmallStraight(x2=not dices.rethrown))

    if dices.dices == [2, 3, 4, 5, 6]:
        result.append(LargeStraight(x2=not dices.rethrown))

    cntr = Counter(dices.dices)
    cnts = sorted(cntr.values(), reverse=True)

    match cnts:
        case [1, 1, 1, 1, 1]:
            ...
        case [2, 1, 1, 1]:
            (value, _), = cntr.most_common(1)
            result.append(Pair(value, x2=not dices.rethrown))
        case [2, 2, 1]:
            (value1, _), (value2, _) = cntr.most_common(2)
            result.append(TwoPairs({value1, value2}, x2=not dices.rethrown))
            result.append(Pair(max(value1, value2), x2=not dices.rethrown))
        case [3, 1, 1]:
            (value, _), = cntr.most_common(1)
            result.append(Set(value, x2=not dices.rethrown))
            result.append(Pair(value, x2=not dices.rethrown))
        case [3, 2]:
            (trio_dice, _), (pair_dice, _) = cntr.most_common(2)
            result.append(FullHouse(pair_dice, trio_dice, x2=not dices.rethrown))
            result.append(TwoPairs({pair_dice, trio_dice}, x2=not dices.rethrown))
            result.append(Set(trio_dice, x2=not dices.rethrown))
            result.append(Pair(max(pair_dice, trio_dice), x2=not dices.rethrown))
        case [4, 1]:
            (value, _), = cntr.most_common(1)
            result.append(Quads(value, x2=not dices.rethrown))
            result.append(Set(value, x2=not dices.rethrown))
            result.append(Pair(value, x2=not dices.rethrown))
        case [5]:
            (value, _), = cntr.most_common(1)
            result.append(Poker(value, x2=not dices.rethrown))
            result.append(Quads(value, x2=not dices.rethrown))
            result.append(Set(value, x2=not dices.rethrown))
            result.append(Pair(value, x2=not dices.rethrown))

    return result


def do():
    from random import randint

    d = Dices.throw()
    print(d)
    variants = sorted(get_all_possible_combinations(d), key=lambda var: var.score, reverse=True)
    print("\n".join(map(str, variants)) + "\n")

    d.rethrow(mask=randint(0b00000, 0b11111))
    print(d)
    variants = sorted(get_all_possible_combinations(d), key=lambda var: var.score, reverse=True)
    print("\n".join(map(str, variants)) + "\n")

    d.rethrow(mask=randint(0b00000, 0b11111))
    print(d)
    variants = sorted(get_all_possible_combinations(d), key=lambda var: var.score, reverse=True)
    print("\n".join(map(str, variants)) + "\n")

def do2():
    from random import randint

    d = Dices.throw()
    print(d, max(get_all_possible_combinations(d), key=lambda variant: variant.score))

    d.rethrow(mask=randint(0b00000, 0b11111))
    print(d, max(get_all_possible_combinations(d), key=lambda variant: variant.score))

    d.rethrow(mask=randint(0b00000, 0b11111))
    print(d, max(get_all_possible_combinations(d), key=lambda variant: variant.score))
