import pandas as pd
from pathlib import Path

def load_csv(filename):
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "raw" / filename
    df = pd.read_csv(file_path)

    return df
