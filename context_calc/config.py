import json
import os
from pathlib import Path

from .models import DEFAULT_CONFIG, DEFAULT_MODELS

CONFIG_DIR_NAME = ".context-calc"
CONFIG_FILE = "config.json"
STORE_FILE = "estimates.json"


def _config_dir():
    env = os.environ.get("XDG_CONFIG_HOME")
    if env:
        return Path(env) / CONFIG_DIR_NAME
    return Path.home() / CONFIG_DIR_NAME


def _data_dir():
    env = os.environ.get("XDG_DATA_HOME")
    if env:
        return Path(env) / CONFIG_DIR_NAME
    return Path.home() / CONFIG_DIR_NAME


def config_path():
    return _config_dir() / CONFIG_FILE


def store_path():
    return _data_dir() / STORE_FILE


def load_config():
    path = config_path()
    if not path.exists():
        return dict(DEFAULT_CONFIG)
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)
    config = dict(DEFAULT_CONFIG)
    config.update(data)
    config.setdefault("models", {})
    return config


def save_config(config):
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2, sort_keys=True)
        handle.write("\n")


def resolve_model(model_id, config):
    models = dict(DEFAULT_MODELS)
    models.update(config.get("models", {}))
    if model_id not in models:
        raise KeyError(f"unknown model: {model_id}")
    entry = dict(models[model_id])
    entry["id"] = model_id
    return entry


def list_models(config):
    models = dict(DEFAULT_MODELS)
    models.update(config.get("models", {}))
    return sorted(models.items())
