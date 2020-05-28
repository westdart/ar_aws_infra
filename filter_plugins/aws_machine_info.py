import json

from ansible.utils.unsafe_proxy import AnsibleUnsafeText

def ec2_machine_info(instances):
    '''
    Args:
        instances: Array of ec2 machines
    Returns: List of machines with relevant information
    '''
    result = {}
    for instance in instances:
        public_hostname = instance['public_dns_name']
        private_hostname = instance['private_dns_name']
        public_ipaddress = instance['public_ip_address'] if 'public_ip_address' in instance else ""
        private_ipaddress = instance['private_ip_address']
        name = instance['tags']['Name']

        machine = dict()
        machine['hostname'] = name
        machine['public_dns'] = public_hostname
        machine['public_ip'] = public_ipaddress
        machine['subnet_id'] = instance['subnet_id']
        machine['cpu_core_count'] = instance['cpu_options']['core_count']
        machine['cpu_threads_per_core'] = instance['cpu_options']['threads_per_core']
        machine['instance_state'] = instance['state']['name']
        machine['instance_type'] = instance['instance_type']
        machine['availability_zone'] = instance['placement']['availability_zone']
        machine['private_dns'] = private_hostname
        machine['private_ip'] = private_ipaddress
        machine['vpc_security_group_ids'] = []
        for security_group in instance['security_groups']:
            machine['vpc_security_group_ids'].append(security_group['group_id'])
        result[machine['hostname']] = machine

    return result



def machine_info(data):
    '''
    Args:
        data: json String or dict object with Machine information
    Returns: List of machines with relevant information
    '''
    result = {}
    if data is None:
        return result

    if type(data) is str or type(data) is AnsibleUnsafeText:
        json_obj = json.loads(data)
    else:
        json_obj = data

    for key in json_obj.keys():
        if key.startswith('machine_') and 'cpu_core_count' in json_obj[key]['value']:
            machine = dict()
            machine['hostname'] = json_obj[key]['value']['tags']['Name']
            machine['public_dns'] = json_obj[key]['value']['public_dns']
            machine['public_ip'] = json_obj[key]['value']['public_ip']
            machine['subnet_id'] = json_obj[key]['value']['subnet_id']
            machine['cpu_core_count'] = json_obj[key]['value']['cpu_core_count']
            machine['cpu_threads_per_core'] = json_obj[key]['value']['cpu_threads_per_core']
            machine['instance_state'] = json_obj[key]['value']['instance_state']
            machine['instance_type'] = json_obj[key]['value']['instance_type']
            machine['availability_zone'] = json_obj[key]['value']['availability_zone']
            machine['private_dns'] = json_obj[key]['value']['private_dns']
            machine['private_ip'] = json_obj[key]['value']['private_ip']
            machine['vpc_security_group_ids'] = json_obj[key]['value']['vpc_security_group_ids']
            result[machine['hostname']] = machine
    return result


class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'machine_info':     machine_info,
            'ec2_machine_info': ec2_machine_info
        }

'''
Testing
'''
import unittest


