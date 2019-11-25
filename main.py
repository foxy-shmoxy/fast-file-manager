# A lot of stuff to refactor. Just starting learning curses so.... a lot of mess
import curses, os
from math import *
from list_files_box import ListFilesBox

screen = curses.initscr()
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
box = curses.newwin(height, width, 0, 0)  # TODO this 10 have to be calculated
box.keypad(1)
box.box()

list_files_box = ListFilesBox(box, cursor_style, directory_style, normalText)

screen.refresh()

while True:
    list_files_box.print()
    x = screen.getch()
    if x == 27:
        break
    if x == curses.KEY_DOWN:
        if list_files_box.page == 1:
            # screen.addstr(17, 1, ("position %s i = %s" % (position, i))[:50], cursor_style)
            if list_files_box.position < list_files_box.current_number_of_elements:
                list_files_box.position = list_files_box.position + 1
            else:
                if list_files_box.pages > 1:
                    list_files_box.page = list_files_box.page + 1
                    list_files_box.position = 1 + (list_files_box.max_row * (list_files_box.page - 1))
        elif list_files_box.page == list_files_box.pages:
            if list_files_box.position < list_files_box.row_num:
                list_files_box.position = list_files_box.position + 1
        else:
            if list_files_box.position < list_files_box.max_row + (list_files_box.max_row * (list_files_box.page - 1)):
                list_files_box.position = list_files_box.position + 1
            else:
                list_files_box.page = list_files_box.page + 1
                list_files_box.position = 1 + (list_files_box.max_row * (list_files_box.page - 1))
    if x == curses.KEY_UP:
        if list_files_box.page == 1:
            if list_files_box.position > 1:
                list_files_box.position = list_files_box.position - 1
        else:
            if list_files_box.position > (1 + (list_files_box.max_row * (list_files_box.page - 1))):
                list_files_box.position = list_files_box.position - 1
            else:
                list_files_box.page = list_files_box.page - 1
                list_files_box.position = list_files_box.max_row + (list_files_box.max_row * (list_files_box.page - 1))
    if x == curses.KEY_LEFT:
        if list_files_box.page > 1:
            list_files_box.page = list_files_box.page - 1
            list_files_box.position = 1 + (list_files_box.max_row * (list_files_box.page - 1))

    if x == curses.KEY_RIGHT:
        if list_files_box.page < list_files_box.pages:
            list_files_box.page = list_files_box.page + 1
            list_files_box.position = (1 + (list_files_box.max_row * (list_files_box.page - 1)))
    if str(x) == "263":  # BACKSPACE - TODO constant here
        list_files_box.go_to_parent()
    if str(chr(x)) == "/":  # SLASH - search
        list_files_box.filter()
    if x == ord("\n") and list_files_box.row_num != 0:
        list_files_box.go_to_selected_directory()

curses.endwin()
exit()
