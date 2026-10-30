
def validate_records(dataframe):
    results = []

    results.append({
        "check": "no_null_codes",
        "passed": dataframe["hcpcs_code"].notna().all()
    })

    results.append({
        "check": "no_empty_descriptions",
        "passed": (
            dataframe["long_description"]
            .fillna("")
            .str.strip()
            .ne("")
            .all()
        )
    })

    results.append({
        "check": "unique_codes",
        "passed": not dataframe["hcpcs_code"].duplicated().any()
    })

    results.append({
        "check": "hashes_present",
        "passed": dataframe["desc_hash"].notna().all()
    })

    return results
