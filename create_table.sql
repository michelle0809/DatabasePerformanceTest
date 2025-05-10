/* Common Object */
DROP SCHEMA IF EXISTS performance_test CASCADE;
CREATE SCHEMA performance_test;

/* Normal Table */
CREATE TABLE performance_test.normal_table (
    id bigserial primary key,
    content varchar not null,
    created_at timestamp with time zone not null default now()
);

/* Partitioned Table (with pg_partman) */
CREATE TABLE performance_test.partitioned_table (
    id bigserial,
    content varchar not null,
    created_at timestamp with time zone not null default now(),
    primary key (id, created_at)
) PARTITION BY RANGE (created_at);

DELETE FROM partman.part_config WHERE parent_table = 'performance_test.partitioned_table';

SELECT partman.create_parent(
    p_parent_table := 'performance_test.partitioned_table' -- 父表
    , p_control := 'created_at' -- Partition Key
    , p_interval := '1 day' -- 每個分區的時間長度
    , p_type := 'range' -- 支援 range/list partition
    , p_premake := 7 -- 領先於當前時間的分區數
    , p_start_partition := (current_date-7)::varchar -- 起始分區的時間/數值
    , p_default_table := true -- 是否建立 Default Partition
    , p_automatic_maintenance := 'on' -- 是否啟動自動維護
    , p_jobmon := false -- 是否透過 pg_jobmon 監控 pg_partman 的工作 (我沒安裝故設定 false)
    , p_control_not_null := true -- 是否 partition key 不能為 NULL
);

/* TimeScaleDB Hypertable */
CREATE TABLE performance_test.hypertable (
    id bigserial,
    content varchar not null,
    created_at timestamp with time zone not null default now(),
    primary key (id, created_at)
);

SELECT create_hypertable(
    relation := 'performance_test.hypertable'::regclass, -- 要轉換為 hypertable 的 table
    dimension := by_range('created_at', INTERVAL '1 day'), -- 維度
    create_default_indexes := true, -- 建立預設索引
    if_not_exists := true, -- 如果已經存在則不會建立
    migrate_data := false -- 是否需遷移資料
);