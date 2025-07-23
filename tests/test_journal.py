import requests
from server.api.ai.resolve import ResolveMD


def test_contexts_loaded_from_builder():
    resolver = ResolveMD()
    assert "journal-mood" in resolver.contexts
    assert "journal-entry" in resolver.contexts
    assert resolver.contexts["journal-mood"]["context_id"] == "journal-mood"
    assert "default_prompt" in resolver.contexts["journal-mood"]

def test_journal_post(capfd):
    response = requests.post("http://127.0.0.1:5000/journal", json={
        "messages": [
            {"role": "system", "content": "Mood: Curious"},
            {"role": "user", "content": "Trying to understand Todo.Ai design."}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    print("Response:", data)
    out, _ = capfd.readouterr()
    with open("tests/tmp/journal_test_output.log", "w") as f:
        f.write(out)
    assert "reply" in data
    assert isinstance(data["reply"], str)
    assert "Response:" in out  # Ensures print output is captured