import ast
from typing import Optional, Tuple, List

SPACER = "%%%"
SET_SPACER = "$$$"
CELL_ERROR_TEXT = "ERROR!"

class Cell:
    """
    The Cell class represents a cell in the sheet.
    The cell has the following attributes:
    - text: the text of the cell
    - formula_result: the result of the formula in the cell if there is a formula, otherwise the text
    - color: the color of the cell
    - font: the font of the cell
    - dependent_formula_cells: a list of the cells that depend on this cell
    """

    def __init__(self, serialized_string: Optional[str]=None) -> None:
        """
        The constructor of the Cell class.
        It initializes the cell with the given text, color, and font.
        it also deserializes the cell if a serialized string is given.
        (for loading)
        """
        self.__text = ""
        self.__formula_result = self.__text
        self.__color = "white"
        self.__font = "Helvetica"
        self.__dependent_formula_cells: List[Tuple[int, int]] = []

        if serialized_string is not None:
            self.deserialize(serialized_string)

    def serialize(self) -> str:
        """
        Makes a string that represents the cell.
        The string is used to save the cell to a file.
        """
        st = ""
        st += self.__text + SPACER
        st += self.__formula_result + SPACER
        st += self.__color + SPACER
        st += self.__font + SPACER
        for cel in self.__dependent_formula_cells:
            st += str(cel) + SET_SPACER
        return st

    def deserialize(self, serialized_string: str) -> None:
        """
        Deserialize the cell from a string.
        The string is used to load the cell from a file.
        """
        param_list = serialized_string.split(SPACER)
        param_list[-1] = param_list[-1].split(SET_SPACER)[:-1]#  type: ignore
        self.__text = param_list[0]
        self.__formula_result = param_list[1]
        self.__color = param_list[2]
        self.__font = param_list[3]
        self.__dependent_formula_cells = []
        temp = list(param_list[4])
        for index in temp:
            self.__dependent_formula_cells.append(ast.literal_eval(index))

    def write_text(self, text: str) -> bool:
        if text == self.__formula_result:
            return False
        if text == CELL_ERROR_TEXT:
            self.__formula_result = text
            return False
        self.__text = text
        self.__formula_result = text
        return True

    def change_color(self, color: str) -> None:
        self.__color = color

    def change_font(self, font: str) -> None:
        self.__font = font

    def get_font(self) -> str:
        return self.__font

    def get_text(self) -> str:
        return self.__text

    def get_color(self) -> str:
        return self.__color

    def get_formula_result(self) -> str:
        return self.__formula_result

    def get_dependent_formula_cells(self) -> List[Tuple[int, int]]:
        return self.__dependent_formula_cells

    def add_dependent_formula_cell(self, formula_cell: Tuple[int, int]) -> None:
        if formula_cell not in self.__dependent_formula_cells:
            self.__dependent_formula_cells.append(formula_cell)

    def update_formula_result(self, formula_result: str) -> None:
        self.__formula_result = formula_result

    def __str__(self) -> str:
        return ("text: " + self.__text + ", formula result: " + self.__formula_result + ", color: " + str(self.__color) +
                ", font: " + str(self.__font) + ", dependent cells: " + str(self.__dependent_formula_cells))

    def __repr__(self) -> str:
        return self.__str__()


