from logic import GameLogic
from ui import GameUI


def main():
    game_logic = GameLogic()
    game_ui = GameUI(game_logic)
    game_ui.run()


if __name__ == "__main__":
    main()
