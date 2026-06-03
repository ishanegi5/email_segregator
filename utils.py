
import json
from pathlib import Path

def save_output(data, filename="output/result.json"):
    Path("output").mkdir(exist_ok=True)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved to {filename}")
