# A lot of stuff to refactor. Just starting learning curses so.... a lot of mess
import curses
import datetime
from list_files_box import ListFilesBox, Fonts


def log(msg):
    log_file.write("[%s]%s\n" % (datetime.datetime.now(), msg))
    log_file.flush()


log_file = open("logs.txt", "w")
screen = curses.initscr()
minimal_panel_width = 20
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.curs_set(0)
height, width = screen.getmaxyx()
fonts = Fonts(curses)
focused_element = ListFilesBox(curses, height, width, 0, 0, fonts, log_file=log_file)
layout = [[focused_element]]
current_col_focused = 0
current_row = layout[current_col_focused]

screen.refresh()

while True:
    height, width = screen.getmaxyx()
    focused_element.print()
    x = screen.getch()
    log("x %s" % x)
    if x == 27:
        break
    elif x == curses.KEY_DOWN or str(chr(x)) == "j":
        focused_element.handle_go_down()
    elif x == curses.KEY_UP or str(chr(x)) == "k":
        focused_element.handle_go_up()
    elif x == 263:  # BACKSPACE -
        focused_element.go_to_parent()
    elif str(chr(x)) == "/":  # SLASH - search
        focused_element.filter()
    elif str(chr(x)) == "H":
        if current_col_focused != 0:
            current_col_focused = current_col_focused - 1
            focused_element = current_row[current_col_focused]
            for i, file_list_window in enumerate(current_row):
                if i == current_col_focused:
                    file_list_window.focused = True
                else:
                    file_list_window.focused = False
                file_list_window.print()
    elif str(chr(x)) == "L":
        if current_col_focused != len(current_row) - 1:
            current_col_focused = current_col_focused + 1
            focused_element = current_row[current_col_focused]
            for i, file_list_window in enumerate(current_row):
                if i == current_col_focused:
                    file_list_window.focused = True
                else:
                    file_list_window.focused = False
                file_list_window.print()
    elif str(chr(x)) == "v":  # TODO calculate limit of vertical panels
        size_of_one_window = int(width / len(current_row))
        if size_of_one_window < minimal_panel_width:
            continue
        height, width = screen.getmaxyx()
        new_file_box = ListFilesBox(curses, height, width, 0, 0, fonts, log_file=log_file)
        focused_element = new_file_box
        current_row.append(new_file_box)
        size_of_one_window = int(width / len(current_row))
        windows_size_left_over = width % len(current_row)
        last_panel_position = 0
        current_col_focused = current_col_focused + 1

        for i, file_list_window in enumerate(current_row):
            temp_size = size_of_one_window
            if i < windows_size_left_over:
                temp_size = temp_size + 1

            file_list_window.resize(height, temp_size)
            file_list_window.move(0, last_panel_position)
            last_panel_position = last_panel_position + temp_size

        for i, file_list_window in enumerate(current_row):
            if i == current_col_focused:
                file_list_window.focused = True
            else:
                file_list_window.focused = False
            file_list_window.box.erase()
            file_list_window.print()
            file_list_window.box.refresh()

    elif (x == ord("\n") or x == 111) and focused_element.all_files_count != 0:
        focused_element.handle_open()
    elif x == 410:  # window resizing
        screen.refresh()
        for i, file_list_window in enumerate(current_row):
            if i == current_col_focused:
                file_list_window.focused = True
            else:
                file_list_window.focused = False
            file_list_window.box.erase()
            file_list_window.print()

curses.endwin()
exit()
