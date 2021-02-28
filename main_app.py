"""
Written by Maciej Fec
email: maciejfec1996@gmail.com
"""

import tkinter as tk
from menu_bar import MenuBar, FileMenu, EditMenu, FormatMenu, ViewMenu, HelpMenu
from text_box import TextBox
from status_bar import StatusBar

# Creates the main GUI window
root = tk.Tk()
root.geometry("1424x720")
root.iconbitmap("images\\notepad.ico")
filename = tk.StringVar()
filename.set("Untitled")
root.title(f"{filename.get()} - TextEditor")

# Allows the text box to stretch across the whole window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Creates the text_area
text_box = TextBox(root)
text_area = text_box.get_text_area()

# Displays the text box
text_box.display_text_box()
# Displays the scrollbars
text_box.display_scroll_bars()

# Creates and displays the status_bar
status_bar = StatusBar(root, text_area)

# Creates a menu bar
menu_bar = MenuBar(root)
file_menu = FileMenu(root)
edit_menu = EditMenu(root)
format_menu = FormatMenu(root)
view_menu = ViewMenu(root)
help_menu = HelpMenu(root)

# Generates a space for the menu bar
root.config(menu=menu_bar.get_menu())

# Displays the menu bar ribbons
menu_bar.display_menu_bar(file_menu.get_file_menu(), edit_menu.get_edit_menu(), format_menu.get_format_menu(),
                          view_menu.get_view_menu(), help_menu.get_help_menu())

# Displays the options of the File ribbon
file_menu.file_menu_options(text_area, root, filename, status_bar)

# Displays the options of the Edit ribbon
edit_menu.edit_menu_options(text_area, root, status_bar)

# Displays the options of the Format ribbon
format_menu.format_menu_options(text_area, text_box)

# Displays the options of the View ribbon
view_menu.view_menu_options(text_area)

# Displays the options of the Help ribbon
help_menu.help_menu_options()

status_bar.display_status_bar()

# Enables the Cut, Copy, Delete and Search With Google edit menu options upon text selection
text_area.bind("<<Selection>>", lambda event: edit_menu.enable_disable_methods_on_select(event, text_area))

# Lets the program know that the file has been modified and has not been saved
text_area.bind("<KeyRelease>", lambda event: file_menu.file_not_saved(event, text_area))

# Updates the word and character count
text_area.bind("<KeyRelease>", lambda event: status_bar.update_word_and_character_count(event, text_area))

# Handles the quit procedure of the x ext button
root.protocol("WM_DELETE_WINDOW", lambda: file_menu.exit_text_editor(root, text_area, filename))

root.mainloop()
