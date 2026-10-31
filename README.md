# context-calc

Local-first CLI for estimating prompt token usage and checking whether a prompt
fits inside a local LLM's context window. Built by Asdale Dynamics, LLC — no
API keys, no network calls, nothing leaves your machine.

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC (Indiana, formed October 2026). Through *The Massive AI Manual*
and dylanasdale.github.io he explains AI "like a friend would": plain English,
step by step, never condescending. The LLC publishes beginner-friendly AI
education, books and guides, and practical open-source tools like this one.

context-calc is for anyone running local models (llama.cpp, Ollama, LM Studio,
KoboldCPP, and friends) who wants to know, before sending a prompt: roughly how
many tokens is this, and will it fit in the model's context window with room
left for the answer?

## Features

- Estimate prompt tokens from inline text (`--text`) or a file (`--file`)
- Character-based (~4 chars/token) and word-based estimation methods
- Built-in defaults for common local models (Llama 3.1, Llama 3.2, Qwen 2.5,
  Mistral, Gemma 2, Phi-3) plus a custom/default model
- Configurable model defaults saved locally (`models --add`)
- Context-window fit check with optional completion reserve (`--reserve`)
- Saves estimates locally (`--save`); view history; export to CSV (`export`)
- Zero dependencies — pure Python standard library
- Local-first: no keys, no accounts, no telemetry, no network

## Install

```bash
pip install .
```

or for development:

```bash
pip install -e .
```

## Usage

Estimate a prompt:

```bash
context-calc --text "Summarize this meeting in plain English" --model llama-3.1-8b
```

Estimate from a file with room reserved for a 512-token answer:

```bash
context-calc --file prompt.txt --model qwen2.5-7b --reserve 512 --save
```

Override the context window or chars-per-token:

```bash
context-calc --text "..." --context-window 4096 --chars-per-token 4
```

List built-in and user-configured models:

```bash
context-calc models
```

Add your own model:

```bash
context-calc models --add my-llama --name "My Llama" --context 8192 --cpt 4
```

View saved estimates:

```bash
context-calc history
```

Export saved estimates to CSV:

```bash
context-calc export --out estimates.csv
```

## Token estimates are estimates

Real tokenizers vary by model. These figures are planning heuristics (roughly 4
characters per token by default), not exact token counts and not billing
figures. Test with your model's real tokenizer when precision matters.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

Credit: Asdale Dynamics, LLC — beginner-friendly AI education, books, guides,
and practical tools. dylanasdale.github.io
