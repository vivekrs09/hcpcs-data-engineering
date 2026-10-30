
import requests
from bs4 import BeautifulSoup
from hcpcs_pipeline.config import REQUEST_TIMEOUT_SECONDS


def fetch_html(url):
    """Download the HTML content of a webpage."""

    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
        headers={"User-Agent": "HCPCS-Data-Engineering-Portfolio/1.0"}
    )
    # Raise an error if the server returns an unsuccessful HTTP status.
    response.raise_for_status()

    return response.text


def extract_hcpcs_records(html):
    """Extract HCPCS codes and descriptions from a recognizable HTML table."""

    soup = BeautifulSoup(html, "html.parser")

    # Find all HTML tables on the page.
    tables = soup.find_all("table")

    if not tables:
        raise ValueError("No HTML tables found on the webpage.")

    for table in tables:

        # Read the column headings.
        header_row = table.find("tr")

        if header_row is None:
            continue

        headers = [
            cell.get_text(" ", strip=True).lower()
            for cell in header_row.find_all(["th", "td"])
        ]

        # Identify the required columns.
        code_index = next(
            (i for i, name in enumerate(headers)
             if name in {"hcpcs code", "hcpcs", "code"}),
            None
        )

        description_index = next(
            (i for i, name in enumerate(headers)
             if name in {"long description", "description"}),
            None
        )

        # Skip tables that don't contain the required columns.
        if code_index is None or description_index is None:
            continue

        records = []

        # Read each data row after the header.
        for row in table.find_all("tr")[1:]:

            cells = [
                cell.get_text(" ", strip=True)
                for cell in row.find_all(["td", "th"])
            ]

            if len(cells) <= max(code_index, description_index):
                continue

            code = cells[code_index].strip()
            description = cells[description_index].strip()

            if code and description:
                records.append({
                    "hcpcs_code": code,
                    "long_description": description
                })

        if records:
            return records

    raise ValueError(
        "Could not find a table with recognized HCPCS code "
        "and description columns. Inspect the source HTML."
    )
