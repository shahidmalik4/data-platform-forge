import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


def fetch_table(table_name, schema="raw"):
    conn = get_connection()
    cur = conn.cursor()
    data = []

    try:
        cur.execute(f'SELECT * FROM "{schema}"."{table_name}"')

        columns = [desc[0].lower() for desc in cur.description]

        rows = cur.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        print(f"[INFO] Fetched {len(data)} rows from {schema}.{table_name}")

    except Exception as e:
        print(f"[ERROR] fetching {schema}.{table_name}: {e}")

    finally:
        cur.close()
        conn.close()

    return data


def is_first_run(table_name, schema="raw"):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f'SELECT COUNT(*) FROM "{schema}"."{table_name}"')
        count = cur.fetchone()[0]
        return count == 0

    except Exception:
        print(f"[WARN] Table {schema}.{table_name} not found → treating as first run")
        return True

    finally:
        cur.close()
        conn.close()