# Python + Ollama Mistral Template

This is a minimal starter template for Python projects that use [Ollama](https://ollama.com) to run local LLMs like Mistral.

---

## 🧰 Features

- ✅ `setup_dev.sh`: Auto-creates a Conda environment or Python venv (depending on version)
- ✅ `start_ollama.sh`: Starts the Ollama Mistral model
- ✅ `.env`: Configurable environment settings
- ✅ `main.py`: Chat client with:
  - Streaming responses from Mistral
  - Chat memory / multi-turn conversation
- ✅ `.vscode/`: Pre-configured Python path and launch support

---

## 🚀 Getting Started

1. **Clone the template**

```bash
git clone <your-new-repo-url>
cd <repo-folder>
```

2. **Name your project**

Update `PROJECT.name` with your project name.

3. **Run setup**

```bash
chmod +x setup_dev.sh start_ollama.sh
./setup_dev.sh
```

4. **Start Ollama (in a separate terminal)**

```bash
./start_ollama.sh
```

5. **Run your app**

```bash
source .venv/bin/activate     # or conda activate <env_name>
python main.py
```

---

## 🛠 Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download)
- (Optional) Conda if using Conda-based setup

---

## 🌱 Environment Variables

You can configure:
- `MODEL=mistral`
- `OLLAMA_URL=http://localhost:11434`
- `GREETING="Your custom greeting here"`

---

## 🧠 Tips

- Exit the chat loop with `exit` or `quit`
- Customize system behavior in `main.py` (`role: system`)
- To create a new project, just copy or re-clone this folder and start again

---

MIT License


---

## 🐙 Publish as a GitHub Template

To turn this into a reusable GitHub template:

1. **Create a new GitHub repository**, e.g., `python-ollama-template`
2. Push this folder’s contents:

```bash
git init
git remote add origin https://github.com/your-username/python-ollama-template.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

3. On GitHub, go to:
   - **Settings → General → Template repository**
   - ✅ Check the box to mark it as a template

Now anyone can click **"Use this template"** on your repo to create their own project from it.

---

Want a `cookiecutter` version later? Let me know.


---

## 🔄 Keeping Your Project Up to Date

When you clone this template, the original repo is saved as `upstream`. You can pull updates later:

```bash
git fetch upstream
git merge upstream/main
```

To update only the template files (e.g., setup scripts):

```bash
git checkout upstream/main -- template/
bash create_symlinks.sh
```

This preserves your custom project while letting you sync improvements to the shared scripts.
