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

import uuid
import os.path as path

from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from resource_management.libraries.resources import *
from resource_management.core.resources.system import Directory, File, Execute, Link
from resource_management.core.source import InlineTemplate
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from common import PRESTO_TAR_URL


class Coordinator(Script):
    def install(self, env):
        from params import presto_server_path
        presto_etc_path = presto_server_path + '/etc'
        presto_catalog_path = presto_etc_path + '/catalog'
        Execute('wget --no-check-certificate {0}  -O /tmp/{1}'.format(PRESTO_TAR_URL, 'presto-server.tar.gz'))
        Directory([presto_server_path, presto_etc_path, presto_catalog_path], create_parents=True, owner='root', group='root')
        Execute('tar xf {0} -C {1} --strip-components 1'.format('/tmp/presto-server.tar.gz', presto_server_path))
        Link('/usr/hdp/current/presto-server', to=presto_server_path)
        self.install_packages(env)
        self.configure(env)

    def stop(self, env):
        launcher = '/usr/hdp/current/presto-server/bin/launcher'
        Execute('{0} stop'.format(launcher))

    def start(self, env):
        self.configure(env)
        import params
        launcher = params.presto_server_path + '/bin/launcher'
        Execute('{0} start'.format(launcher))

    def status(self, env):
        launcher = '/usr/hdp/current/presto-server/bin/launcher'
        try:
            Execute('{0} status'.format(launcher))
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        import params
        import uuid

        presto_etc_path = params.presto_server_path + '/etc'
        presto_catalog_path = presto_etc_path + '/catalog'

        Directory(
            [presto_etc_path, presto_catalog_path], create_parents=True, owner='root', group='root')

        File(
            presto_etc_path + '/node.properties',
            content=InlineTemplate(params.node_properties_content, node_id=str(uuid.uuid4())),
            mode=0644,
            owner='root',
            group='root')

        File(
            presto_etc_path + '/jvm.config',
            content=params.jvm_properties_content,
            mode=0644,
            owner='root',
            group='root')

        properties = dict()
        properties[presto_etc_path + '/log.properties'] = params.log_properties
        properties[presto_etc_path + '/config.properties'] = params.config_properties
        properties[presto_catalog_path + '/mysql.properties'] = params.mysql_properties
        properties[presto_catalog_path + '/hive.properties'] = params.hive_properties
        # properties[presto_catalog_path + '/mongodb.properties'] = params.mongodb_properties

        for key, value in properties.items():
            PropertiesFile(key, properties=value, mode=0644, owner='root', group='root')


if __name__ == '__main__':
    Coordinator().execute()
