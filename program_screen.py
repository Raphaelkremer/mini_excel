import tkinter as tk
from sheet_screen import SheetScreen
from toolbar_screen import ToolbarScreen
from welcome_window import WelcomeWindow


class ProgramScreen:
    """
    The class represents the main screen of the program using tkinter.
    The screen has the following attributes:
    - window: the window of the program
    - toolbar_screen: the toolbar screen of the program
    - sheet_screen: the sheet screen of the program
    """
    def __init__(self) -> None:
        """
        The constructor of the ProgramScreen class. It makes the main screen of the program using tkinter.
        generates the toolbar screen and the sheet screen of the program. and packs them.
        """
        welcome_window = WelcomeWindow()
        welcome_window.show()
        self.__window = tk.Tk()

        self.__toolbar_screen = ToolbarScreen(self.__window, self.__change_color_for_cell,
                                              self.__change_font_for_cell, self.__save_file_button_pressed,
                                              self.__load_file_button_pressed)
        self.__toolbar_screen.get_screen().pack(anchor=tk.W, fill=tk.X, expand=False)

        self.__sheet_screen = SheetScreen(self.__window)
        self.__sheet_screen.update_sheet()
        self.__sheet_screen.get_screen().pack()

        self.__window.title("Super Duper Excel")


    def __change_color_for_cell(self, color: str) -> None:
        self.__sheet_screen.report_cell_color_changed(color)

    def __change_font_for_cell(self, font: str) -> None:
        self.__sheet_screen.report_cell_font_changed(font)

    def __save_file_button_pressed(self, file_name: str) -> None:
        self.__sheet_screen.report_save_file_button_pressed(file_name)

    def __load_file_button_pressed(self, file_name: str) -> None:
        self.__sheet_screen.report_load_file_button_pressed(file_name)

    def get_window(self) -> tk.Tk:
        return self.__window

    def get_sheet_screen(self) -> SheetScreen:
        return self.__sheet_screen

    def show_screen(self) -> None:
        self.__window.mainloop()


