"""
Written by Maciej Fec
email: maciejfec1996@gmail.com
"""

import tkinter as tk
import sqlite3


class TextBox:

    def __init__(self, window):

        # Opens up the data base with the preferences
        self.__conn = sqlite3.connect("text_editor_preferences.db")
        self.__c = self.__conn.cursor()

        # Selects and fetches the relevant preferences from the database
        self.__c.execute("SELECT font, font_style, font_size FROM preferences")
        self.__preferences = self.__c.fetchall()

        if self.__preferences[0][1] == "regular":
            self.__text_area = tk.Text(window, wrap=tk.NONE, font=(self.__preferences[0][0], self.__preferences[0][2]), padx=3, undo=True, relief=tk.FLAT)
        else:
            self.__text_area = tk.Text(window, wrap=tk.NONE, font=(self.__preferences[0][0], self.__preferences[0][2], self.__preferences[0][1]), padx=3, undo=True, relief=tk.FLAT)

        # Focuses on the text area
        self.__text_area.focus()

        # Creates a vertical and horizontal scrollbar
        self.__vertical_scroll_bar = tk.Scrollbar(window)
        self.__horizontal_scroll_bar = tk.Scrollbar(window, orient="horizontal")

        # Closes the data base
        self.__conn.close()

    def display_text_box(self):
        """
        Places the text box in the GUI window
        """

        self.__text_area.grid(row=0, column=0, sticky=tk.N + tk.E + tk.W + tk.S, columnspan=5)

    def display_scroll_bars(self):
        """
        Displays a vertical scrollbar and horizontal scrollbar in the GUI window
        """

        self.__vertical_scroll_bar.grid(row=0, column=5, sticky=tk.N + tk.W + tk.S)
        self.__vertical_scroll_bar.config(command=self.__text_area.yview)

        self.__horizontal_scroll_bar.grid(row=1, column=0, sticky=tk.N + tk.W + tk.E, columnspan=5)
        self.__horizontal_scroll_bar.config(command=self.__text_area.xview)

        self.__text_area.config(xscrollcommand=self.__horizontal_scroll_bar.set, yscrollcommand=self.__vertical_scroll_bar.set)

    def get_text_area(self):
        """
        Returns the text area to be used outside of the class
        """

        return self.__text_area

    def get_horizontal_scroll_bar(self):

        return self.__horizontal_scroll_bar
