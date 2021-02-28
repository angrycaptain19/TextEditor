import tkinter as tk


class Find:

	def __init__(self, text_area):

		# The window for the Find command
		self.__find_window = tk.Toplevel()
		self.__find_window.resizable(0, 0)
		self.__find_window.attributes("-topmost", True)
		self.__find_window.geometry("350x90")
		self.__find_window.title("Find")

		self.__find_label = tk.Label(self.__find_window, text="Find what:", font=("", 9), pady=10, padx=10)
		self.__find_label.place(x=0, y=0)

		self.__entry_field = tk.Entry(self.__find_window, width=32, relief="solid", font=("Consolas", 11))
		self.__entry_field.place(x=80, y=10)
		self.__entry_field.focus()

		self.__find_next_button = tk.Button(self.__find_window, text="Find Next", width=12, state=tk.DISABLED, command=lambda: self.__find_next(text_area))
		self.__find_next_button.place(x=10, y=50)

		self.__find_previous_button = tk.Button(self.__find_window, text="Find Previous", width=12, state=tk.DISABLED)
		self.__find_previous_button.place(x=128, y=50)

		self.__find_all_button = tk.Button(self.__find_window, text="Find All", width=12, state=tk.DISABLED)
		self.__find_all_button.place(x=245, y=50)

		self.__entry_field.bind("<KeyRelease>", self.__activate_buttons)

		self.__find_window.protocol("WM_DELETE_WINDOW", lambda: self.__find_window.destroy())

	def __find_next(self, text_area):

		text_area.tag_configure("RED", foreground="Red")

		text_to_find = self.__entry_field.get().lower()
		text_to_search = text_area.get("1.0", "end-1c").lower()

		print(text_to_search.index(text_to_find))

	def __find_previous(self):
		pass

	def __find_all(self):
		pass

	def __activate_buttons(self, event):

		if len(self.__entry_field.get()) > 0:
			self.__find_next_button.config(state=tk.NORMAL)
			self.__find_previous_button.config(state=tk.NORMAL)
			self.__find_all_button.config(state=tk.NORMAL)
		else:
			self.__find_next_button.config(state=tk.DISABLED)
			self.__find_previous_button.config(state=tk.DISABLED)
			self.__find_all_button.config(state=tk.DISABLED)


class Replace:

	def __init__(self, text_area):

		# The window for the Find command
		self.__replace_window = tk.Toplevel()
		self.__replace_window.resizable(0, 0)
		self.__replace_window.attributes("-topmost", True)
		self.__replace_window.geometry("350x115")
		self.__replace_window.title("Replace")

		self.__find_label = tk.Label(self.__replace_window, text="Find what:", font=("", 9))
		self.__find_label.place(x=0, y=10)

		self.__find_entry = tk.Entry(self.__replace_window, width=32, relief="solid", font=("Consolas", 11))
		self.__find_entry.place(x=80, y=10)
		self.__find_entry.focus()

		self.__replace_label = tk.Label(self.__replace_window, text="Replace with:", font=("", 9))
		self.__replace_label.place(x=0, y=40)

		self.__replace_entry = tk.Entry(self.__replace_window, width=32, relief="solid", font=("Consolas", 11), state=tk.DISABLED)
		self.__replace_entry.place(x=80, y=40)

		self.__find_next_button = tk.Button(self.__replace_window, text="Find Next", width=12, state=tk.DISABLED)
		self.__find_next_button.place(x=10, y=80)

		self.__replace_button = tk.Button(self.__replace_window, text="Replace", width=12, state=tk.DISABLED)
		self.__replace_button.place(x=128, y=80)

		self.__replace_all_button = tk.Button(self.__replace_window, text="Replace All", width=12, state=tk.DISABLED)
		self.__replace_all_button.place(x=245, y=80)

		self.__find_entry.bind("<KeyRelease>", self.__activate_buttons)

		self.__replace_window.protocol("WM_DELETE_WINDOW", lambda: self.__replace_window.destroy())

	def __activate_buttons(self, event):

		if len(self.__find_entry.get()) > 0:
			self.__find_next_button.config(state=tk.NORMAL)
			self.__replace_button.config(state=tk.NORMAL)
			self.__replace_all_button.config(state=tk.NORMAL)
			self.__replace_entry.config(state=tk.NORMAL)
		else:
			self.__find_next_button.config(state=tk.DISABLED)
			self.__replace_button.config(state=tk.DISABLED)
			self.__replace_all_button.config(state=tk.DISABLED)
			self.__replace_entry.config(state=tk.DISABLED)
