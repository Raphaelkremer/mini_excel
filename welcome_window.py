from tkinter import ttk, font, Button, PhotoImage, Label
from ttkthemes import ThemedTk  # type: ignore


class WelcomeWindow:
    """
    This class represents the welcome window of the program.
    The welcome window has the following attributes:
    - window: the window of the welcome window
    - icon: the icon of the welcome window
    """
    def __init__(self) -> None:
        """
        The constructor of the WelcomeWindow class. It makes the welcome window of the program using tkinter.
        """
        self.__window = ThemedTk(theme="yaru")
        self.__window.geometry("1200x600")
        self.__window.configure(bg='alice blue')

        self.__window.withdraw()
        self.__icon = PhotoImage(file="icons8-excel-50.png")

        icon_label = Label(self.__window, image=self.__icon)
        icon_label.pack()
        label_font = font.Font(size=14, weight="bold")
        label = ttk.Label(self.__window, text="Welcome to Super Duper Excel!", font=label_font, foreground="green4")
        label.pack(padx=50, pady=50)  # Add some padding around the label
        close_button = Button(self.__window, text="Press to start", command=self.__window.destroy)
        close_button.pack()

        self.__window.deiconify()

    def show(self) -> None:
        self.__window.mainloop()
