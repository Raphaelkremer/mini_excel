import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable


class ToolbarScreen:
    """
    This class represents the toolbar screen of the program.
    The toolbar screen has the following attributes:
    - root: the root window
    - window: the toolbar screen window
    - color_options_widget: the color options widget
    - font_options_widget: the font options widget
    - color_icon_button: the color icon button
    - font_icon_button: the font icon button
    - save_file_entry: the save file button
    - load_file_entry: the load file button
    and a few callback functions that are used as callbacks to the screen.
    """

    def __init__(self,
                 root: tk.Tk,
                 on_cell_color_chosen: Callable[[str], None],
                 on_cell_font_chosen: Callable[[str], None],
                 on_save_file_button_pressed: Callable[[str], None],
                 on_load_file_button_pressed: Callable[[str], None]) -> None:
        """
        the constructor of the ToolbarScreen class.
        it makes the toolbar screen of the program using tkinter
        and sets the callbacks to the screen.
        """
        self.__on_cell_color_chosen = on_cell_color_chosen
        self.__on_cell_font_chosen = on_cell_font_chosen
        self.__on_save_file_button_pressed = on_save_file_button_pressed
        self.__on_load_file_button_pressed = on_load_file_button_pressed

        self.__root = root
        self.__window = tk.Frame(root, width=800, height=50, bg="LightCyan2")

        self.__load_file_entry = self.__create_load_file_entry()
        self.__load_file_button = self.__create_load_file_button()

        self.__save_file_entry = self.__create_save_file_entry()
        self.__save_file_button = self.__create_save_file_button()

        self.__color_options_widget = self.__create_color_options()
        self.__color_icon_button = self.__create_color_icon_button()

        self.__font_options_widget = self.__create_font_options()
        self.__font_icon_button = self.__create_font_icon_button()

    def __on_color_option_selected(self, event: tk.Event) -> None:  # type: ignore
        self.__on_cell_color_chosen(self.__color_options_widget.get())

    def __on_font_option_selected(self, event: tk.Event) -> None:  # type: ignore
        self.__on_cell_font_chosen(self.__font_options_widget.get())

    def __create_color_options(self) -> ttk.Combobox:
        """
        Makes it possible to change
        the color of the cells in the sheet and using callbacks
        to the sheet it also updates the sheet (logic)
        """
        color_options_widget = ttk.Combobox(self.__window, values=["red", "blue", "green", "white", "yellow", "pink",
                                                                   "purple", "orange", "black", "grey", "brown", "cyan",
                                                                   "magenta", ])
        color_options_widget.set("Choose Color")
        color_options_widget.pack(side=tk.RIGHT)
        color_options_widget.bind("<<ComboboxSelected>>", self.__on_color_option_selected)
        return color_options_widget

    def __create_color_icon_button(self) -> tk.Button:
        color_icon = tk.PhotoImage(file='color-icons-12533.png')
        color_icon = color_icon.subsample(30, 30)
        color_icon_button = tk.Button(self.__window, image=color_icon, borderwidth=0)
        color_icon_button.config(relief=tk.FLAT, bg="LightCyan2")
        color_icon_button.image = color_icon  # type: ignore
        color_icon_button.pack(side=tk.RIGHT)
        return color_icon_button

    def __create_font_options(self) -> ttk.Combobox:
        """
        Makes it possible to change the font of the cells
        and using callbacks to the sheet it also updates the sheet (logic)
        """
        font_options_widget = ttk.Combobox(self.__window, values=["Helvetica", "Times", "Palatino Linotype",
                                                                  "Baskerville Old Face"])
        font_options_widget.set("Choose Font")
        font_options_widget.pack(side=tk.RIGHT)
        font_options_widget.bind("<<ComboboxSelected>>", self.__on_font_option_selected)
        return font_options_widget

    def __create_font_icon_button(self) -> tk.Button:
        font_icon = tk.PhotoImage(file='text-tool.png')
        font_icon = font_icon.subsample(30, 30)
        font_icon_button = tk.Button(self.__window, image=font_icon, borderwidth=0)
        font_icon_button.config(state=tk.DISABLED)
        font_icon_button.image = font_icon  # type: ignore
        font_icon_button.pack(side=tk.RIGHT)
        return font_icon_button

    def __save_file(self) -> None:
        """
        The function that is called when the user presses the save file button.
        it opens a dialog that lets the user choose where to save the file.
        """
        file_path = filedialog.asksaveasfilename()
        self.__on_save_file_button_pressed(file_path)

    def __create_save_file_button(self) -> tk.Button:
        """
        The function that creates the save file button and
        sets the callback to the function that saves the file.
        """
        save_file_button = tk.Button(self.__window, text="Save File", command=self.__save_file)
        save_file_button.pack(side=tk.LEFT)
        return save_file_button

    def __create_save_file_entry(self) -> tk.Entry:
        load_file_entry = tk.Entry(self.__window)
        load_file_entry.pack(side=tk.LEFT)
        return load_file_entry

    def __open_file(self) -> None:
        """
        The function that is called when the user presses the load file button.
        it opens a dialog that lets the user choose where to load the file from.
        """
        file_path = filedialog.askopenfilename()
        self.__on_load_file_button_pressed(file_path)

    def __create_load_file_button(self) -> tk.Button:
        load_file_button = tk.Button(self.__window, text="Load File", command=self.__open_file)

        load_file_button.pack(side=tk.LEFT)
        return load_file_button

    def __create_load_file_entry(self) -> tk.Entry:
        load_file_entry = tk.Entry(self.__window)
        load_file_entry.pack(side=tk.LEFT)
        return load_file_entry

    def get_screen(self) -> tk.Frame:
        return self.__window
