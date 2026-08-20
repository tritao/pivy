"""Backward-compatible imports for the consolidated Pivy typing policy.

The generator used to keep its normalization tables in this module.  Keep the
module available for downstream tooling, but define the tables only in
``pivy_stub_typing_policy`` so generator, validator, and report code cannot
silently drift apart.
"""

try:
    from tools.pivy_stub_typing_policy import *  # noqa: F401,F403
except ImportError:
    from pivy_stub_typing_policy import *  # noqa: F401,F403
