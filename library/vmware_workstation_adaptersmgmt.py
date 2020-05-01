#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
module: vmware_workstation_adaptersmgmt

short_description: Implement the Network Adapters Management part of the API

version_added: "2.4"

description:
    - "Manage VMware Workstation Network Adapters "

options:
    targetVM:
        description:
            - This is the target VM to interact with
        required: true

    action: list || getip || update || create || delete
        description:
            - This is the action we want to do.
        required: true   

    targetFolder: "myFolderName"
        description:
            - Name of the shared folder
        required: Only for create & update & delete

    targetPath: C:\Users\qsypoq\Desktop\odbg110
        description:
            - Path of shared folder
        required: Only for create & update

    targetIndex: 1
        description:
            - Index's number refering to your network adapter
        required: Only for delete & update

    targetType: custom || bridged || nat || hostonly
        description:
                - This is the target VMNET to interact with
        required: only for update & create

    targetVMnet:
        description:
                - This is the target VMNET to interact with
        required: only when targetType = custom
    
    user: "workstation-api-user"
        description:
            - Your workstation API username
        required: true

    pass: "workstation-api-password"
        description:
            - Your workstation API password
        required: true

    apiurl: "http://127.0.0.1"
        description:
            - Your workstation API URL
        required: false
        default: "http://127.0.0.1"

    apiport: "8697"
        description:
            - Your workstation API PORT
        required: false
        default: "8697"

author:
    - Adam Magnier (@qsypoq)  
'''

EXAMPLES = r'''
- name: "Create shared folder named ODBG110 on VM ID 42"
  vmware_workstation_foldersmgmt:
    targetVM: "42"
    targetFolder: "ODBG110"
    targetPath: C:\Users\qsypoq\Desktop\odbg110
    action: "create"
    user: "workstation-api-user"
    pass: "workstation-api-password"
    
- name: "Delete shared folder named ODBG110 on VM ID 42"
  vmware_workstation_foldersmgmt:
    targetVM: "42"
    targetFolder: "ODBG110"
    action: "delete"
    user: "workstation-api-user"
    pass: "workstation-api-password"
'''

RETURN = r'''
'''