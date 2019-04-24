#!/usr/bin/env bash

cd $(dirname $(readlink -f "$0"))

install()
{
    yum install python36.x86_64 -y
    yum install python36-pip -y
    pip3.6 install -r requirements.txt
}

run()
{
    python36 main.py
}

command_parse()
{
    cmd=$1
    if [ "${cmd}" = "install" ]; then
        echo "Install MonitorIDMAudit"
        install
    elif [ "${cmd}" = "run" ]; then
        echo "Run MonitorIDMAudit"
        run
    fi
}

command_parse $1

# 30 17 * * * bash /opt/MonitorIDMAudit/shell.sh run
