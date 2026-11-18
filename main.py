from env.types import DicePokerEnv
from policy.keyboard import KeyboardPolicy


def main():
    env = DicePokerEnv()
    policy = KeyboardPolicy()

    state = env.reset()
    while True:
        print("\x1b[2J\x1b[H", end="", flush=True)
        print(state)
        print()
        action = policy.act(state)
        env.step(action)

if __name__ == "__main__":
    main()
