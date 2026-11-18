from typing import Any

import gymnasium
from gymnasium import spaces

from env.types import BaseAction, State


class GymWrapper(gymnasium.Env[State, BaseAction]):
    action_space: spaces.Space[BaseAction] = spaces.Space()  # todo
    observation_space: spaces.Space[State] = spaces.Space()  # todo

    def reset(self, *, seed=None, options=None):
        raise NotImplementedError()

    def step(self, action: BaseAction) -> tuple[State, float, bool, bool, dict[str, Any]]:
        raise NotImplementedError()
