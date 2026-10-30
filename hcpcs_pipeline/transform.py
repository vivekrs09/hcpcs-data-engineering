
import hashlib
import re
import pandas as pd


def description_hash(description):
    """Create a stable hash from a normalized description."""

    normalized = re.sub(
        r"\s+",
        " ",
        description.strip()
    ).casefold()

    return hashlib.md5(
        normalized.encode("utf-8")
    ).hexdigest()


def transform_records(records):
    """Clean raw records and return a DataFrame."""

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("The extracted dataset is empty.")

    required = {"hcpcs_code", "long_description"}

    if not required.issubset(df.columns):
        raise ValueError(
            f"Missing columns: {required - set(df.columns)}"
        )

    # Clean whitespace.
    for column in ["hcpcs_code", "long_description"]:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # Standardize code casing.
    df["hcpcs_code"] = df["hcpcs_code"].str.upper()

    # Remove records missing required values.
    before = len(df)

    df = df[
        (df["hcpcs_code"] != "") &
        (df["long_description"] != "")
    ].copy()

    rejected = before - len(df)

    # Normalize whitespace in descriptions.
    df["long_description"] = df["long_description"].str.replace(
        r"\s+", " ", regex=True
    )

    # Keep the last record for each code in this batch.
    duplicate_count = int(
        df.duplicated(subset=["hcpcs_code"], keep="last").sum()
    )

    rejected += duplicate_count

    df = df.drop_duplicates(
        subset=["hcpcs_code"],
        keep="last"
    )

    # Create a fingerprint used to detect description changes.
    df["desc_hash"] = df["long_description"].map(
        description_hash
    )

    return df.reset_index(drop=True), rejected
