import requests
from .port_info import socket_info

s = requests.session()


class ambari_service_info(object):
    def __init__(self, ip):
        self.headers = {'X-Requested-By': 'ambari'}
        self.ip = ip
        self.url = 'http://' + self.ip + ':8080/api/v1/clusters/IDB_for_Testing/services/'

    def get_services_state(self, service_name):
        params = {'fields': 'ServiceInfo'}

        url = self.url + service_name
        resp = s.get(
            url=url,
            params=params,
            headers=self.headers,
            verify=False,
            auth=('admin', 'admin'))
        state = resp.json()['ServiceInfo']

        return state

    def get_services_altert(self, service_name):
        params = {'fields': 'alerts_summary'}

        url = self.url + service_name
        resp = s.get(
            url=url,
            params=params,
            headers=self.headers,
            verify=False,
            auth=('admin', 'admin'))
        alter = resp.json()['alerts_summary']

        return alter

    def get_services_component_state(self, service_name, component_name):
        params = {'fields': 'ServiceComponentInfo'}

        url = self.url + service_name + '/components/' + component_name
        resp = s.get(
            url=url,
            params=params,
            headers=self.headers,
            verify=False,
            auth=('admin', 'admin'))
        state = resp.json()['ServiceComponentInfo']

        return state


class port_service_info(object):
    def __init__(self, ip, port):
        self.socket = socket_info(ip, port)

    def get_services_state(self, service_name = None):
        result = self.socket.get_port_info()
        return result


if __name__ == '__main__':
    si = ambari_service_info('192.168.100.66')
    state = si.get_services_state('KAFKA')
    print(state)
    alter = si.get_services_altert('KAFKA')
    print(alter)

    pi = port_service_info('192.168.100.66', 8080)
    state = pi.get_services_state()
    print(state)
