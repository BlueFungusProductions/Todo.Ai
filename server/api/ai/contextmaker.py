import os
import json
from typing import List, Optional
from dataclasses import dataclass
from api.ai.types import AIDirective, AIResolver
from markdown_it.token import Token
from typing import Protocol

from utils.markdown_renderer import MarkdownRenderer

class AIContext(AIResolver):
    def __init__(self, context_id: str, description: str, default_prompt: str):
        self.context_id = context_id
        self.description = description
        self.default_prompt = default_prompt

    def __repr__(self):
        return f"AIContext(id={self.context_id!r}, description={self.description!r})"

    def get_context_id(self) -> str:
        return self.context_id

    def resolve(self, directive: AIDirective) -> str:
        """
        Mocks resolution of an AIDirective using this AI context.
        Replace this logic with actual model invocation as needed.
        """
        context_id = getattr(directive.context, "context_id", None)
        
        if directive.input is None:
            input_rendered = "ERROR: Missing input"
        else:
            input_rendered = MarkdownRenderer().render(directive.input, [])
        return f"## - Resolved: '{directive.prompt}' using context '{context_id}' and '{input_rendered}'"


class MissingAIContext(AIContext):
    def __init__(self, context_id: str):
        super().__init__(
            context_id=context_id,
            description="This context is missing or was not configured.",
            default_prompt="No prompt available because the context is missing."
        )

    def resolve(self, directive: AIDirective) -> str:
        return f"[Missing Context: '{self.context_id}' — cannot resolve directive '{directive.prompt}']"


class AIContextBuilder:
    def __init__(self):
        self.contexts: dict[str, AIContext] = {}

        config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/AI_CONTEXT_CONFIGS"))
        for filename in os.listdir(config_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(config_dir, filename)
                with open(filepath, "r") as f:
                    try:
                        config = json.load(f)
                        context = AIContext(
                            context_id=config["context_id"],
                            description=config["description"],
                            default_prompt=config["default_prompt"]
                        )
                        self.contexts[context.context_id] = context
                    except Exception as e:
                        print(f"Failed to load context from {filepath}: {e}")

    def get_context_object(self, context_id: str) -> AIContext:
        return self.contexts.get(context_id) or MissingAIContext(context_id)

    def to_dict(self):
        return {cid: ctx for cid, ctx in self.contexts.items()}
    
    def __repr__(self):
        context_list = ', '.join(repr(ctx) for ctx in self.contexts.values())
        return f"AIContextBuilder(contexts=[{context_list}])"
