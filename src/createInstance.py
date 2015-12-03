#!/usr/bin/env python2.7
# vim: sts=4 ts=4 sw=4 et ai
import os
import time
#from credentials import get_nova_credentials_v2

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

def get_nova_credentials_v2():
    d = get_config_yaml()
    return d

def __createInstance(hostname):
    from novaclient.client import Client
    try:
        get_cnf = get_config_yaml(name_config="csserver");
        credentials = get_nova_credentials_v2()
        nova_client = Client(**credentials)

        image = nova_client.images.find(name=get_cnf["image_name"])
        flavor = nova_client.flavors.find(name=get_cnf["image_type"])
        net = nova_client.networks.find(label=get_cnf["network"])
        nics = [{'net-id': net.id}]
        instance = nova_client.servers.create(name=hostname, image=image, flavor=flavor, key_name=None, nics=nics, security_groups=get_cnf['sec-groups'])

        #nova_client.floating_ips.list()
        #floating_ip = nova_client.floating_ips.create()
        instance = nova_client.servers.find(name=hostname)
        #instance.add_floating_ip(floating_ip)

        print("Sleeping for 5s after create command")
        time.sleep(5)
        #print("List of VMs")
        #print(nova_client.servers.list())
        return True
    except Exception as e:
        print(str(e))
        return False

def __associateFloatingIP(hostname):
    from novaclient.client import Client
    try:
        get_cnf = get_config_yaml(name_config="csserver");
        credentials = get_nova_credentials_v2()
        nova_client = Client(**credentials)

        #print(nova_client.floating_ips.list())
        floating_ip = nova_client.floating_ips.create(get_cnf['network_floating'])
        instance = nova_client.servers.find(name=hostname)
        instance.add_floating_ip(floating_ip)
        return True

    except Exception as e:
        print(str(e))
        return False

def create(hostname="test"):
    return __createInstance(hostname) and __associateFloatingIP(hostname)

if __name__== "__main__":
    create()
