import curses


class Filter:

    def __init__(self, box) -> None:
        self.box = box

        self.search_style = curses.color_pair(3)
        self.box_height, self.box_width = self.box.box.getmaxyx()

    def handle_filtering(self):
        searching_string = ""
        while True:
            self.render(searching_string)

            search_input = self.box.box.getch()

            if search_input in [ord("\n"), curses.KEY_UP, curses.KEY_DOWN]:  # TODO ENTER
                break
            elif search_input == 27:
                self.box.set_selected_files(self.box.all_files)
                break
            elif search_input in [curses.KEY_BACKSPACE, ord('\b')] or str(search_input) == "127":  # BACKSPACE
                searching_string = searching_string[:-1]
            else:
                input_character = chr(search_input)
                searching_string += input_character

    def render(self, searching_string):
        self.box.box.erase()
        self.box.box.border(0)
        if searching_string == "":  # TODO add handling weird signs :)
            self.box.set_selected_files(self.box.all_files)
        else:
            self.box.set_selected_files(
                list(filter(lambda file: searching_string.lower() in file.lower(), self.box.all_files)))
        self.box.print()
        self.box.box.addstr(self.box_height - 1, 2, "█" + searching_string, self.search_style)
        self.box.box.refresh()
