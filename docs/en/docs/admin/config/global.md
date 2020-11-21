# [global] section
Global service configuration

## loglevel

Default value
:   info

Possible values
:
* critical
* error
* warning
* info
* debug

YAML Path
:   global.loglevel

Key-Value Path
:   global/loglevel

Environment
:   NOC_GLOBAL_LOGLEVEL

## brand

Default value
:   NOC

YAML Path
:   global.brand

Key-Value Path
:   global/brand

Environment
:   NOC_GLOBAL_BRAND

## global_n_instances

Default value
:   1

YAML Path
:   global.global_n_instances

Key-Value Path
:   global/global_n_instances

Environment
:   NOC_GLOBAL_GLOBAL_N_INSTANCES

## installation_name

Default value
:   Unconfigured installation

YAML Path
:   global.installation_name

Key-Value Path
:   global/installation_name

Environment
:   NOC_GLOBAL_INSTALLATION_NAME

## installation_id

Default value
:   

YAML Path
:   global.installation_id

Key-Value Path
:   global/installation_id

Environment
:   NOC_GLOBAL_INSTALLATION_ID

## instance

Default value
:   0

YAML Path
:   global.instance

Key-Value Path
:   global/instance

Environment
:   NOC_GLOBAL_INSTANCE

## language

Default value
:   en

YAML Path
:   global.language

Key-Value Path
:   global/language

Environment
:   NOC_GLOBAL_LANGUAGE

## language_code

Default value
:   en

YAML Path
:   global.language_code

Key-Value Path
:   global/language_code

Environment
:   NOC_GLOBAL_LANGUAGE_CODE

## listen

Default value
:   auto:0

YAML Path
:   global.listen

Key-Value Path
:   global/listen

Environment
:   NOC_GLOBAL_LISTEN

## log_format

Default value
:   %(asctime)s [%(name)s] %(message)s

YAML Path
:   global.log_format

Key-Value Path
:   global/log_format

Environment
:   NOC_GLOBAL_LOG_FORMAT

## thread_stack_size

Default value
:   0

YAML Path
:   global.thread_stack_size

Key-Value Path
:   global/thread_stack_size

Environment
:   NOC_GLOBAL_THREAD_STACK_SIZE

## version_format

Default value
:   %(version)s+%(branch)s.%(number)s.%(changeset)s

YAML Path
:   global.version_format

Key-Value Path
:   global/version_format

Environment
:   NOC_GLOBAL_VERSION_FORMAT

## node

Default value
:   socket.gethostname()

YAML Path
:   global.node

Key-Value Path
:   global/node

Environment
:   NOC_GLOBAL_NODE

## pool

Default value
:   os.environ.get("NOC_POOL", ")

YAML Path
:   global.pool

Key-Value Path
:   global/pool

Environment
:   NOC_GLOBAL_POOL

## secret_key

Default value
:   12345

YAML Path
:   global.secret_key

Key-Value Path
:   global/secret_key

Environment
:   NOC_GLOBAL_SECRET_KEY

## timezone

Default value
:   Europe/Moscow

YAML Path
:   global.timezone

Key-Value Path
:   global/timezone

Environment
:   NOC_GLOBAL_TIMEZONE
