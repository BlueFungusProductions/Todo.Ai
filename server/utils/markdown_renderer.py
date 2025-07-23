from typing import List

from api.ai.types import AIDirective
from markdown_it.token import Token


class MarkdownRenderer:
    def render(self, tokens: List[Token], directives: List[AIDirective]) -> str:
        directive_map = {d.position: d for d in directives if d.position is not None}
        markdown_lines = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == "heading_open":
                level = int(token.tag[1])
                next_token = tokens[i + 1] if i + 1 < len(tokens) else None
                if next_token and next_token.type == "inline":
                    markdown_lines.append(f"{'#' * level} {next_token.content}")
                    i += 2  # skip inline and heading_close
                else:
                    i += 1
            elif token.type == "paragraph_open":
                i += 1  # skip to inline
            elif token.type == "inline":
                markdown_lines.append(token.content)
                i += 1
            elif token.type == "html_block":
                markdown_lines.append(token.content)
                i += 1
            elif token.type == "container_Todo.Ai_open":
                directive = directive_map.get(i)
                if directive:
                    markdown_lines.append(directive.resolve())
                i += 1
            elif token.type == "container_Todo.Ai_close":
                i += 1
            elif token.type in ("paragraph_close", "heading_close"):
                if i + 1 < len(tokens) and tokens[i + 1].type in {"heading_open", "paragraph_open", "container_Todo.Ai_open"}:
                    markdown_lines.append("")
                i += 1
            else:
                i += 1
        return "\n".join(markdown_lines)


__all__ = ["MarkdownRenderer"]