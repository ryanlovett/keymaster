#!/usr/bin/python
#
# This script parses the jupyterhub inventory file and uses the keymaster
# container to generate SSL keys for each host.
# 
# Runs from jupyterhub-deploy/ and uses "inventory" and "vault-password" files.

import subprocess
import ansible.inventory

DEBUG = True

KEYMASTER = ["docker", "run", "--rm", "-v",
	cwd + "/../certificates/:/certificates/", "ds/keymaster"]

if DEBUG: KEYMASTER = ["echo"] + KEYMASTER

subprocess.call(KEYMASTER + ["mkpassword"])
subprocess.call(KEYMASTER + ["ca"])

vault_password = open('vault-password').read().strip()
inv = ansible.inventory.Inventory(host_list='inventory', vault_password=vault_password)
for host in inv.get_group('all').get_hosts():
	keyname = host.name
	ip = host.vars['fqdn']
	hostname = host.vars['ansible_ssh_host']

	subprocess.call(KEYMASTER + ["signed-keypair", "-p", "both", "-n", keyname, "-h", hostname, "-s", "IP:"+ip])
