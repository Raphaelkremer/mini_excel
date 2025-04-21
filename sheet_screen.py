
import tkinter as tk
from typing import Tuple, Dict

from sheet import Sheet
from tkinter import font
from tkinter import messagebox
from formula_box import FormulaBox

DEFAULT_FONT_SIZE = 10


class SheetScreen:
    """
    The class represents the screen of the sheet using tkinter.
    The screen has the following attributes:
    - sheet: a Sheet object
    - window: the window of the screen
    - formula_box: a FormulaBox object
    - live_updaters: a dictionary that stores the StringVars of the Entries
    - entries: a dictionary that stores the Entries
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        The constructor of the SheetScreen class.
        it makes the screen of the sheet using tkinter.
        """

        self.__formula_box = FormulaBox(
            root,
            on_text_change=self.__on_formula_box_text_change,
            on_enter_pressed=self.__on_cell_enter_pressed
        )
        self.__formula_box.pack(side=tk.TOP)
        self.__sheet = Sheet(
            name="sheet1",
            on_cell_text_changed=self.__change_cell_text,
            on_cell_color_changed=self.__change_cell_color,
            on_cell_font_changed=self.__change_cell_font,
            on_error=self.__show_error,
            update_formula_box_text_written_to_cell=self.__update_formula_box_with_text
        )
        self.__window = tk.Frame(root, width=300, height=300, background="alice blue")
        root.configure(background='alice blue')
        self.__live_updaters: Dict[Tuple[int, int], tk.StringVar] = {}
        self.__entries: Dict[Tuple[int, int], tk.Entry] = {}

    def get_screen(self) -> tk.Frame:
        return self.__window

    def report_cell_color_changed(self, color: str) -> None:
        self.__sheet.update_cell_color(color)

    def report_cell_font_changed(self, font: str) -> None:
        self.__sheet.update_cell_font(font)

    def report_save_file_button_pressed(self, file_name: str) -> None:
        self.__sheet.save_to_file(file_name)
        self.update_sheet()

    def report_load_file_button_pressed(self, file_name: str) -> None:
        self.__sheet.load_from_file(file_name)
        self.update_sheet()

    def __change_cell_color(self, coord: Tuple[int, int], color: str) -> None:
        self.__entries[coord].configure(background=color)

    def __change_cell_font(self, coord: Tuple[int, int], new_font: str) -> None:
        tk_font = font.Font(family=new_font, size=DEFAULT_FONT_SIZE, weight="bold")
        self.__entries[coord].configure(font=tk_font)

    def __show_error(self, error_msg: str) -> None:
        messagebox.showerror("ERROR!", error_msg)

    def update_sheet(self) -> None:
        """
        The main function that constantly
        updates the sheet on the screen.
        it creates the sheet on the screen and
        creates the string vars for each cell,
        so they will be updated, and creates the entries
        that will be updated when the user types in them.
        it also binds each entry to the functions that
        will be called when the user clicks, press enter and tab
        in them.
        """
        cur_sheet = self.__sheet.get_sheet()
        for i in range(len(cur_sheet)):
            for j in range(len(cur_sheet[0])):
                if i == 0 and j == 0:
                    label = tk.Label(self.__window, bg="green4", fg="white", text="*", width=10)
                    label.grid(row=i, column=j, padx=5, pady=5)
                elif i == 0:
                    index_letter = self.__get_column_letter_from_index(j)
                    label = tk.Label(self.__window, bg="green4", fg="white", text=index_letter, width=10)
                    label.grid(row=i, column=j, padx=5, pady=5)
                elif j == 0:
                    label = tk.Label(self.__window, bg="green4", fg="white", text=i, width=10)
                    label.grid(row=i, column=j, padx=5, pady=5)
                else:
                    live_updater = tk.StringVar()
                    self.__live_updaters[(i, j)] = live_updater
                    cell_font = font.Font(family=cur_sheet[i][j].get_font(), size=DEFAULT_FONT_SIZE)
                    entry = tk.Entry(
                        self.__window,
                        textvariable=live_updater,
                        width=10,
                        font=cell_font,
                        background=cur_sheet[i][j].get_color()
                    )
                    entry.insert(0, cur_sheet[i][j].get_formula_result())
                    self.__entries[(i, j)] = entry
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    live_updater.trace_add(
                        mode="write",
                        callback=lambda name, index, mode, row=i, col=j: self.__on_text_change(row, col)  # type: ignore
                    )
                    entry.bind('<Button-1>', lambda event, coord=(i, j): self.__on_cell_clicked(event, coord))  # type: ignore

                    entry.bind('<Return>', lambda event, coord=(i, j): self.__on_cell_enter_pressed())  # type: ignore
                    entry.bind('<Tab>', lambda event, coord=(i, j): self.__on_cell_tab_pressed(event, coord))  # type: ignore


    def __get_column_letter_from_index(self, index: int) -> str:
        column_label = ""
        while index >= 0:
            column_label = chr(index % 26 + 64) + column_label
            index = index // 26 - 1
        return column_label

    def __on_cell_tab_pressed(self, event, coord: Tuple[int, int]) -> None:  # type: ignore
        i, j = coord
        num_rows = len(self.__sheet.get_sheet())
        num_columns = len(self.__sheet.get_sheet()[0])
        if event.state & 0x1:
            if j - 1 >= 0:
                next_coord = (i, j - 1)
            elif i - 1 >= 0:
                next_coord = (i - 1, num_columns - 1)
            else:
                next_coord = (num_rows - 1, num_columns - 1)
        else:
            if j + 1 < num_columns:
                next_coord = (i, j + 1)
            elif i + 1 < num_rows:
                next_coord = (i + 1, 0)
            else:
                next_coord = (0, 0)
        self.__sheet.choose_cell(*next_coord)
        chosen_cell_text = self.__sheet.get_chosen_cell_from_sheet().get_text()
        self.__formula_box.set_text(chosen_cell_text)

    def __on_cell_enter_pressed(self) -> None:
        """
        A callback function that is called when the enter key is pressed.
        will make the sheet update a formula if there's one in the chosen cell.
        """
        self.__sheet.enter_pressed()

    def __on_cell_clicked(self, event, coord: Tuple[int, int]) -> None:  # type: ignore
        """
        A callback function that is called when a cell is clicked.
        """
        self.__sheet.choose_cell(coord[0], coord[1])
        chosen_cell_text = self.__sheet.get_chosen_cell_from_sheet().get_text()
        self.__formula_box.set_text(chosen_cell_text)

    def __on_formula_box_text_change(self, text: str) -> None:
        self.__sheet.write_to_chosen_cell(text)

    def __on_text_change(self, row: int, col: int, *args) -> None:  # type: ignore
        """
        A callback function that is called when the text in a cell is changed.
        It updates the cell in the sheet with the new text.
        by using the live updaters it makes it possible to update the cell
        even when the user types in it.
        """
        live_updater = self.__live_updaters[(row, col)]
        self.__sheet.write_to_chosen_cell(live_updater.get())

    def __change_cell_text(self, coord: Tuple[int, int], text: str) -> None:
        x = coord[0]
        y = coord[1]
        self.__live_updaters[(x, y)].set(text)

    def __update_formula_box_with_text(self, text: str) -> None:
        self.__formula_box.set_text(text)

