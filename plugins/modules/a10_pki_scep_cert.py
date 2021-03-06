#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_pki_scep_cert
description:
    - SCEP Certificate enrollment object
short_description: Configures A10 pki.scep-cert
author: A10 Networks 2018
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
          - noop
          - present
          - absent
        required: True
    ansible_host:
        description:
        - Host for AXAPI authentication
        required: True
    ansible_username:
        description:
        - Username for AXAPI authentication
        required: True
    ansible_password:
        description:
        - Password for AXAPI authentication
        required: True
    ansible_port:
        description:
        - Port for AXAPI authentication
        required: True
    a10_device_context_id:
        description:
        - Device ID for aVCS configuration
        choices: [1-8]
        required: False
    a10_partition:
        description:
        - Destination/target partition for object/command
        required: False
    renew_every_type:
        description:
        - "'hour'= Periodic interval in hours; 'day'= Periodic interval in days; 'week'=
          Periodic interval in weeks; 'month'= Periodic interval in months(1 month=30
          days);"
        required: False
    encrypted:
        description:
        - "Do NOT use this option manually. (This is an A10 reserved keyword.) (The
          ENCRYPTED secret string)"
        required: False
    log_level:
        description:
        - "level for logging output of scepclient commands(default 1 and detailed 4)"
        required: False
    uuid:
        description:
        - "uuid of the object"
        required: False
    renew_before_type:
        description:
        - "'hour'= Number of hours before cert expiry; 'day'= Number of days before cert
          expiry; 'week'= Number of weeks before cert expiry; 'month'= Number of months
          before cert expiry(1 month=30 days);"
        required: False
    renew_every:
        description:
        - "Specify periodic interval in which to renew the certificate"
        required: False
    key_length:
        description:
        - "'1024'= Key size 1024 bits; '2048'= Key size 2048 bits(default); '4096'= Key
          size 4096 bits; '8192'= Key size 8192 bits;"
        required: False
    method:
        description:
        - "'GET'= GET request; 'POST'= POST request;"
        required: False
    dn:
        description:
        - "Specify the Distinguished-Name to use while enrolling the certificate (Format=
          'cn=user, dc=example, dc=com')"
        required: False
    subject_alternate_name:
        description:
        - "Field subject_alternate_name"
        required: False
        suboptions:
            san_type:
                description:
                - "'email'= Enter e-mail address of the subject; 'dns'= Enter hostname of the
          subject; 'ip'= Enter IP address of the subject;"
            san_value:
                description:
                - "Value of subject-alternate-name"
    renew_every_value:
        description:
        - "Value of renewal period"
        required: False
    max_polltime:
        description:
        - "Maximum time in seconds to poll when SCEP response is PENDING (default 180)"
        required: False
    password:
        description:
        - "Specify the password used to enroll the device's certificate"
        required: False
    minute:
        description:
        - "Periodic interval in minutes"
        required: False
    secret_string:
        description:
        - "secret password"
        required: False
    enroll:
        description:
        - "Initiates enrollment of device with the CA"
        required: False
    renew_before_value:
        description:
        - "Value of renewal period"
        required: False
    name:
        description:
        - "Specify Certificate name to be enrolled"
        required: True
    url:
        description:
        - "Specify the Enrollment Agent's absolute URL (Format= http=//host/path)"
        required: False
    interval:
        description:
        - "Interval time in seconds to poll when SCEP response is PENDING (default 5)"
        required: False
    user_tag:
        description:
        - "Customized tag"
        required: False
    renew_before:
        description:
        - "Specify interval before certificate expiry to renew the certificate"
        required: False

