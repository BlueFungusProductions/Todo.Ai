#!/bin/bash
ln -sf template/setup_dev.sh setup_dev.sh
chmod +x setup_dev.sh
ln -sf template/start_ollama.sh start_ollama.sh
chmod +x setup_dev.sh
echo "✅ Symlinks created for setup_dev.sh and start_ollama.sh"
