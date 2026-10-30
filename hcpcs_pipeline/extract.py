import logging

from hcpcs_pipeline.scraper import extract_hcpcs_records
from hcpcs_pipeline.scraper import fetch_html
from hcpcs_pipeline.config import SOURCE_URL
from hcpcs_pipeline.raw_storage import save_raw_records

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting extraction")

    # Step 1: Download the website HTML
    html = fetch_html(SOURCE_URL)

    # Step 2: Extract HCPCS records from the HTML
    records = extract_hcpcs_records(html)
    path = save_raw_records(records)

    print("Raw file saved:", path)

    # Step 3: Display the extraction results
    print("Records extracted:", len(records))
    print(records[:3])


if __name__ == "_main_":
    main()
