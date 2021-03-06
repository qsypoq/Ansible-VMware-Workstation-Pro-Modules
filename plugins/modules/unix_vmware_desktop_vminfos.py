#!/usr/bin/python

import base64
import json
import re
import sys
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: unix_vmware_desktop_vminfos

short_description: Get VMware Workstation Pro VM infos

version_added: "2.4"

description:
    - "Get VMware Workstation Pro VM infos"

options:
    target_vm:
        description:
            - This is the target VM to interact with:
                When not set: return all VMs id & path
                When set: return CPU & RAM of the target VM
        required: false

    username: "api-username"
        description:
            - Your workstation API username
        required: true

    password: "api-password"
        description:
            - Your workstation API password
        required: true

    api_url: "http://127.0.0.1"
        description:
            - Your workstation API URL
        required: false
        default: "http://127.0.0.1"

    api_port: "8697"
        description:
            - Your workstation API PORT
        required: false
        default: "8697"

    validate_certs: "no || yes"
        description:
            - Validate Certificate it HTTPS connection
        required: false

author:
    - Adam Magnier (@qsypoq)
'''

EXAMPLES = r'''
# Get infos about all the VMs
- name: "Get infos"
  unix_vmware_desktop_vminfos:
    username: "api-username"
    password: "api-password"

# Retrieve CPU & RAM from VM with ID 42
- name: "Get infos about VM ID 42"
  unix_vmware_desktop_vminfos:
    target_vm: "42"
    username: "api-username"
    password: "api-password"

# Retrieve restrictions from VM with name "Windows 10"
- name: "Get restrictions"
  unix_vmware_desktop_vminfos:
    target_vm_name: "Windows 10"
    restrictions: True
    username: "api-username"
    password: "api-password"

# Retrieve extendedConfigFile from VM with ID 42
- name: "Get infos about VM ID 42"
  unix_vmware_desktop_vminfos:
    target_vm: "42"
    param: "extendedConfigFile"
    username: "api-username"
    password: "api-password"

# Retrieve restrictions from VM with name "Windows 10"
- name: "Get restrictions"
  unix_vmware_desktop_vminfos:
    target_vm_name: "Windows 10"
    restrictions: True
    username: "api-username"
    password: "api-password"

# Retrieve extendedConfigFile from VM with ID 42
- name: "Get infos about VM ID 42"
  unix_vmware_desktop_vminfos:
    target_vm: "42"
    param: "extendedConfigFile"
    username: "api-username"
    password: "api-password"
'''

RETURN = r'''
# Get infos about all the VMs
[{
  "id": "0J319913PHLM1304J1P6EPLADAM",
  "path": "G:\\VMs\\ESXi\\ESXi.vmx"},
{
  "id": "19915KM24UQ0J0OADAMH69H16T125LOL",
  "path": "G:\\VMs\\pfsense\\pfsense.vmx"
}]

# Retrieve CPU & RAM from VM with ID 42
{
  "cpu": {"processors": 1},
  "id": "42",
  "memory": 2048
}
# Retrieve restrictions from VM with name "pfsense"
{
    "changed": false,
    "infos": {
        "applianceView": {
            "author": "",
            "port": "",
            "showAtPowerOn": "",
            "version": ""
        },
        "cddvdList": {
            "devices": [],
            "num": 0
        },
        "cpu": {
            "processors": 1
        },
        "firewareType": 0,
        "floppyList": {
            "devices": [],
            "num": 0
        },
        "groupID": "",
        "guestIsolation": {
            "copyDisabled": false,
            "dndDisabled": false,
            "hgfsDisabled": true,
            "pasteDisabled": false
        },
        "id": "R33IRMF281FGQ584LH7FSVA58L4LN76N",
        "integrityConstraint": "",
        "memory": 1024,
        "nicList": {
            "nics": [
                {
                    "index": 1,
                    "macAddress": "00:0C:29:5B:FD:35",
                    "type": "custom",
                    "vmnet": "vmnet2"
                },
                {
                    "index": 2,
                    "macAddress": "00:0C:29:5B:FD:3F",
                    "type": "custom",
                    "vmnet": "vmnet10"
                },
                {
                    "index": 4,
                    "macAddress": "00:0C:29:5B:FD:53",
                    "type": "custom",
                    "vmnet": "vmnet4"
                }
            ],
            "num": 3
        },
        "orgDisplayName": "",
        "parallelPortList": {
            "devices": [],
            "num": 0
        },
        "remoteVNC": {
            "VNCEnabled": false,
            "VNCPort": 5900
        },
        "serialPortList": {
            "devices": [],
            "num": 0
        },
        "usbList": {
            "num": 2,
            "usbDevices": [
                {
                    "BackingType": 8,
                    "backingInfo": "",
                    "connected": false,
                    "index": 0
                },
                {
                    "BackingType": 2,
                    "backingInfo": "",
                    "connected": false,
                    "index": 1
                }
            ]
        }
    }
}
# Retrieve extendedConfigFile from VM with ID 42
{
  "name": "extendedConfigFile",
  "value": "pfsense.vmxf"
}
'''

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        target_vm=dict(type='str', required=False, default=''),
        target_vm_name=dict(type='str', required=False, default=''),
        api_url=dict(type='str', default='http://127.0.0.1'),
        api_port=dict(type='str', default='8697'),
        validate_certs=dict(type='bool', default='no'),
        restrictions=dict(type='bool', required=False, default='no'),
        param=dict(type='str', required=False, default='no'),
    )

    result = dict(
        changed=False,
        msg=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    api_username = module.params['username']
    api_password = module.params['password']
    creds = api_username + ':' + api_password
    if PY3:
        encodedBytes = base64.b64encode(creds.encode("utf-8"))
        request_creds = str(encodedBytes, "utf-8")
    else:
        encodedBytes = base64.b64encode(creds)
        request_creds = str(encodedBytes).encode("utf-8")
    request_server = module.params['api_url']
    request_port = module.params['api_port']
    headers = {
        'Accept': 'application/vnd.vmware.vmw.rest-v1+json',
        'Authorization': 'Basic ' + request_creds
    }

    target_vm = module.params['target_vm']
    target_vm_name = module.params['target_vm_name']
    restrictions = module.params['restrictions']
    param = module.params['param']
    vmlist = []
    if target_vm_name != "":
        requestnamesurl = request_server + ':' + request_port + '/api/vms'
        reqname, infoname = fetch_url(module, requestnamesurl, headers=headers, method="Get")
        responsename = json.loads(reqname.read())

        for vm in responsename:
            currentvmx = vm['path']
            with open(currentvmx, 'r') as vmx:
                for line in vmx:
                    if re.search(r'^displayName', line):
                        currentname = line.split('"')[1]
            finalname = currentname.lower()
            vm.update({'name': finalname})
            vmlist.append(vm)

        vm_name_search = target_vm_name.lower()
        for vm in vmlist:
            if vm['name'] == vm_name_search:
                target_vm = vm['id']

    if target_vm != "":
        if restrictions is True:
            request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/restrictions'
        elif param != "no":
            request_url = request_server + ':' + request_port + '/api/vms/' + target_vm + '/params/' + param
        else:
            request_url = request_server + ':' + request_port + '/api/vms/' + target_vm
    else:
        request_url = request_server + ':' + request_port + '/api/vms'

    method = "Get"
    req, info = fetch_url(module, request_url, headers=headers, method=method)

    if req is None:
        module.fail_json(msg=info['msg'])

    result['msg'] = json.loads(req.read())
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
