"""
Written by Maciej Fec
email: maciejfec1996@gmail.com
"""

import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
import os
from datetime import datetime
import webbrowser
from font_menu import Fonts
import sqlite3


class MenuBar:

    def __init__(self, window):
        self.__menu = tk.Menu(window)

    def display_menu_bar(self, file_menu, edit_menu, format_menu, view_menu, help_menu):
        """
        Creates drop down menus and displays them in the GUI window.
        """

        self.__menu.add_cascade(label="File", menu=file_menu)
        self.__menu.add_cascade(label="Edit", menu=edit_menu)
        self.__menu.add_cascade(label="Format", menu=format_menu)
        self.__menu.add_cascade(label="View", menu=view_menu)
        self.__menu.add_cascade(label="Help", menu=help_menu)

    def get_menu(self):
        return self.__menu


class FileMenu:

    def __init__(self, window):

        # Creates a File ribbon for the menu
        self.__file_menu = tk.Menu(window, tearoff=0)

        # Types of files which the text editor can work with
        self.__file_types = [("Text Document", "*.txt")]

        # Checks whether the file has been saved
        self.__file_saved = tk.BooleanVar(False)

    def file_menu_options(self, text_area, window, filename, status_bar):
        """
        Displays the options of the File ribbon in the menu
        """

        self.__file_menu.add_command(label="New", command=lambda: self.__new(text_area, window, filename, status_bar))
        self.__file_menu.add_command(label="Open...", command=lambda: self.__open_file(text_area, window, filename, status_bar))
        self.__file_menu.add_command(label="Save", command=lambda: self.__save(text_area, window, filename))
        self.__file_menu.add_command(label="Save As...", command=lambda: self.__save_as(text_area, window, filename))

        self.__file_menu.add_separator()

        self.__file_menu.add_command(label="Exit", command=lambda: self.exit_text_editor(window, text_area, filename))

    def __new(self, text_area, window, filename, status_bar):
        """
        Allows for creating a new file
        """

        # If the file is untitled and the text area has been modified, prompts the user user to save
        if filename.get() == "Untitled" and len(text_area.get("1.0", "end-1c")) > 0:
            response = messagebox.askyesnocancel("TextEditor", f"Do you want to save changes to {filename.get()}")

            # If the response is yes, brings up the save as menu and then clears the text area
            if response == 1:
                file = self.__save_as(text_area, window, filename)

                if file:
                    text_area.delete("1.0", "end")
                    filename.set("Untitled")
                    window.title(f"{filename.get()} - TextEditor")
                    text_area.edit_modified(False)
                    self.__file_saved.set(False)
                    status_bar.update_word_and_character_count(None, text_area)
                else:
                    pass
            # If the response is no, clears the text area without saving
            elif response == 0:
                text_area.delete("1.0", "end")
                filename.set("Untitled")
                window.title(f"{filename.get()} - TextEditor")
                text_area.edit_modified(False)
                self.__file_saved.set(False)
                status_bar.update_word_and_character_count(None, text_area)
            # If the response is cancel nothing happens
            else:
                pass
        # If the file is an existing file and the text area has been modified and the file was not saved,
        # prompts the user to save
        elif filename.get() != "Untitled" and text_area.edit_modified() and not self.__file_saved.get():
            response = messagebox.askyesnocancel("TextEditor", f"Do you want to save changes to {filename.get()}")

            # If the response is yes, saves any modifications made before starting a new file
            if response == 1:
                self.__save(text_area, window, filename)

                text_area.delete("1.0", "end")
                filename.set("Untitled")
                window.title(f"{filename.get()} - TextEditor")
                text_area.edit_modified(False)
                self.__file_saved.set(False)
                status_bar.update_word_and_character_count(None, text_area)
            # If the response is no, starts a new file without saving
            elif response == 0:
                text_area.delete("1.0", "end")
                filename.set("Untitled")
                window.title(f"{filename.get()} - TextEditor")
                text_area.edit_modified(False)
                self.__file_saved.set(False)
                status_bar.update_word_and_character_count(None, text_area)
            # If the response is cancel, nothing happens
            else:
                pass
        # If the file is untitled or an existing file and the file has not been modified, starts a new file without
        # prompting to save
        else:
            text_area.delete("1.0", "end")
            filename.set("Untitled")
            window.title(f"{filename.get()} - TextEditor")
            status_bar.update_word_and_character_count(None, text_area)

    def __open_file(self, text_area, window, filename, status_bar):
        """
        Allows for opening existing .txt files
        """

        try:
            # If the file is untitled and there is text in the text area, prompts the user to save
            if filename.get() == "Untitled" and len(text_area.get("1.0", "end-1c")) > 0:
                response = messagebox.askyesnocancel("TextEditor", f"Do you want to save changes to {filename.get()}?")

                if response == 1:
                    # If the user response is yes, brings up the save as menu
                    file = self.__save_as(text_area, window, filename)

                    if file:
                        # After saving prompts user to pick which file to open
                        file = askopenfilename(filetypes=self.__file_types)
                        filename.set(file)
                        window.title(f"{os.path.basename(filename.get())} - TextEditor")
                        file = open(file, "r")
                        text_from_file = file.read()
                        text_area.delete("1.0", "end")
                        text_area.insert(tk.END, text_from_file)
                        file.close()
                        text_area.edit_modified(False)
                        self.__file_saved.set(False)
                        status_bar.update_word_and_character_count(None, text_area)
                    else:
                        pass
                elif response == 0:
                    # If the user response is no, opens a new file without prompting to save
                    file = askopenfilename(filetypes=self.__file_types)
                    filename.set(file)
                    window.title(f"{os.path.basename(filename.get())} - TextEditor")
                    file = open(file, "r")
                    text_from_file = file.read()
                    text_area.delete("1.0", "end")
                    text_area.insert(tk.END, text_from_file)
                    file.close()
                    text_area.edit_modified(False)
                    self.__file_saved.set(False)
                    status_bar.update_word_and_character_count(None, text_area)
                else:
                    # If the user response is cancel nothing happens
                    pass
            # If the file is an existing file and the file has been modified, prompts the user to save
            elif filename.get() != "Untitled" and text_area.edit_modified() and not self.__file_saved.get():
                response = messagebox.askyesnocancel("TextEditor", f"Do you want to save changes to {filename.get()}?")

                if response == 1:
                    # If the user response is yes, saves the file
                    self.__save(text_area, window, filename)

                    # After saving, prompts the user to pick a file to open
                    file = askopenfilename(filetypes=self.__file_types)
                    filename.set(file)
                    window.title(f"{os.path.basename(filename.get())} - TextEditor")
                    file = open(file, "r")
                    text_from_file = file.read()
                    text_area.delete("1.0", "end")
                    text_area.insert(tk.END, text_from_file)
                    file.close()
                    text_area.edit_modified(False)
                    self.__file_saved.set(False)
                    status_bar.update_word_and_character_count(None, text_area)
                elif response == 0:
                    # If the user response is no, prompts the user to pick a file to open without prompting to save
                    file = askopenfilename(filetypes=self.__file_types)
                    filename.set(file)
                    window.title(f"{os.path.basename(filename.get())} - TextEditor")
                    file = open(file, "r")
                    text_from_file = file.read()
                    text_area.delete("1.0", "end")
                    text_area.insert(tk.END, text_from_file)
                    file.close()
                    text_area.edit_modified(False)
                    self.__file_saved.set(False)
                    status_bar.update_word_and_character_count(None, text_area)
                else:
                    # If the user response is cancel nothing happens
                    pass
            else:
                # If the file is an untitled file or existing file and the file has not been modified, prompts user
                # to open a file without first prompting to save
                file = askopenfilename(filetypes=self.__file_types)

                if file:
                    filename.set(file)
                    window.title(f"{os.path.basename(filename.get())} - TextEditor")

                file = open(file, "r")
                text_from_file = file.read()
                text_area.delete("1.0", "end")
                text_area.insert(tk.END, text_from_file)
                file.close()
                text_area.edit_modified(False)
                self.__file_saved.set(False)
                status_bar.update_word_and_character_count(None, text_area)
        # Catches the FileNotFoundError is user clicks cancel on the Open File pop up
        except FileNotFoundError:
            pass

    def __save(self, text_area, window, filename):
        """
        Allows for saving changes made to existing files
        """

        if filename.get() == "Untitled":
            self.__save_as(text_area, window, filename)
        else:
            text = text_area.get("1.0", "end-1c")
            file = open(filename.get(), "w")
            file.write(text)
            file.close()
            self.__file_saved.set(True)

    def __save_as(self, text_area, window, filename):
        """
        Allows for saving new files, and new copies of existing files
        """

        try:
            file = asksaveasfilename(filetypes=self.__file_types, defaultextension=self.__file_types)

            if file:
                window.title(f"{os.path.basename(file)} - TextEditor")
                filename.set(file)

            text = text_area.get("1.0", "end-1c")
            file = open(file, "w")
            file.write(text)
            file.close()
            text_area.edit_modified(False)
            self.__file_saved.set(True)

            return file
        except FileNotFoundError:
            pass

    def exit_text_editor(self, window, text_area, filename):
        """
        Allows for closing an existing window
        """

        # If the file is untitled and the text area has been modified, prompts the user user to save
        if filename.get() == "Untitled" and len(text_area.get("1.0", "end-1c")) > 0:
            response = messagebox.askyesnocancel("TextEditor", f"Do you want to save changes to {filename.get()}")

            # If the response is yes, brings up the save as menu and then closes the window
            if response == 1:
                file = self.__save_as(text_area, window, filename)
                if file:
                    window.destroy()
                else:
                    pass
            # If the response is no, closes the window without saving
            elif response == 0:
                window.destroy()
            # If the response is cancel, nothing happens
            else:
                pass
        # If the file is an existing file and the text area has been modified and the file was not saved,
        # prompts the user to save
        elif filename.get() != "Untitled" and text_area.edit_modified() and not self.__file_saved.get():
            response = messagebox.askyesnocancel("TextEditor", f"Do you want to save changes to {filename.get()}")

            # If the response is yes, saves any modifications made before closing the window
            if response == 1:
                self.__save(text_area, window, filename)
                window.destroy()
            # If the response is no, starts a new file without saving
            elif response == 0:
                window.destroy()
            # If the response is cancel, nothing happens
            else:
                pass
        # If the file is untitled or an existing file and the file has not been modified, closes the window without
        # prompting to save
        else:
            window.destroy()

    def file_not_saved(self, event, text_area):
        """
        Changes the state of the self.__file_saved variable to False if the text area has been modified
        """

        if text_area.edit_modified():
            self.__file_saved.set(False)

    def get_file_menu(self):
        """
        Returns the file menu to be used outside of class
        """

        return self.__file_menu


