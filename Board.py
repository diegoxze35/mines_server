from typing import Callable

from AdjacentMinesSquare import AdjacentMinesSquare
from Difficulty import Difficulty
from EmptySquare import EmptySquare
from MineSquare import MineSquare
from Square import Square
from random import choice


class Board:

    def __init__(self, difficulty: Difficulty, first_shoot: (int, int), on_click_mine: Callable[[], None]) -> None:
        self.__size = difficulty.squares
        self.__squares: list[list[Square | None]] = [[None for _ in range(self.__size)] for _ in range(self.__size)]
        board_coordinates = [(x, y) for y in range(self.__size) for x in range(self.__size) if (x, y) != first_shoot]
        for _ in range(difficulty.mines):
            point = choice(board_coordinates)
            x, y = point
            self.__squares[x][y] = MineSquare(on_click_mine)
            board_coordinates.remove(point)
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__squares[i][j] is None:
                    self.__init_square(i, j)
        self.on_click_square(first_shoot)

    def __init_square(self, i: int, j: int):
        adjacent_squares: list[Square] = self.__get_adjacent_squares((i, j))
        adjacent_mines_count = sum(1 for s in adjacent_squares if isinstance(s, MineSquare))
        if adjacent_mines_count != 0:
            self.__squares[i][j] = AdjacentMinesSquare(adjacent_mines_count)
        else:
            self.__squares[i][j] = EmptySquare(self.__get_adjacent_squares, i, j)

    def on_click_square(self, point: (int, int)):
        self.__squares[point[0]][point[1]].on_click()

    def __get_adjacent_squares(self, point: (int, int)) -> list[Square]:
        last = self.__size - 1
        i, j = point
        if i == j == 0:
            return [self.__squares[0][1], self.__squares[1][1], self.__squares[1][0]]
        elif i == 0 and j == last:
            return [self.__squares[0][last - 1], self.__squares[1][last - 1], self.__squares[1][last]]
        elif i == 0:
            return [
                self.__squares[0][j - 1], self.__squares[1][j - 1], self.__squares[1][j],
                self.__squares[1][j + 1], self.__squares[0][j + 1]
            ]
        elif i == last and j == 0:
            return [self.__squares[last - 1][0], self.__squares[last - 1][1], self.__squares[last][1]]
        elif j == 0:
            return [
                self.__squares[i - 1][0], self.__squares[i - 1][1], self.__squares[i + 1][0],
                self.__squares[i][1], self.__squares[i + 1][1]
            ]
        elif i == j == last:
            return [self.__squares[last - 1][last], self.__squares[last - 1][last - 1], self.__squares[last][last - 1]]
        elif j == last:
            return [
                self.__squares[i - 1][last], self.__squares[i - 1][last - 1], self.__squares[i][last - 1],
                self.__squares[i + 1][last - 1], self.__squares[i + 1][last]
            ]
        elif i == last:
            return [
                self.__squares[last][j - 1], self.__squares[last - 1][j - 1], self.__squares[last - 1][j],
                self.__squares[last - 1][j + 1], self.__squares[last][j + 1]
            ]
        else:
            return [
                self.__squares[i - 1][j - 1], self.__squares[i - 1][j], self.__squares[i - 1][j + 1],
                self.__squares[i][j - 1], self.__squares[i][j + 1], self.__squares[i + 1][j - 1],
                self.__squares[i + 1][j], self.__squares[i + 1][j + 1]
            ]

    def reveal_mines(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if isinstance(self.__squares[i][j], MineSquare):
                    self.__squares[i][j].on_click()

    def player_has_won(self) -> bool:
        import itertools
        all_squares = itertools.chain(*self.__squares)
        no_mines: list[Square] = list(filter(lambda square: not isinstance(square, MineSquare), all_squares))
        return all(map(lambda s: s.is_visible(), no_mines))

    def __str__(self):
        str_board = '\t'
        for n in range(self.__size):
            str_board += f'{n}\t'
        else:
            str_board += '\n'
        str_board += '\t'
        str_board += '_' * (len(str_board) * 2)
        str_board += '\n'
        for i in range(self.__size):
            str_board += f' {i}|\t'
            for j in range(self.__size):
                str_board += f'{self.__squares[i][j]}\t'
            str_board += '\n'
        return str_board
