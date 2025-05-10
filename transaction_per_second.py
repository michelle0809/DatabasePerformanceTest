from utility import db_related as db
from utility import run_test as ts
from datetime import datetime, timedelta
import time


def rest():
    time.sleep(60)


def main():
    # 設定時間範圍
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    start_date_compressed = end_date - timedelta(days=3)

    # 測試 Normal Table
    print("[Normal Table - Insert] Testing...")
    ts.run_test("normal_table", "insert", start_date, end_date)
    rest()

    print("[Normal Table - Update] Testing...")
    db.vacuum_analyze_table("normal_table")
    ts.run_test("normal_table", "update", start_date, end_date)
    rest()

    print("[Normal Table - Select] Testing...")
    db.vacuum_analyze_table("normal_table")
    ts.run_test("normal_table", "select", start_date, end_date)
    rest()

    # 測試 Partitioned Table
    print("[Partitioned Table - Insert] Testing...")
    ts.run_test("partitioned_table", "insert", start_date, end_date)
    rest()

    print("[Partitioned Table - Update] Testing...")
    db.vacuum_analyze_table("partitioned_table")
    ts.run_test("partitioned_table", "update", start_date, end_date)
    rest()

    print("[Partitioned Table - Select] Testing...")
    db.vacuum_analyze_table("partitioned_table")
    ts.run_test("partitioned_table", "select", start_date, end_date)
    rest()

    # 測試 Hypertable
    print("[Hypertable - Insert] Testing...")
    ts.run_test("hypertable", "insert", start_date, end_date)
    rest()

    print("[Hypertable - Update] Testing...")
    db.vacuum_analyze_table("hypertable")
    ts.run_test("hypertable", "update", start_date, end_date)
    rest()

    print("[Hypertable - Select] Testing...")
    db.vacuum_analyze_table("hypertable")
    ts.run_test("hypertable", "select", start_date, end_date)
    rest()

    # 測試壓縮後的 Hypertable
    print("[Compress Hypertable - Insert] Testing...")
    db.set_hypertable_compress_policy("hypertable")
    ts.run_test("hypertable", "insert", start_date, start_date_compressed)
    rest()

    print("[Compress Hypertable - Update] Testing...")
    db.vacuum_analyze_table("hypertable")
    ts.run_test("hypertable", "update", start_date, start_date_compressed)
    rest()

    print("[Compress Hypertable - Select] Testing...")
    db.vacuum_analyze_table("hypertable")
    ts.run_test("hypertable", "select", start_date, start_date_compressed)

    print("All tests completed.")


if __name__ == "__main__":
    main()