class EditMenu:

    def __init__(self, window):
        # Creates a Edit ribbon for the menu
        self.__edit_menu = tk.Menu(window, tearoff=0)

    def edit_menu_options(self, text_area, window, status_bar):
        """
        Displays the options of the Edit ribbon in the menu
        """

        self.__edit_menu.add_command(label="Undo", command=lambda: self.__undo(text_area, status_bar))
        self.__edit_menu.add_command(label="Redo", command=lambda: self.__redo(text_area, status_bar))

        self.__edit_menu.add_separator()

        self.__edit_menu.add_command(label="Cut", state=tk.DISABLED, command=lambda: self.__cut(text_area, window, status_bar))
        self.__edit_menu.add_command(label="Copy", state=tk.DISABLED, command=lambda: self.__copy(text_area, window))
        self.__edit_menu.add_command(label="Paste", command=lambda: self.__paste(text_area, window, status_bar))
        self.__edit_menu.add_command(label="Delete", state=tk.DISABLED, command=lambda: self.__delete(text_area, status_bar))

        self.__edit_menu.add_separator()

        self.__edit_menu.add_command(label="Search With Google...", state=tk.DISABLED, command=lambda: self.__search_with_google(text_area))

        self.__edit_menu.add_separator()

        self.__edit_menu.add_command(label="Select All", command=lambda: self.__select_all(text_area))
        self.__edit_menu.add_command(label="Time/Date", command=lambda: self.__time_date(text_area, status_bar))

    @staticmethod
    def __undo(text_area, status_bar):
        """
        To undo an edit made to the text area
        """

        try:
            text_area.edit_undo()
            status_bar.update_word_and_character_count(None, text_area)
        except tk.TclError:
            pass

    @staticmethod
    def __redo(text_area, status_bar):
        """
        To redo an edit made to the text area
        """

        try:
            text_area.edit_redo()
            status_bar.update_word_and_character_count(None, text_area)
        except tk.TclError:
            pass

    @staticmethod
    def __cut(text_area, window, status_bar):
        """
        Cuts selected text out of the text box
        """

        selected_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        window.clipboard_clear()
        window.clipboard_append(selected_text)
        status_bar.update_word_and_character_count(None, text_area)

    @staticmethod
    def __copy(text_area, window):
        """
        Copies selected text to the clipboard
        """

        selected_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        window.clipboard_clear()
        window.clipboard_append(selected_text)

    @staticmethod
    def __paste(text_area, window, status_bar):
        """
        Pastes copied or cut text from the clipboard into the text box
        """

        try:
            text_area.insert(tk.INSERT, window.clipboard_get())
            status_bar.update_word_and_character_count(None, text_area)
        except:
            pass

    @staticmethod
    def __delete(text_area, status_bar):
        """
        Deletes selected text from the text box
        """

        text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        status_bar.update_word_and_character_count(None, text_area)

    @staticmethod
    def __search_with_google(text_area):

        url = f"https://www.google.com.tr/search?q={text_area.get(tk.SEL_FIRST, tk.SEL_LAST)}"
        webbrowser.open(url, new=2)

    @staticmethod
    def __select_all(text_area):
        """
        Selects everything inside the text box
        """

        text_area.tag_add(tk.SEL, "1.0", "end-1c")

    @staticmethod
    def __time_date(text_area, status_bar):
        """
        Inserts the current date and time into the textbox
        """

        current_date_and_time = datetime.now().strftime("%H:%M %d/%m/%Y")
        text_area.insert(tk.INSERT, current_date_and_time)
        status_bar.update_word_and_character_count(None, text_area)

    def enable_disable_methods_on_select(self, event, text_area):
        """
        Enables and disables the Cut, Copy, Delete and Search With Google methods based on whether text is selected
        """

        if text_area.tag_ranges(tk.SEL):
            self.__edit_menu.entryconfig("Cut", state=tk.NORMAL)
            self.__edit_menu.entryconfig("Copy", state=tk.NORMAL)
            self.__edit_menu.entryconfig("Delete", state=tk.NORMAL)
            self.__edit_menu.entryconfig("Search With Google...", state=tk.NORMAL)
        else:
            self.__edit_menu.entryconfig("Cut", state=tk.DISABLED)
            self.__edit_menu.entryconfig("Copy", state=tk.DISABLED)
            self.__edit_menu.entryconfig("Delete", state=tk.DISABLED)
            self.__edit_menu.entryconfig("Search With Google...", state=tk.DISABLED)

    def get_edit_menu(self):
        """
        Returns the file menu to be used outside of class
        """

        return self.__edit_menu


