from abc import ABC
from dataclasses import dataclass

from env.game import Aces, BaseCombination, Dices, Fives, Fours, Sixes, Threes, Twos
from env.utils import get_all_possible_combinations


@dataclass
class WriteCombinationAction:
    combination: BaseCombination

    def __repr__(self) -> str:
        return self.combination.__repr__()


@dataclass
class RethrowAction:
    mask: int

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({bin(self.mask)[2:]})"


type Action = WriteCombinationAction | RethrowAction


@dataclass
class State:
    table: list[BaseCombination]
    dices: Dices
    move: int

    def get_possible_actions(self) -> list[Action]:
        result = []

        if self.move < 3:
            result += self.get_write_school_combination_actions(self.dices)
        else:
            result += [
                WriteCombinationAction(combination)
                for combination in get_all_possible_combinations(self.dices)
                if type(combination) not in [type(c) for c in self.table]
            ]

        if self.dices.rethrown < 2:
            result += self.get_all_rethrow_actions()

        return result

    def get_all_rethrow_actions(self) -> list[RethrowAction]:
        return [RethrowAction(mask) for mask in range(0b100000)]

    def get_write_school_combination_actions(self, dices: Dices) -> list[WriteCombinationAction]:
        all = [
            Aces(dices.dices.count(1)),
            Twos(dices.dices.count(2)),
            Threes(dices.dices.count(3)),
            Fours(dices.dices.count(4)),
            Fives(dices.dices.count(5)),
            Sixes(dices.dices.count(6)),
        ]
        return [WriteCombinationAction(combination) for combination in all if type(combination) not in [type(c) for c in self.table]]


class DicePokerEnv:
    def __init__(self):
        self.current_state = State(
            table=[],
            dices=Dices.throw(),
            move=0,
        )

    def reset(self) -> State:
        self.current_state = State(
            table=[],
            dices=Dices.throw(),
            move=0,
        )
        return self.current_state

    def step(self, action: Action) -> State:
        if isinstance(action, WriteCombinationAction):
            self.current_state.table.append(action.combination)
            self.current_state.dices = Dices.throw()
            self.current_state.move += 1

        if isinstance(action, RethrowAction):
            assert self.current_state.dices.rethrown <= 1, "you can rethrow dices only two times in one move"
            self.current_state.dices.rethrow(action.mask)

        return self.current_state
