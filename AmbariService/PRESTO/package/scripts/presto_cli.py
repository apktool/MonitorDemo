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

from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.resources.system import Execute, Directory, Link
from resource_management.libraries.script.script import Script
from common import PRESTO_CLI_URL


class Cli(Script):
    def install(self, env):
        import params
        presto_cli_path = params.presto_cli_path
        Directory(presto_cli_path, create_parents=True, owner='root', group='root')
        Execute('wget --no-check-certificate {0} -O {1}'.format(PRESTO_CLI_URL, presto_cli_path + '/presto-cli'))
        Execute('chmod +x {0}'.format(presto_cli_path + '/presto-cli'))
        Link('/usr/hdp/current/presto-client', to=params.presto_cli_path)
        Link('/usr/bin/presto-cli', to='/usr/hdp/current/presto-client/presto-cli')

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def configure(self, env):
        import params
        env.set_params(params)

    def start(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)


if __name__ == '__main__':
    Cli().execute()
