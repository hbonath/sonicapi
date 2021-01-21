#!/usr/bin/env python3
#
#
# Copyright (c) 2021, Henry Bonath (henry@thebonaths.com)
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
import urllib3
from collections import OrderedDict
from requests.auth import HTTPDigestAuth
urllib3.disable_warnings()


class sonicapi:
    """
    A class represting a connection to a SonicWALL Appliance.

    Attributes:
    -----------
    hostname : str
        IP Address or Hostname of Appliance
    port : int
        TCP Port used for HTTPS Management
    username : str
        Username of admin-level user
    password : str
        Password of admin-level user

    Methods:
    --------
    auth
    AddressObjects
    AddressGroups
    ServiceObjects
    ServiceGroups
    Zones
    NatPolicies
    AccessRules
    RoutePolicies
    Restart
    """
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
        self.response = {
            'status': {
                'success': None,
                'info': [{
                    'level': None,
                    'code': None,
                    'message': None
                }]
            },
        }

    def _api_head(self, controller, data=None):
        """
        Internal method used to send HTTP HEAD
        """
        uri = controller
        url = self.baseurl + uri
        if data != None:
            try:
                jsondata = json.dumps(data)
            except:
                jsondata = json.dumps({})
            r = requests.head(url, data=jsondata, **self.kwargs)
        else:
            r = requests.head(url, **self.kwargs)
        response = r.json()
        return response

    def _api_get(self, controller):
        """
        Internal method used to send HTTP GET
        """
        uri = controller
        url = self.baseurl + uri
        r = requests.get(url, **self.kwargs)
        response = r.json()
        return response

    def _api_post(self, controller, data=None):
        """
        Internal method used to send HTTP POST
        """
        uri = controller
        url = self.baseurl + uri
        if data != None:
            try:
                jsondata = json.dumps(data)
            except:
                jsondata = json.dumps({})
            r = requests.post(url, data=jsondata, **self.kwargs)
        else:
            r = requests.post(url, **self.kwargs)
        response = r.json()
        return response

    def _api_put(self, controller, data=None):
        """
        Internal method used to send HTTP PUT
        """
        uri = controller
        url = self.baseurl + uri
        if data != None:
            try:
                jsondata = json.dumps(data)
            except:
                jsondata = json.dumps({})
            r = requests.put(url, data=jsondata, **self.kwargs)
        else:
            r = requests.put(url, **self.kwargs)
        response = r.json()
        return response

    def _api_patch(self, controller, data=None):
        """
        Internal method used to send HTTP PATCH
        """
        uri = controller
        url = self.baseurl + uri
        if data != None:
            try:
                jsondata = json.dumps(data)
            except:
                jsondata = json.dumps({})
            r = requests.patch(url, data=jsondata, **self.kwargs)
        else:
            r = requests.patch(url, **self.kwargs)
        response = r.json()
        return response

    def _api_delete(self, controller):
        """
        Internal method used to send HTTP DELETE
        """
        uri = controller
        url = self.baseurl + uri
        r = requests.delete(url, **self.kwargs)
        response = r.json()
        return response

    def auth(self, authmethod='Digest', login=False, logout=False):
        """
        Authenticate to the SonicWALL Appliance
        
        Keyword arguments:
        ------------------
        authmethod : str
            Either 'Basic' or 'Digest' (Defaults to Digest)
            HTTP Basic auth requires this to be enabled on your Appliance which is not enabled by default
        login      : bool
            Set this to True if logging in
        logout     : bool
            Set this to True if logging out
        """
        controller = 'auth'
        url = self.baseurl + controller
        response = self.response
        if authmethod == 'Digest' and login == True:
            self.kwargs['auth'] = HTTPDigestAuth(self.authinfo[0], self.authinfo[1])
            r = requests.head(url, **self.kwargs)
            if r.status_code == 200:
                response['status']['success'] = True
                response['status']['info'][0]['level'] = 'info'
                response['status']['info'][0]['code'] = 'E_OK'
                response['status']['info'][0]['message'] = 'Success.'
        elif authmethod == 'Basic' and login == True:
            r = requests.post(url, **self.kwargs)
            response = r.json()
        elif logout == True:
            r = requests.delete(url, **self.kwargs)
            response = r.json()
        return response

    def Version(self):
        """
        Outputs version information
        """
        controller = 'version'
        response = self._api_get(controller)
        return response

    def getPendingChanges(self):
        """
        Returns any pending changes
        """
        controller = 'config/pending'
        response = self._api_get(controller)
        return response

    def commitPendingChanges(self):
        """
        Commits all pending changes to the running and startup config
        """
        controller = 'config/pending'
        response = self._api_post(controller)
        return response

    def AddressObjects(self, objectlist=[], method='get', type='ipv4', name=None, uuid=None):
        """
        Interact with Address Objects
        
        Keyword arguments:
        method     -- HTTP method to use ('get', 'post', 'put', 'delete')
        type       -- 'ipv4', 'ipv6', 'mac', or 'fqdn'
        objectlist -- list of address objects you are creating/deleting/modifying.
        name       -- Optional string containing the name of the object you wish to interact with.
        uuid       -- Optional string containing the uuid of the object you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'address-objects/{}/'.format(type)
        if name != None:
            controller = '{}name/{}'.format(controller, name)
        if uuid != None:
            controller = '{}name/{}'.format(controller, uuid)
        data = {
            'address_objects': objectlist
        }
        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def AddressGroups(self, objectlist=[], method='get', ipversion='ipv4', name=None, uuid=None):
        """
        Interact with Address Groups
        
        Keyword arguments:
        method     -- HTTP method to use ('get', 'post', 'put', 'delete')
        ipversion  -- 'ipv4' or 'ipv6'
        objectlist -- list of address groups you are creating/deleting/modifying.
        name       -- Optional string containing the name of the group you wish to interact with.
        uuid       -- Optional string containing the uuid of the group you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'address-groups/{}/'.format(ipversion)
        if name != None:
            controller = '{}name/{}'.format(controller, name)
        if uuid != None:
            controller = '{}name/{}'.format(controller, uuid)
        data = {
            'address_groups': objectlist
        }
        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def ServiceObjects(self, objectlist=[], method='get', name=None, uuid=None):
        """
        Interact with Service Objects
        
        Keyword arguments:
        method     -- HTTP method to use ('get', 'post', 'put', 'delete')
        objectlist -- list of service objects you are creating/deleting/modifying.
        name       -- Optional string containing the name of the object you wish to interact with.
        uuid       -- Optional string containing the uuid of the object you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'service-objects/'
        if name != None:
            controller = '{}name/{}'.format(controller, name)
        if uuid != None:
            controller = '{}name/{}'.format(controller, uuid)
        data = {
            'service_objects': objectlist
        }
        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def ServiceGroups(self, objectlist=[], method='get', name=None, uuid=None):
        """
        Interact with Service Groups
        
        Keyword arguments:
        method     -- HTTP method to use ('get', 'post', 'put', 'delete')
        objectlist -- list of service groups you are creating/deleting/modifying.
        name       -- Optional string containing the name of the group you wish to interact with.
        uuid       -- Optional string containing the uuid of the group you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'service-groups/'
        if name != None:
            controller = '{}name/{}'.format(controller, name)
        if uuid != None:
            controller = '{}name/{}'.format(controller, uuid)
        data = {
            'service_groups': objectlist
        }
        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def Zones(self, objectlist=[], method='get', name=None, uuid=None):
        """
        Interact with Zones
        
        Keyword arguments:
        method     -- HTTP method to use ('get', 'post', 'put', 'delete')
        objectlist -- list of zones you are creating/deleting/modifying.
        name       -- Optional string containing the name of the zone you wish to interact with.
        uuid       -- Optional string containing the uuid of the zone you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'zones/'

        if name != None:
            controller = '{}name/{}'.format(controller, name)
        if uuid != None:
            controller = '{}uuid/{}'.format(controller, uuid)

        if name != None or uuid != None:
            data = {
                'zone': objectlist
            }
        else:
            data = {
                'zones': objectlist
            }

        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def NatPolicies(self, objectlist=[], method='get', ipversion='ipv4', uuid=None):
        """
        Interact with NAT Policies
        
        Keyword arguments:
        method     -- HTTP method to use ('get', 'post', 'put', 'delete')
        objectlist -- list of NAT Policies you are creating/deleting/modifying.
        uuid       -- Optional string containing the uuid of the NAT Policy you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'nat-policies/'

        if ipversion == 'ipv6':
            controller = '{}ipv6/'.format(controller)
        else:
            controller = '{}ipv4/'.format(controller)

        if uuid != None:
            controller = '{}uuid/{}'.format(controller, uuid)

        data = {
            'nat_policies': objectlist
        }

        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def AccessRules(self, objectlist=[], method='get', ipversion='ipv4', uuid=None):
        """
        Interact with Access Rules
        
        Keyword arguments:
        method     -- HTTP method to use ('get', 'post', 'put', 'delete')
        objectlist -- list of Access Rules you are creating/deleting/modifying.
        uuid       -- Optional string containing the uuid of the Access Rule you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'access-rules/'

        if ipversion == 'ipv6':
            controller = '{}ipv6/'.format(controller)
        else:
            controller = '{}ipv4/'.format(controller)

        if uuid != None:
            controller = '{}uuid/{}'.format(controller, uuid)

        data = {
            'access_rules': objectlist
        }

        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def RoutePolicies(self, objectlist=[], method='get', ipversion='ipv4', uuid=None):
        """
        Interact with Route Policies
        
        Keyword arguments:
        objectlist -- list of Route Policies you are creating/deleting/modifying.
        method     -- HTTP method to use ('get', 'post', 'put', 'delete') Defaults to 'get'
        ipversion  -- ipv4 or ipv6 - Defaults to 'ipv4'
        uuid       -- Optional string containing the uuid of the Route Policy you wish to interact with.
        """
        response = self.response
        validmethods = ['get', 'post', 'put', 'delete']
        if method not in validmethods:
            response['status']['success'] = False
            response['status']['info'][0]['level'] = 'error'
            response['status']['info'][0]['code'] = 'E_INVALID'
            response['status']['info'][0]['message'] = 'Invalid Method.'
            return response
        controller = 'route-policies/'

        if ipversion == 'ipv6':
            controller = '{}ipv6/'.format(controller)
        else:
            controller = '{}ipv4/'.format(controller)

        if uuid != None:
            controller = '{}uuid/{}'.format(controller, uuid)

        data = {
            'route_policies': objectlist
        }

        if method == 'post':
            response = self._api_post(controller, data)
        elif method == 'put':
            response = self._api_put(controller, data)
        elif method == 'delete':
            response = self._api_delete(controller)
        else:
            response = self._api_get(controller)
        return response

    def Restart(self, at=None, minutes=None, hours=None, days=None):
        """
        Reboot the SonicWALL Appliance.
        (Defaults to restart the appliance immediately)
        
        Keyword arguments:
        at      -- Optional str: Timestamp in the form: 'YYYY:MM:DD:HH:MM:SS'
        minutes -- Optional int: Number of minutes in the future
        hours   -- Optional int: Number of hours in the future
        days    -- Optional int: Number of days in the future
        """
        controller = 'restart/'
        if at != None and minutes == None and hours == None and days == None:
            pass
        elif minutes != None and at == None and hours == None and days == None:
            controller = '{}in/{}/minutes'.format(controller, minutes)
        elif hours != None and at == None and minutes == None and days == None:
            controller = '{}in/{}/hours'.format(controller, hours)
        elif days != None and at == None and minutes == None and hours == None:
            controller = '{}in/{}/days'.format(controller, days)

        response = self._api_post(controller)
        return response

