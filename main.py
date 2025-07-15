from dotenv import load_dotenv
import os
import requests

# Load config
load_dotenv()
MODEL = os.getenv("MODEL", "mistral")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def stream_chat(messages):
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": MODEL, "messages": messages},
        stream=True
    )
    response.raise_for_status()
    reply = ""
    for chunk in response.iter_lines(decode_unicode=True):
        if chunk:
            data = eval(chunk.strip())
            token = data.get("message", {}).get("content", "")
            print(token, end="", flush=True)
            reply += token
    print()
    return reply

def main():
    print(f"🤖 Connected to Ollama model: {MODEL}")
    print("💬 Type 'exit' to quit.\n")

    history = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        user_input = input("👤 You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        history.append({"role": "user", "content": user_input})
        print("🤖 Mistral:", end=" ", flush=True)
        assistant_reply = stream_chat(history)
        history.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    main()
