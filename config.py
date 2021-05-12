# ----------------------------------------------------------------------
# NOC config
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
import os
import socket
import sys
from urllib.parse import quote as urllib_quote

# NOC modules
from noc.core.config.base import BaseConfig, ConfigSection
from noc.core.config.params import (
    StringParameter,
    MapParameter,
    IntParameter,
    BooleanParameter,
    HandlerParameter,
    SecondsParameter,
    BytesParameter,
    FloatParameter,
    ServiceParameter,
    SecretParameter,
    ListParameter,
)


class Config(BaseConfig):
    loglevel = MapParameter(
        default="info",
        mappings={
            # pylint: disable=used-before-assignment
            "critical": logging.CRITICAL,
            # pylint: disable=used-before-assignment
            "error": logging.ERROR,
            # pylint: disable=used-before-assignment
            "warning": logging.WARNING,
            # pylint: disable=used-before-assignment
            "info": logging.INFO,
            # pylint: disable=used-before-assignment
            "debug": logging.DEBUG,
        },
    )

    class activator(ConfigSection):
        tos = IntParameter(min=0, max=255, default=0)
        script_threads = IntParameter(default=10)
        buffer_size = IntParameter(default=1048576)
        connect_retries = IntParameter(default=3, help="retries on immediate disconnect")
        connect_timeout = IntParameter(default=3, help="timeout after immediate disconnect")
        http_connect_timeout = IntParameter(default=20)
        http_request_timeout = IntParameter(default=30)
        http_validate_cert = BooleanParameter(default=False)

    class audit(ConfigSection):
        command_ttl = SecondsParameter(default="1m")
        login_ttl = SecondsParameter(default="1m")
        reboot_ttl = SecondsParameter(default="0")
        config_ttl = SecondsParameter(default="1y")
        db_ttl = SecondsParameter(default="5y")
        config_changed_ttl = SecondsParameter(default="1y")

    class backup(ConfigSection):
        keep_days = SecondsParameter(default="14d")
        keep_weeks = SecondsParameter(default="12w")
        keep_day_of_week = IntParameter(default="6")
        keep_months = IntParameter(default="12")
        keep_day_of_month = IntParameter(default="1")

    class bi(ConfigSection):
        language = StringParameter(default="en", help="Language BI interface")
        query_threads = IntParameter(default=10)
        extract_delay_alarms = SecondsParameter(default="1h")
        clean_delay_alarms = SecondsParameter(default="1d")
        reboot_interval = SecondsParameter(default="1M")
        extract_delay_reboots = SecondsParameter(default="1h")
        clean_delay_reboots = SecondsParameter(default="1d")
        chunk_size = IntParameter(default=500)
        extract_window = SecondsParameter(default="1d")
        enable_alarms = BooleanParameter(default=False)
        enable_reboots = BooleanParameter(default=False)
        enable_managedobjects = BooleanParameter(default=False)
        enable_alarms_archive = BooleanParameter(default=False)
        alarms_archive_policy = MapParameter(
            default="weekly",
            mappings={
                "weekly": '{{doc["clear_timestamp"].strftime("y%Yw%W")}}',
                "monthly": '{{doc["clear_timestamp"].strftime("y%Ym%m")}}',
                "quarterly": '{{doc["clear_timestamp"].strftime("y%Y")}}'
                '_quarter{{(doc["clear_timestamp"].month-1)//3 + 1}}',
                "yearly": '{{doc["clear_timestamp"].strftime("y%Y")}}',
            },
        )
        alarms_archive_batch_limit = IntParameter(default=10000)

    class biosegmentation(ConfigSection):
        processed_trials_ttl = SecondsParameter(default="1w")

    brand = StringParameter(default="NOC")

    class cache(ConfigSection):
        vcinterfacescount = SecondsParameter(default="1h")
        vcprefixes = SecondsParameter(default="1h")
        cache_class = StringParameter(default="noc.core.cache.mongo.MongoCache")
        default_ttl = SecondsParameter(default="1d")
        pool_size = IntParameter(default=8)

    class card(ConfigSection):
        language = StringParameter(default="en")
        alarmheat_tooltip_limit = IntParameter(default=5)

    class chwriter(ConfigSection):
        # LiftBridge partition (CH shard id)
        shard_id = IntParameter(help="CH Shard Id", default=0)
        # Unique replica number within shard
        replica_id = IntParameter(help="CH Partition Replica Id", default=0)
        # <address:port> of ClickHouse server to write
        write_to = StringParameter()
        #
        batch_size = IntParameter(default=50000, help="Size of one portion from queue")
        batch_delay_ms = IntParameter(default=10000, help="Send every period time")

    class classifier(ConfigSection):
        lookup_handler = HandlerParameter(default="noc.services.classifier.rulelookup.RuleLookup")
        default_interface_profile = StringParameter(default="default")
        default_rule = StringParameter(default="Unknown | Default")
        allowed_time_drift = SecondsParameter(default="5m")

    class clickhouse(ConfigSection):
        rw_addresses = ServiceParameter(service="clickhouse", wait=True)
        db = StringParameter(default="noc")
        rw_user = StringParameter(default="default")
        rw_password = SecretParameter()
        ro_addresses = ServiceParameter(service="clickhouse", wait=True)
        ro_user = StringParameter(default="readonly")
        ro_password = SecretParameter()
        request_timeout = SecondsParameter(default="1h")
        connect_timeout = SecondsParameter(default="10s")
        default_merge_tree_granularity = IntParameter(default=8192)
        encoding = StringParameter(default="", choices=["", "deflate", "gzip"])
        # Enable LowCardinality fileds
        enable_low_cardinality = BooleanParameter(default=False)
        # Cluster name for sharded/replicated configuration
        # Matches appropriative <remote_servers> part
        cluster = StringParameter()
        # Cluster topology
        # Expression in form
        # <topology> ::= <shard> | <shard>,<topology>
        # <shard> ::= [<weight>]<replicas>
        # <weight> := <DIGITS>
        # <replicas> := <DIGITS>
        # Examples:
        # 1 - non-replicated, non-sharded configuration
        # 1,1 - 2 shards, non-replicated
        # 2,2 - 2 shards, 2 replicas in each
        # 3:2,2 - first shard has 2 replicas an weight 3,
        #   second shard has 2 replicas and weight 1
        cluster_topology = StringParameter(default="1")

    class collections(ConfigSection):
        allow_sharing = BooleanParameter(default=True)

    class consul(ConfigSection):
        token = SecretParameter()
        connect_timeout = SecondsParameter(default="5s")
        request_timeout = SecondsParameter(default="1h")
        near_retry_timeout = IntParameter(default=1)
        host = StringParameter(default="consul")
        port = IntParameter(default=8500)
        check_interval = SecondsParameter(default="10s")
        check_timeout = SecondsParameter(default="1s")
        release = SecondsParameter(default="1M")
        session_ttl = SecondsParameter(default="10s")
        lock_delay = SecondsParameter(default="20s")
        retry_timeout = SecondsParameter(default="1s")
        keepalive_attempts = IntParameter(default=5)
        base = StringParameter(default="noc", help="kv lookup base")

    class correlator(ConfigSection):
        max_threads = IntParameter(default=20)
        topology_rca_window = IntParameter(default=0)
        discovery_delay = SecondsParameter(default="10M")
        auto_escalation = BooleanParameter(default=True)
        rca_lock_initial_timeout = FloatParameter(default=0.1)
        rca_lock_max_timeout = FloatParameter(default=3.0)
        rca_lock_rate = FloatParameter(default=1.61)
        rca_lock_dev = FloatParameter(default=0.1)
        rca_lock_expiry = SecondsParameter(default="10s")

    class customization(ConfigSection):
        favicon_url = StringParameter(default="/ui/web/img/logo_24x24_deep_azure.png")
        logo_url = StringParameter(default="/ui/web/img/logo_white.svg")
        logo_width = IntParameter(default=24)
        logo_height = IntParameter(default=24)
        branding_color = StringParameter(default="#ffffff")
        branding_background_color = StringParameter(default="#34495e")
        preview_theme = StringParameter(default="midnight")

    class date_time_formats(StringParameter):
        date_format = StringParameter(default="d.m.Y")
        datetime_format = StringParameter(default="d.m.Y H:i:s")
        month_day_format = StringParameter(default="F j")
        time_format = StringParameter(default="H:i:s")
        year_month_format = StringParameter(default="F Y")

    class dcs(ConfigSection):
        resolution_timeout = SecondsParameter(default="5M")
        resolver_expiration_timeout = SecondsParameter(default="10M")

    class discovery(ConfigSection):
        max_threads = IntParameter(default=20)
        sample = IntParameter(default=0)

    class dns(ConfigSection):
        warn_before_expired = SecondsParameter(default="30d")

    class escalator(ConfigSection):
        max_threads = IntParameter(default=5)
        retry_timeout = SecondsParameter(default="60s")
        tt_escalation_limit = IntParameter(default=10)
        ets = SecondsParameter(default="60s")
        wait_tt_check_interval = SecondsParameter(default="60s")
        sample = IntParameter(default=0)

    class etl(ConfigSection):
        compression = StringParameter(choices=["plain", "gzip", "bz2", "lzma"], default="gzip")

    class features(ConfigSection):
        use_uvloop = BooleanParameter(default=False)
        cp = BooleanParameter(default=True)
        sentry = BooleanParameter(default=False)
        traefik = BooleanParameter(default=False)
        cpclient = BooleanParameter(default=False)
        telemetry = BooleanParameter(
            default=False, help="Enable internal telemetry export to Clickhouse"
        )
        consul_healthchecks = BooleanParameter(
            default=True, help="While registering serive in consul also register health check"
        )
        service_registration = BooleanParameter(
            default=True, help="Permit consul self registration"
        )
        forensic = BooleanParameter(default=False)

    class fm(ConfigSection):
        active_window = SecondsParameter(default="1d")
        keep_events_wo_alarm = IntParameter(default=0)
        keep_events_with_alarm = IntParameter(default=-1)
        alarm_close_retries = IntParameter(default=5)
        outage_refresh = SecondsParameter(default="60s")
        total_outage_refresh = SecondsParameter(default="60s")

    class geocoding(ConfigSection):
        order = StringParameter(default="yandex,google")
        yandex_key = SecretParameter(default="")
        yandex_apikey = SecretParameter(default="")
        google_key = SecretParameter(default="")
        google_language = StringParameter(default="en")
        negative_ttl = SecondsParameter(default="7d", help="Period then saving bad result")
        ui_geocoder = StringParameter(default="")

    class gis(ConfigSection):
        ellipsoid = StringParameter(default="PZ-90")
        enable_osm = BooleanParameter(default=True)
        enable_google_sat = BooleanParameter(default=False)
        enable_google_roadmap = BooleanParameter(default=False)
        tile_size = IntParameter(default=256, help="Tile size 256x256")
        tilecache_padding = IntParameter(default=0)

    global_n_instances = IntParameter(default=1)

    class grafanads(ConfigSection):
        db_threads = IntParameter(default=10)

    class http_client(ConfigSection):
        connect_timeout = SecondsParameter(default="10s")
        request_timeout = SecondsParameter(default="1h")
        user_agent = StringParameter(default="noc")
        buffer_size = IntParameter(default=128 * 1024)
        max_redirects = IntParameter(default=5)

        ns_cache_size = IntParameter(default=1000)
        resolver_ttl = SecondsParameter(default="3s")

        http_port = IntParameter(default=80)
        https_port = IntParameter(default=443)
        validate_certs = BooleanParameter(default=False, help="Have to be set as True")

    class initial(ConfigSection):
        admin_user_name = StringParameter(default="admin")
        admin_password = StringParameter(default="admin")
        admin_email = StringParameter(default="test@example.com")

    installation_name = StringParameter(default="Unconfigured installation")
    installation_id = StringParameter(default="")

    instance = IntParameter(default=0)

    class kafkasender(ConfigSection):
        bootstrap_servers = StringParameter()
        username = StringParameter()
        password = SecretParameter()
        sasl_mechanism = StringParameter(
            choices=["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512"], default="PLAIN"
        )
        security_protocol = StringParameter(
            choices=["PLAINTEXT", "SASL_PLAINTEXT", "SSL", "SASL_SSL"], default="PLAINTEXT"
        )

    language = StringParameter(default="en")
    language_code = StringParameter(default="en")

    class layout(ConfigSection):
        ring_ring_edge = IntParameter(default=150)
        ring_chain_edge = IntParameter(default=150)
        ring_chain_spacing = IntParameter(default=100)
        tree_horizontal_step = IntParameter(default=100)
        tree_vertical_step = IntParameter(default=100)
        tree_max_levels = IntParameter(default=4)
        spring_propulsion_force = FloatParameter(default=1.5)
        spring_edge_force = FloatParameter(default=1.2)
        spring_bubble_force = FloatParameter(default=2.0)
        spring_edge_spacing = IntParameter(default=190)
        spring_iterations = IntParameter(default=50)

    class liftbridge(ConfigSection):
        addresses = ServiceParameter(service="liftbridge", wait=True, near=True, full_result=False)
        max_message_size = IntParameter(default=921600, help="Max message size for GRPC client")
        publish_async_ack_timeout = IntParameter(default=10)
        compression_threshold = IntParameter(default=524288)
        compression_method = StringParameter(choices=["", "zlib", "lzma"], default="zlib")
        enable_http_proxy = BooleanParameter(default=False)
        #  mx, kafkasender, events, dispose
        stream_events_retention_max_age = SecondsParameter(
            default="24h",
            help="FM events stream retention interval. If 0 use Liftbrdige setting value",
        )
        stream_events_retention_max_bytes = BytesParameter(
            default=0,
            help="FM events stream retention size (in bytes). If 0 use Liftbrdige setting value",
        )
        stream_events_segment_max_age = SecondsParameter(
            default="1h",
            help="FM events stream segment interval. Must be less retention age. If 0 use Liftbrdige setting value",
        )
        stream_events_segment_max_bytes = BytesParameter(
            default=0,
            help="FM events stream segment size. Must be less retention size. If 0 use Liftbrdige setting value",
        )
        stream_events_auto_pause_time = SecondsParameter(
            default=0, help="FM events stream pause time. If 0 use Liftbrdige setting value"
        )
        stream_events_auto_pause_disable_if_subscribers = BooleanParameter(default=False)
        stream_dispose_retention_max_age = SecondsParameter(
            default="24h",
            help="FM alarms stream retention interval. If 0 use Liftbrdige setting value",
        )
        stream_dispose_retention_max_bytes = BytesParameter(
            default=0,
            help="FM alarms stream retention size (in bytes). If 0 use Liftbrdige setting value",
        )
        stream_dispose_segment_max_age = SecondsParameter(
            default="1h",
            help="FM alarms stream segment interval. Must be less retention age. If 0 use Liftbrdige setting value",
        )
        stream_dispose_segment_max_bytes = BytesParameter(
            default=0,
            help="FM alarms stream segment size. Must be less retention size. If 0 use Liftbrdige setting value",
        )
        stream_dispose_auto_pause_time = SecondsParameter(
            default=0, help="FM alarms stream pause time. If 0 use Liftbrdige setting value"
        )
        stream_dispose_auto_pause_disable_if_subscribers = BooleanParameter(default=False)
        stream_message_retention_max_age = SecondsParameter(default="1h")
        stream_message_retention_max_bytes = BytesParameter(default=0)
        stream_message_segment_max_age = SecondsParameter(default="30M")
        stream_message_segment_max_bytes = BytesParameter(default=0)
        stream_message_auto_pause_time = SecondsParameter(default=0)
        stream_message_auto_pause_disable_if_subscribers = BooleanParameter(default=False)
        stream_kafkasender_retention_max_age = SecondsParameter(default="1h")
        stream_kafkasender_retention_max_bytes = BytesParameter(default=0)
        stream_kafkasender_segment_max_age = SecondsParameter(default="30M")
        stream_kafkasender_segment_max_bytes = BytesParameter(default=0)
        stream_kafkasender_auto_pause_time = SecondsParameter(default=0)
        stream_kafkasender_auto_pause_disable_if_subscribers = BooleanParameter(default=False)
        stream_ch_retention_max_age = SecondsParameter(default="1h")
        stream_ch_retention_max_bytes = BytesParameter(default="100M")
        stream_ch_segment_max_age = SecondsParameter(default="30M")
        stream_ch_segment_max_bytes = BytesParameter(default="50M")
        stream_ch_auto_pause_time = SecondsParameter(default=0)
        stream_ch_auto_pause_disable_if_subscribers = BooleanParameter(default=False)
        stream_ch_replication_factor = IntParameter(
            default=1, help="Replicaton factor for clickhouse streams"
        )
        metrics_send_delay = FloatParameter(default=0.25)

    listen = StringParameter(default="auto:0")

    log_format = StringParameter(default="%(asctime)s [%(name)s] %(message)s")

    thread_stack_size = IntParameter(default=0)
    version_format = StringParameter(default="%(version)s+%(branch)s.%(number)s.%(changeset)s")

    class logging(ConfigSection):
        log_api_calls = BooleanParameter(default=False)
        log_sql_statements = BooleanParameter(default=False)

    class login(ConfigSection):
        methods = StringParameter(default="local")
        session_ttl = SecondsParameter(default="7d")
        language = StringParameter(default="en")
        restrict_to_group = StringParameter(default="")
        single_session_group = StringParameter(default="")
        mutual_exclusive_group = StringParameter(default="")
        idle_timeout = SecondsParameter(default="1w")
        pam_service = StringParameter(default="noc")
        radius_secret = SecretParameter(default="noc")
        radius_server = StringParameter()
        register_last_login = BooleanParameter(default=True)
        jwt_cookie_name = StringParameter(default="noc_jwt")
        jwt_algorithm = StringParameter(default="HS256", choices=["HS256", "HS384", "HS512"])

    class mailsender(ConfigSection):
        smtp_server = StringParameter()
        smtp_port = IntParameter(default=25)
        use_tls = BooleanParameter(default=False)
        helo_hostname = StringParameter(default="noc")
        from_address = StringParameter(default="noc@example.com")
        smtp_user = StringParameter()
        smtp_password = SecretParameter()

    class memcached(ConfigSection):
        addresses = ServiceParameter(service="memcached", wait=True, full_result=True)
        pool_size = IntParameter(default=8)
        default_ttl = SecondsParameter(default="1d")

    class message(ConfigSection):
        enable_alarm = BooleanParameter(default=False)
        enable_managedobject = BooleanParameter(default=False)
        enable_reboot = BooleanParameter(default=False)

    class mongo(ConfigSection):
        addresses = ServiceParameter(service="mongo", wait=True)
        db = StringParameter(default="noc")
        user = StringParameter()
        password = SecretParameter()
        rs = StringParameter()
        retries = IntParameter(default=20)
        timeout = SecondsParameter(default="3s")
        retry_writes = BooleanParameter(default=False)
        app_name = StringParameter()
        max_idle_time = SecondsParameter(default="60s")

    class mrt(ConfigSection):
        max_concurrency = IntParameter(default=50)
        enable_command_logging = BooleanParameter(default=False)

    node = socket.gethostname()

    class nbi(ConfigSection):
        max_threads = IntParameter(default=10)
        objectmetrics_max_interval = SecondsParameter(default="3h")

    class nsqd(ConfigSection):
        addresses = ServiceParameter(service="nsqd", wait=True, near=True, full_result=False)
        http_addresses = ServiceParameter(
            service="nsqdhttp", wait=True, near=True, full_result=False
        )
        pub_retries = IntParameter(default=5)
        pub_retry_delay = FloatParameter(default=1)
        mpub_messages = IntParameter(default=10000)
        mpub_size = IntParameter(default=1048576)
        topic_mpub_rate = IntParameter(default=10)
        ch_chunk_size = IntParameter(default=4000)
        connect_timeout = SecondsParameter(default="3s")
        request_timeout = SecondsParameter(default="30s")
        reconnect_interval = IntParameter(default=15)
        compression = StringParameter(choices=["", "deflate", "snappy"], default="")
        compression_level = IntParameter(default=6)
        max_in_flight = IntParameter(default=1)

    class nsqlookupd(ConfigSection):
        addresses = ServiceParameter(service="nsqlookupd", wait=True, near=True, full_result=False)
        http_addresses = ServiceParameter(service="nsqlookupdhttp", wait=True, full_result=False)

    class path(ConfigSection):
        smilint = StringParameter()
        smidump = StringParameter()
        dig = StringParameter()
        vcs_path = StringParameter(default="/usr/local/bin/hg")
        repo = StringParameter(default="/var/repo")
        backup_dir = StringParameter(default="/var/backup")
        etl_import = StringParameter(default="/var/lib/noc/import")
        ssh_key_prefix = StringParameter(default="etc/noc_ssh")
        cp_new = StringParameter(default="/var/lib/noc/cp/crashinfo/new")
        bi_data_prefix = StringParameter(default="/var/lib/noc/bi")
        babel_cfg = StringParameter(default="etc/babel.cfg")
        babel = StringParameter(default="./bin/pybabel")
        pojson = StringParameter(default="./bin/pojson")
        collection_fm_mibs = StringParameter(default="collections/fm.mibs/")
        supervisor_cfg = StringParameter(default="etc/noc_services.conf")
        legacy_config = StringParameter(default="etc/noc.yml")
        cythonize = StringParameter(default="./bin/cythonize")
        npkg_root = StringParameter(default="/var/lib/noc/var/pkg")
        card_template_path = StringParameter(default="services/card/templates/card.html.j2")
        pm_templates = StringParameter(default="templates/ddash/")
        custom_path = StringParameter()
        mib_path = StringParameter(default="/var/mib")

    class pg(ConfigSection):
        addresses = ServiceParameter(service="postgres", wait=True, near=True, full_result=False)
        db = StringParameter(default="noc")
        user = StringParameter()
        password = SecretParameter()
        connect_timeout = IntParameter(default=5)

    class ping(ConfigSection):
        throttle_threshold = FloatParameter()
        restore_threshold = FloatParameter()
        tos = IntParameter(min=0, max=255, default=0)
        # Recommended send buffer size, 4M by default
        send_buffer = IntParameter(default=4 * 1048576)
        # Recommended receive buffer size, 4M by default
        receive_buffer = IntParameter(default=4 * 1048576)
        # DataStream request limit
        ds_limit = IntParameter(default=1000)

    class proxy(ConfigSection):
        http_proxy = StringParameter(default=os.environ.get("http_proxy"))
        https_proxy = StringParameter(default=os.environ.get("https_proxy"))
        ftp_proxy = StringParameter(default=os.environ.get("ftp_proxy"))

    pool = StringParameter(default=os.environ.get("NOC_POOL", ""))

    class redis(ConfigSection):
        addresses = ServiceParameter(service="redis", wait=True, full_result=True)
        db = IntParameter(default=0)
        default_ttl = SecondsParameter(default="1d")

    class rpc(ConfigSection):
        retry_timeout = StringParameter(default="0.1,0.5,1,3,10,30")
        sync_connect_timeout = SecondsParameter(default="20s")
        sync_request_timeout = SecondsParameter(default="1h")
        sync_retry_timeout = FloatParameter(default=1.0)
        sync_retry_delta = FloatParameter(default=2.0)
        sync_retries = IntParameter(default=5)
        async_connect_timeout = SecondsParameter(default="20s")
        async_request_timeout = SecondsParameter(default="1h")

    class sae(ConfigSection):
        db_threads = IntParameter(default=20)
        activator_resolution_retries = IntParameter(default=5)
        activator_resolution_timeout = SecondsParameter(default="2s")

    class scheduler(ConfigSection):
        max_threads = IntParameter(default=20)
        submit_threshold_factor = IntParameter(default=10)
        max_chunk_factor = IntParameter(default=1)
        updates_per_check = IntParameter(default=4)
        cache_default_ttl = SecondsParameter(default="1d")
        autointervaljob_interval = SecondsParameter(default="1d")
        autointervaljob_initial_submit_interval = SecondsParameter(default="1d")

    class script(ConfigSection):
        timeout = SecondsParameter(default="2M", help="default sa script script timeout")
        session_idle_timeout = SecondsParameter(default="1M", help="default session timeout")
        caller_timeout = SecondsParameter(default="1M")
        calling_service = StringParameter(default="script")

    secret_key = StringParameter(default="12345")

    class selfmon(ConfigSection):
        enable_managedobject = BooleanParameter(default=True)
        managedobject_ttl = IntParameter(default=30)
        enable_task = BooleanParameter(default=False)
        task_ttl = IntParameter(default=30)
        enable_inventory = BooleanParameter(default=False)
        inventory_ttl = IntParameter(default=30)
        enable_fm = BooleanParameter(default=False)
        fm_ttl = IntParameter(default=30)
        enable_liftbridge = BooleanParameter(default=False)
        liftbridge_ttl = IntParameter(default=30)

    class sentry(ConfigSection):
        url = StringParameter(default="")
        shutdown_timeout = IntParameter(min=1, max=10, default=2)
        default_integrations = BooleanParameter(default=False)
        debug = BooleanParameter(default=False)
        max_breadcrumbs = IntParameter(min=1, max=100, default=10)

    class syslogcollector(ConfigSection):
        listen = StringParameter(default="0.0.0.0:514")
        enable_reuseport = BooleanParameter(default=True)
        enable_freebind = BooleanParameter(default=False)
        # DataStream request limit
        ds_limit = IntParameter(default=1000)

    class icqsender(ConfigSection):
        token = SecretParameter()
        retry_timeout = IntParameter(default=2)
        use_proxy = BooleanParameter(default=False)

    class tgsender(ConfigSection):
        token = SecretParameter()
        retry_timeout = IntParameter(default=2)
        use_proxy = BooleanParameter(default=False)

    class threadpool(ConfigSection):
        idle_timeout = SecondsParameter(default="30s")
        shutdown_timeout = SecondsParameter(default="1M")

    timezone = StringParameter(default="Europe/Moscow")

    class traceback(ConfigSection):
        reverse = BooleanParameter(default=True)

    class trapcollector(ConfigSection):
        listen = StringParameter(default="0.0.0.0:162")
        enable_reuseport = BooleanParameter(default=True)
        enable_freebind = BooleanParameter(default=False)
        # DataStream request limit
        ds_limit = IntParameter(default=1000)

    class web(ConfigSection):
        theme = StringParameter(default="gray")
        api_row_limit = IntParameter(default=0)
        api_unlimited_row_limit = IntParameter(default=1000)
        api_arch_alarm_limit = IntParameter(default=4 * 86400)
        api_alarm_comments_limit = IntParameter(
            default=10, help="Max Alarm comment count on UI Popup"
        )
        max_upload_size = IntParameter(default=16777216)
        language = StringParameter(default="en")
        install_collection = BooleanParameter(default=False)
        max_threads = IntParameter(default=10)
        macdb_window = IntParameter(default=4 * 86400)
        enable_remote_system_last_extract_info = BooleanParameter(default=False)
        heatmap_lon = StringParameter(default="108.567849")
        heatmap_lat = StringParameter(default="66.050063")
        heatmap_zoom = StringParameter(default="4")

    class ui(ConfigSection):
        max_avatar_size = BytesParameter(default="256K")
        max_rest_limit = IntParameter(default=100)

    class datasource(ConfigSection):
        chunk_size = IntParameter(default=1000)
        max_threads = IntParameter(default=10)
        default_ttl = SecondsParameter(default="1h")

    class datastream(ConfigSection):
        enable_administrativedomain = BooleanParameter(default=False)
        enable_administrativedomain_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for Adm. Domain datastream (Mongo greater 3.6 needed)",
        )
        administrativedomain_ttl = SecondsParameter(
            default="0",
            help="Removing datastream administrativedomain records older days",
        )
        enable_alarm = BooleanParameter(default=False)
        enable_alarm_wait = BooleanParameter(
            default=True, help="Activate Wait Mode for Alarm datastream (Mongo greater 3.6 needed)"
        )
        alarm_ttl = SecondsParameter(
            default="14d",
            help="Removing datastream alarm records older days",
        )
        enable_cfgping = BooleanParameter(default=True)
        enable_cfgping_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for CfgPing datastream (Mongo greater 3.6 needed)",
        )
        cfgping_ttl = SecondsParameter(
            default="0",
            help="Removing datastream cfgping records older days",
        )
        enable_cfgsyslog = BooleanParameter(default=True)
        enable_cfgsyslog_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for CfgSyslog datastream (Mongo greater 3.6 needed)",
        )
        cfgsyslog_ttl = SecondsParameter(
            default="0",
            help="Removing datastream cfgsyslog records older days",
        )
        enable_cfgtrap = BooleanParameter(default=True)
        enable_cfgtrap_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for CfgTrap datastream (Mongo greater 3.6 needed)",
        )
        cfgtrap_ttl = SecondsParameter(
            default="0",
            help="Removing datastream cfgtrap records older days",
        )
        enable_dnszone = BooleanParameter(default=False)
        enable_dnszone_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for DNS Zone datastream (Mongo greater 3.6 needed)",
        )
        dnszone_ttl = SecondsParameter(
            default="0",
            help="Removing datastream dnszone records older days",
        )
        enable_managedobject = BooleanParameter(default=False)
        enable_managedobject_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for ManagedObject datastream (Mongo greater 3.6 needed)",
        )
        managedobject_ttl = SecondsParameter(
            default="0",
            help="Removing datastream managedobject records older days",
        )
        enable_resourcegroup = BooleanParameter(default=False)
        enable_resourcegroup_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for ResourceGroup datastream (Mongo greater 3.6 needed)",
        )
        resourcegroup_ttl = SecondsParameter(
            default="0",
            help="Removing datastream resourcegroup records older days",
        )
        enable_vrf = BooleanParameter(default=False)
        enable_vrf_wait = BooleanParameter(
            default=True, help="Activate Wait Mode for VRF datastream (Mongo greater 3.6 needed)"
        )
        vrf_ttl = SecondsParameter(
            default="0",
            help="Removing datastream vrf records older days",
        )
        enable_prefix = BooleanParameter(default=False)
        enable_prefix_wait = BooleanParameter(
            default=True, help="Activate Wait Mode for Prefix datastream (Mongo greater 3.6 needed)"
        )
        prefix_ttl = SecondsParameter(
            default="0",
            help="Removing datastream prefix records older days",
        )
        enable_address = BooleanParameter(default=False)
        enable_address_wait = BooleanParameter(
            default=True,
            help="Activate Wait Mode for Address datastream (Mongo greater 3.6 needed)",
        )
        address_ttl = SecondsParameter(
            default="0",
            help="Removing datastream address records older days",
        )

    class help(ConfigSection):
        base_url = StringParameter(default="https://docs.getnoc.com")
        branch = StringParameter(default="microservices")
        language = StringParameter(default="en")

    class tests(ConfigSection):
        # List of pyfilesystem URLs holding intial data
        fixtures_paths = ListParameter(item=StringParameter(), default=["tests/data"])
        # List of pyfilesystem URLs holding event classification samples
        events_paths = ListParameter(item=StringParameter())
        # List of pyfilesystem URLs holding beef test cases
        beef_paths = ListParameter(item=StringParameter())

    class peer(ConfigSection):
        enable_ripe = BooleanParameter(default=True)
        enable_arin = BooleanParameter(default=True)
        enable_radb = BooleanParameter(default=True)
        prefix_list_optimization = BooleanParameter(default=True)
        prefix_list_optimization_threshold = IntParameter(default=1000)
        max_prefix_length = IntParameter(default=24)
        rpsl_inverse_pref_style = BooleanParameter(default=False)

    class metrics(ConfigSection):
        default_hist = ListParameter(
            item=FloatParameter(), default=[0.001, 0.005, 0.01, 0.05, 0.5, 1.0, 5.0, 10.0]
        )
        enable_mongo_hist = BooleanParameter(default=False)
        mongo_hist = ListParameter(
            item=FloatParameter(), default=[0.001, 0.005, 0.01, 0.05, 0.5, 1.0, 5.0, 10.0]
        )
        enable_postgres_hist = BooleanParameter(default=False)
        postgres_hist = ListParameter(
            item=FloatParameter(), default=[0.001, 0.005, 0.01, 0.05, 0.5, 1.0, 5.0, 10.0]
        )
        default_quantiles = ListParameter(item=FloatParameter(), default=[0.5, 0.9, 0.95])
        default_quantiles_epsilon = 0.01
        default_quantiles_window = 60
        default_quantiles_buffer = 100
        enable_mongo_quantiles = BooleanParameter(default=False)
        enable_postgres_quantiles = BooleanParameter(default=False)

    # pylint: disable=super-init-not-called
    def __init__(self):
        self.setup_logging()

    @property
    def pg_connection_args(self):
        """
        PostgreSQL database connection arguments
        suitable to pass to psycopg2.connect
        """
        return {
            "host": self.pg.addresses[0].host,
            "port": self.pg.addresses[0].port,
            "database": self.pg.db,
            "user": self.pg.user,
            "password": self.pg.password,
        }

    @property
    def mongo_connection_args(self):
        """
        Mongo connection arguments. Suitable to pass to
        pymongo.connect and mongoengine.connect
        """
        if not hasattr(self, "_mongo_connection_args"):
            self._mongo_connection_args = {
                "db": self.mongo.db,
                "username": self.mongo.user,
                "password": self.mongo.password,
            }
            if self.mongo.app_name:
                self._mongo_connection_args["appname"] = self.mongo.app_name
            if self.mongo.retry_writes:
                self._mongo_connection_args["retryWrites"] = True
            has_credentials = self.mongo.user or self.mongo.password
            if has_credentials:
                self._mongo_connection_args["authentication_source"] = self.mongo.db
            hosts = self.mongo.addresses
            if self.mongo.rs:
                self._mongo_connection_args["replicaSet"] = self.mongo.rs
                self._mongo_connection_args["readPreference"] = "secondaryPreferred"
            elif len(hosts) > 1:
                raise ValueError("Replica set name must be set")
            if self.mongo.max_idle_time:
                self._mongo_connection_args["maxIdleTimeMS"] = self.mongo.max_idle_time * 1000
            url = ["mongodb://"]
            if has_credentials:
                url += [
                    "%s:%s@" % (urllib_quote(self.mongo.user), urllib_quote(self.mongo.password))
                ]
            url += [",".join(str(h) for h in hosts)]
            url += ["/%s" % self.mongo.db]
            self._mongo_connection_args["host"] = "".join(url)
            if self.metrics.enable_mongo_hist:
                from noc.core.mongo.monitor import MongoCommandSpan

                self._mongo_connection_args["event_listeners"] = [MongoCommandSpan()]
        return self._mongo_connection_args

    def setup_logging(self, loglevel=None):
        """
        Create new or setup existing logger
        """
        if not loglevel:
            loglevel = self.loglevel
        logger = logging.getLogger()
        if len(logger.handlers):
            # Logger is already initialized
            fmt = logging.Formatter(self.log_format, None)
            for h in logging.root.handlers:
                if isinstance(h, logging.StreamHandler):
                    h.stream = sys.stdout
                h.setFormatter(fmt)
            logging.root.setLevel(loglevel)
        else:
            # Initialize logger
            logging.basicConfig(stream=sys.stdout, format=self.log_format, level=loglevel)
        logging.captureWarnings(True)

    def get_customized_paths(self, *args, **kwargs):
        """
        Check for customized path for given repo path.
        Repo path may be given in os.path.join-style components.
        Returns list of possible paths. One of elements is always repo path,
        while other may be custom counterpart, if exists.
        :param prefer_custom: True - customized path first, False - repo path first
        :param args: Path or path components in os.path.join-style
        :return: List of possible paths
        """
        prefer_custom = kwargs.get("prefer_custom", False)
        rpath = os.path.join(*args)
        if not self.path.custom_path:
            return [rpath]
        cpath = os.path.join(self.path.custom_path, *args)
        if os.path.exists(cpath):
            if prefer_custom:
                return [cpath, rpath]
            else:
                return [rpath, cpath]
        return [rpath]

    def get_hist_config(self, name):
        """
        Get configuration for hist `name`. Returns list of times or None, if hist is disabled
        :param name: Hist name
        :return: List of hist config or None
        """
        # Check hist is enabled
        if not getattr(self.metrics, "enable_%s_hist" % name, False):
            return None
        # Get config
        cfg = getattr(self.metrics, "%s_hist" % name)
        if cfg:
            return cfg
        # Fallback to defaults
        return self.metrics.default_hist or None

    def get_quantiles_config(self, name):
        """
        Check if quantile is enabled
        :return: True if quantile is enabled
        """
        # Check quantiles is enabled
        return getattr(self.metrics, "enable_%s_quantiles" % name, False)


config = Config()
config.load()
config.setup_logging()
