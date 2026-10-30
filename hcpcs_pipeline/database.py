
import os
import psycopg2
from dotenv import load_dotenv
from datetime import date

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "hcpcs_db"),
        user=os.getenv("POSTGRES_USER", "hcpcs"),
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=10
    )


def test_connection():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database(), CURRENT_USER")
            result = cursor.fetchone()

            print("Database:", result[0])
            print("Connected as:", result[1])
    finally:
        connection.close()

def load_scd2(connection, dataframe):
    new_versions = 0
    unchanged = 0

    with connection:
        with connection.cursor() as cursor:

            for row in dataframe.itertuples(index=False):
                cursor.execute(
                    """
                    SELECT id, desc_hash, version
                    FROM hcpcs_codes
                    WHERE hcpcs_code = %s
                      AND is_current = TRUE
                    FOR UPDATE
                    """,
                    (row.hcpcs_code,)
                )

                existing = cursor.fetchone()

                if existing is None:
                    cursor.execute(
                        """
                        INSERT INTO hcpcs_codes (
                            hcpcs_code,
                            long_description,
                            desc_hash,
                            effective_date,
                            version,
                            is_current
                        )
                        VALUES (%s, %s, %s, %s, 1, TRUE)
                        """,
                        (
                            row.hcpcs_code,
                            row.long_description,
                            row.desc_hash,
                            date.today()
                        )
                    )
                    new_versions += 1

                elif existing[1].strip() == row.desc_hash:
                    unchanged += 1

                else:
                    cursor.execute(
                        """
                        UPDATE hcpcs_codes
                        SET is_current = FALSE,
                            end_date = %s
                        WHERE id = %s
                        """,
                        (date.today(), existing[0])
                    )

                    cursor.execute(
                        """
                        INSERT INTO hcpcs_codes (
                            hcpcs_code,
                            long_description,
                            desc_hash,
                            effective_date,
                            version,
                            is_current
                        )
                        VALUES (%s, %s, %s, %s, %s, TRUE)
                        """,
                        (
                            row.hcpcs_code,
                            row.long_description,
                            row.desc_hash,
                            date.today(),
                            existing[2] + 1
                        )
                    )
                    new_versions += 1

    return new_versions, unchanged


if __name__ == "__main__":
    test_connection()
