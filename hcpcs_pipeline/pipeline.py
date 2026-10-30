
import logging

from hcpcs_pipeline.config import SOURCE_URL
from hcpcs_pipeline.scraper import fetch_html, extract_hcpcs_records
from hcpcs_pipeline.raw_storage import save_raw_records
from hcpcs_pipeline.transform import transform_records
from hcpcs_pipeline.database import get_connection, load_scd2
from hcpcs_pipeline.quality import validate_records

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_pipeline():
    connection = None

    try:
        # 1. Extract
        logger.info("Downloading HCPCS source page")
        html = fetch_html(SOURCE_URL)

        records = extract_hcpcs_records(html)
        logger.info("Extracted %s records", len(records))

        # 2. Preserve raw data
        raw_path = save_raw_records(records)
        logger.info("Raw snapshot: %s", raw_path)

        # 3. Transform
        dataframe, rejected = transform_records(records)
        logger.info(
            "Valid records: %s; rejected records: %s",
            len(dataframe),
            rejected
        )

        checks = validate_records(dataframe)

        for check in checks:
            logger.info("%s: %s", check["check"], check["passed"])

        failed_checks = [
            check for check in checks
            if not check["passed"]
        ]

        if failed_checks:
            raise ValueError(f"Quality checks failed: {failed_checks}")                  

        # 4. Basic quality gate
        if dataframe.empty:
            raise ValueError("No valid records to load")

        if dataframe["hcpcs_code"].duplicated().any():
            raise ValueError("Duplicate codes detected after transformation")

        # 5. Load into PostgreSQL
        connection = get_connection()

        new_versions, unchanged = load_scd2(
            connection,
            dataframe
        )

        logger.info(
            "Load completed: %s new versions, %s unchanged",
            new_versions,
            unchanged
        )

        return {
            "extracted": len(records),
            "valid": len(dataframe),
            "rejected": rejected,
            "new_versions": new_versions,
            "unchanged": unchanged
        }

    except Exception:
        logger.exception("HCPCS pipeline failed")
        raise

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    run_pipeline()
