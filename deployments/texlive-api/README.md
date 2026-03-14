# TeX Live API

Lightweight LaTeX compilation API.

## Setup

```bash
# Install dependencies
pip install flask

# Install LaTeX
# macOS
brew install texlive

# Ubuntu
sudo apt install texlive-xelatex

# Run
python texlive_api.py
```

## Usage

```bash
# Compile
curl -X POST http://localhost:8080/compile \
  -H "Content-Type: application/json" \
  -d '{"tex": "\\documentclass{article}\\n\\begin{document}\\nHello\\n\\end{document}"}'
```

## Docker

```bash
docker-compose up -d
```
