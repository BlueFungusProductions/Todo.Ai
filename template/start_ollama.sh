#!/bin/bash
set -e

MODEL="mistral"

echo "🚀 Starting Ollama with model '$MODEL'..."
ollama run $MODEL
