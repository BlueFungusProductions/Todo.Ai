import pytest
from server.api.ai.resolve import ResolveMD

@pytest.fixture
def resolver():
    return ResolveMD()

@pytest.fixture
def prompt_text():
    with open("tests/fixtures/sample_prompt.txt", "r") as f:
        return f.read().strip()

def test_resolve_markdown_with_prompt_and_context_id(resolver: ResolveMD, prompt_text: str):
    markdown = prompt_text  # The full markdown is loaded from the fixture

    assert markdown

    print("Markdown passed in for test:"+markdown, flush=True)

    result = resolver.resolve(request_json={}, markdown_text=markdown)

    print("\nResolved directives:")
    for item in result.directives:
        print(item)

    print(result.response)
    directives = result.directives
    assert len(directives) == 2

    assert directives[0].resolver == "Todo.Ai"
    assert directives[0].prompt == "What was the emotional tone of this entry?"
    assert directives[0].context.get_context_id() == "journal-entry"

    assert directives[1].resolver == "Todo.Ai"
    assert directives[1].prompt == "What are the key takeaways or ideas in this entry? Summarize them and end with a thought-provoking question to explore further."
    assert directives[1].context.get_context_id() == "journal-mood"

def test_all_contexts_have_resolve_method():
    resolver = ResolveMD()
    for context_id, context in resolver.builder.contexts.items():
        assert hasattr(context, "resolve") and callable(context.resolve), f"Context '{context_id}' is missing a callable 'resolve' method"