from Square import Square

class AdjacentMinesSquare(Square):

    def __init__(self, adjacent_mines_count: int):
        super().__init__()
        self.__adjacent_mines_count = adjacent_mines_count

    def on_click(self):
        super().on_click()

    def _draw(self) -> str:
        return str(self.__adjacent_mines_count)

