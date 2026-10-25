import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def save_records(df, filename):
    try:
        project_root = Path(__file__).resolve().parent.parent
        file_path = project_root / "data" / filename
        
        file_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(file_path, index=False)
        logger.info("Successfully saved %s records to %s", len(df), file_path.name)

    except Exception:
        logger.exception("Failed to write records to %s", filename)
        raise 

    