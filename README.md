# PostgreSQL Insert / Update TPS Performance Test

## 說明

簡單測試對 PostgreSQL 的 Normal Table / Partitioned Table / TimeScaleDB Hypertable 寫入資料，測試 Insert / Update / SELECT TPS。

* 均透過 pgBouncer (6432 port) 連線 PostgreSQL test_database 資料庫。
* 環境已安裝 pg_partman、timescaledb 套件，並已透過 create_table.sql 語法建立 Normal Table / Partitioned Table / TimeScaleDB Hypertable 資料表。
* 測試會開 10 個 Thread 個別連線資料庫，有 10 個連線同時執行 INSERT 或 UPDATE 操作，最終計算 TPS。
* Hypertable 已壓縮的表仍可 INSERT / UPDATE 資料，故也測試壓縮對 INSERT / UPDATE TPS 的影響。
* 每次 INSERT / UPDATE 都是 1 筆資料操作。

## 測試項目
* Normal Table
    * Insert 7天前 ~ 當日共 1,000,000 筆資料
    * Update 7天前 ~ 當日共 1,000,000 筆資料
    * Select 7天前 ~ 當日期間隨機 1 小時資料共 10,000 次
* Partitioned Table
    * Insert 7天前 ~ 當日共 1,000,000 筆資料
    * Update 7天前 ~ 當日共 1,000,000 筆資料
    * Select 7天前 ~ 當日期間隨機 1 小時資料共 10,000 次
* Hypertable
    * Insert 7天前 ~ 當日共 1,000,000 筆資料
    * Update 7天前 ~ 當日共 1,000,000 筆資料
    * Select 7天前 ~ 當日期間隨機 1 小時資料共 10,000 次
* Compressed Hypertable
    * Insert 7天前 ~ 3天前共 1,000,000 筆資料
    * Update 7天前 ~ 3天前共 1,000,000 筆資料
    * Select 7天前 ~ 3天前期間隨機 1 小時資料共 10,000 次

## 檔案結構

```.
├── README.md                 # 說明文件
├── transaction_per_second.py # 主要執行檔
├── create_table.sql          # 建立測試用表格的 SQL 腳本
├── requirements.txt          # 所需套件
└── utility/                  # 功能
    ├── __init__.py           # 初始化檔
    ├── db_related.py         # 資料庫相關操作函式
    └── run_test.py           # 測試執行相關函式
```

## 測試結果表格
* 測試時間 2025/05/10(六)
```
[Normal Table - Insert] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 649,772.00
TPS:                      1,539.00  
==================================================

[Normal Table - Update] Testing...
Complete 99%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 656,834.26
TPS:                      1,522.45  
==================================================

[Normal Table - Select] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        10,000    
Average affected data:    5,936.69  
Total execution time(ms): 607,044.08
TPS:                      16.47     
==================================================

[Partitioned Table - Insert] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 655,100.30
TPS:                      1,526.48  
==================================================

[Partitioned Table - Update] Testing...
Complete 99%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 883,995.75
TPS:                      1,131.23  
==================================================

[Partitioned Table - Select] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        10,000    
Average affected data:    5,931.11  
Total execution time(ms): 135,430.86
TPS:                      73.84     
==================================================

[Hypertable - Insert] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 706,785.63
TPS:                      1,414.86  
==================================================

[Hypertable - Update] Testing...
Complete 99%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 959,176.44
TPS:                      1,042.56  
==================================================

[Hypertable - Select] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        10,000    
Average affected data:    5,939.73  
Total execution time(ms): 108,437.72
TPS:                      92.22     
==================================================

[Compress Hypertable - Insert] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 740,068.81
TPS:                      1,351.23  
==================================================

[Compress Hypertable - Update] Testing...
Complete 99%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        1,000,000 
Average affected data:    1.00      
Total execution time(ms): 1,258,084.59
TPS:                      794.86    
==================================================

[Compress Hypertable - Select] Testing...
Complete 100%
==================================================
                     Summary                      
--------------------------------------------------
Connection count:         10
Transaction count:        10,000    
Average affected data:    16,297.73 
Total execution time(ms): 330,449.19
TPS:                      30.26     
==================================================
```