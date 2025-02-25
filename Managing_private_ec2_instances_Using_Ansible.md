# Managing private ec2 instances Using Ansible
![image](images/ansible.jpeg)
### Purpose:
The purpose of this document is to help you to manage private ec2 instances using Ansible. This document provides a step-by-step guide to manage private EC2 instances using Ansible through a bastion host.

### Prerequisite
- Ansible Installed: Ensure Ansible is installed on your control node.
- Access to Bastion Server: The Ansible control node must have access to the bastion server.
- Access to Target Nodes via Bastion: The bastion server must have access to the target private nodes.

### Methord 1
## SSH Config File methord
1. Configure the SSH Config File

Create an SSH configuration file under the .ssh directory of your ansible user on the control node. Use the following template as an example:


```
Host prod_bastion
  hostname 52.24.198.125
  user ubuntu
  port 22
  identityfile /home/users/<user>/.ssh/id_rsa

Host prod_node1
  hostname 10.10.2.11  
  user ubuntu
  port 22
  identityfile /home/users/<user>/.ssh/id_rsa
  ProxyCommand ssh prod_bastion -W %h:%p

Host prod_node2
  hostname 10.10.2.12  
  user ubuntu
  port 22
  identityfile /home/users/<user>/.ssh/id_rsa
  ProxyCommand ssh prod_bastion -W %h:%p

Host stage_bastion
  hostname 55.334.128.194
  user ubuntu
  port 22
  identityfile /home/users/<user>/.ssh/id_rsa

Host stage_node1
  hostname 10.10.3.111  
  user ubuntu
  port 22
  identityfile /home/users/<user>/.ssh/id_rsa
  ProxyCommand ssh stage_bastion -W %h:%p

Host stage_node2
  hostname 10.10.3.112  
  user ubuntu
  port 22
  identityfile /home/users/<user>/.ssh/id_rsa
  ProxyCommand ssh stage_bastion -W %h:%p
```

2. Edit your ansible inventory with restected nodes. (a template is given below)

```
[bastions]
prod_bastion
stage_bastion

[stage_nodes]
stage_node1
stage_node2

[prod_nodes]
prod_node1
prod_node2

[children]
nodes = [
    prod_nodes,
    stage_nodes,
]
```

3. Test Connectivity

Verify SSH connectivity to the bastion server and nodes using the ssh command.

4. Test Ansible connectivity 

Test Ansible connectivity by a ping test,
```
ansible all -m ping
```
5. Automate Tasks

Use Ansible playbooks to manage the nodes. For example, create a playbook,
 manage_nodes.yml:

```
- name: Manage private EC2 instances
  hosts: nodes
  tasks:
    - name: Update all packages
      apt:
        update_cache: yes
        upgrade: dist
```
### Methord 2
## Inventory File methord
Add the bastion and node variables in the inventory file and follow the same same steps.

```
[bastion]
54.202.195.130
[nodes:vars]
ansible_user=ubuntu
ansible_become=yes
ansible_become_method=sudo
#ansible_become_pass='PASSWORD'
ansible_ssh_common_args: '-o ProxyCommand="ssh ssh -i /home/ubuntu/.private-key.pem -t -W %h:%p -q ubuntu@bastion"'
[nodes]
10.10.2.11
10.10.2.12
```
### Outcome
You can now seamlessly manage private EC2 instances using Ansible via a bastion server.