class FormatMenu:

    def __init__(self, window):
        # Creates a Format ribbon for the menu
        self.__format_menu = tk.Menu(window, tearoff=0)

        # Boolean variable for toggling word wrap
        self.__word_wrap_is_on = tk.IntVar()

    def format_menu_options(self, text_area, text_box):
        """
        Displays the options of the Format ribbon in the menu
        """

        self.__format_menu.add_checkbutton(label="Word Wrap", variable=self.__word_wrap_is_on, command=lambda: self.__toggle_word_wrap(text_area, text_box))
        self.__format_menu.add_command(label="Font...", command=lambda: self.__change_font(text_area))

        conn = sqlite3.connect("text_editor_preferences.db")
        c = conn.cursor()
        c.execute("SELECT word_wrap FROM preferences")
        result = c.fetchall()

        if result[0][0] == 1:
            self.__format_menu.invoke(self.__format_menu.index("Word Wrap"))
        else:
            pass

        conn.close()

    def __toggle_word_wrap(self, text_area, text_box):
        """
        Toggles word wrap on and off
        """

        conn = sqlite3.connect("text_editor_preferences.db")
        c = conn.cursor()

        if self.__word_wrap_is_on.get() == 1:
            # If word wrap is off, switches word wrap on
            text_box.get_horizontal_scroll_bar().grid_remove()
            text_area["wrap"] = tk.CHAR
            c.execute("UPDATE preferences SET word_wrap = :word_wrap", {"word_wrap": 1})
        else:
            # If word wrap is on, switches word wrap off
            text_box.get_horizontal_scroll_bar().grid()
            text_area["wrap"] = tk.NONE
            c.execute("UPDATE preferences SET word_wrap = :word_wrap", {"word_wrap": 0})

        conn.commit()
        conn.close()

    @staticmethod
    def __change_font(text_area):
        """
        Allows for the change of the font, font style and font size
        """

        window = tk.Toplevel()
        window.resizable(0, 0)
        window.geometry("425x439")
        window.iconbitmap("images\\notepad.ico")
        window.title("Font")
        window.grab_set()

        fonts = Fonts(window, text_area)
        fonts.display_font_options()

        window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())

    def get_format_menu(self):
        """
        Returns the format menu to be used outside of class
        """

        return self.__format_menu


