# ----------------------------------------------------------------------
# BaseReportDatasource
# ----------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Iterable, Any
import time
import re
import heapq
import itertools
import logging

# NOC modules
from django.db.models import Q as d_Q
from noc.sa.models.managedobject import ManagedObject
from .report_objectstat import (
    AttributeIsolator,
    CapabilitiesIsolator,
    StatusIsolator,
    ProblemIsolator,
)

logger = logging.getLogger(__name__)


def iterator_to_stream(iterator):
    """Convert an iterator into a stream (None if the iterator is empty)."""
    try:
        return next(iterator), iterator
    except StopIteration:
        return None


def stream_next(stream):
    """Get (next_value, next_stream) from a stream."""
    val, iterator = stream
    return val, iterator_to_stream(iterator)


def merge(iterators):
    """Make a lazy sorted iterator that merges lazy sorted iterators."""
    streams = [iterator_to_stream(g) for g in [iter(y) for y in iterators]]
    heapq.heapify(streams)
    while streams:
        stream = heapq.heappop(streams)
        if stream is not None:
            val, stream = stream_next(stream)
            heapq.heappush(streams, stream)
            yield val


class BaseReportColumn(object):
    """
    Base report column class.
    Column is dataseries: ((id1: value1), (id2: value2)) - id - index sorted by asc
    """

    MAX_ITERATOR = 800000
    name = None  # ColumnName
    fields = None  # RowFields List
    unknown_value = (None,)  # Fill this if empty value
    builtin_sorted = False  # Column index builtin sorted
    multiple_series = False  # Extract return dict columns dataseries
    # {"Series1_name": dataseries1, "Series2_name": dataseries2}

    def __init__(self, sync_ids=None):
        """

        :param sync_ids:
        """
        self.sync_ids = sync_ids  # Sorted Index list
        self.sync_count = itertools.count()
        self.sync_ids_i = iter(self.sync_ids)
        self._current_id = next(self.sync_ids_i, None)  # Current id
        self._value = None  #
        self._end_series = False  # Tre

    def safe_next(self):
        if next(self.sync_count) > self.MAX_ITERATOR:
            raise StopIteration
        return next(self.sync_ids_i, None)

    def _extract(self):
        """
        Generate list of rows. Each row is a list of fields. ("id1", "row1", "row2", "row3", ...)
        :return:
        """
        prev_id = 0
        if self.multiple_series and self.builtin_sorted:
            # return {STREAM_NAME1: iterator1, ....}
            yield from merge(self.extract())
        elif self.multiple_series and not self.builtin_sorted:
            raise NotImplementedError("Multiple series supported onl with builtin sorted")
        elif not self.builtin_sorted:
            # Unsupported builtin sorted.
            yield from sorted(self.extract())
        else:
            # Supported builtin sorted.
            for v in self.extract():
                if v[0] < prev_id:  # Todo
                    return  # Detect unordered stream
                yield v
                prev_id = v[0]

    def extract(self):
        """
        Generate list of rows. Each row is a list of fields. First value - is id
        :return:
        """
        raise NotImplementedError

    def __iter__(self):
        for row in self._extract():
            if not self._current_id:
                break
            # Row: (row_id, row1, ....)
            row_id, row_value = row[0], row[1:]
            if row_id == self._current_id:
                # @todo Check Duplicate ID
                # If row_id equal current sync_id - set value
                self._value = row_value
            elif row_id < self._current_id:
                # row_id less than sync_id, go to next row
                continue
            elif row_id > self._current_id:
                # row_id more than sync_id, go to next sync_id
                while self._current_id and row_id > self._current_id:
                    # fill row unknown_value
                    yield self.unknown_value
                    self._current_id = self.safe_next()
                if row_id == self._current_id:
                    # Match sync_id and row_id = set value
                    self._value = row_value
                else:
                    # Step over current sync_id, set unknown_value
                    # self._value = self.unknown_value
                    continue
            yield self._value  # return current value
            self._current_id = self.safe_next()  # Next sync_id
        self._end_series = True
        # @todo Variant:
        # 1. if sync_ids use to filter in _extract - sync_ids and _extract ending together
        # 2. if sync_ids end before _extract ?
        # 3. if _extract end before sync_ids ?
        if self._current_id:
            # If _extract end before sync_ids to one element
            yield self.unknown_value
        for _ in self.sync_ids_i:
            yield self.unknown_value

    def get_dictionary(self, filter_unknown=False):
        """
        return Dictionary id: value
        :return:
        """
        r = {}
        if not self._current_id:
            return r
        for _ in self:
            if filter_unknown and _[0] is self.unknown_value:
                continue
            r[self._current_id] = _[0]
            if self._end_series:
                break
        return r

    def __getitem__(self, item):
        # @todo use column as dict
        if item == self._current_id:
            return self._value
        return self.unknown_value
        # raise NotImplementedError


