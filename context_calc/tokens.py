import math


def estimate_tokens(text, chars_per_token=4, method="char", words_per_token=0.75):
    if text is None:
        return 0
    text = str(text)
    if not text:
        return 0
    if method == "char":
        return max(1, math.ceil(len(text) / max(chars_per_token, 1)))
    if method == "word":
        words = len(text.split())
        return max(1, math.ceil(words / max(words_per_token, 0.0001)))
    raise ValueError(f"unknown estimation method: {method}")


def context_fit(estimated_tokens, context_window, reserve_completion=0):
    if context_window is None:
        context_window = 0
    available = max(context_window - max(reserve_completion, 0), 0)
    remaining = available - int(estimated_tokens)
    fits = int(estimated_tokens) <= available
    percent = (int(estimated_tokens) / context_window * 100) if context_window else 0.0
    return {
        "estimated_tokens": int(estimated_tokens),
        "context_window": int(context_window),
        "reserve_completion": int(reserve_completion),
        "available_for_prompt": int(available),
        "remaining_tokens": int(remaining),
        "fits_within_context": bool(fits),
        "percent_of_context": round(percent, 2),
    }
