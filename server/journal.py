import uuid
from server.chat_utils import generate_ai_reply
import os
from datetime import datetime
from flask import request, jsonify, current_app

def chat():
    if current_app.debug:
        print(f"📥 POST to /journal — Headers: {dict(request.headers)}")
        print(f"📥 POST Body: {request.get_data(as_text=True)}")
    messages = request.json.get("messages", [])
    if not messages:
        return jsonify({"error": "No messages provided."}), 400

    reply = generate_ai_reply(messages)

    # Write to data/JOURNAL/YYYY-MM-DD-HH-MM-<uuid>.md
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    journal_dir = "data/JOURNAL"
    os.makedirs(journal_dir, exist_ok=True)
    unique_id = uuid.uuid4().hex[:8]
    filepath = os.path.join(journal_dir, f"{timestamp}-{unique_id}.md")

    with open(filepath, "w") as f:
        f.write("# Journal Entry\n\n")
        f.write("## Messages\n")
        for msg in messages:
            f.write(f"- {msg.get('role', 'user')}: {msg.get('content', '').strip()}\n")
        f.write("\n## Reply\n")
        f.write(reply.strip())

    print(f"✅ Journal entry saved to {filepath}")

    return jsonify({"reply": reply})
