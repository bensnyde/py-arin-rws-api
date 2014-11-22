py-arin-rws-api
===============

<b>Python Library for ARIN's REG-RWS REST API</b>

https://www.arin.net/resources/restful-interfaces.html

Requirements
---
- requests

Usage
---
`arin = Arin("API-XXXX-YYYY-ZZZZ-XXXX")`

`# Fetch NET details`<br>
`print arin.get_net("NET-XXX-YYY-ZZZ-0-1")`

`# Reassign NET`<br>
`netblock = NetBlockPayload("S", "", "XXX.15.219.0", "XXX.15.219.31", "27")`<br>
`net = NetPayload("", "YYYY", "", "NET-XXX-15-128-0-1", "YYYY-XXX-15-219-0", "ASXXXX", netblock)`<br>
`print arin.reassign_net("NET-XXX-15-128-0-1", net)`
