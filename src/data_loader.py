import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_csv(filename):
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "raw" / filename

    try:
        df = pd.read_csv(file_path)
        row_count = len(df)
        if not df.empty:
            logger.info("Loaded %s rows from %s", row_count, filename)
            return df

        else:
            logger.warning("The file %s is empty", filename)
            return df

    except Exception:
        logger.exception("Failed to load %s", filename)
        raise
