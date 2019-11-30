# A lot of stuff to refactor. Just starting learning curses so.... a lot of mess
import curses, os
from math import *
from list_files_box import ListFilesBox


def create_box(curses, y, x):
    box = curses.newwin(height, width, y, x)
    box.keypad(1)
    box.box()
    return box


def log(msg):
    log_file.write("%s\n" % msg)
    log_file.flush()


log_file = open("logs.txt", "w")
screen = curses.initscr()
minimal_panel_width = 15
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
cursor_style = curses.color_pair(1)
directory_style = curses.color_pair(2)
normalText = curses.A_NORMAL
curses.curs_set(0)
height, width = screen.getmaxyx()
box = create_box(curses, 0, 0)

focused_element = ListFilesBox(box, cursor_style, directory_style, normalText, log_file=log_file)
layout = [[focused_element]]
current_col_focused = 0
current_row = layout[current_col_focused]

screen.refresh()

while True:
    height, width = screen.getmaxyx()
    focused_element.print()
    x = screen.getch()
    if x == 27:
        break
    if x == curses.KEY_DOWN:
        focused_element.key_down()
    if x == curses.KEY_UP:
        focused_element.key_up()
    if x == curses.KEY_LEFT:
        if focused_element.page_number > 1:
            focused_element.page_number = focused_element.page_number - 1
            focused_element.position = 1 + (focused_element.max_row * (focused_element.page_number - 1))
    if x == curses.KEY_RIGHT:
        if focused_element.page_number < focused_element.pages:
            focused_element.page_number = focused_element.page_number + 1
            focused_element.position = (1 + (focused_element.max_row * (focused_element.page_number - 1)))
    if str(x) == "263":  # BACKSPACE -
        focused_element.go_to_parent()
    if str(chr(x)) == "/":  # SLASH - search
        focused_element.filter()
    if str(chr(x)) == "h":
        if current_col_focused != 0:
            current_col_focused = current_col_focused - 1
            focused_element = current_row[current_col_focused]
    if str(chr(x)) == "l":
        if current_col_focused != len(current_row) - 1:
            current_col_focused = current_col_focused + 1
            focused_element = current_row[current_col_focused]
    if str(chr(x)) == "v":  # TODO calculate limit of vertical panels
        size_of_one_window = int(width / len(current_row) + 1)
        if size_of_one_window < minimal_panel_width:
            continue
        height, width = screen.getmaxyx()
        log("width %s \n" % width)
        new_box = create_box(curses, 0, 0)
        new_file_box = ListFilesBox(new_box, cursor_style, directory_style, normalText, log_file=log_file)
        focused_element = new_file_box
        current_row.append(new_file_box)
        size_of_one_window = int(width / len(current_row))
        windows_size_left_over = width % len(current_row)
        last_panel_position = 0
        current_col_focused = current_col_focused + 1

        for i, file_list_window in enumerate(current_row):
            log("=========== i %s" % i)
            log("left_over %s" % windows_size_left_over)
            log("last %s " % last_panel_position)
            temp_size = size_of_one_window
            if i < windows_size_left_over:
                log("true")
                temp_size = temp_size + 1

            log("temp_size %s" % temp_size)
            file_list_window.resize(height, temp_size)
            file_list_window.move(0, last_panel_position)
            last_panel_position = last_panel_position + temp_size

        for i, file_list_window in enumerate(current_row):
            file_list_window.box.erase()
            file_list_window.print()
            file_list_window.box.refresh()

    if x == ord("\n") and focused_element.row_num != 0:
        focused_element.go_to_selected_directory()

curses.endwin()
exit()
