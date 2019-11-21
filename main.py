# A lot of stuff to refactor. Just starting learning curses so.... a lot of mess
import curses, os
from math import *
from pathlib import Path
from filter import Filter

systemPathSeparator = os.path.sep
currentPath = homePath = str(Path.home())
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
screen.border(0)
curses.curs_set(0)
max_row = 10  # max number of rows
box = curses.newwin(max_row + 2, 64, 1, 1)  # TODO rename box.... man
box.keypad(1)
box.box()

files = os.listdir(currentPath)
row_num = len(files)

pages = int(ceil(row_num / max_row))
position = 1
page = 1

box.addstr(0, 2, currentPath)
for i in range(1, max_row + 1):
    if row_num == 0:
        box.addstr(1, 1, "There aren't strings", cursor_style)
    else:
        if i == position:
            box.addstr(i, 2, files[i - 1], cursor_style)
        elif os.path.isdir(currentPath + systemPathSeparator + files[i - 1]):
            box.addstr(i, 2, files[i - 1], directory_style)
        else:
            box.addstr(i, 2, files[i - 1], normalText)
        if i == row_num:
            break

screen.refresh()
box.refresh()


def render_list(list_of_files):
    row_num = len(list_of_files)
    for i in range(1 + (max_row * (page - 1)), max_row + 1 + (max_row * (page - 1))):
        if row_num == 0:
            box.addstr(1, 1, "There aren't strings", cursor_style)
        else:
            if i + (max_row * (page - 1)) == position + (max_row * (page - 1)):
                box.addstr(i - (max_row * (page - 1)), 2, list_of_files[i - 1], cursor_style)
            elif os.path.isdir(currentPath + systemPathSeparator + list_of_files[i - 1]):
                box.addstr(i - (max_row * (page - 1)), 2, list_of_files[i - 1], directory_style)
            else:
                box.addstr(i - (max_row * (page - 1)), 2, list_of_files[i - 1], normalText)
            if i == row_num:
                break


x = screen.getch()
while x != 27:  # TODO extract
    if x == curses.KEY_DOWN:
        if page == 1:
            # screen.addstr(17, 1, ("position %s i = %s" % (position, i))[:50], cursor_style)
            if position < i:
                position = position + 1
            else:
                if pages > 1:
                    page = page + 1
                    position = 1 + (max_row * (page - 1))
        elif page == pages:
            if position < row_num:
                position = position + 1
        else:
            if position < max_row + (max_row * (page - 1)):
                position = position + 1
            else:
                page = page + 1
                position = 1 + (max_row * (page - 1))
    if x == curses.KEY_UP:
        if page == 1:
            if position > 1:
                position = position - 1
        else:
            if position > (1 + (max_row * (page - 1))):
                position = position - 1
            else:
                page = page - 1
                position = max_row + (max_row * (page - 1))
    if x == curses.KEY_LEFT:
        if page > 1:
            page = page - 1
            position = 1 + (max_row * (page - 1))

    if x == curses.KEY_RIGHT:
        if page < pages:
            page = page + 1
            position = (1 + (max_row * (page - 1)))
    if str(x) == "263":  # BACKSPACE - TODO constant here
        screen.erase()
        screen.border(0)
        lastSlashPosition = currentPath.rfind('/')  # todo change to multisystem
        if lastSlashPosition == 0:  # TODO duplicates, duplciates - extract to method
            currentPath = "/"
            files = os.listdir(currentPath)
            page = 1
            position = 1
            row_num = len(files)
            pages = int(ceil(row_num / max_row))
        else:
            currentPath = currentPath[:lastSlashPosition]
            files = os.listdir(currentPath)
            page = 1
            position = 1
            row_num = len(files)
            pages = int(ceil(row_num / max_row))
    if str(chr(x)) == "/":  # SLASH - search
        filter = Filter(curses, box, files, render_list)
        files = filter.handle_filtering()
        position = 1
        page = 1
        row_num = len(files)
        pages = int(ceil(row_num / max_row))
        # box.addstr(max_row + 1, 2, "█", directory_style)
        pass
    if x == ord("\n") and row_num != 0:
        screen.erase()
        screen.border(0)
        # screen.addstr(14, 3, "Selected: '" + files[position - 1])
        if os.path.isdir(currentPath + systemPathSeparator + files[position - 1]):
            currentPath = currentPath + systemPathSeparator + files[position - 1]
            files = os.listdir(currentPath)
            position = 1
            page = 1
            row_num = len(files)
            pages = int(ceil(row_num / max_row))

    box.erase()
    screen.border(0)
    box.border(0)

    # screen.addstr(16, 3, "x =  " + str(chr(x)))
    box.addstr(0, 2, currentPath)
    render_list(files)
    screen.refresh()
    box.refresh()
    x = screen.getch()

curses.endwin()
exit()
