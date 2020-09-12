class CodeText:
    def __init__(self, text, width, lines):
        self.text = text
        self.width = width
        self.lines = lines
        self.width_pixels = 0
        self.height_pixels = 0
        self.state = "OK"
