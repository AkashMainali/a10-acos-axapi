#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_automatic_update
description:
    - Automatic update configuration
short_description: Configures A10 automatic-update
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    partition:
        description:
        - Destination/target partition for object/command
    info:
        description:
        - "Field info"
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
    reset:
        description:
        - "Field reset"
        required: False
        suboptions:
            feature_name:
                description:
                - "'app-fw'= Application Firewall; "
    uuid:
        description:
        - "uuid of the object"
        required: False
    use_mgmt_port:
        description:
        - "Use management port to connect"
        required: False
    checknow:
        description:
        - "Field checknow"
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
    revert:
        description:
        - "Field revert"
        required: False
        suboptions:
            feature_name:
                description:
                - "'app-fw'= Application Firewall; "
    proxy_server:
        description:
        - "Field proxy_server"
        required: False
        suboptions:
            username:
                description:
                - "Username for proxy authentication"
            domain:
                description:
                - "Realm for NTLM authentication"
            uuid:
                description:
                - "uuid of the object"
            https_port:
                description:
                - "Proxy server HTTPs port"
            encrypted:
                description:
                - "Do NOT use this option manually. (This is an A10 reserved keyword.) (The ENCRYPTED secret string)"
            proxy_host:
                description:
                - "Proxy server hostname or IP address"
            auth_type:
                description:
                - "'ntlm'= NTLM authentication(default); 'basic'= Basic authentication; "
            password:
                description:
                - "Password for proxy authentication"
            secret_string:
                description:
                - "password value"
    check_now:
        description:
        - "Field check_now"
        required: False
        suboptions:
            feature_name:
                description:
                - "'app-fw'= Application Firewall; "
    config_list:
        description:
        - "Field config_list"
        required: False
        suboptions:
            day_time:
                description:
                - "Time of day to update (hh=mm) in 24 hour local time"
            uuid:
                description:
                - "uuid of the object"
            schedule:
                description:
                - "Field schedule"
            feature_name:
                description:
                - "'app-fw'= Application Firewall Configuration; "
            week_day:
                description:
                - "'Monday'= Monday; 'Tuesday'= Tuesday; 'Wednesday'= Wednesday; 'Thursday'= Thursday; 'Friday'= Friday; 'Saturday'= Saturday; 'Sunday'= Sunday; "
            daily:
                description:
                - "Every day"
            week_time:
                description:
                - "Time of day to update (hh=mm) in 24 hour local time"
            weekly:
                description:
                - "Every week"

"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["check_now","checknow","config_list","info","proxy_server","reset","revert","use_mgmt_port","uuid",]

# our imports go at the top so we fail fast.
try:
    from a10_ansible import errors as a10_ex
    from a10_ansible.axapi_http import client_factory, session_factory
    from a10_ansible.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent", "noop"]),
        a10_port=dict(type='int', required=True),
        a10_protocol=dict(type='str', choices=["http", "https"]),
        partition=dict(type='str', required=False),
        get_type=dict(type='str', choices=["single", "list"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        info=dict(type='dict',uuid=dict(type='str',)),
        reset=dict(type='dict',feature_name=dict(type='str',choices=['app-fw'])),
        uuid=dict(type='str',),
        use_mgmt_port=dict(type='bool',),
        checknow=dict(type='dict',uuid=dict(type='str',)),
        revert=dict(type='dict',feature_name=dict(type='str',choices=['app-fw'])),
        proxy_server=dict(type='dict',username=dict(type='str',),domain=dict(type='str',),uuid=dict(type='str',),https_port=dict(type='int',),encrypted=dict(type='str',),proxy_host=dict(type='str',),auth_type=dict(type='str',choices=['ntlm','basic']),password=dict(type='bool',),secret_string=dict(type='str',)),
        check_now=dict(type='dict',feature_name=dict(type='str',choices=['app-fw'])),
        config_list=dict(type='list',day_time=dict(type='str',),uuid=dict(type='str',),schedule=dict(type='bool',),feature_name=dict(type='str',required=True,choices=['app-fw']),week_day=dict(type='str',choices=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']),daily=dict(type='bool',),week_time=dict(type='str',),weekly=dict(type='bool',))
    ))
   

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/automatic-update"

    f_dict = {}

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/automatic-update"

    f_dict = {}

    return url_base.format(**f_dict)

def list_url(module):
    """Return the URL for a list of resources"""
    ret = existing_url(module)
    return ret[0:ret.rfind('/')]

def build_envelope(title, data):
    return {
        title: data
    }

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
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

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
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

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if x in params and params.get(x) is not None])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def get(module):
    return module.client.get(existing_url(module))

def get_list(module):
    return module.client.get(list_url(module))

def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("automatic-update", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        if post_result:
            result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
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

def update(module, result, existing_config):
    payload = build_json("automatic-update", module)
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
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result, existing_config)

def absent(module, result):
    return delete(module, result)

def replace(module, result, existing_config):
    payload = build_json("automatic-update", module)
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

    result = dict(
        changed=False,
        original_message="",
        message="",
        result={}
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    a10_port = module.params["a10_port"] 
    a10_protocol = module.params["a10_protocol"]
    
    partition = module.params["partition"]

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        for ve in validation_errors:
            run_errors.append(ve)
    
    if not valid:
        err_msg = "\n".join(run_errors)
        result["messages"] = "Validation failure: " + str(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)
    if partition:
        module.client.activate_partition(partition)

    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)
        module.client.session.close()
    elif state == 'absent':
        result = absent(module, result)
        module.client.session.close()
    elif state == 'noop':
        if module.params.get("get_type") == "single":
            result["result"] = get(module)
        elif module.params.get("get_type") == "list":
            result["result"] = get_list(module)
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()