class TestAwsMachineInfo(unittest.TestCase):
    data1 = \
        '{' \
        '  "machine_lab1-bastion_labs_estafet_org": {' \
        '    "sensitive": false,' \
        '    "type": [' \
        '    ],' \
        '    "value": {' \
        '      "availability_zone": "eu-west-2a",' \
        '      "cpu_core_count": 1,' \
        '      "cpu_threads_per_core": 1,' \
        '      "instance_state": "running",' \
        '      "instance_type": "t2.micro",' \
        '      "private_dns": "ip-10-0-125-129.eu-west-2.compute.internal",' \
        '      "private_ip": "10.0.125.129",' \
        '      "public_dns": "ec2-35-178-131-17.eu-west-2.compute.amazonaws.com",' \
        '      "public_ip": "35.178.131.17",' \
        '      "subnet_id": "subnet-09398a2cafd98293a",' \
        '      "tags": {' \
        '        "Name": "lab1-bastion.labs.estafet.org"' \
        '      },' \
        '      "vpc_security_group_ids": [' \
        '        "sg-002cae7a263ab14c1",' \
        '        "sg-023aef710c717a83f",' \
        '        "sg-029df123313fd2bcf",' \
        '       "sg-0d3b809c871e79faf"' \
        '      ]' \
        '    }' \
        '  }' \
        '}'

    data2 = \
        '{' \
        '  "machine_lab1-bastion_labs_estafet_org": {' \
        '    "sensitive": false,' \
        '    "type": [' \
        '    ],' \
        '    "value": {' \
        '      "availability_zone": "eu-west-2a",' \
        '      "cpu_core_count": 1,' \
        '      "cpu_threads_per_core": 1,' \
        '      "instance_state": "running",' \
        '      "instance_type": "t2.micro",' \
        '      "private_dns": "ip-10-0-125-129.eu-west-2.compute.internal",' \
        '      "private_ip": "10.0.125.129",' \
        '      "public_dns": "ec2-35-178-131-17.eu-west-2.compute.amazonaws.com",' \
        '      "public_ip": "35.178.131.17",' \
        '      "subnet_id": "subnet-09398a2cafd98293a",' \
        '      "tags": {' \
        '        "Name": "lab1-bastion.labs.estafet.org"' \
        '      },' \
        '      "vpc_security_group_ids": [' \
        '        "sg-002cae7a263ab14c1",' \
        '        "sg-023aef710c717a83f",' \
        '        "sg-029df123313fd2bcf",' \
        '        "sg-0d3b809c871e79faf"' \
        '      ]' \
        '    }' \
        '  },' \
        '  "machine_lab2-bastion_labs_estafet_org": {' \
        '    "sensitive": false,' \
        '    "type": [' \
        '    ],' \
        '    "value": {' \
        '      "availability_zone": "eu-west-2b",' \
        '      "cpu_core_count": 2,' \
        '      "cpu_threads_per_core": 2,' \
        '      "instance_state": "stopped",' \
        '      "instance_type": "t2.micro",' \
        '      "private_dns": "ip-10-0-125-130.eu-west-2.compute.internal",' \
        '      "private_ip": "10.0.125.130",' \
        '      "public_dns": "ec2-35-178-131-18.eu-west-2.compute.amazonaws.com",' \
        '      "public_ip": "35.178.131.18",' \
        '      "subnet_id": "subnet-09398a2cafd98293b",' \
        '      "tags": {' \
        '        "Name": "lab2-bastion.labs.estafet.org"' \
        '      },' \
        '      "vpc_security_group_ids": [' \
        '        "sg-002cae7a263ab14c1",' \
        '        "sg-023aef710c717a83f",' \
        '        "sg-029df123313fd2bcf",' \
        '        "sg-0d3b809c871e79faf"' \
        '      ]' \
        '    }' \
        '  }' \
        '}'

    def test_size_one(self):
        result = machine_info(self.data1)
        self.assertEqual(1, len(result))

    def test_size_empty(self):
        result = machine_info({})
        self.assertEqual(0, len(result))

    def test_size_empty(self):
        result = machine_info(None)
        self.assertEqual(0, len(result))

    def test_entries(self):
        result = machine_info(self.data1)
        self.assertEqual('eu-west-2a', result.values()[0]['availability_zone'])
        self.assertEqual(1, result.values()[0]['cpu_core_count'])
        self.assertEqual(1, result.values()[0]['cpu_threads_per_core'])
        self.assertEqual('running', result.values()[0]['instance_state'])
        self.assertEqual('t2.micro', result.values()[0]['instance_type'])
        self.assertEqual('ip-10-0-125-129.eu-west-2.compute.internal', result.values()[0]['private_dns'])
        self.assertEqual('10.0.125.129', result.values()[0]['private_ip'])
        self.assertEqual('ec2-35-178-131-17.eu-west-2.compute.amazonaws.com', result.values()[0]['public_dns'])
        self.assertEqual('35.178.131.17', result.values()[0]['public_ip'])
        self.assertEqual('subnet-09398a2cafd98293a', result.values()[0]['subnet_id'])
        self.assertEqual('lab1-bastion.labs.estafet.org', result.values()[0]['hostname'])

    def test_entries_two(self):
        result = machine_info(self.data2)
        self.assertEqual('eu-west-2a', result['machine_lab1-bastion_labs_estafet_org']['availability_zone'])
        self.assertEqual(1, result['machine_lab1-bastion_labs_estafet_org']['cpu_core_count'])
        self.assertEqual(1, result['machine_lab1-bastion_labs_estafet_org']['cpu_threads_per_core'])
        self.assertEqual('running', result['machine_lab1-bastion_labs_estafet_org']['instance_state'])
        self.assertEqual('t2.micro', result['machine_lab1-bastion_labs_estafet_org']['instance_type'])
        self.assertEqual('ip-10-0-125-129.eu-west-2.compute.internal', result['machine_lab1-bastion_labs_estafet_org']['private_dns'])
        self.assertEqual('10.0.125.129', result['machine_lab1-bastion_labs_estafet_org']['private_ip'])
        self.assertEqual('ec2-35-178-131-17.eu-west-2.compute.amazonaws.com', result['machine_lab1-bastion_labs_estafet_org']['public_dns'])
        self.assertEqual('35.178.131.17', result['machine_lab1-bastion_labs_estafet_org']['public_ip'])
        self.assertEqual('subnet-09398a2cafd98293a', result['machine_lab1-bastion_labs_estafet_org']['subnet_id'])
        self.assertEqual('lab1-bastion.labs.estafet.org', result['machine_lab1-bastion_labs_estafet_org']['hostname'])

        self.assertEqual('eu-west-2b', result['machine_lab2-bastion_labs_estafet_org']['availability_zone'])
        self.assertEqual(2, result['machine_lab2-bastion_labs_estafet_org']['cpu_core_count'])
        self.assertEqual(2, result['machine_lab2-bastion_labs_estafet_org']['cpu_threads_per_core'])
        self.assertEqual('stopped', result['machine_lab2-bastion_labs_estafet_org']['instance_state'])
        self.assertEqual('t2.micro', result['machine_lab2-bastion_labs_estafet_org']['instance_type'])
        self.assertEqual('ip-10-0-125-130.eu-west-2.compute.internal', result['machine_lab2-bastion_labs_estafet_org']['private_dns'])
        self.assertEqual('10.0.125.130', result['machine_lab2-bastion_labs_estafet_org']['private_ip'])
        self.assertEqual('ec2-35-178-131-18.eu-west-2.compute.amazonaws.com', result['machine_lab2-bastion_labs_estafet_org']['public_dns'])
        self.assertEqual('35.178.131.18', result['machine_lab2-bastion_labs_estafet_org']['public_ip'])
        self.assertEqual('subnet-09398a2cafd98293b', result['machine_lab2-bastion_labs_estafet_org']['subnet_id'])
        self.assertEqual('lab2-bastion.labs.estafet.org', result['machine_lab2-bastion_labs_estafet_org']['hostname'])


if __name__ == '__main__':
    unittest.main()
