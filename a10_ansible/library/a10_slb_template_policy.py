#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_slb_template_policy
description:
    - None
short_description: Configures A10 slb.template.policy
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
    forward_policy:
        description:
        - "Field forward_policy"
        required: False
        suboptions:
            filtering:
                description:
                - "Field filtering"
            uuid:
                description:
                - "None"
            local_logging:
                description:
                - "None"
            action_list:
                description:
                - "Field action_list"
            no_client_conn_reuse:
                description:
                - "None"
            source_list:
                description:
                - "Field source_list"
    use_destination_ip:
        description:
        - "None"
        required: False
    name:
        description:
        - "None"
        required: True
    over_limit:
        description:
        - "None"
        required: False
    class_list:
        description:
        - "Field class_list"
        required: False
        suboptions:
            header_name:
                description:
                - "None"
            lid_list:
                description:
                - "Field lid_list"
            name:
                description:
                - "None"
            client_ip_l3_dest:
                description:
                - "None"
            client_ip_l7_header:
                description:
                - "None"
            uuid:
                description:
                - "None"
    interval:
        description:
        - "None"
        required: False
    share:
        description:
        - "None"
        required: False
    full_domain_tree:
        description:
        - "None"
        required: False
    over_limit_logging:
        description:
        - "None"
        required: False
    bw_list_name:
        description:
        - "None"
        required: False
    timeout:
        description:
        - "None"
        required: False
    sampling_enable:
        description:
        - "Field sampling_enable"
        required: False
        suboptions:
            counters1:
                description:
                - "None"
    user_tag:
        description:
        - "None"
        required: False
    bw_list_id:
        description:
        - "Field bw_list_id"
        required: False
        suboptions:
            pbslb_interval:
                description:
                - "None"
            action_interval:
                description:
                - "None"
            service_group:
                description:
                - "None"
            logging_drp_rst:
                description:
                - "None"
            fail:
                description:
                - "None"
            pbslb_logging:
                description:
                - "None"
            id:
                description:
                - "None"
            bw_list_action:
                description:
                - "None"
    over_limit_lockup:
        description:
        - "None"
        required: False
    uuid:
        description:
        - "None"
        required: False
    over_limit_reset:
        description:
        - "None"
        required: False
    overlap:
        description:
        - "None"
        required: False