class ViewMenu:

    def __init__(self, window):
        # Creates a View ribbon for the menu
        self.__view_menu = tk.Menu(window, tearoff=0)

        # Boolean variable for toggling dark mode
        self.__dark_mode_is_on = tk.IntVar()

    def view_menu_options(self, text_area):
        """
        Displays the options of the View ribbon in the menu
        """

        self.__view_menu.add_checkbutton(label="Dark Mode", variable=self.__dark_mode_is_on, command=lambda: self.__toggle_dark_mode(text_area))

        conn = sqlite3.connect("text_editor_preferences.db")
        c = conn.cursor()
        c.execute("SELECT dark_mode FROM preferences")
        result = c.fetchall()

        if result[0][0] == 1:
            self.__view_menu.invoke(self.__view_menu.index("Dark Mode"))
        else:
            pass

        conn.close()

    def __toggle_dark_mode(self, text_area):
        """
        Toggles dark mode on and off
        """

        conn = sqlite3.connect("text_editor_preferences.db")
        c = conn.cursor()

        if self.__dark_mode_is_on.get() == 1:
            text_area.config(bg="black", fg="white", insertbackground="white")
            c.execute("UPDATE preferences SET dark_mode = :dark_mode", {"dark_mode": 1})
        else:
            text_area.config(bg="white", fg="black", insertbackground="black")
            c.execute("UPDATE preferences SET dark_mode = :dark_mode", {"dark_mode": 0})

        conn.commit()
        conn.close()

    def get_view_menu(self):
        """
        Returns the view menu to be used outside of class
        """

        return self.__view_menu


