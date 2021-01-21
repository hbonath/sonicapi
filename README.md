# sonicapi
## Python3 Module to interact with the SonicWall® SonicOS API  


> This Module currently only contains basic functionality:
>
>* Address Objects
>* Address Groups
>* Service Objects
>* Service Groups
>* Zones
>* Access Rules
>* NAT Policies
>* Route Policies
>* Restart

### Installation:

```
pip3 install sonicapi
```

### Usage:

```
from sonicapi import sonicapi
import json

def main():
    # This example connects to the API, dumps out a JSON list of Address Objects, and logs out.
    s = sonicapi('192.168.168.168', 443, 'admin', 'password')
    print(json.dumps(s.auth(login=True), indent=2))
    print(json.dumps(s.AddressObjects(type='ipv4'), indent=2))
    print(json.dumps(s.AddressObjects(type='ipv6'), indent=2))
    print(json.dumps(s.auth(logout=True), indent=2))


if __name__ == "__main__":
    main()
```
