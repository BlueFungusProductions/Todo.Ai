# server/api/ai/types.py

from dataclasses import dataclass
from markdown_it.token import Token
from typing import List, Optional
from typing import Protocol

class AIResolver(Protocol):
    def get_context_id(self) -> str: ...
    def resolve(self, directive: 'AIDirective') -> str: ...



@dataclass
class _AIDirective:
    type: str
    resolver: str
    context: AIResolver
    prompt: Optional[str]
    input: Optional[List[Token]] = None
    structure: Optional[List[Token]] = None
    position: Optional[int] = None
    token: Optional[Token] = None  # New field for the directive token

    @classmethod
    def _create(
        cls,
        type: str,
        resolver: str,
        context: AIResolver,
        prompt: Optional[str],
        input: Optional[List[Token]] = None,
        structure: Optional[List[Token]] = None,
        position: Optional[int] = None,
        token: Optional[Token] = None
    ) -> '_AIDirective':
        return cls(
            type=type,
            resolver=resolver,
            context=context,
            prompt=prompt,
            input=input,
            structure=structure,
            position=position,
            token=token
        )

    def resolve(self) -> str:
        if self.context is None:
            return "[No context assigned to directive]"
        return self.context.resolve(self)


# Public alias for backward compatibility
AIDirective = _AIDirective


# Builder class for creating directives
class DirectiveBuilder:
    def create_directive(
        self,
        type: str,
        resolver: str,
        context: AIResolver,
        prompt: Optional[str],
        input: Optional[List[Token]] = None,
        structure: Optional[List[Token]] = None,
        position: Optional[int] = None,
        token: Optional[Token] = None
    ) -> AIDirective:
        return AIDirective._create(
            type=type,
            resolver=resolver,
            context=context,
            prompt=prompt,
            input=input,
            structure=structure,
            position=position,
            token=token
        )