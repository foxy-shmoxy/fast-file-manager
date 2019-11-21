class Filter:

    def __init__(self, curses, box, possibilities, render_files) -> None:
        self.curses = curses
        self.box = box
        self.filtered_files = self.files = possibilities
        self.render_files = render_files

        self.search_style = curses.color_pair(3)
        self.box_height, self.box_width = self.box.getmaxyx()

    def handle_filtering(self):
        searching_string = ""
        while True:
            self.render(searching_string)

            search_input = self.box.getch()

            if search_input in [ord("\n"), self.curses.KEY_UP, self.curses.KEY_DOWN]:  # TODO ENTER
                return self.filtered_files
            elif search_input == 27:
                pass
                # return self.files
            elif search_input in [self.curses.KEY_BACKSPACE, ord('\b')] or str(search_input) == "127":  # BACKSPACE
                searching_string = searching_string[:-1]
            else:
                input_character = chr(search_input)
                searching_string += input_character

    def render(self, searching_string):
        self.box.erase()
        self.box.border(0)
        self.box.addstr(self.box_height - 1, 2, "█" + searching_string, self.search_style)
        if searching_string == "":  # TODO add handling weird signs :)
            self.filtered_files = self.files
        else:
            self.filtered_files = list(filter(lambda file: searching_string.lower() in file.lower(), self.files))
        self.render_files(self.filtered_files)
        self.box.refresh()
