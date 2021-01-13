#!/usr/bin/env python3
#
#
# Copyright (c) 2020, Henry Bonath (henry@thebonaths.com)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests
import json
import ipaddress
import urllib3
from collections import OrderedDict
urllib3.disable_warnings()

# This module requires "Enable RFC-2617 HTTP Basic Access authentication" be enabled on the SonicWALL


class sonicapi:
    def __init__(self, hostname, port, username, password):
        self.baseurl = 'https://{}:{}/api/sonicos/'.format(
            hostname, str(port))
        self.authinfo = (username, password)
        self.headers = OrderedDict([
            ('Accept', 'application/json'),
            ('Content-Type', 'application/json'),
            ('Accept-Encoding', 'application/json'),
            ('Charset', 'UTF-8')])
        self.kwargs = {
            'auth': self.authinfo,
            'headers': self.headers,
            'verify': False,
        }

    def auth(self, login=False, logout=False):
        controller = 'auth'
        url = self.baseurl + controller
        response = {}
        if login == True:
            r = requests.post(url, **self.kwargs)
            response = r.json()
        elif logout == True:
            r = requests.delete(url, **self.kwargs)
            response = r.json()
        return response

    def api_get(self, controller):
        uri = controller
        url = self.baseurl + uri
        r = requests.get(url, **self.kwargs)
        response = r.json()
        return response
        
    def api_post(self, controller):
        uri = controller
        url = self.baseurl + uri
        r = requests.post(url, **self.kwargs)
        response = r.json()
        return response

    def api_put(self, controller):
        uri = controller
        url = self.baseurl + uri
        r = requests.put(url, **self.kwargs)
        response = r.json()
        return response

    def api_patch(self, controller):
        uri = controller
        url = self.baseurl + uri
        r = requests.patch(url, **self.kwargs)
        response = r.json()
        return response

    def api_delete(self, controller):
        uri = controller
        url = self.baseurl + uri
        r = requests.delete(url, **self.kwargs)
        response = r.json()
        return response

    def getVersion(self):
        controller = 'version'
        response = self.api_get(controller)
        return response

    def getPendingChanges(self):
        controller = 'config/pending'
        response = self.api_get(controller)
        return response

    def commitPendingChanges(self):
        controller = 'config/pending'
        response = self.api_post(controller)
        return response

    def getFqdnAddressObjects(self):
        controller = 'address-objects/fqdn'
        response = self.api_get(controller).pop('address_objects')
        return response

    def getIPv6AddressObjects(self):
        controller = 'address-objects/ipv6'
        response = self.api_get(controller).pop('address_objects')
        return response

    def getIPv6AddressGroups(self):
        controller = 'address-groups/ipv6'
        response = self.api_get(controller).pop('address_groups')
        return response

    def getIPv4AddressObjects(self):
        controller = 'address-objects/ipv4'
        response = self.api_get(controller).pop('address_objects')
        return response

    def createIPv4HostObject(self, name, zone, address):
        controller = 'address-objects/ipv4/'
        url = self.baseurl + controller
        data = {
            'address_objects': [
                {
                    'ipv4': {
                        'name': name,
                        'zone': zone,
                        'host': {
                            'ip': address
                        }
                    }
                }
            ]
        }
        jsondata = json.dumps(data)
        r = requests.post(url, data=jsondata, **self.kwargs)
        response = r.json()
        return response

    def createIPv4AddressObjects(self, objectlist):
        controller = 'address-objects/ipv4/'
        url = self.baseurl + controller
        data = {
            'address_objects': objectlist
        }
        jsondata = json.dumps(data)
        r = requests.post(url, data=jsondata, **self.kwargs)
        response = r.json()
        return response

    def getIPv4AddressGroups(self):
        controller = 'address-groups/ipv4'
        response = self.api_get(controller).pop('address_groups')
        return response

    def createIPv4AddressGroups(self, objectlist):
        controller = 'address-groups/ipv4/'
        url = self.baseurl + controller
        data = {
            'address_groups': objectlist
        }
        jsondata = json.dumps(data)
        r = requests.post(url, data=jsondata, **self.kwargs)
        response = r.json()
        return response

    def putIPv4AddressGroups(self, objectlist):
        controller = 'address-groups/ipv4/'
        url = self.baseurl + controller
        data = {
            'address_groups': objectlist
        }
        jsondata = json.dumps(data)
        r = requests.put(url, data=jsondata, **self.kwargs)
        response = r.json()
        return response

    def getIPv4NatPolicies(self):
        controller = 'nat-policies/ipv4'
        response = self.api_get(controller).pop('nat_policies')
        return response

    def getIPv4ACLs(self):
        controller = 'access-rules/ipv4'
        response = self.api_get(controller).pop('access_rules')
        return response

    def getIPv4routes(self):
        controller = 'route-policies/ipv4'
        response = self.api_get(controller).pop('route_policies')
        return response


def main():
    # This example connects to the API, dumps out a JSON list of Address Objects, and logs out.
    s = sonicapi('192.168.168.168', 4343, 'admin', 'password')
    print(json.dumps(s.auth(login=True)))
    print(json.dumps(s.getIPv4AddressObjects()))
    print(json.dumps(s.getIPv6AddressObjects()))
    print(json.dumps(s.auth(logout=True)))


if __name__ == "__main__":
    main()
