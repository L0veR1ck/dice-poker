from abc import ABC, abstractmethod

from env.types import Action, State


class BasePokerPolicy(ABC):
    @abstractmethod
    def act(self, state: State) -> Action:
        ...
