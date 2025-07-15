#!/bin/bash
set -e

PROJECT_NAME=$(cat PROJECT.name)

echo "Creating conda environment: $PROJECT_NAME"
conda create -y -n "$PROJECT_NAME" python=3.10

eval "$(conda shell.bash hook)"
conda activate "$PROJECT_NAME"

if ! command -v ollama &> /dev/null; then
  echo "Installing Ollama..."
  brew install ollama || echo "Please install Ollama manually from https://ollama.com/download"
fi

touch requirements.txt
pip install -r requirements.txt

echo "✅ Setup complete. Environment '$PROJECT_NAME' is ready."
