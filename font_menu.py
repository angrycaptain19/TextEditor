"""
Written by Maciej Fec
email: maciejfec1996@gmail.com
"""

import tkinter as tk
from tkinter import font
from tkinter import messagebox
import sqlite3


class Fonts:

    def __init__(self, window, text_area):
        # A list of all the available fonts
        self.__available_fonts = [i.title() for i in font.families()]
        self.__available_fonts.sort()

        # A list of the available font styles
        self.__available_font_styles = ["Regular", "Italic", "Bold", "Bold Italic"]

        # A list of default font sizes
        self.__font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]

        # Fonts GUI
        self.__font_label = tk.Label(window, text="Font:", padx=8)
        self.__font_entry = tk.Entry(window, width=28)
        self.__list_of_fonts = tk.Listbox(window, width=28, height=7, activestyle=tk.NONE, exportselection=0)

        # Font Styles GUI
        self.__font_style_label = tk.Label(window, text="Font style:", padx=8)
        self.__font_style_entry = tk.Entry(window, width=20)
        self.__list_of_font_styles = tk.Listbox(window, width=20, height=7, activestyle=tk.NONE, exportselection=0)

        # Font Sizes GUI
        self.__font_size_label = tk.Label(master=window, text="Size", padx=4)
        self.__font_size_entry = tk.Entry(window, width=12)
        self.__list_of_font_sizes = tk.Listbox(window, width=12, height=7, activestyle=tk.NONE, exportselection=0)

        self.__ok_button = tk.Button(window, text="OK", width=8, command=lambda: self.__apply_changes(text_area, window))
        self.__cancel_button = tk.Button(window, text="Cancel", width=8, command=lambda: window.destroy())

        # Last used preferences
        self.__conn = sqlite3.connect("text_editor_preferences.db")
        self.__c = self.__conn.cursor()
        self.__c.execute("SELECT font, font_style, font_size FROM preferences")
        self.__preferences = self.__c.fetchall()

        # For switching font style option when program is running
        self.__current_font = self.__preferences[0][0]
        self.__current_font_style = self.__preferences[0][1]
        self.__current_font_size = self.__preferences[0][2]

        # A label which displays a sample of the elected font
        self.__sample_text_frame = tk.LabelFrame(window, text="Sample", width=402, height=225)
        self.__sample_text_frame.pack_propagate(False)
        if self.__preferences[0][1] == "regular":
            self.__sample_text = tk.Label(self.__sample_text_frame, text="AaBbYyZz", font=(self.__preferences[0][0], 50), pady=180)
        else:
            self.__sample_text = tk.Label(self.__sample_text_frame, text="AaBbYyZz", font=(self.__preferences[0][0], 50, self.__preferences[0][1]))

        # Commit changes and close database
        self.__conn.commit()
        self.__conn.close()

    def display_font_options(self):
        """
        Displays all available fonts and font options within the Font window
        """

        self.__font_label.grid(row=0, column=0, sticky=tk.W)
        self.__font_entry.grid(row=1, column=0, padx=(10, 5), sticky=tk.W)
        self.__list_of_fonts.grid(row=2, column=0, padx=(10, 5), sticky=tk.N)

        # Loads the available fonts into the self.__list_of_fonts listbox
        for i in self.__available_fonts:
            self.__list_of_fonts.insert(tk.END, i)

        self.__font_style_label.grid(row=0, column=1, sticky=tk.W)
        self.__font_style_entry.grid(row=1, column=1, padx=10, sticky=tk.W)
        self.__list_of_font_styles.grid(row=2, column=1, padx=10, sticky=tk.N)

        # Loads the available font styles into the self.__list_of_font_styles listbox
        for i in self.__available_font_styles:
            self.__list_of_font_styles.insert(tk.END, i)

        self.__font_size_label.grid(row=0, column=2, sticky=tk.W)
        self.__font_size_entry.grid(row=1, column=2, padx=(5, 10), sticky=tk.W)
        self.__list_of_font_sizes.grid(row=2, column=2, padx=(5, 10), sticky=tk.N)

        # Loads the font sizes into the self.__list_of_font_sizes listbox
        for i in self.__font_sizes:
            self.__list_of_font_sizes.insert(tk.END, i)

        # Inserts the correct, font, font style and font size into the entry widget
        self.__font_entry.insert(tk.END, self.__current_font)
        if self.__current_font_style == "regular":
            self.__font_style_entry.insert(tk.END, "Regular")
        else:
            self.__font_style_entry.insert(tk.END, self.__current_font_style.title())
        self.__font_size_entry.insert(tk.END, self.__current_font_size)

        # Highlights the correct font, font style and font size in the list boxes
        self.__list_of_fonts.see(self.__list_of_fonts.get(0, tk.END).index(self.__current_font))
        self.__list_of_fonts.select_set(self.__list_of_fonts.get(0, tk.END).index(self.__current_font))
        if self.__current_font_style == "":
            self.__list_of_font_styles.select_set(self.__list_of_font_styles.get(0, tk.END).index("Regular"))
        else:
            self.__list_of_font_styles.select_set(self.__list_of_font_styles.get(0, tk.END).index(self.__current_font_style.title()))

        if self.__current_font_size in self.__font_sizes:
            self.__list_of_font_sizes.see(self.__list_of_font_sizes.get(0, tk.END).index(self.__current_font_size))
            self.__list_of_font_sizes.select_set(self.__list_of_font_sizes.get(0, tk.END).index(self.__current_font_size))
        else:
            pass

        self.__sample_text_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.__sample_text.pack()

        self.__ok_button.grid(row=4, column=1, sticky=tk.E+tk.S, pady=(0, 160))
        self.__cancel_button.grid(row=4, column=2, sticky=tk.E+tk.S, padx=(5, 10), pady=(0, 160))

        self.__bindings()

    def __font_selection(self, event):
        """
        Allows for the selection of a font and enters the selected font in to the entry widget
        """

        selected_font = self.__list_of_fonts.get(tk.ANCHOR)
        self.__font_entry.delete(0, tk.END)
        self.__font_entry.insert(tk.END, selected_font)
        self.__sample_text.config(font=(selected_font, 50))

    def __font_style_selection(self, event):
        """
        Allows for the selection of a font styles and enters the selected font style into the entry widget
        """

        selected_font_style = self.__list_of_font_styles.get(tk.ANCHOR)
        self.__font_style_entry.delete(0, tk.END)
        self.__font_style_entry.insert(tk.END, selected_font_style)

        sample_text_font = font.Font(font=self.__sample_text["font"])

        if selected_font_style == "Regular":
            sample_text_font.config(weight="normal", slant="roman")
        elif selected_font_style == "Italic":
            sample_text_font.config(weight="normal", slant="italic")
        elif selected_font_style == "Bold Italic":
            sample_text_font.config(weight="bold", slant="italic")
        else:
            sample_text_font.config(weight="bold", slant="roman")

        self.__sample_text.config(font=sample_text_font)

    def __font_size_selection(self, event):
        """
        Allows for the selection of a font size and enters the selected font size in to the entry widget
        """

        selected_font_size = self.__list_of_font_sizes.get(tk.ANCHOR)
        self.__font_size_entry.delete(0, tk.END)
        self.__font_size_entry.insert(tk.END, selected_font_size)

    def __font_search(self, event):
        """
        Searches for the font typed into the font entry widget
        """

        typed_font = self.__font_entry.get().lower()

        # If the font entry widget is empty views all fonts
        if typed_font == "":
            fonts = self.__available_fonts
        # Otherwise views fonts which match what is in the font entry widget
        else:
            available_fonts = [i.lower() for i in self.__available_fonts]

            # Uses modified versions of the binary search algorithm to find the first and
            # last occurrence of what has been typed in the font entry widget
            first_occ = self.__binary_search_first_occ(available_fonts, typed_font)
            last_occ = self.__binary_search_last_occ(available_fonts, typed_font)

            # If the binary search finds no match, all the fonts remain in the list
            if first_occ == -1:
                fonts = self.__available_fonts
            # If binary search finds a match, only the fonts which match will be in the list
            else:
                fonts = []
                for i in self.__available_fonts[first_occ: last_occ + 1]:
                    fonts.append(i)

        # Updates the fonts listbox to view appropriate fonts
        self.__update_fonts(fonts)

    def __update_fonts(self, fonts):
        """
        Updates the self.__list_of_fonts listbox based on searched font name
        """

        # Clears the listbox
        self.__list_of_fonts.delete(0, tk.END)

        # Adds the appropriate fonts to the list box
        for i in fonts:
            self.__list_of_fonts.insert(tk.END, i)

    def __apply_changes(self, text_area, window):
        """
        Applies the specified font modifications
        """

        available_fonts = self.__available_fonts
        typed_font = self.__font_entry.get()
        font_found = self.__binary_search(available_fonts, typed_font)

        available_font_styles = sorted(self.__available_font_styles)
        typed_font_style = self.__font_style_entry.get()
        font_style_found = self.__binary_search(available_font_styles, typed_font_style.title())

        if font_found == -1:
            messagebox.showwarning("Font", "There is no font with that name.\nChoose a font from the list of fonts.")
        elif font_style_found == -1:
            messagebox.showwarning("Font", "There is no font style with that name.\nChoose a font style from the list of font styles.")
        elif not self.__font_size_entry.get().isnumeric():
            messagebox.showwarning("Font", "Size must be a number.")
        else:
            # Unique key of the list of preferences
            oid = 1

            # Connects to the database
            conn = sqlite3.connect("text_editor_preferences.db")
            # Creates a cursor
            c = conn.cursor()

            c.execute("""UPDATE preferences SET
            font = :font,
            font_style = :font_style,
            font_size = :font_size
            
            WHERE oid =  """ + str(oid),
            {"font": typed_font,
             "font_style": typed_font_style.lower(),
             "font_size": int(self.__font_size_entry.get())
            })

            c.execute("SELECT font, font_style, font_size FROM preferences")
            preferences = c.fetchall()

            self.__current_font = preferences[0][0]

            if typed_font_style.title() == "Regular":
                self.__current_font_style = ""
            else:
                self.__current_font_style = preferences[0][1]

            self.__current_font_size = preferences[0][2]

            text_area.config(font=(self.__current_font, self.__current_font_size, self.__current_font_style))

            # Commit changes and close database
            conn.commit()
            conn.close()

            # Destroy the window
            window.destroy()

    def __bindings(self):
        """
        Bindings for the listboxes and entry widgets
        """

        self.__list_of_fonts.bind("<<ListboxSelect>>", self.__font_selection)
        self.__list_of_font_styles.bind("<<ListboxSelect>>", self.__font_style_selection)
        self.__list_of_font_sizes.bind("<<ListboxSelect>>", self.__font_size_selection)

        self.__font_entry.bind("<KeyRelease>", self.__font_search)

    @staticmethod
    def __binary_search(arr, val):
        first = 0
        last = len(arr) - 1

        while first <= last:
            middle = (first + last) // 2
            if val < arr[middle]:
                last = middle - 1
            elif val > arr[middle]:
                first = middle + 1
            else:
                return middle

        return -1

    @staticmethod
    def __binary_search_first_occ(arr, val):
        """
        Searches for the first occurrence of a passed value in the passed list
        """

        low = 0
        high = len(arr) - 1
        result = -1

        while low <= high:
            mid = (low + high) // 2

            if val == arr[mid][:len(val)]:
                result = mid
                high = mid - 1
            elif val < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1

        return result

    @staticmethod
    def __binary_search_last_occ(arr, val):
        """
        Searches for the last occurrence of a passed value in the passed list
        """

        low = 0
        high = len(arr) - 1
        result = -1

        while low <= high:
            mid = (low + high) // 2

            if val == arr[mid][:len(val)]:
                result = mid
                low = mid + 1
            elif val < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1

        return result
