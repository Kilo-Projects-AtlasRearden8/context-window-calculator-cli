import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .config import (
    DEFAULT_MODELS,
    list_models,
    load_config,
    resolve_model,
    save_config,
)
from .store import clear_estimates, export_csv, load_estimates, save_estimate, store_path
from .tokens import context_fit, estimate_tokens


def _read_source(args):
    if args.text is not None:
        return args.text, "text"
    if args.file is not None:
        path = Path(args.file)
        if not path.exists():
            print(f"error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        return path.read_text(encoding="utf-8"), f"file:{path}"
    print("error: provide --text or --file", file=sys.stderr)
    sys.exit(1)


def _format_result(model, result, source, source_excerpt, method, chars_per_token, context_window):
    lines = []
    lines.append(f"model: {model['name']} ({model['id']})")
    lines.append(f"context window: {context_window:,} tokens")
    lines.append(f"estimation method: {method} ({chars_per_token} chars/token)" if method == "char" else f"estimation method: {method}")
    lines.append(f"source: {source}")
    if source_excerpt:
        lines.append(f"excerpt: {source_excerpt}")
    lines.append(f"estimated tokens: {result['estimated_tokens']:,}")
    lines.append(f"available for prompt: {result['available_for_prompt']:,}")
    lines.append(f"remaining tokens: {result['remaining_tokens']:,}")
    lines.append(f"percent of context: {result['percent_of_context']}%")
    lines.append(f"fits within context: {'yes' if result['fits_within_context'] else 'no'}")
    return "\n".join(lines)


def cmd_estimate(args):
    config = load_config()
    model_id = args.model or config.get("default_model", "default")
    try:
        model = resolve_model(model_id, config)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    context_window = args.context_window if args.context_window is not None else model["context_window"]
    chars_per_token = (
        args.chars_per_token if args.chars_per_token is not None else model["chars_per_token"]
    )
    method = args.method or config.get("default_method", "char")
    words_per_token = args.words_per_token if args.words_per_token is not None else config.get("default_words_per_token", 0.75)
    reserve = args.reserve if args.reserve is not None else config.get("default_reserve_completion", 256)

    text, source = _read_source(args)
    excerpt = " ".join(text.split())[:120]
    if len(text) > 120:
        excerpt += "..."

    tokens = estimate_tokens(text, chars_per_token=chars_per_token, method=method, words_per_token=words_per_token)
    result = context_fit(tokens, context_window, reserve_completion=reserve)

    print(_format_result(model, result, source, excerpt, method, chars_per_token, context_window))
    print()
    from .models import KNOWN_ESTIMATION_NOTE
    print(KNOWN_ESTIMATION_NOTE)

    if args.save:
        record = {
            "model": model["id"],
            "model_name": model["name"],
            "context_window": context_window,
            "chars_per_token": chars_per_token,
            "method": method,
            "words_per_token": words_per_token,
            "reserve_completion": reserve,
            "source": source,
            "source_excerpt": excerpt,
            "estimated_tokens": result["estimated_tokens"],
            "available_for_prompt": result["available_for_prompt"],
            "remaining_tokens": result["remaining_tokens"],
            "fits_within_context": result["fits_within_context"],
            "percent_of_context": result["percent_of_context"],
        }
        saved = save_estimate(record)
        print(f"saved estimate to {store_path()} ({saved.get('saved_at')})")

    if not result["fits_within_context"]:
        return 1
    return 0


def cmd_models(args):
    config = load_config()
    if args.add:
        if args.context is None or args.name is None:
            print("error: --add requires --name and --context", file=sys.stderr)
            sys.exit(1)
        models = config.setdefault("models", {})
        models[args.add] = {
            "name": args.name,
            "context_window": args.context,
            "chars_per_token": args.cpt if args.cpt is not None else 4,
        }
        save_config(config)
        print(f"added model {args.add!r}")
        return 0
    if args.remove:
        models = config.setdefault("models", {})
        if args.remove not in models:
            print(f"error: no user model {args.remove!r}", file=sys.stderr)
            sys.exit(1)
        del models[args.remove]
        save_config(config)
        print(f"removed model {args.remove!r}")
        return 0
    for model_id, entry in list_models(config):
        marker = " (user)" if model_id in config.get("models", {}) else ""
        print(f"{model_id}: {entry['name']}  context={entry['context_window']:,}  cpt={entry['chars_per_token']}{marker}")
    return 0


def cmd_history(args):
    estimates = load_estimates()
    if not estimates:
        print("no saved estimates")
        return 0
    for idx, record in enumerate(estimates, start=1):
        fits = "yes" if record.get("fits_within_context") else "no"
        print(
            f"{idx}. [{record.get('saved_at', '?')}] {record.get('model', '?')}"
            f"  tokens={record.get('estimated_tokens', 0):,}"
            f"  context={record.get('context_window', 0):,}"
            f"  remaining={record.get('remaining_tokens', 0):,}"
            f"  fits={fits}"
        )
    return 0


def cmd_export(args):
    count = export_csv(args.out)
    print(f"exported {count} estimate(s) to {args.out}")
    return 0


def cmd_clear(args):
    clear_estimates()
    print("cleared saved estimates")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="context-calc",
        description="Estimate prompt token usage and context-window fit for local LLMs.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    p_est = sub.add_parser("estimate", help="estimate tokens for a prompt")
    p_est.add_argument("--text", help="prompt text inline")
    p_est.add_argument("--file", help="path to a file containing the prompt")
    p_est.add_argument("--model", help="model id (use 'context-calc models' to list)")
    p_est.add_argument("--method", choices=["char", "word"], help="estimation method")
    p_est.add_argument("--chars-per-token", type=int, help="chars per token (char method)")
    p_est.add_argument("--words-per-token", type=float, help="words per token (word method)")
    p_est.add_argument("--context-window", type=int, help="override model context window")
    p_est.add_argument("--reserve", type=int, help="tokens reserved for completion")
    p_est.add_argument("--save", action="store_true", help="save estimate locally")
    p_est.set_defaults(func=cmd_estimate)

    p_models = sub.add_parser("models", help="list or configure model defaults")
    p_models.add_argument("--list", action="store_true", help="list configured models")
    p_models.add_argument("--add", metavar="ID", help="add a user model id")
    p_models.add_argument("--name", help="display name for --add")
    p_models.add_argument("--context", type=int, help="context window for --add")
    p_models.add_argument("--cpt", type=int, help="chars per token for --add")
    p_models.add_argument("--remove", metavar="ID", help="remove a user model")
    p_models.set_defaults(func=cmd_models)

    p_hist = sub.add_parser("history", help="show saved estimates")
    p_hist.set_defaults(func=cmd_history)

    p_exp = sub.add_parser("export", help="export saved estimates to CSV")
    p_exp.add_argument("--out", required=True, help="output CSV path")
    p_exp.set_defaults(func=cmd_export)

    p_clr = sub.add_parser("clear", help="clear saved estimates")
    p_clr.set_defaults(func=cmd_clear)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
