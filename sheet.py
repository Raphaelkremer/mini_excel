
from typing import List, Tuple, Callable
from cell import Cell
from cell import CELL_ERROR_TEXT
from sheet_parser import SheetParser
from sheet_parser import PARSER_ERROR, PARSER_FORMULA, PARSER_NOT_FORMULA,PARSER_FORMULA_ERROR_CALCULATING

SHEET_SPACER = "@"
BAD_FORMULA_ERROR_MSG = "Please enter a valid formula!"
ERROR_LOADING_FILE_MSG = "Error loading file! Please try again or choose a different one..."
ERROR_SAVING_FILE_MSG = "Error saving file! Please try again later..."


class Sheet:
    """The class represents a sheet of cells.
    The sheet is a 2D array of cells and has the following attributes:
    - name: name of the sheet
    - sheet: a 2D array of cells
    - parser: an instance of SheetParser
    - chosen_cell: the cell that is currently chosen
    """

    def __init__(self,
                 name: str,
                 on_cell_text_changed: Callable[[Tuple[int, int], str], None],
                 on_cell_color_changed: Callable[[Tuple[int, int], str], None],
                 on_cell_font_changed: Callable[[Tuple[int, int], str], None],
                 on_error: Callable[[str], None],
                 update_formula_box_text_written_to_cell: Callable[[str], None]) -> None:

        """
        :param name: name of the sheet
        the following parameters are functions that are used as callbacks to the screen:
        :param on_cell_text_changed: function to call when cell text is changed
        :param on_cell_color_changed: function to call when cell color is changed
        :param on_cell_font_changed: function to call when cell font is changed
        :param on_error: function to call when error occurs
        :param update_formula_box_text_written_to_cell: function to call when formula box text is written to cell

        """
        self.__on_cell_text_changed = on_cell_text_changed
        self.__name = name

        self.__sheet: List[List[Cell]] = [[Cell() for i in range(15)] for j in range(20)]
        self.__parser = SheetParser(self.__sheet)  # type: ignore
        self.__chosen_cell = (1, 1)
        self.__on_cell_color_changed = on_cell_color_changed
        self.__on_cell_font_changed = on_cell_font_changed
        self.__on_error = on_error
        self.__update_formula_box_text_written_to_cell = update_formula_box_text_written_to_cell

    def serialize(self) -> str:
        """
        Serialize the sheet to a string that
        can be written to a file.
        """
        st = str(len(self.__sheet)) + SHEET_SPACER + str(len(self.__sheet[0])) + "\n"
        for i, row in enumerate(self.__sheet):
            for j, cell in enumerate(row):
                st += cell.serialize()
                if j != len(self.__sheet[0]) - 1:
                    st += "\t"
            if i != len(self.__sheet) - 1:
                st += "\n"
        return st

    def deserialize(self, serialized_string: str) -> None:
        """
        Deserialize the sheet from a string that was
        read from a file.
        """
        rows_strings = serialized_string.split("\n")
        row_num, col_num = rows_strings[0].split(SHEET_SPACER)
        serialized_sheet_array = list(map(lambda x: x.split("\t"), rows_strings[1:]))
        self.__sheet = [[Cell(serialized_sheet_array[i][j]) for j in range(int(col_num))] for i in range(int(row_num))]

    def get_sheet(self) -> List[List[Cell]]:
        return self.__sheet.copy()

    def get_length(self) -> int:
        return len(self.__sheet)

    def get_width(self) -> int:
        return len(self.__sheet[0])

    def choose_cell(self, row: int, col: int) -> None:
        self.__chosen_cell = (row, col)

    def enter_pressed(self) -> None:
        """
        Called when the enter key is pressed.
        send the text in the chosen cell to the parser
        and update the cell with the result.
        """
        result, dependent_cell_list, answer =\
            self.__parser.parse_expression(self.get_chosen_cell_from_sheet().get_text())
        if result == PARSER_FORMULA:
            self.__add_dependent_cell_to_relevant_cells(dependent_cell_list)
            self.__update_formula_result_in_chosen_cell_in_sheet(answer)
            self.__update_screen_formula_applied()
        if result == PARSER_FORMULA_ERROR_CALCULATING:
            self.__add_dependent_cell_to_relevant_cells(dependent_cell_list)
            self.__on_cell_text_changed(self.__chosen_cell, CELL_ERROR_TEXT)
        if result == PARSER_ERROR:
            self.__on_error(BAD_FORMULA_ERROR_MSG)
        if result == PARSER_NOT_FORMULA:
            self.__on_cell_text_changed(self.__chosen_cell, answer)

    def __add_dependent_cell_to_relevant_cells(self, dependent_cell_list: List[Tuple[int, int]]) -> None:
        """
        Adding the dependent cell to the relevant cells in the sheet.
        """
        for cell in dependent_cell_list:
            self.get_sheet()[cell[0]][cell[1]].add_dependent_formula_cell(self.__chosen_cell)

    def __update_formula_result_in_chosen_cell_in_sheet(self, answer: str) -> None:
        self.get_chosen_cell_from_sheet().update_formula_result(answer)

    def __update_screen_formula_applied(self) -> None:
        self.__on_cell_text_changed(self.__chosen_cell, self.get_chosen_cell_from_sheet().get_formula_result())

    def update_cell_color(self, color: str) -> None:
        self.__sheet[self.__chosen_cell[0]][self.__chosen_cell[1]].change_color(color)
        self.__on_cell_color_changed(self.__chosen_cell, color)

    def update_cell_font(self, font: str) -> None:
        self.__sheet[self.__chosen_cell[0]][self.__chosen_cell[1]].change_font(font)
        self.__on_cell_font_changed(self.__chosen_cell, font)

    def save_to_file(self, file_name: str) -> None:
        """
        this function saves the sheet to a file with the given name.
        """
        data = self.serialize()
        filename = file_name + ".txt"
        try:
            with open(filename, 'w') as file:
                file.write(data)
        except:
            self.__on_error(ERROR_SAVING_FILE_MSG)

    def load_from_file(self, file_name: str) -> None:
        """
        this function loads the sheet from a file with the given name.
        """
        filename = file_name  # + ".txt"
        try:
            with open(filename, 'r') as file:
                data_str = file.read()
                self.deserialize(data_str)
                self.__parser.update_sheet(self.__sheet)  # type: ignore
        except:
            self.__on_error(ERROR_LOADING_FILE_MSG)

    def write_to_chosen_cell(self, text: str) -> None:
        self.__write_text_to_cell(text)
        self.__update_dependent_cells()

    def __update_dependent_cells(self) -> None:
        """
        updating the dependent cells of each cell that
        a change was made in them.
        """
        cur_cell_loc = self.get_chosen_cell_loc()
        cur_cell = self.get_chosen_cell_from_sheet()
        cells_to_update = cur_cell.get_dependent_formula_cells()
        for cell in cells_to_update:
            self.__chosen_cell = cell
            self.enter_pressed()
        self.__chosen_cell = cur_cell_loc

    def get_chosen_cell_from_sheet(self) -> Cell:
        x = self.__sheet[self.__chosen_cell[0]][self.__chosen_cell[1]]
        return self.__sheet[self.__chosen_cell[0]][self.__chosen_cell[1]]

    def __write_text_to_cell(self, text: str) -> None:
        did_cell_write_new_text = self.get_chosen_cell_from_sheet().write_text(text)
        if did_cell_write_new_text:
            self.__update_formula_box_text_written_to_cell(text)
            self.__on_cell_text_changed(self.__chosen_cell, text)

    def get_chosen_cell_loc(self) -> Tuple[int, int]:
        return self.__chosen_cell



