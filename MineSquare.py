from typing import Callable

from Square import Square

class MineSquare(Square):

    def __init__(self, on_game_over: Callable[[], None]):
        super().__init__()
        self.__on_game_over = on_game_over

    def on_click(self):
        super().on_click()
        self.__on_game_over()

    def _draw(self) -> str:
        return '*'
