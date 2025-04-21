import tkinter as tk
from typing import Callable, Any

FORMULA_BOX_TITLE = "Formula Box:"


class FormulaBox:
    """
    A class that represents a text box for entering formulas.
    """
    def __init__(self, parent: tk.Tk, on_text_change: Callable[[str], None], on_enter_pressed: Callable[[], None]):
        self.__frame = tk.Frame(parent)
        self.__on_text_change = on_text_change
        self.__text_var = tk.StringVar(parent, value="")
        self.__text_box = tk.Entry(self.__frame, textvariable=self.__text_var, width=50)
        self.__text_box.bind('<Return>', lambda event: on_enter_pressed())
        self.trace_id = self.__text_var.trace_add("write", lambda a, b, c: on_text_change(self.__text_var.get()))
        self.__description_label = tk.Label(self.__frame, text=FORMULA_BOX_TITLE)

    def get_text(self) -> str:
        return self.__text_var.get()

    def set_text(self, text: str) -> None:
        self.__text_var.set(text)

    def pack(self, **kwargs: Any) -> None:
        self.__text_box.pack(side=tk.RIGHT)
        self.__description_label.pack(side=tk.LEFT)
        self.__frame.pack(**kwargs)
