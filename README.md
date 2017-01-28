py-arin-rws-api
===============

**Python Library for ARIN's REG-RWS REST API**

https://www.arin.net/resources/restful-interfaces.html

- Author: Benton Snyder
- Website: http://bensnyde.me
- Created: 8/30/2014
- Revised: 12/31/2014

Usage
---
```
API_KEY = "API-XXXX-XXXX-XXXX-XXXX"

arin = Arin(API_KEY)

# Get NetHandle details
print arin.get_net("NET-XXX-YYY-ZZZ-0-1")

# Reassign NetBlock
netblock = NetBlockPayload("S", "", "XXX.15.219.0", "XXX.15.219.31", "27")
net = NetPayload("", "YYYY", "", "NET-XXX-15-128-0-1", "YYYY-XXX-15-219-0", "ASXXXX", netblock)
print arin.reassign_net("NET-XXX-15-128-0-1", net)

# Reassign DNS Delegation
import xmltodict

NEW_NS1 = "NS1.EXAMPLE.COM"
NEW_NS2 = "NS2.EXAMPLE.COM"
TARGET_NETNAME  = "EXAMPL"

nethandles = ["NET-AAA-BBB-CCC-0-1", "NET-XXX-YYY-ZZZ-0-1"]
for nh in nethandles:
    response = arin.get_net(nh)
    result = xmltodict.parse(response)

    try:
        if result['net']['netName'] != TARGET_NETNAME:
            continue

        iparr = result['net']['netBlocks']['netBlock']['startAddress'].split('.')

        delegation = "%s.%s.%s.in-addr.arpa." % (
            iparr[2].lstrip('0'),
            iparr[1].lstrip('0'),
            iparr[0].lstrip('0')
        )

        arin.modify_delegation_delete_all_nameservers(delegation)
        arin.modify_delegation_add_nameserver(delegation, NEW_NS1)
        arin.modify_delegation_add_nameserver(delegation, NEW_NS2)
        print arin.get_delegation(delegation)
    except Exception as ex:
        print "Nethandle %s returned unexpected result: %s %s" %(
            nh,
            response,
            str(ex)
        )
```
