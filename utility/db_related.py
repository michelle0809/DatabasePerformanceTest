import psycopg2


def get_db_conn():
    conn = psycopg2.connect(
        host="localhost",
        port=6432,
        database="test_database",
        user="postgres",
        password="0000",
    )
    conn.autocommit = True
    return conn


def vacuum_analyze_table(target_table):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"""
            VACUUM ANALYZE performance_test.{target_table};
        """
    )
    conn.close()


def set_hypertable_compress_policy(target_table):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"""
            ALTER TABLE performance_test.{target_table}
            SET (
                timescaledb.compress = true,
                timescaledb.compress_orderby = 'created_at DESC',
                timescaledb.compress_segmentby = 'id'
            );
        """
    )

    cursor.execute(
        f"""
            SELECT add_compression_policy(
                hypertable := 'performance_test.{target_table}'::regclass,
                compress_after := INTERVAL '2 days'
            );
        """
    )
    conn.close()


def get_id_list(target_table, start_date, end_date):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"""
            SELECT id FROM performance_test.{target_table}
            WHERE created_at BETWEEN '{start_date}' AND '{end_date}';
        """
    )
    id_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    return id_list


def insert_data(cursor, target_table, data):
    try:
        cursor.execute(
            f"""
                INSERT INTO performance_test.{target_table} (
                content,
                created_at
            ) VALUES (
                '{data[0]}',
                '{data[1]}'::timestamp
            );
        """
        )
        return cursor.rowcount
    except Exception as e:
        print(f"Insert failed: {e}")
        return 0


def update_data(cursor, target_table, data):
    try:
        cursor.execute(
            f"""
                UPDATE performance_test.{target_table} 
            SET content = '{data[0]}'
                WHERE id = {data[1]};
            """
        )
        return cursor.rowcount
    except Exception as e:
        print(f"Update failed: {e}")
        return 0


def select_data(cursor, target_table, data):
    try:
        cursor.execute(
            f"""
                SELECT content 
            FROM performance_test.{target_table} 
            WHERE created_at BETWEEN '{data[0]}' AND '{data[1]}';
        """
        )
        result = cursor.fetchall()
        return len(result)
    except Exception as e:
        print(f"Select failed: {e}")
        return 0
