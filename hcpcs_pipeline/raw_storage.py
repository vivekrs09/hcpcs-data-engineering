
import json
from datetime import datetime, timezone
from pathlib import Path

from hcpcs_pipeline.config import RAW_DATA_DIR


def save_raw_records(records):
    # Create a dated folder for this extraction.
    now = datetime.now(timezone.utc)

    folder = Path(RAW_DATA_DIR) / now.strftime("%Y/%m/%d")
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"hcpcs_{now.strftime('%H%M%S_%f')}.json"
    file_path = folder / filename

    payload = {
        "extracted_at": now.isoformat(),
        "record_count": len(records),
        "records": records
    }

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return file_path
