import os
from math import *
from pathlib import Path


class ListFilesBox:

    def __init__(self, box, cursor_style, directory_style, normal_text, directory=str(Path.home())):
        self.box = box
        self.cursor_style = cursor_style
        self.directory_style = directory_style
        self.normal_text = normal_text
        self.directory = directory
        self.selected_files = self.all_files = []
        self.max_row = 10  # TODO calculate it
        self.page = 1
        self.pages = 0
        self.position = 1
        self.systemPathSeparator = os.path.sep
        self.row_num = 0
        self.systemPathSeparator = os.path.sep
        self.current_number_of_elements = 0
        self.previous_states = []

        self.load_from_directory(self.directory)

    def load_from_directory(self, directory):
        self.directory = str(directory)
        self.selected_files = self.all_files = os.listdir(self.directory)
        self.position = 1
        self.page = 1
        self.row_num = len(self.selected_files)
        self.pages = int(ceil(self.row_num / self.max_row))

    def go_to_parent(self):
        current_path = Path(self.directory).parent
        self.load_from_directory(current_path)
        if len(self.previous_states) == 0:
            self.position = 1
            self.page = 1
        else:
            previous_state = self.previous_states.pop()
            self.position = previous_state.position
            self.page = previous_state.page

    def go_to_selected_directory(self):
        selected_file = self.directory + self.systemPathSeparator + self.selected_files[self.position - 1]
        if os.path.isdir(selected_file):
            self.directory = selected_file
            self.previous_states.append(State(self))
            self.load_from_directory(selected_file)

    def print(self):
        self.box.erase()
        self.box.border(0)
        self.box.addstr(0, 2, self.directory)
        for self.current_number_of_elements in range(1 + (self.max_row * (self.page - 1)),
                                                     self.max_row + 1 + (self.max_row * (self.page - 1))):
            i = self.current_number_of_elements
            if self.row_num != 0:
                if i + (self.max_row * (self.page - 1)) == self.position + (self.max_row * (self.page - 1)):
                    self.box.addstr(i - (self.max_row * (self.page - 1)), 2, self.selected_files[i - 1],
                                    self.cursor_style)
                elif os.path.isdir(self.directory + self.systemPathSeparator + self.selected_files[i - 1]):
                    self.box.addstr(i - (self.max_row * (self.page - 1)), 2, self.selected_files[i - 1],
                                    self.directory_style)
                else:
                    self.box.addstr(i - (self.max_row * (self.page - 1)), 2, self.selected_files[i - 1],
                                    self.normal_text)
                if self.current_number_of_elements >= self.row_num:
                    break

        self.box.refresh()


class State:

    def __init__(self, list_files_box):
        self.position = list_files_box.position
        self.page = list_files_box.page
