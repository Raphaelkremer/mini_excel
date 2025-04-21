import sys

from sheet import Sheet
from program_screen import ProgramScreen


class Program:
    """
    The main class of the program.
    """

    def __init__(self) -> None:
        self.__program_screen = ProgramScreen()

    def start(self) -> None:
        self.__program_screen.show_screen()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        program = Program()
        program.start()
    elif sys.argv[1] == "--help":
        print(
              "To SUM, MIN, AVG and MAX use the following syntax:\n"
              "for an operation on a range of cells(can be executed in rows and in columns)\n"
              ": SUM(A1:A5), MIN(A1:J1), AVG(A1:A5), MAX(A1:J1)\n"
              "for an operation on a list of cells:\n"
              " SUM(A1, A2, A3), MIN(A1, C7, J8), AVG(D4, A2, F6), MAX(B7, A2, A3))\n"
              "To make mathematical calculations(between cells and numbers) function use the following syntax:\n"
              "MATH(1+2*3/4-5) or MATH(1+A2*3/4-5, 1+B7*3/4-C9)\n"
              "do not use spaces between the cells, the operator, parentheses and the numbers\n")


