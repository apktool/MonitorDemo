import requests

s = requests.session()

class hosts_info(object):
    def __init__(self, ambari):
        self.headers = {'X-Requested-By': 'ambari'}
        self.ip = ambari['master']
        self.cluster = ambari['cluster']
        self.url = 'http://' + self.ip + ':8080/api/v1/clusters/' + self.cluster + '/hosts/'

    def get_hosts_info(self):
        url = self.url

        resp = s.get(
            url=url,
            headers=self.headers,
            verify=False,
            auth=('admin', 'admin'))

        hosts_info = resp.json()['items']
        return hosts_info

    def get_specified_host_info(self, host_name):
        params = {'fields': 'alerts_summary'}
        url = self.url + host_name

        resp = s.get(
            url=url,
            params=params,
            headers=self.headers,
            verify=False,
            auth=('admin', 'admin'))

        alter = resp.json()['alerts_summary']
        return alter


if __name__ == '__main__':
    si = hosts_info('192.168.100.66')
    hosts_info = si.get_hosts_info()
    print(hosts_info)
    host_info = si.get_specified_host_info('master')
    print(host_info)
