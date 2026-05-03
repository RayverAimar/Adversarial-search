"""Render a CLI self-play transcript as a PNG for the README."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from cli import main as cli_main  # noqa: E402

buffer = io.StringIO()
with redirect_stdout(buffer):
    cli_main(["--self-play", "--size", "3", "--depth", "9"])

text = buffer.getvalue()

fig, ax = plt.subplots(figsize=(10, 12))
ax.set_facecolor("#0d1117")
fig.patch.set_facecolor("#0d1117")
ax.text(
    0.02,
    0.98,
    text,
    family="monospace",
    fontsize=10,
    color="#e6edf3",
    verticalalignment="top",
    transform=ax.transAxes,
)
ax.axis("off")
plt.tight_layout()
out = ROOT / "cli_demo.png"
plt.savefig(out, dpi=140, bbox_inches="tight", facecolor="#0d1117")
print(f"Saved {out}")
