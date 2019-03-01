#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions.default import default

# config object that holds the configurations declared in the config xml file
config = Script.get_config()
stack_version = default("/commandParams/version", None)
presto_coordinator_hosts = default("/clusterHostInfo/presto_coordinator_hosts", None)[0]

stack_path = format('/usr/hdp/' + stack_version)
presto_server_path = format(stack_path + '/presto-server')
presto_worker_path = format(stack_path + '/presto-worker')
presto_cli_path = format(stack_path + '/presto-client')

jvm_properties_content = config['configurations']['jvm.config']['content']
node_properties_content = config['configurations']['node.properties']['content']
log_properties = config['configurations']['log.properties']
port = config['configurations']['config.properties']['http-server.http.port']
config_properties = config['configurations']['config.properties'].copy()

import socket
discovery_uri = socket.gethostbyname(presto_coordinator_hosts)

config_properties['discovery.uri'] = 'http://{0}:{1}'.format(discovery_uri, port)

hostname = socket.gethostname()
if hostname == presto_coordinator_hosts:
    config_properties['coordinator'] = 'true'
else:
    config_properties['coordinator'] = 'false'

hive_properties = config['configurations']['hive.properties']
mysql_properties = config['configurations']['mysql.properties']
# mongodb_properties = config['configurations']['mongodb.properties']
# postgresql_properties = config['configurations']['postgresql.properties']
