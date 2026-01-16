import os.path
from resources import side_to_side

class DynamicTextFormatError(Exception):...

class DynamicTextFormat:
    IDENTIFIER = "identifier"
    KEYWORD = "keyword"
    TEXT = "text"

    @staticmethod
    def render_text(path: str, **context):
        if not path.endswith(".dtf"):
            raise RuntimeError("Path for DynamicTextFormat.render_text must be a .dtf file")

        contents = None
        with open(os.path.join("templates", path)) as f:
            contents = f.read()

        if not contents:
            return ""

        tokens = DynamicTextFormat._tokenize_text(path, contents)
        result = DynamicTextFormat._parse_text(path, tokens, **context)

        return result

    @staticmethod
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
                if idf == DynamicTextFormat.TEXT:
                    exec_str += value.replace("\n", "\\n")

                elif idf == DynamicTextFormat.IDENTIFIER:
                    exec_str += "\"\"\" + str(" + value.replace("\n", "\\n") + ") + \"\"\""

                elif idf == DynamicTextFormat.KEYWORD:
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

            elif idf == DynamicTextFormat.TEXT:
                content += value

            elif idf == DynamicTextFormat.IDENTIFIER:
                try:
                    if ("[" in value and "]" in value) or ("(" in value and ")" in value):
                        content += eval(value, context)

                    else:
                        content += context[value]

                except KeyError:
                    raise DynamicTextFormatError(f"{path}:~{line} '{value}' is not defined")

            elif idf == DynamicTextFormat.KEYWORD:
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
                            rendered.append(DynamicTextFormat.render_text(render_path, **context).split("\n"))

                        kwargs = {}
                        if "with " in value:
                            for i in value.split("with ")[1].replace(" = ", "=").replace(" =", "=").replace("= ", "=").split(" "):
                                arg = i.split("=")
                                kwargs.update({arg[0]: eval(arg[1], context)})

                        content += side_to_side(rendered, **kwargs)

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

    @staticmethod
    def _tokenize_text(path: str, content: str) -> ...:
        tokens = []

        context = []
        text = []

        line = 1

        for idx, ch in enumerate(content):
            if idx < len(content) - 1:
                if ch == "{" and content[idx + 1] == "{":
                    context.append([DynamicTextFormat.IDENTIFIER, "", line])

                if ch == "{" and content[idx + 1] == "%":
                    context.append([DynamicTextFormat.KEYWORD, "", line])

                if ch == "}" and content[idx + 1] == "}":
                    if context[-1][0] != DynamicTextFormat.IDENTIFIER:
                        raise DynamicTextFormatError(f"{path}:{line} Expected '%}}' not '}}}}'")

                    tokens.append(context.pop())

                if ch == "%" and content[idx + 1] == "}":
                    if context[-1][0] != DynamicTextFormat.KEYWORD:
                        raise DynamicTextFormatError(f"{path}:{line} Expected '}}}}' not '%}}'")

                    tokens.append(context.pop())

            if context:
                if text:
                    tokens.append([DynamicTextFormat.TEXT, "".join(text), line])
                    text = []

                context[-1][1] += ch

            else:
                text.append(ch)

            if ch == "\n": line += 1

        if text:
            tokens.append([DynamicTextFormat.TEXT, "".join(text), line])

        return [
            [
                idf,
                DynamicTextFormat._clean_text(val) if idf == DynamicTextFormat.TEXT else DynamicTextFormat._clean_text(val).strip(),
                ln,
            ]
            for idf, val, ln in tokens
        ]

    @staticmethod
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
