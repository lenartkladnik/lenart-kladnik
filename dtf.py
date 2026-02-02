'''
An implementation of the Dynamic Text Format.

This implementation and format are made by Lenart Kladnik
(https://github.com/lenartkladnik)
2026
'''

import os.path
import re

_IDENTIFIER = "identifier"
_KEYWORD = "keyword"
_TEXT = "text"
_ansi_str = re.compile(r'\x1b\[[0-?]*[ -\/]*[@-~]')

class DynamicTextFormatError(Exception):...

class Options:
    template_folder = "templates/"

def _remove_ansi(string: str):
    removed = _ansi_str.sub('', string)

    return removed

def _visual_len(string: str) -> int:
    return len(_remove_ansi(string))

def _visual_ljust(string: str, width: int) -> str:
    if len(string) < 1:
        return string.rjust(width)

    non_ansi = _remove_ansi(string).ljust(width, "\x00")
    right = 0

    for i in non_ansi[::-1]:
        if i != "\x00":
            break
        right += 1

    return string + " " * right

def _side_to_side(rendered: list[list[str]], gap: int = 0, padding: int = 0, padding_left: int = 0, padding_right: int = 0, padding_top: int = 0, padding_bottom: int = 0) -> str:
    padding_left = max(padding_left + padding, 0)
    padding_right = max(padding_right + padding, 0)
    padding_top = max(padding_top + padding, 0)
    padding_bottom = max(padding_bottom + padding, 0)

    max_height = len(max(rendered, key=len))

    for i in range(len(rendered)): # Set all to same height
        rendered[i] += ["" for _ in range(max_height - rendered[i].count('\n'))]

    widths = [_visual_len(max(each, key=_visual_len)) for each in rendered]

    final = []
    line = ""

    for i in range(max_height):
        for j, each in enumerate(rendered):
            if i < len(each):
                line += _visual_ljust(each[i], widths[j]) + " " * gap

        final.append(" " * padding_left + line.rstrip() + " " * padding_right)
        line = ""

    return "\n" * padding_top + "\n".join(final) + "\n" * padding_bottom

def _clean_text(text: str) -> str:
    for i in ["{%", "%}"]:
        text = text.replace("\n" + i + "\n", "")
        text = text.replace(i + "\n", "")
        text = text.replace("\n" + i, "")
        text = text.replace(i, "")

    for i in ["{{", "}}"]:
        text = text.replace(i, "")

    for i in [("{\\{", "{{"), ("}\\}", "}}"), ("{\\%", "{%"), ("%\\}", "%}")]:
        text = text.replace(i[0], i[1])

    return text

def _tokenize_text(path: str, content: str) -> ...:
    tokens = []

    context = []
    text = []

    line = 1

    for idx, ch in enumerate(content):
        if idx < len(content) - 1:
            if ch == "{" and content[idx + 1] == "{":
                context.append([_IDENTIFIER, "", line])

            if ch == "{" and content[idx + 1] == "%":
                context.append([_KEYWORD, "", line])

            if ch == "}" and content[idx + 1] == "}":
                if context[-1][0] != _IDENTIFIER:
                    raise DynamicTextFormatError(f"{path}:{line} Expected '%}}' not '}}}}'")

                tokens.append(context.pop())

            if ch == "%" and content[idx + 1] == "}":
                if context[-1][0] != _KEYWORD:
                    raise DynamicTextFormatError(f"{path}:{line} Expected '}}}}' not '%}}'")

                tokens.append(context.pop())

        if context:
            if text:
                tokens.append([_TEXT, "".join(text), line])
                text = []

            context[-1][1] += ch

        else:
            text.append(ch)

        if ch == "\n": line += 1

    if text:
        tokens.append([_TEXT, "".join(text), line])

    return [
        [
            idf,
            _clean_text(val) if idf == _TEXT else _clean_text(val).strip(),
            ln,
        ]
        for idf, val, ln in tokens
    ]

def _parse_text(path: str, tokens: list[set[str]], **context) -> str:
    content = ""

    keyword_depth = 0
    exec_str = ""

    for token in tokens:
        idf, value, line = token

        if keyword_depth == 0 and exec_str:
            exec("_DTF_RESULT_STRING=\"\"\n" + exec_str, context)
            content += context["_DTF_RESULT_STRING"]

            exec_str = ""

        if keyword_depth > 0:
            if idf == _TEXT:
                exec_str += value.replace("\n", "\\n")

            elif idf == _IDENTIFIER:
                exec_str += "\"\"\" + str(" + value.replace("\n", "\\n") + ") + \"\"\""

            elif idf == _KEYWORD:
                if value == "end":
                    if keyword_depth == 0:
                        raise DynamicTextFormatError(f"{path}:~{line} Nothing to end")

                    keyword_depth -= 1

                    if keyword_depth == 0:
                        exec_str += "\"\"\"\n"

                else:
                    exec_str += "\"\"\"\n"
                    exec_str += "\t" * keyword_depth + value.replace("\n", "\\n") + ":\n" + "\t" * (keyword_depth + 1) + "_DTF_RESULT_STRING += \"\"\""
                    keyword_depth += 1

        elif idf == _TEXT:
            content += value

        elif idf == _IDENTIFIER:
            try:
                if ("[" in value and "]" in value) or ("(" in value and ")" in value):
                    content += eval(value, context)

                else:
                    content += context[value]

            except KeyError:
                raise DynamicTextFormatError(f"{path}:~{line} '{value}' is not defined")

        elif idf == _KEYWORD:
            if value.startswith("set "):
                try:
                    exec(value.split("set ")[1], context)
                except IndexError:
                    raise DynamicTextFormatError(f"{path}:~{line} '{value}' is incomplete")

            elif value.startswith("include "):
                try:
                    rendered = []
                    render_paths = []
                    current = ""
                    in_quotes = False

                    for i in value.split("include ")[1]:
                        if i == '"':
                            if current:
                                render_paths.append(current)
                                current = ""
                            in_quotes = not in_quotes

                        elif in_quotes:
                            current += i

                    for render_path in render_paths:
                        rendered.append(render_text(render_path, **context).split("\n"))

                    kwargs = {}
                    if "with " in value:
                        for i in value.split("with ")[1].replace(", ", " ").replace(",", " ").replace(" = ", "=").replace(" =", "=").replace("= ", "=").split(" "):
                            arg = i.split("=")
                            kwargs.update({arg[0]: eval(arg[1], context)})

                    content += _side_to_side(rendered, **kwargs)

                except IndexError:
                    raise DynamicTextFormatError(f"{path}:~{line} '{value}' is incomplete. Maybe you missed a '\"' in the path?")
                except Exception as e:
                    raise DynamicTextFormatError(f"{path}:~{line} '{value}' failed with exception: {e}")

            elif value == "end":
                raise DynamicTextFormatError(f"{path}:~{line} Nothing to end")

            else:
                exec_str = value.replace("\n", "\\n") + ":\n" + "\t_DTF_RESULT_STRING += \"\"\""
                keyword_depth = 1

    return content

def render_text(path_or_text: str, **context):
    path = os.path.join(Options.template_folder, path_or_text)
    if os.path.exists(path):
        if not path.endswith(".dtf"):
            raise RuntimeError("Path for render_text must be a .dtf file")

        contents = None
        with open(path) as f:
            contents = f.read()

    else:
        path = "Text"
        contents = path_or_text

    if not contents:
        return ""

    tokens = _tokenize_text(path, contents)
    result = _parse_text(path, tokens, **context)

    return result

