import curses
import datetime
import os
import platform
import subprocess
from math import *
from pathlib import Path

from filter import Filter


class ListFilesBox:

    # TODO take care of duplicates
    def __init__(self, curses, height, width, x, y, fonts, directory=str(Path.home()),
                 log_file=open("logs.txt", "w")):
        self.log_file = log_file
        self.box = ListFilesBox.create_box(curses, height, width, x, y)
        self.fonts = fonts
        self.directory = directory
        self.selected_files = self.all_files = []
        self.max_rows_in_page, self.max_cols = self.box.getmaxyx()
        self.max_rows_in_page = self.max_rows_in_page - 2
        self.page_number = 0
        self.page = []
        self.number_of_pages = 0
        self.position = 0
        self.systemPathSeparator = os.path.sep
        self.all_files_count = 0
        self.systemPathSeparator = os.path.sep
        self.current_number_of_elements = 0
        self.previous_states = []
        self.focused = True

        self.load_from_directory(self.directory)

    @staticmethod
    def create_box(curses, height, width, y, x):
        box = curses.newwin(height, width, y, x)
        box.keypad(1)
        box.box()
        return box

    def load_from_directory(self, directory):
        self.directory = str(directory)
        self.selected_files = self.all_files = os.listdir(self.directory)
        self.selected_files.sort()
        self.position = 0
        self.page_number = 0
        self.all_files_count = len(self.selected_files)
        self.number_of_pages = int(ceil(self.all_files_count / self.max_rows_in_page))
        self.page = self.selected_files[0: self.max_rows_in_page]

    def go_to_parent(self):
        current_path = Path(self.directory).parent
        self.load_from_directory(current_path)
        self.box.erase()
        if len(self.previous_states) == 0:
            self.position = 0
            self.page_number = 0
        else:
            previous_state = self.previous_states.pop()
            self.position = previous_state.position
            self.page_number = previous_state.page_number

    def handle_open(self):
        selected_file = self.directory + self.systemPathSeparator + self.page[self.position]
        if os.path.isdir(selected_file):
            self.box.erase()
            self.directory = selected_file
            self.previous_states.append(State(self))
            self.load_from_directory(selected_file)
        else:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', selected_file))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(selected_file)
            else:  # linux variants
                subprocess.call(('xdg-open', selected_file))

    def print(self):
        self.max_rows_in_page, self.max_cols = self.box.getmaxyx()
        self.max_rows_in_page = self.max_rows_in_page - 2
        self.number_of_pages = int(ceil(self.all_files_count / self.max_rows_in_page))
        start_element_index = self.page_number * self.max_rows_in_page
        if start_element_index < 0:
            start_element_index = 0
        self.page = self.selected_files[start_element_index: start_element_index + self.max_rows_in_page]
        if self.focused:
            self.box.border(0)
        else:
            self.box.border(':', ':', ' ', '.', ' ', ' ', ' ', ' ')
        self.box.addstr(0, 1, self.directory[: self.max_cols - 2])
        for self.current_number_of_elements, element in enumerate(self.page):
            croped_element = element[: self.max_cols - 3]
            if self.current_number_of_elements == self.position:
                self.box.addstr(self.current_number_of_elements + 1, 2, croped_element, self.fonts.cursor_style)
            elif os.path.isdir(self.directory + self.systemPathSeparator + element):
                self.box.addstr(self.current_number_of_elements + 1, 2, croped_element, self.fonts.directory_style)
            else:
                self.box.addstr(self.current_number_of_elements + 1, 2, croped_element, self.fonts.normal_text)
        self.box.refresh()

    def filter(self):
        Filter(self).handle_filtering()

    def set_selected_files(self, selected_files):
        self.selected_files = selected_files
        self.position = 0
        self.page_number = 0
        self.all_files_count = len(self.selected_files)
        self.number_of_pages = int(ceil(self.all_files_count / self.max_rows_in_page))

    def handle_go_up(self):
        if self.position == 0 and self.page_number == 0:
            return

        self.position = self.position - 1
        if self.position < 0:
            if self.page_number > 0:
                self.page_number = self.page_number - 1
                self.box.erase()
                self.box.refresh()
            self.position = self.position % self.max_rows_in_page
            start_element_index = self.page_number * self.max_rows_in_page
            if start_element_index < 0:
                start_element_index = 0
            self.page = self.selected_files[start_element_index: start_element_index + self.max_rows_in_page]

    def handle_go_down(self):
        if self.position + 1 < len(self.page):
            self.position = self.position + 1
        elif self.position + 1 >= len(self.page) and self.page_number + 1 < self.number_of_pages:
            self.position = 0
            self.page_number = self.page_number + 1
            self.box.erase()
            self.box.refresh()

    def resize(self, height, width):
        self.log("")
        self.box.erase()
        self.box.resize(height, width)
        current_position = (self.page_number * self.max_rows_in_page) + self.position
        self.log("current position %s" % current_position)
        self.all_files_count = len(self.selected_files)
        self.max_rows_in_page, self.max_cols = self.box.getmaxyx()
        self.max_rows_in_page = self.max_rows_in_page - 2
        self.number_of_pages = int(ceil(self.all_files_count / self.max_rows_in_page))
        self.position = current_position % self.max_rows_in_page
        self.page_number = int(current_position / self.max_rows_in_page)
        self.print()
        self.box.refresh()

    def move(self, y, x):
        self.box.mvwin(y, x)
        self.box.refresh()

    def gethw(self):
        return self.box.getmaxyx()

    def log(self, msg):
        self.log_file.write("[%s]%s\n" % (datetime.datetime.now(), msg))
        self.log_file.flush()


class Fonts:
    def __init__(self, crs):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        self.cursor_style = curses.color_pair(1)
        self.directory_style = curses.color_pair(2)
        self.normal_text = curses.A_NORMAL


class State:

    def __init__(self, list_files_box):
        self.position = list_files_box.position
        self.page_number = list_files_box.page_number