class LongestIter(object):
    """
    c_did = DiscoveryID._get_collection()
    did = c_did.find({"hostname": {"$exists": 1}},
    {"object": 1, "hostname": 1}).sort("object")
        # did = DiscoveryID.objects.filter(hostname__exists=True
        ).order_by("object").scalar("object", "hostname").no_cache()
    hostname = LongestIter(did)
    """

    def __init__(self, it):
        self._iterator = it
        self._end_iterator = False
        self._id = 0
        self._value = None
        self._default_value = None

    def __getitem__(self, item):
        if self._end_iterator:
            return self._default_value
        if self._id == item:
            return self._value
        elif self._id < item:
            self._id = item
            next(self, None)
            return self._value
        elif self._id > item:
            # print("Overhead")
            pass
        return self._default_value

    def __iter__(self):
        for val in self._iterator:
            if val["object"] == self._id:
                self._value = val["hostname"]
            elif val["object"] < self._id:
                continue
            elif val["object"] > self._id:
                self._id = val["object"]
                self._value = val["hostname"]
            yield
        self._end_iterator = True


class ReportModelFilter(object):
    """
    Getting statictics info for ManagedObject
    """

    decode_re = re.compile(r"(\d+)(\S+)(\d+)")

    model = ManagedObject  # Set on base class

    def __init__(self):
        self.formulas = """2is1.3hs0, 2is1.3hs0.5is1, 2is1.3hs0.5is2,
                2is1.3hs0.5is2.4hs0, 2is1.3hs0.5is2.4hs1, 2is1.3hs0.5is2.4hs1.5hs1"""
        self.f_map = {
            "is": StatusIsolator(),
            "hs": CapabilitiesIsolator(),
            "a": AttributeIsolator(),
            "isp": ProblemIsolator(),
        }
        self.logger = logger

    def decode(self, formula):
        """
        Decode stat formula and return isolated set
        :param formula:
        :return: moss: Result Query for Object
        :return: ids: Result id list for object
        """
        ids = []
        moss = self.model.objects.filter()
        for f in formula.split("."):
            self.logger.debug("Decoding: %s" % f)
            f_num, f_type, f_val = self.decode_re.findall(f.lower())[0]
            func_stat = self.f_map[f_type]
            func_stat = getattr(func_stat, "get_stat")(f_num, f_val)
            if isinstance(func_stat, set):
                ids += [func_stat]
            # @todo remove d_Q, example changing to class
            elif isinstance(func_stat, d_Q):
                moss = moss.filter(func_stat)
        self.logger.debug(moss.query)
        return moss, ids

    def proccessed(self, column):
        """
        Intersect set for result
        :param column: comma separated string stat formula.
        Every next - intersection prev
        :return:
        """
        r = {}
        for c in column.split(","):
            # print("Next column: %s" % c)
            moss, idss = self.decode(c.strip())
            ids = set(moss.values_list("id", flat=True))
            for i_set in idss:
                ids = ids.intersection(i_set)
            r[c.strip()] = ids.copy()
        return r


@dataclass
class ReportField:
    name: str
    label: str
    description: Optional[str] = ""
    unit: Optional[str] = None
    default: Optional[str] = None
    metric_name: Optional[str] = None  # Field name on clickhouse
    group: bool = False


@dataclass
class FilterValues:
    value: Any
    description: str


@dataclass
class ReportFilter:
    name: str
    type: str
    description: str
    values: Optional[FilterValues]
    required: bool


@dataclass
class ReportConfig:
    name: str
    description: str
    timebased: bool
    enabled: bool
    fields: List[ReportField]
    columns: List[ReportField] = field(init=False)
    groupby: List[str]
    intervals: List[str]
    filters: List[ReportFilter]
    dataretentiondays: int

    def __post_init__(self):
        self.columns = [f for f in self.fields]


class ReportDataSource(object):
    name = None
    description = None
    object_model = None

    # (List#, Name, Alias): TypeNormalizer or (TypeNormalizer, DefaultValue)
    FIELDS: List[ReportField] = []
    INTERVALS: List[str] = ["HOUR"]
    TIMEBASED: bool = False
    SORTED: bool = True

    def __init__(
        self,
        fields: List[str],
        objectids: List[str] = None,
        allobjectids: bool = False,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        interval: Optional[str] = None,
        max_intervals: Optional[int] = None,
        filters: Optional[List[str]] = None,
        rows: Optional[int] = None,
    ):
        self.fields = fields
        self.objectids = objectids
        self.allobjectids = allobjectids
        self.filters = filters or []
        self.interval = interval
        self.max_intervals = max_intervals
        self.rows = rows
        if self.TIMEBASED and not start:
            raise ValueError("Timebased Report required start param")
        self.end = end or datetime.datetime.now()
        self.start = start or self.end - datetime.timedelta(days=1)

    @classmethod
    def get_config(cls) -> ReportConfig:
        """
        Return ReportConfig
        :return:
        """
        return ReportConfig(
            name=cls.name,
            description=cls.description,
            timebased=cls.TIMEBASED,
            enabled=True,
            fields=cls.FIELDS,
            groupby=[f.name for f in cls.FIELDS if f.group],
            intervals=cls.INTERVALS,
            filters=[],
            dataretentiondays=1,
        )

    def iter_data(self):
        pass

    def extract(self) -> Iterable[Dict[str, int]]:
        """
        Generate list of rows. Each row is a list of fields. First value - is id
        :return:
        """
        raise NotImplementedError


