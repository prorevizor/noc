# [activator] section
Activator service configuration

## tos
Set [Type of Service](https://en.wikipedia.org/wiki/Type_of_service) for
all outgoing CLI/SNMP requests.

Default value
:   0

Possible values
:   0..255

YAML Path
:   activator.tos

Key-Value Path
:   activator/tos

Environment
:   NOC_ACTIVATOR_TOS

## script_threads

==================  ============================
**YAML Path**       activator.script_threads
**Key-Value Path**  activator/script_threads
**Environment**     NOC_ACTIVATOR_SCRIPT_THREADS
**Default Value**   10
==================  ============================


.. _config-activator-buffer_size:

buffer_size
~~~~~~~~~~~

==================  =========================
**YAML Path**       activator.buffer_size
**Key-Value Path**  activator/buffer_size
**Environment**     NOC_ACTIVATOR_BUFFER_SIZE
**Default Value**   1048576
==================  =========================


.. _config-activator-connect_retries:

connect_retries
~~~~~~~~~~~~~~~

retries on immediate disconnect

==================  =============================
**YAML Path**       activator.connect_retries
**Key-Value Path**  activator/connect_retries
**Environment**     NOC_ACTIVATOR_CONNECT_RETRIES
**Default Value**   3
==================  =============================


.. _config-activator-connect_timeout:

connect_timeout
~~~~~~~~~~~~~~~

timeout after immediate disconnect

==================  =============================
**YAML Path**       activator.connect_timeout
**Key-Value Path**  activator/connect_timeout
**Environment**     NOC_ACTIVATOR_CONNECT_TIMEOUT
**Default Value**   3
==================  =============================


.. _config-activator-http_connect_timeout:

http_connect_timeout
~~~~~~~~~~~~~~~~~~~~

==================  ==================================
**YAML Path**       activator.http_connect_timeout
**Key-Value Path**  activator/http_connect_timeout
**Environment**     NOC_ACTIVATOR_HTTP_CONNECT_TIMEOUT
**Default Value**   20
==================  ==================================


.. _config-activator-http_request_timeout:

http_request_timeout
~~~~~~~~~~~~~~~~~~~~

==================  ==================================
**YAML Path**       activator.http_request_timeout
**Key-Value Path**  activator/http_request_timeout
**Environment**     NOC_ACTIVATOR_HTTP_REQUEST_TIMEOUT
**Default Value**   30
==================  ==================================


.. _config-activator-http_validate_cert:

http_validate_cert
~~~~~~~~~~~~~~~~~~

==================  ================================
**YAML Path**       activator.http_validate_cert
**Key-Value Path**  activator/http_validate_cert
**Environment**     NOC_ACTIVATOR_HTTP_VALIDATE_CERT
**Default Value**   False
==================  ================================


