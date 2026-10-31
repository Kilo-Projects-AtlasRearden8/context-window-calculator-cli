DEFAULT_MODELS = {
    "llama-3.1-8b": {
        "name": "Llama 3.1 8B",
        "context_window": 8192,
        "chars_per_token": 4,
    },
    "llama-3.2-3b": {
        "name": "Llama 3.2 3B",
        "context_window": 131072,
        "chars_per_token": 4,
    },
    "qwen2.5-7b": {
        "name": "Qwen 2.5 7B",
        "context_window": 131072,
        "chars_per_token": 4,
    },
    "mistral-7b": {
        "name": "Mistral 7B",
        "context_window": 32768,
        "chars_per_token": 4,
    },
    "gemma-2-9b": {
        "name": "Gemma 2 9B",
        "context_window": 8192,
        "chars_per_token": 4,
    },
    "phi-3-mini": {
        "name": "Phi-3 Mini",
        "context_window": 131072,
        "chars_per_token": 4,
    },
    "default": {
        "name": "Custom / Default",
        "context_window": 4096,
        "chars_per_token": 4,
    },
}

DEFAULT_CONFIG = {
    "default_model": "default",
    "default_method": "char",
    "default_chars_per_token": 4,
    "default_words_per_token": 0.75,
    "default_reserve_completion": 256,
    "models": {},
}

KNOWN_ESTIMATION_NOTE = (
    "Token counts are estimates. Real tokenizers vary by model; "
    "use these figures for planning, not exact billing."
)
