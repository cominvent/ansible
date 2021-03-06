#!/usr/bin/python
# Copyright (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: nios_network_view
version_added: "2.5"
author: "Peter Sprygada (@privateip)"
short_description: Configure Infoblox NIOS network views
description:
  - Adds and/or removes instances of network view objects from
    Infoblox NIOS servers.  This module manages NIOS C(networkview) objects
    using the Infoblox WAPI interface over REST.
requirements:
  - infoblox_client
extends_documentation_fragment: nios
options:
  name:
    description:
      - Specifies the name of the network view to either add or remove
        from the configuration.
    required: true
    aliases:
      - network_view
  extattrs:
    description:
      - Allows for the configuration of Extensible Attributes on the
        instance of the object.  This argument accepts a set of key / value
        pairs for configuration.
    required: false
    default: null
  comment:
    description:
      - Configures a text string comment to be associated with the instance
        of this object.  The provided text string will be configured on the
        object instance.
    required: false
    default: null
  state:
    description:
      - Configures the intended state of the instance of the object on
        the NIOS server.  When this value is set to C(present), the object
        is configured on the device and when this value is set to C(absent)
        the value is removed (if necessary) from the device.
    required: false
    default: present
    choices:
      - present
      - absent
'''

EXAMPLES = '''
- name: configure a new network view
  nios_network_view:
    name: ansible
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin

- name: update the comment for network view
  nios_network_view:
    name: ansible
    comment: this is an example comment
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin

- name: remove the network view
  nios_network_view:
    name: ansible
    state: absent
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.net_tools.nios.api import get_provider_spec, Wapi


def main():
    ''' Main entry point for module execution
    '''
    ib_spec = dict(
        name=dict(required=True, aliases=['network_view'], ib_req=True),

        extattrs=dict(type='dict'),
        comment=dict(),
    )

    argument_spec = dict(
        provider=dict(required=True),
        state=dict(default='present', choices=['present', 'absent'])
    )

    argument_spec.update(ib_spec)
    argument_spec.update(get_provider_spec())

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    wapi = Wapi(module)
    result = wapi.run('networkview', ib_spec)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
