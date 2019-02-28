#!/bin/bash

path=/MonitorDemo/MonitorService
cd ${path}

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
        echo "Install MonitorService"
        install
    elif [ "${cmd}" = "run" ]; then
        echo "Run MonitorService"
        run
    fi
}

command_parse $1