'''

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = [
    "dn",
    "encrypted",
    "enroll",
    "interval",
    "key_length",
    "log_level",
    "max_polltime",
    "method",
    "minute",
    "name",
    "password",
    "renew_before",
    "renew_before_type",
    "renew_before_value",
    "renew_every",
    "renew_every_type",
    "renew_every_value",
    "secret_string",
    "subject_alternate_name",
    "url",
    "user_tag",
    "uuid",
]

from ansible_collections.a10.acos_axapi.plugins.module_utils import \
    errors as a10_ex
from ansible_collections.a10.acos_axapi.plugins.module_utils.axapi_http import \
    client_factory
from ansible_collections.a10.acos_axapi.plugins.module_utils.kwbl import \
    KW_OUT, translate_blacklist as translateBlacklist


def get_default_argspec():
    return dict(
        ansible_host=dict(type='str', required=True),
        ansible_username=dict(type='str', required=True),
        ansible_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str',
                   default="present",
                   choices=['noop', 'present', 'absent']),
        ansible_port=dict(type='int', choices=[80, 443], required=True),
        a10_partition=dict(
            type='dict',
            name=dict(type='str', ),
            shared=dict(type='str', ),
            required=False,
        ),
        a10_device_context_id=dict(
            type='int',
            choices=[1, 2, 3, 4, 5, 6, 7, 8],
            required=False,
        ),
        get_type=dict(type='str', choices=["single", "list", "oper", "stats"]),
    )


def get_argspec():
    rv = get_default_argspec()
    rv.update({
        'renew_every_type': {
            'type': 'str',
            'choices': ['hour', 'day', 'week', 'month']
        },
        'encrypted': {
            'type': 'str',
        },
        'log_level': {
            'type': 'int',
        },
        'uuid': {
            'type': 'str',
        },
        'renew_before_type': {
            'type': 'str',
            'choices': ['hour', 'day', 'week', 'month']
        },
        'renew_every': {
            'type': 'bool',
        },
        'key_length': {
            'type': 'str',
            'choices': ['1024', '2048', '4096', '8192']
        },
        'method': {
            'type': 'str',
            'choices': ['GET', 'POST']
        },
        'dn': {
            'type': 'str',
        },
        'subject_alternate_name': {
            'type': 'dict',
            'san_type': {
                'type': 'str',
                'choices': ['email', 'dns', 'ip']
            },
            'san_value': {
                'type': 'str',
            }
        },
        'renew_every_value': {
            'type': 'int',
        },
        'max_polltime': {
            'type': 'int',
        },
        'password': {
            'type': 'bool',
        },
        'minute': {
            'type': 'int',
        },
        'secret_string': {
            'type': 'str',
        },
        'enroll': {
            'type': 'bool',
        },
        'renew_before_value': {
            'type': 'int',
        },
        'name': {
            'type': 'str',
            'required': True,
        },
        'url': {
            'type': 'str',
        },
        'interval': {
            'type': 'int',
        },
        'user_tag': {
            'type': 'str',
        },
        'renew_before': {
            'type': 'bool',
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/pki/scep-cert/{name}"

    f_dict = {}
    f_dict["name"] = module.params["name"]

    return url_base.format(**f_dict)


def list_url(module):
    """Return the URL for a list of resources"""
    ret = existing_url(module)
    return ret[0:ret.rfind('/')]


def get(module):
    return module.client.get(existing_url(module))


def get_list(module):
    return module.client.get(list_url(module))


def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return None


def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")


def _build_dict_from_param(param):
    rv = {}

    for k, v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        elif isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv


def build_envelope(title, data):
    return {title: data}


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/pki/scep-cert/{name}"

    f_dict = {}
    f_dict["name"] = ""

    return url_base.format(**f_dict)


def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([
        x for x in requires_one_of if x in params and params.get(x) is not None
    ])

    errors = []
    marg = []

    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc, msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc, msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc, msg = REQUIRED_VALID

    if not rc:
        errors.append(msg.format(", ".join(marg)))

    return rc, errors


def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v is not None:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            elif isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)


def report_changes(module, result, existing_config, payload):
    if existing_config:
        for k, v in payload["scep-cert"].items():
            if isinstance(v, str):
                if v.lower() == "true":
                    v = 1
                else:
                    if v.lower() == "false":
                        v = 0
            elif k not in payload:
                break
            else:
                if existing_config["scep-cert"][k] != v:
                    if result["changed"] is not True:
                        result["changed"] = True
                    existing_config["scep-cert"][k] = v
            result.update(**existing_config)
    else:
        result.update(**payload)
    return result


def create(module, result, payload):
    try:
        post_result = module.client.post(new_url(module), payload)
        if post_result:
            result.update(**post_result)
        result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def update(module, result, existing_config, payload):
    try:
        post_result = module.client.post(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def present(module, result, existing_config):
    payload = build_json("scep-cert", module)
    changed_config = report_changes(module, result, existing_config, payload)
    if module.check_mode:
        return changed_config
    elif not existing_config:
        return create(module, result, payload)
    elif existing_config and not changed_config.get('changed'):
        return update(module, result, existing_config, payload)
    else:
        result["changed"] = True
        return result


def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def absent(module, result, existing_config):
    if module.check_mode:
        if existing_config:
            result["changed"] = True
            return result
        else:
            result["changed"] = False
            return result
    else:
        return delete(module, result)


def replace(module, result, existing_config, payload):
    try:
        post_result = module.client.put(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def run_command(module):
    run_errors = []

    result = dict(changed=False, original_message="", message="", result={})

    state = module.params["state"]
    ansible_host = module.params["ansible_host"]
    ansible_username = module.params["ansible_username"]
    ansible_password = module.params["ansible_password"]
    ansible_port = module.params["ansible_port"]
    a10_partition = module.params["a10_partition"]
    a10_device_context_id = module.params["a10_device_context_id"]

    if ansible_port == 80:
        protocol = "http"
    elif ansible_port == 443:
        protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        for ve in validation_errors:
            run_errors.append(ve)

    if not valid:
        err_msg = "\n".join(run_errors)
        result["messages"] = "Validation failure: " + str(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(ansible_host, ansible_port, protocol,
                                   ansible_username, ansible_password)

    if a10_partition:
        module.client.activate_partition(a10_partition)

    if a10_device_context_id:
        module.client.change_context(a10_device_context_id)

    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)

    if state == 'absent':
        result = absent(module, result, existing_config)

    if state == 'noop':
        if module.params.get("get_type") == "single":
            result["result"] = get(module)
        elif module.params.get("get_type") == "list":
            result["result"] = get_list(module)
    module.client.session.close()
    return result


def main():
    module = AnsibleModule(argument_spec=get_argspec(),
                           supports_check_mode=True)
    result = run_command(module)
    module.exit_json(**result)


# standard ansible module imports
from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    main()
