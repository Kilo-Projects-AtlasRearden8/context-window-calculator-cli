"""context_calc: local-first prompt token and context-window estimator."""

__version__ = "1.0.0"

from .tokens import context_fit, estimate_tokens

__all__ = ["estimate_tokens", "context_fit"]
