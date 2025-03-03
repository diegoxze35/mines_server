from typing import Callable

from MineSquare import MineSquare
from Square import Square

class EmptySquare(Square):

    def __init__(self, get_adjacent_squares: Callable[[(int, int)], list[Square]], x, y):
        super().__init__()
        self.__get_adjacent_squares = get_adjacent_squares
        self.__x = x
        self.__y = y

    def on_click(self):
        super().on_click()
        for square in self.__get_adjacent_squares((self.__x, self.__y)):
            if not square.is_visible() and not isinstance(square, MineSquare):
                square.on_click()

    def _draw(self) -> str:
        return '●'
