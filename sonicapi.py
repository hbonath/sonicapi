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
        self.baseurl = 'https://{0}:{1}/api/sonicos/'.format(hostname, str(port))
        self.authinfo = (username, password)
        self.headers = OrderedDict([
            ('Accept', 'application/json'),
            ('Content-Type', 'application/json'),
            ('Accept-Encoding', 'application/json'),
            ('Charset', 'UTF-8')])

    def auth(self, login=False, logout=False):
        controller = 'auth'
        url = self.baseurl + controller
        if login == True:
            r = requests.post(url, auth=self.authinfo, headers=self.headers, verify=False)
            if r.status_code != 200:
                return r.status_code
            else:
                response = r.json()
                return response
        elif logout == True:
            r = requests.delete(url, headers=self.headers, verify=False)
            if r.status_code != 200:
                return r.status_code
            else:
                response = r.json()
                return response
        return {}

    def getVersion(self):
        controller = 'version'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getPendingChanges(self):
        controller = 'config/pending'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def commitPendingChanges(self):
        controller = 'config/pending'
        url = self.baseurl + controller
        r = requests.post(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getIPv6AddressObjects(self):
        controller = 'address-objects/ipv6'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getIPv6AddressGroups(self):
        controller = 'address-groups/ipv6'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getIPv4AddressObjects(self):
        controller = 'address-objects/ipv4'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getIPv4AddressGroups(self):
        controller = 'address-groups/ipv4'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getIPv4NatPolicies(self):
        controller = 'nat-policies/ipv4'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getIPv4ACL(self):
        controller = 'access-rules/ipv4'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
            return response

    def getIPv4routes(self):
        controller = 'route-policies/ipv4'
        url = self.baseurl + controller
        r = requests.get(url, auth=self.authinfo, headers=self.headers, verify=False)
        if r.status_code != 200:
            return r.status_code
        else:
            response = r.json()
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
