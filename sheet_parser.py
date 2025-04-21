import re
from typing import Tuple, List, Optional, Any

EXPRESSIONS_LIST = ["MATH", "SUM", "AVG", "MIN", "MAX"]
FUNC_LIST = ["MATH", "SUM", "AVG", "MIN", "MAX"]

PARSER_ERROR = "parser_error"
PARSER_FORMULA = "parser_formula"
PARSER_NOT_FORMULA = "parser_not_formula"
PARSER_FORMULA_ERROR_CALCULATING = "parser_formula_error_calculating"


class SheetParser:
    """This class is responsible for parsing the expression in the cells
    that the user presses enter on. It is also responsible for calculating
    the result of the expression and updating the cell with the result.
    """
    def __init__(self, sheet: List[List[Optional[Any]]]) -> None:
        """
        The constructor creates a sheet
        that will be called when the sheetscreen
        will construct the parser, and will be used to
        access the cells in the sheet.
        """
        self.__sheet = sheet

    def update_sheet(self, sheet: List[List[Optional[Any]]]) -> None:
        self.__sheet = sheet

    def parse_expression(self, expression: str): # type: ignore
        """
        The main function that parses the expression in the cell.
        It checks if the expression is a formula or not, according to the rules
        and if it is a formula
        it calculates the result of the formula and returns the result.
        """
        func = expression.split("(", 2)[0]
        if func not in FUNC_LIST:
            return PARSER_NOT_FORMULA, [], expression

        start = expression.find('(') + 1
        end = expression.find(')')
        if start == -1 or end == -1:
            return PARSER_ERROR, [], None
        inside_brackets = expression[start:end]
        tuples_cells_list = []

        if func == "MATH":
            cells_list = self.__split_and_keep(inside_brackets)
            if not cells_list:
                return PARSER_ERROR, [], None
            index_operators_list = self.__swap_alphabetical_cells_with_index_tuples(cells_list, True, True)
            if not index_operators_list:
                return PARSER_ERROR, [], None
            values_list = self.__swap_locations_with_values(index_operators_list, True)
            if not values_list:
                return PARSER_FORMULA_ERROR_CALCULATING, self.__get_only_tuples_from_list(index_operators_list), None
            math_result = self.__calculate_math_expression(values_list)
            if math_result == PARSER_FORMULA_ERROR_CALCULATING:
                return PARSER_FORMULA_ERROR_CALCULATING, self.__get_only_tuples_from_list(index_operators_list), None
            return PARSER_FORMULA, self.__get_only_tuples_from_list(index_operators_list), str(math_result)

        if ":" in inside_brackets:
            cells_list = inside_brackets.split(":")
            if len(cells_list) != 2:
                return PARSER_ERROR, [], None
            tuples_cells_list = self.__swap_alphabetical_cells_with_index_tuples(cells_list, False, False)
            if not tuples_cells_list:
                return PARSER_ERROR, [], None
            tuples_cells_list = self.__add_missing_tuples(tuples_cells_list)

        if "," in inside_brackets:
            cells_list = inside_brackets.split(",")
            tuples_cells_list = self.__swap_alphabetical_cells_with_index_tuples(cells_list, True, False)
            if not tuples_cells_list:
                return PARSER_ERROR, [], None

        values_list = self.__swap_locations_with_values(tuples_cells_list, False)
        if not values_list:
            return PARSER_FORMULA_ERROR_CALCULATING, self.__get_only_tuples_from_list(tuples_cells_list), None

        if func == "SUM":
            return PARSER_FORMULA, self.__get_only_tuples_from_list(tuples_cells_list), str(sum(values_list))
        if func == "AVG":
            return (PARSER_FORMULA, self.__get_only_tuples_from_list(tuples_cells_list),
                    str(sum(values_list) / len(values_list)))
        if func == "MIN":
            return PARSER_FORMULA, self.__get_only_tuples_from_list(tuples_cells_list), str(min(values_list))
        if func == "MAX":
            return PARSER_FORMULA, self.__get_only_tuples_from_list(tuples_cells_list), str(max(values_list))

    def __split_and_keep(self, s: str) -> List[str]:
        """
        Return a list of the words in the string, using sep as the delimiter string,
        but keeping the delimiters as well. For example, 'A+B-C' -> ['A', '+', 'B', '-', 'C']
        """
        delimiters = ['*', '+', '-', '/']
        pattern = '|'.join(map(re.escape, delimiters))
        split_arr = re.split(f'({pattern})', s)
        if split_arr[-1] == "":
            return []
        for i, item in enumerate(split_arr):
            if i % 2 == 1 and item not in delimiters:
                return []
        return split_arr

    # def __calculate_math_expression(self, expression: List[float]):  # type: ignore
    #     """
    #     Gets a list of numbers and operators and calculates the result of the expression.
    #     """
    #     if len(expression) % 2 == 0:
    #         return []
    #
    #     result = expression[0]
    #     for i in range(1, len(expression), 2):
    #         operator = expression[i]
    #         number = expression[i + 1]
    #         if operator == '+':  # type: ignore
    #             result += number
    #         elif operator == '-':  # type: ignore
    #             result -= number
    #         elif operator == '*':  # type: ignore
    #             result *= number
    #         elif operator == '/':  # type: ignore
    #             if number == 0:
    #                 return PARSER_FORMULA_ERROR_CALCULATING
    #             result /= number
    #         else:
    #             return []
    #     return result

    def __calculate_math_expression(self, expression: List[str]) -> float or str:  # type: ignore
        """
        Gets a list of numbers and operators and calculates the result of the expression.
        """
        try:
            expression_str = ''.join(str(e) for e in expression)
            result = eval(expression_str)
            return result
        except ZeroDivisionError:
            return PARSER_FORMULA_ERROR_CALCULATING
        except Exception as e:
            return str(e)

    def __get_only_tuples_from_list(self, lst: List[Any]) -> List[Tuple[int, int]] or List[Tuple[None]]:  # type: ignore
        return [item for item in lst if isinstance(item, tuple)]

    def __swap_alphabetical_cells_with_index_tuples(self, cells_list, allow_floats, is_math) -> List[Tuple[int, int]] or List[float] or None:  # type: ignore
        """
        This function is responsible for swapping the cells in the expression
        with their indexes in the sheet. It also checks if the cells are valid.
        """
        alpha_cells_list = []
        for i, cell in enumerate(cells_list):
            if (i % 2 == 1) and is_math:
                alpha_cells_list.append(cell)
                continue
            if allow_floats and self.__check_if_string_is_float(cell):
                alpha_cells_list.append(float(cell))
                continue
            if len(cell) > 3 or len(cell) < 2:
                return []
            letter = cell[0]
            if not letter.isupper():
                return []
            letter_num = ord(letter) - ord('A') + 1
            for c in cell[1:]:
                if not c.isdigit():
                    return []
            number = int(cell[1:])
            alpha_cells_list.append((number, letter_num))
        return alpha_cells_list

    def __check_if_string_is_float(self, string: str) -> bool:
        try:
            float(string)
            return True
        except ValueError:
            return False

    def __add_missing_tuples(self, location: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        cell1 = location[0]
        cell2 = location[1]

        result = []
        if cell1[0] == cell2[0]:
            for col in range(cell1[1], cell2[1] + 1):
                result.append((cell1[0], col))

        elif cell1[1] == cell2[1]:
            for row in range(cell1[0], cell2[0] + 1):
                result.append((row, cell1[1]))
        else:
            return []
        return result

    def __swap_locations_with_values(self, locations, is_math) -> List[float] or List[str] or None: # type: ignore
        """
        This func is responsible for swapping the locations in the expression
        with their values in the sheet. It also checks if the locations are valid.
        """
        values = []
        for i, loc in enumerate(locations):
            if (i % 2 == 1) and is_math:
                values.append(loc)
                continue
            if type(loc) is float:
                values.append(loc)
                continue
            if loc[0] >= len(self.__sheet) or loc[1] >= len(self.__sheet[0]):
                return []
            if loc[0] <= 0 or loc[1] <= 0:
                return []
            x = self.__sheet[loc[0]][loc[1]].get_formula_result()
            try:
                y = float(x)
                values.append(y)
            except ValueError:
                return []
        return values
