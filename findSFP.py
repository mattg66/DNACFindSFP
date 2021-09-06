import requests
from requests.api import request
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = ""
password = ""
dnacIp = "x.x.x.x"
sfpModulesSN = [
    'xxx',
    'xxx'
]
loginHeader = username + ":" + password
base64Login = base64.b64encode(loginHeader.encode()).decode()

sess = requests.session()
login = sess.post("https://" + dnacIp + "/api/system/v1/auth/token", headers={"Authorization": "Basic " + base64Login}, verify=False)
token = login.json()['Token']

devices = sess.get("https://" + dnacIp + "/dna/intent/api/v1/network-device", headers={"x-auth-token": token}, verify=False).json()
for device in devices['response']:
        sfpModules = sess.get("https://" + dnacIp + "/api/v1/network-device/" + device['id'] + "/equipment?type=SFP", headers={"x-auth-token": token}, verify=False).json()
        for sfpModule in sfpModules['response']:
            for SN in sfpModulesSN:
                if (sfpModule['serialNumber'] == SN):
                    print("SFP Serial: " + sfpModule['serialNumber'] + ", Device Hostname: " + device['hostname']  + ", Port: " + sfpModule['name'])
