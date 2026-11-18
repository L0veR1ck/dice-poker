from env.types import Action, State
from policy.base import BasePokerPolicy


class KeyboardPolicy(BasePokerPolicy):
    def act(self, state: State) -> Action:
        available_actions = state.get_possible_actions()
        for i, action in enumerate(available_actions):
            print(f"{i+1}. {action}")

        print("\nChoose action: ", end="")
        choice = int(input()) - 1
        chosen_action = available_actions[choice]

        return chosen_action
