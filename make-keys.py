#!/usr/bin/python
#
# This script parses the jupyterhub inventory file and uses the keymaster
# container to generate SSL keys for each host.
# 
# Runs from jupyterhub-deploy/ and uses "inventory" and "vault-password" files.

import sys
import os
import subprocess
import ansible.inventory
import argparse

DEBUG = False

parser = argparse.ArgumentParser()
specific_hosts = False
if len(sys.argv) > 1:
	specific_hosts = True
	args, arg_hosts = parser.parse_known_args(sys.argv[1:])


KEYMASTER = ["docker", "run", "--rm", "-v",
	os.getcwd() + "/../certificates/:/certificates/", "ds/keymaster"]

if DEBUG: KEYMASTER = ["echo"] + KEYMASTER

subprocess.call(KEYMASTER + ["mkpassword"])
subprocess.call(KEYMASTER + ["ca"])

vault_password = open('../jupyterhub-deploy/vault-password').read().strip()
inv = ansible.inventory.Inventory(host_list='../jupyterhub-deploy/inventory', vault_password=vault_password)
for host in inv.get_group('all').get_hosts():
	if specific_hosts and host.name not in arg_hosts:
		continue
	keyname = host.name
	ip = host.vars['fqdn']
	hostname = host.vars['ansible_ssh_host']

	subprocess.call(KEYMASTER + ["signed-keypair", "-p", "both", "-n", keyname, "-h", hostname, "-s", "IP:"+ip])
