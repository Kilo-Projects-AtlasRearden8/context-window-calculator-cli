# STATUS.md

## What was built

`context-calc` — a local-first Python CLI (pure standard library, zero
dependencies) that estimates prompt token usage and checks whether a prompt fits
inside a local LLM's context window, with configurable model defaults, local
saved estimates, and CSV export.

Files:
- `pyproject.toml` — project metadata and `context-calc` console entry point
- `context_calc/__init__.py` — package init, version, public API
- `context_calc/tokens.py` — estimation math: `estimate_tokens()` (char and word
  methods) and `context_fit()` (context-window fit with completion reserve)
- `context_calc/models.py` — built-in model defaults (Llama 3.1, Llama 3.2,
  Qwen 2.5, Mistral, Gemma 2, Phi-3, custom default)
- `context_calc/config.py` — local XDG config/store paths, load/save config,
  user models, model resolution
- `context_calc/store.py` — local JSON estimate store and CSV export
- `context_calc/cli.py` — argparse CLI: estimate, models, history, export, clear
- `tests/test_tokens.py` — 14 unit tests for estimation math
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — usage docs, credits Asdale Dynamics, LLC
- `.gitignore` — excludes `.venv`, egg-info, `__pycache__`, local store

## How to run it

```bash
# install
pip install .          # or: pip install -e . for editable development

# estimate inline text
context-calc estimate --text "Summarize this meeting" --model llama-3.1-8b

# estimate from a file, reserve room for the answer, save locally
context-calc estimate --file prompt.txt --model qwen2.5-7b --reserve 512 --save

# override context window / chars per token
context-calc estimate --text "..." --context-window 4096 --chars-per-token 4

# list models; add your own; view history; export CSV
context-calc models
context-calc models --add my-llama --name "My Llama" --context 8192 --cpt 4
context-calc history
context-calc export --out estimates.csv

# exit code is 1 when the prompt does not fit within the context window
```

Estimates and config are stored locally under XDG config/data dirs
(`~/.config/.context-calc/` and `~/.local/share/.context-calc/` by default).
No API keys, no network calls, no telemetry.

## Verification results

- `python -m unittest discover -s tests -v`: 14 tests, OK
- CLI smoke tests all passed:
  - `estimate --text` / `--file` with built-in models
  - `--context-window`, `--reserve`, `--chars-per-token` overrides
  - `--save` writes to local JSON store
  - `models` list / `--add` / `--remove` user models
  - `history` lists saved estimates
  - `export --out` writes a CSV with header and all saved rows
  - overflow case (10,000 estimated tokens vs 8,192 context): reports
    `fits within context: no` and exits with code 1

## Known gaps

- Token counts are heuristics (~4 chars/token by default; word method also
  available), not real tokenizer counts. Test with your model's tokenizer when
  precision matters.
- No tkinter/GUI; CLI only.
- Config/store locations follow XDG; no built-in UI to relocate them (set
  `XDG_CONFIG_HOME` / `XDG_DATA_HOME`).
- Credits Asdale Dynamics, LLC (dylanasdale.github.io).
