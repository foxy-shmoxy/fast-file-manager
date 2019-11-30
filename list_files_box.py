import os
from math import *
from pathlib import Path
from filter import Filter


class ListFilesBox:

    # TODO take care of duplicates
    def __init__(self, box, cursor_style, directory_style, normal_text, directory=str(Path.home()),
                 log_file=open("logs.txt", "w")):
        self.log_file = log_file
        self.box = box
        self.cursor_style = cursor_style
        self.directory_style = directory_style
        self.normal_text = normal_text
        self.directory = directory
        self.selected_files = self.all_files = []
        self.max_row, self.max_cols = self.box.getmaxyx()
        self.max_row = self.max_row - 1
        self.page_number = 0
        self.page = []
        self.pages = 0
        self.position = 0
        self.systemPathSeparator = os.path.sep
        self.row_num = 0
        self.systemPathSeparator = os.path.sep
        self.current_number_of_elements = 0
        self.previous_states = []

        self.load_from_directory(self.directory)

    def load_from_directory(self, directory):
        self.directory = str(directory)
        self.selected_files = self.all_files = os.listdir(self.directory)
        self.selected_files.sort()
        self.position = 0
        self.page_number = 0
        self.row_num = len(self.selected_files)
        self.pages = int(ceil(self.row_num / self.max_row))
        self.page = self.selected_files[0: self.max_row - 1]

    def go_to_parent(self):
        current_path = Path(self.directory).parent
        self.load_from_directory(current_path)
        if len(self.previous_states) == 0:
            self.position = 0
            self.page_number = 0
        else:
            previous_state = self.previous_states.pop()
            self.position = previous_state.position
            self.page_number = previous_state.page

    def go_to_selected_directory(self):
        selected_file = self.directory + self.systemPathSeparator + self.page[self.position]
        if os.path.isdir(selected_file):
            self.directory = selected_file
            self.previous_states.append(State(self))
            self.load_from_directory(selected_file)

    def print(self):
        self.max_row, self.max_cols = self.box.getmaxyx()
        self.max_row = self.max_row - 1
        self.pages = int(ceil(self.row_num / self.max_row))
        self.page = self.selected_files[0: self.max_row - 1]
        self.box.erase()
        self.box.border(0)
        self.box.addstr(0, 2, self.directory)
        for self.current_number_of_elements, element in enumerate(self.page):
            croped_element = element[: self.max_cols - 3]
            # self.log("cropped element %s" % croped_element)
            if self.current_number_of_elements == self.position:
                self.box.addstr(self.current_number_of_elements + 1, 2, croped_element, self.cursor_style)
            elif os.path.isdir(self.directory + self.systemPathSeparator + element):
                self.box.addstr(self.current_number_of_elements + 1, 2, croped_element, self.directory_style)
            else:
                self.box.addstr(self.current_number_of_elements + 1, 2, croped_element, self.normal_text)
            self.box.refresh()

        self.box.refresh()

    def filter(self):
        Filter(self).handle_filtering()

    def set_selected_files(self, selected_files):
        self.selected_files = selected_files
        self.position = 0
        self.page_number = 0
        self.row_num = len(self.selected_files)
        self.pages = int(ceil(self.row_num / self.max_row))

    def key_up(self):
        if self.position == 0 and self.page_number == 0:
            return

        self.position = self.position - 1
        if self.position < 0:
            if self.page_number > 0:
                self.page_number = self.page_number - 1
            self.position = self.position % self.max_row - 1
            start_element_index = self.page_number * self.max_row - 1
            if start_element_index < 0:
                start_element_index = 0
            self.page = self.selected_files[start_element_index: start_element_index + self.max_row - 1]

    def key_down(self):
        if self.position < self.current_number_of_elements:
            self.position = self.position + 1
        elif self.position + 1 < len(self.selected_files):
            self.position = 0
            self.page_number = self.page_number + 1
            start_element_index = self.page_number * self.max_row - 1
            self.page = self.selected_files[start_element_index: start_element_index + self.max_row - 1]

    def resize(self, height, width):
        self.box.erase()
        self.box.resize(height, width)
        self.position = 0
        self.page_number = 0
        self.row_num = len(self.selected_files)
        self.max_row, self.max_cols = self.box.getmaxyx()
        self.max_row = self.max_row - 1
        self.pages = int(ceil(self.row_num / self.max_row))
        self.page = self.selected_files[0: self.max_row - 1]
        self.print()
        self.box.refresh()

    def move(self, y, x):
        self.box.mvwin(y, x)
        self.box.refresh()

    def gethw(self):
        self.log("y = %s x = %s" % self.box.getmaxyx())
        return self.box.getmaxyx()

    def log(self, msg):
        self.log_file.write("%s\n" % msg)
        self.log_file.flush()


class State:

    def __init__(self, list_files_box):
        self.position = list_files_box.position
        self.page = list_files_box.page
