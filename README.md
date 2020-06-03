# ar_aws_infra

Create AWS infrastructure

## Requirements
- awscli and related python modules


## Role Variables
The following details:
- the parameters that should be passed to the role (aka vars)
- the defaults that are held
- the secrets that should generally be sourced from an ansible vault.

### Parameters:

Mandatory variables:

| Variable                 | Description                                                                                     | Default |
| --------                 | -----------                                                                                     | ------- |
| ar_aws_infra_dest_dir    | Directory in which to generate environment specific files needed during creation and management | None    |
| ar_aws_infra_key_path    | Path to an SSH key to inject into machines                                                      | None    |
| ar_aws_infra_name        | Unique name to give the infra                                                                   | None    |
| ar_aws_infra_description | Description for the infra                                                                       | None    |
| ar_aws_infra_domain      | The domain for the machines                                                                     | None    |
| ar_aws_infra_region      | The AWS region to put machines                                                                  | None    |
| ar_aws_infra_envs        | Array of environments (see below for format)                                                    | []      |

Variables required if 'ar_aws_infra_create_cloud' is false:

| Variable                              | Description                               | Default |
| --------                              | -----------                               | ------- |
| ar_aws_infra_vpc_id                   | Id of VPC to use                          | None    |
| ar_aws_infra_main_route_table_id      | The main routing table for the VPC        | None    |
| ar_aws_infra_existing_security_groups | List of existing security groups to apply | None    |
| ar_aws_infra_instance_profile_id      | Profile ID to use                         | None    |


The structure of the 'ar_aws_infra_envs' is:
```
[
  { prefix: "<env prefix>", subnet_cidr: "<Subnet CIDR for the env>", availability_zone: '<AWS Availablility zone>',
    subnet_name: '<Name for the subnet to be created>', name: "<Name of the environment>",
    node_groups: [
      { name: '<Machine name prefix>', machine_type: '<Machine Type>', count: <Number of machines> }
    ]
  }
]
```
This structure references another structure of Machine Types:


### Defaults
| Variable                           | Description                                                                                        | Default                                                           |
| --------                           | -----------                                                                                        | -------                                                           |
| ar_aws_infra_create_cloud          | Whether to create the VPC in AWS or not (if not 'ar_aws_infra_existing_security_groups',           | true                                                              |
|                                    | 'ar_aws_infra_vpc_id' and 'ar_aws_infra_instance_profile_id' must be provided                      |                                                                   |
| ar_aws_infra_use_aws_dns           |                                                                                                    | false                                                             |
| ar_aws_infra_terraform_modules_dir | Where Terraform modules can be found                                                               | {{ role_path }}/files/terraform                                   |
| ar_aws_infra_terraform_template    | Which Terraform template to use                                                                    | aws-infra-main.tf.j2                                              |
| ar_aws_infra_terraform_variables   | Which template to use to provide Terraform vars                                                    | aws-infra-variables.tf.j2                                         |
| ar_aws_infra_terraform_varagrs     | What args to pass terraform through 'terraform.tfvars'                                             | terraform.tfvars.j2                                               |
| ar_aws_infra_terraform_outputs     | deprecated                                                                                         | aws-infra-outputs.tf.j2                                           |
| ar_aws_infra_cloud_cidr            | The cloud CIDR (only required if ar_aws_infra_create_cloud = true)                                 | 10.0.0.0/16                                                       |
| ar_aws_infra_ami_images            | Search details for AMI images                                                                      | Array including RHEL 7.7 and Centos 7 images                      |
| ar_aws_infra_root_block_device     | The block device to add to all machines to hold OS etc                                             | {size: "10", type: "gp2"}                                         |
| ar_aws_infra_machine_types         | List of machine types that can be used                                                             | Consists of one machine type ('default_node') - t2.micro RHEL 7.7 |
| ar_aws_infra_network_rules         | List of rules that can be used in Security Groups                                                  | Open network internally and SSH allowed from outside              |
| ar_aws_infra_security_groups       | Application of group of specific rules from 'ar_aws_infra_network_rules' to a specific environment | Open network internally and SSH allowed from outside              |


### Secrets
The following variables should be provided through an encrypted source:

## Example Playbook

```
- hosts: localhost
  tasks:
    - name: Generate AWS Infra
      include_role:
        name: ar_aws_infra
      vars:
        ar_aws_infra_dest_dir:                 "{{ dest_dir }}"
        ar_aws_infra_key_path:                 "{{ key_path }}"
        ar_aws_infra_name:                     "{{ infra_name }}"
        ar_aws_infra_description:              "{{ infra_name }}"
        ar_aws_infra_domain:                   "{{ base_domain }}"
        ar_aws_infra_region:                   "{{ aws_region }}"
        ar_aws_infra_envs:                     "{{ envs }}"    
```
