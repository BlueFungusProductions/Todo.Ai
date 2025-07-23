from api.ai.types import DirectiveBuilder
from markdown_it import MarkdownIt
from mdit_py_plugins.container import container_plugin
from markdown_it.token import Token
import re
from dataclasses import dataclass
from typing import Optional, Union, NamedTuple, List, Dict, Any
from server.api.ai.contextmaker import AIContextBuilder, AIDirective
from server.utils.markdown_renderer import MarkdownRenderer

class ResolveMD:
    def __init__(self, model=None, context=None):
        self.md_parser = MarkdownIt("commonmark").use(container_plugin, "Todo.Ai")
        self.builder = AIContextBuilder()
        self.directive_builder = DirectiveBuilder()

    class ParsedResult(NamedTuple):
        structure: List[Any]
        directives: List[AIDirective]

    def parse_structure(self, markdown_text: str) -> ParsedResult:
        tokens = self.md_parser.parse(markdown_text)
        structure = tokens

        directives = []
        for token in tokens:
            if token.type == "container_Todo.Ai_open":
                attributes = dict(re.findall(r'([a-zA-Z_][\w\-\.]*)="([^"]+)"', token.info))
                context_id = attributes.get("context_id")
                context = self.builder.get_context_object(context_id or f"MissingContext for directive with prompt: {attributes.get('prompt')}")
                directive = self.directive_builder.create_directive(
                    type="directive",
                    resolver="Todo.Ai",
                    prompt=attributes.get("prompt"),
                    context=context,
                    structure=tokens,
                    position=tokens.index(token),
                    token=token
                )
                md_selector = attributes.get("md")
                if md_selector:
                    found = False
                    collecting = False
                    collected_tokens = []
                    for i, t in enumerate(tokens):
                        if not found and t.type == "heading_open":
                            if i + 1 < len(tokens):
                                next_token = tokens[i + 1]
                                if next_token.content.strip().lower() == md_selector.lstrip("#").strip().lower():
                                    found = True
                                    collecting = True
                                    continue
                        elif collecting:
                            if t.type == "heading_open" and t.tag.startswith("h"):
                                break
                            collected_tokens.append(t)
                    if collected_tokens:
                        directive.input = collected_tokens
                directives.append(directive)

        return self.ParsedResult(structure=structure, directives=directives)

    class ResolvedResult(NamedTuple):
        request: dict
        structure: List[Token]
        directives: List[AIDirective]
        response: str

    def resolve(self, request_json: dict, markdown_text: str) -> "ResolveMD.ResolvedResult":
        parsed = self.parse_structure(markdown_text)
        print(f"Configured contexts: {list(self.builder.contexts.keys())}")
        return self.ResolvedResult(
            request=request_json,
            structure=parsed.structure,
            directives=parsed.directives,
            response=MarkdownRenderer().render(parsed.structure, parsed.directives)
        )