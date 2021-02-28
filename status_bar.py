"""
Written by Maciej Fec
email: maciejfec1996@gmail.com
"""

import tkinter as tk
import platform


class StatusBar:

    def __init__(self, window, text_area):

        self.__empty_label = tk.Label(window, relief="groove", padx=10, pady=2, borderwidth=0.5)

        self.__word_count = tk.StringVar()
        self.__word_count.set(f"Words: {len(list(text_area.get('1.0', 'end-1c')))}")
        self.__word_count_label = tk.Label(window, textvariable=self.__word_count, relief="groove", padx=10, pady=2, anchor=tk.W, borderwidth=0.5)

        self.__char_count = tk.StringVar()
        self.__char_count.set(f"Characters: {len(text_area.get('1.0', 'end-1c'))}")
        self.__char_count_label = tk.Label(window, textvariable=self.__char_count, relief="groove", padx=10, pady=2, anchor=tk.W, borderwidth=0.5)

        self.__os_label = tk.Label(window, text=f"Operating System: {platform.system()} {platform.release()} ({platform.architecture()[0]})", relief="groove", padx=10, pady=2, borderwidth=0.5)

    def display_status_bar(self):
        self.__empty_label.grid(row=2, column=0, sticky=tk.W + tk.E)
        self.__word_count_label.grid(row=2, column=1)
        self.__char_count_label.grid(row=2, column=2)
        self.__os_label.grid(row=2, column=4, columnspan=2)

    def update_word_and_character_count(self, event, text_area):
        """
        Updates the count of currently inputted words and characters within the text box
        """

        words = text_area.get('1.0', 'end-1c').split()
        self.__word_count.set(f"Words: {len(words)}")
        self.__char_count.set(f"Characters: {len(text_area.get('1.0', 'end-1c'))}")
