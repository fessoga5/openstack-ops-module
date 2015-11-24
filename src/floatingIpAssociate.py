#!/usr/bin/env python2.7
# vim: sts=4 ts=4 sw=4 et ai
import os
import time
#from credentials import get_nova_credentials_v2
#from novaclient.client import Client
from neutronclient.v2_0 import client

def get_config_yaml( path_config=os.path.dirname(os.path.realpath(__file__)) + "/../config.d/config.yaml", name_config="openstack"):
    import yaml
    from yaml import Loader, SafeLoader

    def construct_yaml_str(self, node):
        # Override the default string handling function 
        # to always return unicode objects
        return self.construct_scalar(node)

    Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
    SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)

    f = open(path_config)
    # use safe_load instead load
    dataMap = yaml.load(f)[name_config]
    f.close()
    return dataMap

def floatingipadd(hostname, ipaddress):
    neutron = client.Client(**get_config_yaml())
    nets = neutron.list_networks()
    print(nets)

if __name__== "__main__":
    floatingipadd(hostname='test-floating', ipaddress='94.137.192.162')
