from state import service_info, hosts_info
from notify import exmail
from yaml import safe_load, dump
from datetime import datetime


def ambari_service(master_ip):
    state_machine = {
        'INIT': 'The initial clean state after the service is first created.',
        'INSTALLING': 'In the process of installing the service.',
        'INSTALL_FAILED': 'The service install failed.',
        'INSTALLED': 'The service has been installed successfully but is not currently running.',
        'STARTING': 'In the process of starting the service.',
        'STARTED': 'service has been installed and started.',
        'STOPPING': 'In the process of stopping the service.',
        'UNINSTALLING': 'In the process of uninstalling the service.',
        'UNINSTALLED': 'service has been successfully uninstalled.',
        'WIPING_OUT': 'In the process of wiping out the installed service.',
        'UPGRADING': 'In the process of upgrading the service.',
        'MAINTENANCE': 'service has been marked for maintenance.',
        'UNKNOWN': 'service state can not be determined.',
    }

    services_components_dict = {
        'SPARK2': list(),
        'KAFKA': list(),
        'FLUME': list(),
        'HDFS': list(),
        'HIVE': list(),
        'SQOOP': list(),
        'HBASE': ['PHOENIX_QUERY_SERVER']
    }
    msg = str()

    si = service_info.ambari_service_info(master_ip)

    for service, component in services_components_dict.items():
        state = si.get_services_state(service)
        if state['state'] not in ['STARTED', 'INSTALLED']:
            msg = msg + service + '\t' + state_machine[state['state']] + '\n'

        if component:
            for item in component:
                state = si.get_services_component_state(service, item)
                if state['state'] != 'STARTED':
                    msg = msg + item + '\t' + state_machine[state['state']] + '\n'

    return msg


def port_service(services_name_prot_dict):
    msg = str()

    for service, ip_port in services_name_prot_dict.items():
        for item in ip_port:
            ip = item.split(':')[0]
            port = item.split(':')[1]
            si = service_info.port_service_info(ip, int(port))
            state = si.get_services_state()
            if state != 0:
                msg = msg + service + '\t' + ip + ':' + port + '\t' + 'The service is not currently running.\n'

    return msg


def host_info(host):
    msg = str()

    hi = hosts_info.hosts_info(host)

    hosts = hi.get_hosts_info()
    msg = 'There are ' + str(len(hosts)) + ' hosts\n'
    for item in hosts:
        msg = msg + item['Hosts']['host_name'] + '\t'

    msg = msg + '\n\n'

    return msg


if __name__ == '__main__':
    documents = safe_load(open('config.yaml', 'r'))

    msg_host = host_info(documents['ambari']['master'])
    msg_ambari = ambari_service(documents['ambari']['master'])
    msg_port = port_service(documents['services'])

    if msg_ambari or msg_port:
        msg = msg_host + msg_ambari + msg_port

        title = 'Monitor status | ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exmail = exmail.exmail(documents['email'])
        exmail.send(title, msg)
