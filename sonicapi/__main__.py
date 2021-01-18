import sonicapi
import json

def main():
    # This example connects to the API, dumps out a JSON list of Address Objects, and logs out.
    s = sonicapi.sonicapi('192.168.168.168', 443, 'admin', 'password')
    print(json.dumps(s.auth(login=True), indent=2))
    print(json.dumps(s.AddressObjects(type='ipv4'), indent=2))
    print(json.dumps(s.AddressObjects(type='ipv6'), indent=2))
    print(json.dumps(s.auth(logout=True), indent=2))


if __name__ == "__main__":
    main()
