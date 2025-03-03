from abc import ABC, abstractmethod


class Square(ABC):

    def __init__(self):
        self.__is_visible = False

    def on_click(self):
        self.__is_visible = True

    @abstractmethod
    def _draw(self) -> str:
        pass

    def is_visible(self) -> bool:
        return self.__is_visible

    def __str__(self):
        return self._draw() if self.__is_visible else '-'