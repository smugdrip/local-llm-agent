class Color:
    # ANSI Escape Codes
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"  # Note: Not all terminals support this

    def __init__(self):
        pass

    def color(self, codes, text):
        """Apply multiple ANSI codes to text."""
        code_str = ";".join(codes)
        return f"\033[{code_str}{text}\033[0m"

    def red(self, text):
        return self.color([self.RED], text)

    def green(self, text):
        return self.color([self.GREEN], text)

    def yellow(self, text):
        return self.color([self.YELLOW], text)

    def blue(self, text):
        return self.color([self.BLUE], text)

    def magenta(self, text):
        return self.color([self.MAGENTA], text)

    def cyan(self, text):
        return self.color([self.CYAN], text)

    def white(self, text):
        return self.color([self.WHITE], text)

    def black(self, text):
        return self.color([self.BLACK], text)

    def bg_red(self, text):
        return self.color([self.BG_RED], text)

    def bg_green(self, text):
        return self.color([self.BG_GREEN], text)

    def bg_yellow(self, text):
        return self.color([self.BG_YELLOW], text)

    def bg_blue(self, text):
        return self.color([self.BG_BLUE], text)

    def bg_magenta(self, text):
        return self.color([self.BG_MAGENTA], text)

    def bg_cyan(self, text):
        return self.color([self.BG_CYAN], text)

    def bg_white(self, text):
        return self.color([self.BG_WHITE], text)

    def bold(self, text):
        return self.color([self.BOLD], text)

    def underline(self, text):
        return self.color([self.UNDERLINE], text)

    def blink(self, text):
        return self.color([self.BLINK], text)

    def reverse(self, text):
        return self.color([self.REVERSE], text)

    def hidden(self, text):
        return self.color([self.HIDDEN], text)

    def strikethrough(self, text):
        return self.color([self.STRIKETHROUGH], text)

    def bold_underline(self, text):
        return self.color([self.BOLD, self.UNDERLINE], text)

    def bold_red(self, text):
        return self.color([self.BOLD, self.RED], text)
    