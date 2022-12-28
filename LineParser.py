class LineParser:
    def __init__(self, line):
        self.line = line
        self.first_arg = None
        self.second_arg = None
        self.third_arg = None
        self.parse()

    # Parse line and store first, second and third argument in first_arg, second_arg and third_arg.
    # The line is split by one or more spaces
    # The third argument is optional
    def parse(self):
        # Split the line by \t or space and remove \n if it exists
        line = self.line.replace("\n", "").split()
        if len(line) < 1:
            return
        self.first_arg = line[0]
        self.second_arg = line[1]
        if len(line) > 2:
            self.third_arg = line[2]

    def get_first_arg(self):
        return self.first_arg

    def get_second_arg(self):
        return self.second_arg

    def get_third_arg(self):
        return self.third_arg

    def __contains__(self, item):
        return item in self.line
