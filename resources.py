from typing import cast
from dtf import _side_to_side, _remove_ansi, _visual_len, _visual_ljust

ESC = "\033"

def _color_id(color: str) -> int:
    match color:
        case "white": return 255
        case "black": return 0
        case "mid-black": return 16
        case "text": return 223
        case "dark-gray": return 234
        case "gray": return 236
        case "mid-gray": return 242
        case "light-gray": return 248
        case "black": return 16
        case "light-gray": return 242
        case "purple": return 129
        case "light-purple": return 127
        case "mid-purple": return 128
        case "dark-purple": return 171
        case "darker-purple": return 92
        case "magenta": return 212
        case "aqua": return 81
        case "lime": return 154
        case "blue": return 33
        case "mid-blue": return 26
        case "dark-blue": return 18
        case "light-blue": return 68
        case "yellow": return 220
        case "orange": return 202

    return -1 # Invalid color

def color(color: str) -> str:
    id = _color_id(color)
    if id >= 0:
        return f"{ESC}[38;5;{id}m"
    else:
        return ""

def background_color(color: str) -> str:
    match color:
        case "transparent": return ESC+"[49m"

    id = _color_id(color)
    if id >= 0:
        return f"{ESC}[48;5;{id}m"
    else:
        return ""

def bold() -> str:
    return ESC+"[1m"

def italic() -> str:
    return ESC+"[3m"

def end_italic() -> str:
    return ESC+"[23m"

def end_color() -> str:
    return ESC+"[0m"

def save_cursor() -> str:
    return ESC+" 7"

def restore_cursor() -> str:
    return ESC+" 8"

def left(amount: int) -> str:
    return ESC+f"[{amount}D"

def right(amount: int) -> str:
    return ESC+f"[{amount}C"

remove_ansi = _remove_ansi
visual_len = _visual_len
side_to_side = _side_to_side
visual_ljust = _visual_ljust

def visual_center(string: str, width: int) -> str:
    if len(string) < 1:
        return string.center(width)

    non_ansi = remove_ansi(string).center(width, "\x00")
    left = 0
    right = 0

    for i in non_ansi:
        if i != "\x00":
            break
        left += 1

    for i in non_ansi[::-1]:
        if i != "\x00":
            break
        right += 1

    return " " * left + string + " " * right

def visual_rjust(string: str, width: int) -> str:
    if len(string) < 1:
        return string.rjust(width)

    non_ansi = remove_ansi(string).rjust(width, "\x00")
    left = 0

    for i in non_ansi:
        if i != "\x00":
            break
        left += 1

    return " " * left + string

def box(data: str | list[str] | list[list[str]], title: str | None = None, padding_left: int = 0, padding_right: int = 0, padding_top: int = 0, padding_bottom: int = 0, align: str = "center") -> str:
    if isinstance(data, str):
        data = [data]

    elif isinstance(data, list):
        if all(isinstance(x, list) for x in data):
            data = ["\n".join(x) for x in data]

    data = cast(list[str], data) # Tell the type checker that we have converted str and list[list[str]] data inputs to list[str]

    max_height = len(max(map(lambda x: x.split('\n'), data), key=len))
    for i in range(len(data)): # Set all to the same height
        data[i] += "\n" * (max_height - data[i].count('\n'))

    widths = [visual_len(max(x.split("\n"), key=visual_len)) + padding_right + padding_left for x in data]

    box_list = ['' for _ in range(max_height + padding_top + padding_bottom + 2)]

    align_func = lambda *args: args[0] # Simple identity function (for the first argument), so that if no align is supplied the program doesn't crash
    if align == "center":
        align_func = visual_center

    elif align == "right":
        align_func = visual_rjust

    elif align == "left":
        align_func = visual_ljust

    idx = 0
    for i, width in enumerate(widths):
        if not title:
            box_list[idx] += f"{color('light-gray')}{'╭' if i == 0 else ''}{'─' * (width + padding_left + padding_right)}{'╮' if i == len(widths) - 1 else '┬'}{end_color()}"

        else:
            if visual_len(title) + 1 > width:
                widths[i] = visual_len(title) + 1 + padding_left + padding_right

            box_list[idx] += f"{color('light-gray')}{f'╭─{color('text')}{title}{color('light-gray')}' if i == 0 else ''}{'─' * ((width + padding_left + padding_right) - visual_len(title) - 1 if i == 0 else (width + padding_left + padding_right))}{'╮' if i == len(widths) - 1 else '┬'}{end_color()}"

    for i in range(padding_top):
        idx += 1
        for j, each in enumerate(data):
            box_list[idx] += f"{color('light-gray')}│{end_color()}{' ' * padding_left}{' ' * widths[j]}{' ' * padding_right}{f'{color('light-gray')}│{end_color()}' if j == len(data) - 1 else ''}"

    for i in range(max_height):
        idx += 1
        for j, each in enumerate(data):
            box_list[idx] += f"{color('light-gray')}│{end_color()}{' ' * padding_left}{align_func(each.split("\n")[i], widths[j])}{' ' * padding_right}{f'{color('light-gray')}│{end_color()}' if j == len(data) - 1 else ''}"

    for i in range(padding_bottom):
        idx += 1
        for j, each in enumerate(data):
            box_list[idx] += f"{color('light-gray')}│{end_color()}{' ' * padding_left}{' ' * widths[j]}{' ' * padding_right}{f'{color('light-gray')}│{end_color()}' if j == len(data) - 1 else ''}"

    idx += 1
    for i, width in enumerate(widths):
        box_list[idx] += f"{color('light-gray')}{'╰' if i == 0 else ''}{'─' * (width + padding_left + padding_right)}{'╯' if i == len(widths) - 1 else '┴'}{end_color()}"

    return "\n".join(box_list)