"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["bw_list_id","bw_list_name","class_list","forward_policy","full_domain_tree","interval","name","over_limit","over_limit_lockup","over_limit_logging","over_limit_reset","overlap","sampling_enable","share","timeout","use_destination_ip","user_tag","uuid",]

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
        state=dict(type='str', default="present", choices=["present", "absent"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        forward_policy=dict(type='dict',filtering=dict(type='list',ssli_url_filtering=dict(type='str',choices=['bypassed-sni-disable','intercepted-sni-enable','intercepted-http-disable','no-sni-allow'])),uuid=dict(type='str',),local_logging=dict(type='bool',),action_list=dict(type='list',log=dict(type='bool',),forward_snat=dict(type='str',),uuid=dict(type='str',),http_status_code=dict(type='str',choices=['301','302']),action1=dict(type='str',choices=['forward-to-internet','forward-to-service-group','forward-to-proxy','drop']),fake_sg=dict(type='str',),user_tag=dict(type='str',),real_sg=dict(type='str',),drop_message=dict(type='str',),sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','hits'])),fall_back=dict(type='str',),fall_back_snat=dict(type='str',),drop_redirect_url=dict(type='str',),name=dict(type='str',required=True,)),no_client_conn_reuse=dict(type='bool',),source_list=dict(type='list',match_any=dict(type='bool',),name=dict(type='str',required=True,),match_authorize_policy=dict(type='str',),destination=dict(type='dict',class_list_list=dict(type='list',uuid=dict(type='str',),dest_class_list=dict(type='str',required=True,),priority=dict(type='int',),sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','hits'])),action=dict(type='str',),ntype=dict(type='str',choices=['host','url','ip'])),web_category_list_list=dict(type='list',uuid=dict(type='str',),web_category_list=dict(type='str',required=True,),priority=dict(type='int',),sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','hits'])),action=dict(type='str',),ntype=dict(type='str',choices=['host','url'])),any=dict(type='dict',action=dict(type='str',),sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','hits'])),uuid=dict(type='str',))),user_tag=dict(type='str',),priority=dict(type='int',),sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','hits','destination-match-not-found','no-host-info'])),match_class_list=dict(type='str',),uuid=dict(type='str',))),
        use_destination_ip=dict(type='bool',),
        name=dict(type='str',required=True,),
        over_limit=dict(type='bool',),
        class_list=dict(type='dict',header_name=dict(type='str',),lid_list=dict(type='list',request_rate_limit=dict(type='int',),action_value=dict(type='str',choices=['forward','reset']),request_per=dict(type='int',),bw_rate_limit=dict(type='int',),conn_limit=dict(type='int',),log=dict(type='bool',),direct_action_value=dict(type='str',choices=['drop','reset']),conn_per=dict(type='int',),direct_fail=dict(type='bool',),conn_rate_limit=dict(type='int',),direct_pbslb_logging=dict(type='bool',),dns64=dict(type='dict',prefix=dict(type='str',),exclusive_answer=dict(type='bool',),disable=dict(type='bool',)),lidnum=dict(type='int',required=True,),over_limit_action=dict(type='bool',),response_code_rate_limit=dict(type='list',threshold=dict(type='int',),code_range_end=dict(type='int',),code_range_start=dict(type='int',),period=dict(type='int',)),direct_service_group=dict(type='str',),uuid=dict(type='str',),request_limit=dict(type='int',),direct_action_interval=dict(type='int',),bw_per=dict(type='int',),interval=dict(type='int',),user_tag=dict(type='str',),direct_action=dict(type='bool',),lockout=dict(type='int',),direct_logging_drp_rst=dict(type='bool',),direct_pbslb_interval=dict(type='int',)),name=dict(type='str',),client_ip_l3_dest=dict(type='bool',),client_ip_l7_header=dict(type='bool',),uuid=dict(type='str',)),
        interval=dict(type='int',),
        share=dict(type='bool',),
        full_domain_tree=dict(type='bool',),
        over_limit_logging=dict(type='bool',),
        bw_list_name=dict(type='str',),
        timeout=dict(type='int',),
        sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','fwd-policy-dns-unresolved','fwd-policy-dns-outstanding','fwd-policy-snat-fail','fwd-policy-hits','fwd-policy-forward-to-internet','fwd-policy-forward-to-service-group','fwd-policy-forward-to-proxy','fwd-policy-policy-drop','fwd-policy-source-match-not-found','exp-client-hello-not-found'])),
        user_tag=dict(type='str',),
        bw_list_id=dict(type='list',pbslb_interval=dict(type='int',),action_interval=dict(type='int',),service_group=dict(type='str',),logging_drp_rst=dict(type='bool',),fail=dict(type='bool',),pbslb_logging=dict(type='bool',),id=dict(type='int',),bw_list_action=dict(type='str',choices=['drop','reset'])),
        over_limit_lockup=dict(type='int',),
        uuid=dict(type='str',),
        over_limit_reset=dict(type='bool',),
        overlap=dict(type='bool',)
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/slb/template/policy/{name}"
    f_dict = {}
    f_dict["name"] = ""

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/slb/template/policy/{name}"
    f_dict = {}
    f_dict["name"] = module.params["name"]

    return url_base.format(**f_dict)


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
        if isinstance(v, list):
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
            if isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if params.get(x)])
    
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

def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("policy", module)
    try:
        post_result = module.client.post(new_url(module), payload)
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
    payload = build_json("policy", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
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

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    # TODO(remove hardcoded port #)
    a10_port = 443
    a10_protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)
    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)
        module.client.session.close()
    elif state == 'absent':
        result = absent(module, result)
        module.client.session.close()
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