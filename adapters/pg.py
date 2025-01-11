import psycopg2
import psycopg2.extras


from contextlib import contextmanager


@contextmanager
def conn_context_postgres(pg_dsl: dict):
    conn = psycopg2.connect(**pg_dsl ,cursor_factory=psycopg2.extras.DictCursor)
    try:
        yield conn
    finally:
        conn.close()


def sql_exec_transaction(sql_list: list, pg_dsl: dict):
    with conn_context_postgres(pg_dsl) as conn:
        cursor = conn.cursor()
        for sql in sql_list:
            cursor.execute(sql)
        conn.commit()


def sql_get_cursor(query: str, pg_dsl: dict):
    with conn_context_postgres(pg_dsl) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    conn.close()
    return rows
