import time
import random
from queue import Queue
from threading import Thread
import string
from . import db_related as db
from datetime import timedelta


def random_string(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_time(start_date, end_date):
    return start_date + (end_date - start_date) * random.random()


def generate_insert_test_data(queues, target_table, start_date, end_date):
    data_count = 1000000
    for i in range(1, data_count + 1):
        if i % 10000 == 0:
            print(f"Complete {int(i / data_count * 100)}%", end="\r", flush=True)
        params = [random_string(), random_time(start_date, end_date)]
        queue_idx = i % len(queues)
        queues[queue_idx].put(("insert", target_table, params))


def generate_update_test_data(queues, target_table, start_date, end_date):
    data_count = 1000000
    id_list = db.get_id_list(target_table, start_date, end_date)

    if len(id_list) == 0:
        print("No data to update")
        return

    # 打亂 ID 清單
    random.shuffle(id_list)

    # 如果資料量不足，重複使用 ID
    if len(id_list) < data_count:
        id_list = id_list * (data_count // len(id_list) + 1)

    for i in range(data_count):
        if i % 10000 == 0:
            print(f"Complete {int(i / data_count * 100)}%", end="\r", flush=True)
        params = [random_string(), id_list[i]]
        queue_idx = i % len(queues)
        queues[queue_idx].put(("update", target_table, params))


def generate_select_test_data(queues, target_table, start_date, end_date):
    data_count = 10000
    for i in range(1, data_count + 1):
        if i % 100 == 0:
            print(f"Complete {int(i / data_count * 100)}%", end="\r", flush=True)
        input_start_date = random_time(start_date, end_date)
        input_end_date = input_start_date + timedelta(hours=1)
        params = [input_start_date, input_end_date]
        queue_idx = i % len(queues)
        queues[queue_idx].put(("select", target_table, params))


def executor(queue, in_out_dict):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    cnt = 0
    aff = 0
    start_time = time.time() * 1000  # milliseconds

    while True:
        task = queue.get()
        # task = [action, table, params]

        if task is None:
            # 結束，記錄時間
            end_time = time.time() * 1000  # milliseconds
            in_out_dict["transaction_cnt"] = cnt
            in_out_dict["affected_data_cnt"] = aff
            in_out_dict["start_time"] = start_time
            in_out_dict["end_time"] = end_time
            cursor.close()
            conn.close()
            break

        if task[0] == "insert":
            res = db.insert_data(cursor, task[1], task[2])
            if res == 0:
                print("Insert failed")
            else:
                cnt += 1
                aff += res

        elif task[0] == "update":
            res = db.update_data(cursor, task[1], task[2])
            if res == 0:
                print("Update failed")
            else:
                cnt += 1
                aff += res
        elif task[0] == "select":
            res = db.select_data(cursor, task[1], task[2])
            if res == 0:
                print(f"Select failed: {task[2]}")
            else:
                cnt += 1
                aff += res


def run_test(target_table, action, start_date, end_date):
    connection_count = 10

    # 為每個 Thread 的執行數和起迄時間
    thread_results = [
        {
            "transaction_cnt": 0,
            "affected_data_cnt": 0,
            "start_time": 0,
            "end_time": 0,
        }
        for _ in range(connection_count)
    ]

    # 建立 Queue
    queues = [Queue(maxsize=100) for _ in range(connection_count)]

    # 建立 Threads，每個執行緒使用自己的結果字典
    threads = [
        Thread(target=executor, args=(queues[i], thread_results[i]))
        for i in range(connection_count)
    ]

    # 啟動 Threads
    for thread in threads:
        thread.start()

    # 產生資料
    if action == "insert":
        generate_insert_test_data(queues, target_table, start_date, end_date)
    elif action == "update":
        generate_update_test_data(queues, target_table, start_date, end_date)
    elif action == "select":
        generate_select_test_data(queues, target_table, start_date, end_date)

    # 發送結束Task
    for queue in queues:
        queue.put(None)

    # 等待所有Thread結束並收集結果
    total_cnt = 0
    total_aff_data_cnt = 0
    execution_time = 0

    for thread in threads:
        thread.join()

    # 彙整結果
    for result in thread_results:
        total_cnt += result["transaction_cnt"]
        total_aff_data_cnt += result["affected_data_cnt"]
        execution_time += result["end_time"] - result["start_time"]

    tps = total_cnt / (execution_time / 1000)

    print("\n" + "=" * 50)
    print("Summary".center(50))
    print("-" * 50)
    print(f"Connection count:         {connection_count}")
    print(f"Transaction count:        {total_cnt:<10,}")
    print(f"Average affected data:    {total_aff_data_cnt / total_cnt:<10,.2f}")
    print(f"Total execution time(ms): {execution_time:<10,.2f}")
    print(f"TPS:                      {tps:<10,.2f}")
    print("=" * 50 + "\n")
