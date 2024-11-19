ANSI_RESET = "\033[0m"

ANSI_STYLES = {
    'BOLD': '1',
    'ITALIC': '3',
    'UNDERLINE': '4',
    'NORMAL': '0'
}

ANSI_COLORS = {
    'RED': '31',
    'GREEN': '32',
    'YELLOW': '33',
    'BLUE': '34',
    'MAGENTA': '35',
    'CYAN': '36',
    'WHITE': '37',
    'BRIGHT_RED': '91',
    'BRIGHT_GREEN': '92',
    'BRIGHT_YELLOW': '93',
    'BRIGHT_BLUE': '94',
    'BRIGHT_MAGENTA': '95',
    'BRIGHT_CYAN': '96',
    'BRIGHT_WHITE': '97',
}

def ansi_style_(style_code):
    def style_(text):
        if text.startswith("\033["):
            text = text[len("\033["):]
            current_seq, text = text.split("m", 1)
            return f'\033[{style_code};{current_seq}m{text}{ANSI_RESET}'
        return f'\033[{style_code}m{text}{ANSI_RESET}'
    return style_

def ansi_color_(color_code):
    def color_(text, style=None):
        style_code = ANSI_STYLES['NORMAL']
        if text.startswith("\033["):
            text = text[len("\033["):]
            current_seq, text = text.split("m", 1)
            ansiseq = f'\033[{current_seq};{color_code}m{text}{ANSI_RESET}'
        elif style:
            if style.upper() in ANSI_STYLES:
                style_code = ANSI_STYLES[style.upper()]
            else:
                raise ValueError(f"Invalid style: {style}")
            ansiseq = f'\033[{style_code};{color_code}m{text}{ANSI_RESET}'
        else:
            ansiseq = f'\033[{color_code}m{text}{ANSI_RESET}'
        return ansiseq
    return color_

bold_ = ansi_style_(ANSI_STYLES['BOLD'])
italic_ = ansi_style_(ANSI_STYLES['ITALIC'])
underline_ = ansi_style_(ANSI_STYLES['UNDERLINE'])

red_ = ansi_color_(ANSI_COLORS['RED'])
green_ = ansi_color_(ANSI_COLORS['GREEN'])
yellow_ = ansi_color_(ANSI_COLORS['YELLOW'])
blue_ = ansi_color_(ANSI_COLORS['BLUE'])
magenta_ = ansi_color_(ANSI_COLORS['MAGENTA'])
cyan_ = ansi_color_(ANSI_COLORS['CYAN'])
white_ = ansi_color_(ANSI_COLORS['WHITE'])

bright_red_ = ansi_color_(ANSI_COLORS['BRIGHT_RED'])
bright_green_ = ansi_color_(ANSI_COLORS['BRIGHT_GREEN'])
bright_yellow_ = ansi_color_(ANSI_COLORS['BRIGHT_YELLOW'])
bright_blue_ = ansi_color_(ANSI_COLORS['BRIGHT_BLUE'])
bright_magenta_ = ansi_color_(ANSI_COLORS['BRIGHT_MAGENTA'])
bright_cyan_ = ansi_color_(ANSI_COLORS['BRIGHT_CYAN'])
bright_white_ = ansi_color_(ANSI_COLORS['BRIGHT_WHITE'])

print(italic_(bright_green_("italic bright green")))
print(green_(underline_("green underline")))
print(red_("red, bold", 'bold'))
print(underline_(italic_(blue_("underline italic blue"))))
print(underline_(italic_(blue_("underline italic blue, bold", 'bold'))))

