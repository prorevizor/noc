# ----------------------------------------------------------------------
# Convert path PM Schema to labels
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime

# NOC Modules
from noc.pm.models.metricscope import MetricScope
from noc.core.clickhouse.connect import connection
from noc.config import config

# DB with old schema data (with path)
SOURCE_DB_NAME = "noc_old"
DEST_DB_NAME = config.clickhouse.db
# DEST_DB_NAME = "noc"
CH_USER = config.clickhouse.rw_user
# CH_USER = "noc"
CH_PASSWORD = config.clickhouse.rw_password
# END data for old data
# END_DATE = datetime.datetime(2021, 4, 4)
END_DATE = None
# For speedup if used cluster replica data will be query between replica
CH_REPLICAS = []
#
# If needed one query - MIGRATE_CHUNK great than MIGRATE_DEPTH
MIGRATE_DEPTH = 7
MIGRATE_CHUNK = 30

client = connection()


def fix():
    if CH_REPLICAS:
        # For replicated schema
        for rep1, rep2 in CH_REPLICAS:
            rep1_migrate = []
            rep2_migrate = []
            for ms in MetricScope.objects.filter():
                for start, stop in iter_time_interval():
                    query = get_insert_query(ms, start, stop, remote=rep2)
                    if not query:
                        continue
                    # print(f'clickhouse-client -h {rep1} --query="{query}"')
                    rep1_migrate += [f'clickhouse-client -h {rep1} --query="{query}"']
                    query = get_insert_query(ms, start, stop, remote=rep1)
                    rep2_migrate += [f'clickhouse-client -h {rep2} --query="{query}"']
                    # print(f'clickhouse-client -h {rep2} --query="{query}"\n\n')
            rep2_migrate = "\n\n".join(rep2_migrate)
            rep1_migrate = "\n\n".join(rep1_migrate)
            print(f'\n{"="*10}Migrate: {rep1} to {rep2}{"="*10}\n{rep2_migrate}')
            print(f'\n{"="*10}Migrate: {rep2} to {rep1}{"="*10}\n{rep1_migrate}')
    else:
        for ms in MetricScope.objects.filter():
            for start, stop in iter_time_interval():
                query = get_insert_query(ms, start, stop, remote=None)
                if not query:
                    continue
                print(f'clickhouse-client -h 0.0.0.0 --query="{query}"\n\n')


def get_insert_query(metric_scope: "MetricScope", start, stop, remote=None):
    table_name = metric_scope._get_raw_db_table()
    if remote:
        # For migrate remote table use another DB
        query_from = (
            f"remote('{remote}', '{SOURCE_DB_NAME}', '{table_name}', '{CH_USER}', '{CH_PASSWORD}')"
        )
    else:
        query_from = f"{SOURCE_DB_NAME}.{table_name}"
    try:
        r = client.execute(f"DESCRIBE {SOURCE_DB_NAME}.{table_name}")
    except Exception:
        # print(f"No Old Table for metricScope: {metric_scope.name}")
        return ""
    path_ex = []
    # Expression for path convert
    for num, label in enumerate(metric_scope.labels, start=1):
        if not label.is_path:
            continue
        path_ex += [f"arrayStringConcat(['{label.label_prefix}',path[{num}]])"]
    insert_fields = []
    select_fields = []
    for fn, *_ in r:
        if fn == "path" and path_ex:
            insert_fields += ["labels"]
            select_fields += [
                f'arrayFilter(x -> NOT endsWith(x, \'::\'), [{", ".join(path_ex)}]) as labels'
            ]
            continue
        elif fn == "path":
            continue
        insert_fields += [fn]
        select_fields += [fn]
    return (
        f"INSERT INTO {DEST_DB_NAME}.{metric_scope._get_raw_db_table()} "
        f'({", ".join(insert_fields)}) '
        f'SELECT {", ".join(select_fields)} '
        f"FROM {query_from} "
        f"WHERE date >= '{start.date().isoformat()}' AND date < '{stop.date().isoformat()}' ;"
    )


def iter_time_interval():
    now = datetime.datetime.now()
    end = END_DATE or now.replace(minute=0, second=0, microsecond=0)
    start = end - datetime.timedelta(days=MIGRATE_DEPTH)
    if MIGRATE_DEPTH <= MIGRATE_CHUNK:
        stop = min(end, start + datetime.timedelta(days=MIGRATE_CHUNK))
        yield start, stop
        return
    # Shft stop to chunked interval
    # stop += datetime.timedelta(days=MIGRATE_CHUNK)
    # start = start.date()
    while start < end:
        stop = min(end, start + datetime.timedelta(days=MIGRATE_CHUNK))
        if start.month != stop.month:
            # Split query to month chunked
            yield start.replace(day=1), stop.replace(day=1)
        start += datetime.timedelta(days=MIGRATE_CHUNK)
    else:
        yield start.replace(day=1), stop