class HelpMenu:

    def __init__(self, window):
        # Creates a Help ribbon for the menu
        self.__help_menu = tk.Menu(window, tearoff=0)

        self.__logo = tk.PhotoImage(file="images\\notepad.gif")

        self.__github_img = tk.PhotoImage(file="images\\github.gif")

    def help_menu_options(self):
        """
        Displays the options of the Help ribbon in the menu
        """

        self.__help_menu.add_command(label="View Help")

        self.__help_menu.add_separator()

        self.__help_menu.add_command(label="About TextEditor", command=lambda: self.__view_about_info())

    def __view_help(self):
        pass

    def __view_about_info(self):

        window = tk.Toplevel()
        window.resizable(0, 0)
        window.geometry("400x400")
        window.iconbitmap("images\\notepad.ico")
        window.title("About")
        window.grab_set()
        window.focus()

        logo_label = tk.Label(window, image=self.__logo)
        logo_label.place(x=10, y=10)

        title_label = tk.Label(window, text="TextEditor", font=("Consolas", 35, "bold"))
        title_label.place(x=122, y=30)

        about_label = tk.Label(window, text="This is a simple text editor built with Python, Tkinter and SQLite3. \nVisit my GitHub page to see more.")
        about_label.place(x=25, y=150)

        github_img_button = tk.Button(window, image=self.__github_img, relief="solid", command=lambda: self.__open_github())
        github_img_button.place(x=25, y=215)

        ok_button = tk.Button(window, text="OK", width=8, command=lambda: window.destroy())
        ok_button.place(x=320, y=360)

        window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())

    @staticmethod
    def __open_github():
        """
        Opens my GitHub page
        """

        webbrowser.open("https://github.com/fecrol", new=2)

    def get_help_menu(self):
        """
        Returns the help menu to be used outside of class
        """

        return self.__help_menu
