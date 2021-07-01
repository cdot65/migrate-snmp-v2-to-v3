from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from rich import print

import os

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/config.yaml")

snmp_template = f"{script_dir}/templates/snmp.j2"

firewall = nr.filter(name="juniper-vsrx0")


def configure_snmpv3(task):
    config = {}
    config['snmp'] = task.host['snmp']

    response = task.run(
        task=pyez_config,
        template_path=snmp_template,
        template_vars=data,
        data_format='set')

    print(response)

    if response:
        diff = task.run(pyez_diff)
        print(diff)
        task.run(task=pyez_commit)
    else:
        response = "No response from the box"

    print(response)

    return response

response = nr.run(task=configure_snmpv3)

print(response)
