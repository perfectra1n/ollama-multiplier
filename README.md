# Ollama API Fun

This repo just allows you at this point to chat with multiple models at once.

# Instructions

```bash
git clone https://github.com/perfectra1n/ollama-multiplier
cd ollama-multiplier
python3 -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt
```

# Running

Then you can just run the command

```
python main_module.py
```

```bash
usage: main_module.py [-h] [--models MODELS [MODELS ...]] [--debug] host

This is the description for the main parser!

positional arguments:
  host                  The URL of the Ollama host.

options:
  -h, --help            show this help message and exit
  --models MODELS [MODELS ...]
                        Optional. List of models to use.
  --debug               Optional. Use this argument if you are debugging any
                        errors.

```

An example command to call multiple models that are already stored on your Ollama:

```bash
python main_module.py "https://ollama.local" --models gemma:latest codestral:latest qwen:14b phi3:latest llama3:latest mistral:7b mistral-openorca:latest
```
