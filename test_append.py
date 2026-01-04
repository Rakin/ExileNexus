import time
from pathlib import Path

# Use o mesmo caminho que você colocou no watcher
log_file = Path.home() / "poe_test.txt"

with open(log_file, "a", encoding="utf-8") as f:
    f.write(": You have entered Lioneye's Watch.\n")
    f.flush() # Força o Windows a gravar no disco
    print("Line written and flushed!")