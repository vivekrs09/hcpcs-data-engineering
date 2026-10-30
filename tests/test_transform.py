
from hcpcs_pipeline.transform import transform_records


def test_transform_removes_invalid_records():
    records = [
        {
            "hcpcs_code": "A1234",
            "long_description": "Example service"
        },
        {
            "hcpcs_code": "",
            "long_description": "Invalid code"
        }
    ]

    dataframe, rejected = transform_records(records)

    assert len(dataframe) == 1
    assert rejected == 1
    assert dataframe.iloc[0]["hcpcs_code"] == "A1234"


def test_transform_removes_duplicate_codes():
    records = [
        {
            "hcpcs_code": "A1234",
            "long_description": "Old description"
        },
        {
            "hcpcs_code": "A1234",
            "long_description": "Updated description"
        }
    ]

    dataframe, rejected = transform_records(records)

    assert len(dataframe) == 1
    assert rejected == 1
    assert dataframe.iloc[0]["long_description"] == "Updated description"