class CHTableReportDataSource(ReportDataSource):
    CHUNK_SIZE = 5000
    TABLE_NAME = None
    object_field = "sa.ManagedObject"

    def get_client(self):
        if not hasattr(self, "_client"):
            from noc.core.clickhouse.connect import connection

            self._client = connection()
        return self._client

    def get_object_filter(self, ids) -> str:
        return f'{self.object_field} IN ({", ".join([str(c) for c in ids])})'

    group_intervals = {
        "HOUR": "toStartOfHour(toDateTime(any(ts))))",
        "DAY": "toStartOfDay(toDateTime(any(ts)))",
        "WEEK": "toStartOfWeek(toDateTime(any(ts)))",
        "MONTH": "toMonth(toDateTime(any(ts)))",
    }

    def get_group_interval(self) -> str:
        """
        If set max_intervals - use variants interval
        :return:
        """
        if self.max_intervals:
            minutes = ((self.end - self.start).total_seconds() / 60) / self.max_intervals
            return f"toStartOfInterval(ts, INTERVAL {minutes} minute)"
        return self.group_intervals[self.interval]

    def get_custom_conditions(self) -> Dict[str, List[str]]:
        return {
            "q_where": [
                f'{f} IN ({", ".join([str(c) for c in self.filters[f]])})' for f in self.filters
            ]
        }

    def get_query_ch(self, from_date: datetime.datetime, to_date: datetime.datetime) -> str:
        ts_from_date = time.mktime(from_date.timetuple())
        ts_to_date = time.mktime(to_date.timetuple())
        query_map = {
            "q_select": [],
            "q_where": [
                f"(date >= toDate({ts_from_date})) AND (ts >= toDateTime({ts_from_date}) AND ts <= toDateTime({ts_to_date})) %s",  # objectids_filter
            ],
        }
        ts = self.get_group_interval()
        query_map["q_select"] += [f"{ts} AS ts"]
        query_map["q_group"] = ["ts"]
        # if self.interval == "HOUR":
        #    query_map["q_select"] += ["toStartOfHour(toDateTime(ts)) AS ts"]
        #    query_map["q_group"] = ["ts"]
        for f in self.FIELDS:
            if f.name not in self.fields:
                continue
            query_map["q_select"] += [f"{f.metric_name} as {f.name}"]
        query_map["q_order_by"] = ["ts"]
        custom_conditions = self.get_custom_conditions()
        if "where" in custom_conditions:
            query_map["q_where"] += custom_conditions["where"]
        if "having" in custom_conditions:
            query_map["q_having"] = custom_conditions["having"]
        query = [
            f'SELECT {",".join(query_map["q_select"])}',
            f"FROM {self.TABLE_NAME}",
            f'WHERE {" AND ".join(query_map["q_where"])}',
        ]
        if "q_group" in query_map:
            query += [f'GROUP BY {",".join(query_map["q_group"])}']
        if "q_having" in query_map:
            query += [f'HAVING {" AND ".join(query_map["q_having"])}']
        if "q_order_by" in query_map:
            query += [f'ORDER BY {",".join(query_map["q_order_by"])}']
        if self.rows:
            query += [f"LIMIT {self.rows}"]
        return "\n ".join(query)

    def do_query(self):
        f_date, to_date = self.start, self.end
        query = self.get_query_ch(f_date, to_date)
        logger.info("Query: %s", query)
        client = self.get_client()
        if self.allobjectids or not self.objectids:
            for row in client.execute(query % ""):
                yield row
        else:
            # chunked query
            ids = self.objectids
            while ids:
                chunk, ids = ids[: self.CHUNK_SIZE], ids[self.CHUNK_SIZE :]
                for row in client.execute(query % f" AND {self.get_object_filter(chunk)}"):
                    yield row

    def extract(self):
        fields = []
        if self.interval:
            fields += ["ts"]
        fields += [f.name for f in self.FIELDS if f.name in self.fields]
        for row in self.do_query():
            yield dict(zip(fields, row))
