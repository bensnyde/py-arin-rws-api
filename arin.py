"""

Python library for ARIN's REG-RWS REST API

    https://www.arin.net/resources/restful-interfaces.html

Author: Benton Snyder
Website: http://bensnyde.me
Created: 11/20/2014
Revised: 1/1/2015

"""
import requests


class DelegationKeyPayload:
    """ Delegation Key Payload"""
    def __init__(self, algorithm, digest, ttl, digestType, keyTag):
        if digestType is not 1 and digestType is not 2:
            raise Exception("Invalid digestType")
        if algorithm is not 5 and algorithm is not 7 and algorithm is not 8:
            raise Exception("Invalid algorithm")

        self.algorithm = algorithm
        self.digest = digest
        self.ttl = ttl
        self.digestType = digestType
        self.keyTag = keyTag

    def __str__(self):
        return """<delegationKey xmlns="http://www.arin.net/regrws/core/v1">
                    <algorithm>%s</algorithm>
                    <digest>%s</digest>
                    <ttl>%s</ttl>
                    <digestType>%s</digestType>
                    <keyTag>%s</keyTag>
                </delegationkey>""" % (self.algorithm, self.digest, self.ttl, self.digestType, self.keyTag)


class AttachmentPayload:
    """Attachment Payload"""
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename

    def __str__(self):
        return """<attachment xmlns="http://www.arin.net/regrws/core/v1">
                    <data>%s</data>
                    <filename>%s</filename>
                </attachment>""" % (self.data, self.filename)


class PhonePayload:
    """Phone Payload"""
    def __init__(self, description, code, number, extension=None):
        if code is not "O" and code is not "F" and code is not "M":
            raise Exception("Invalid code")

        self.description = description
        self.code = code
        self.number = number
        self.extension = extension

    def __str__(self):
        return """<phone xmlns="http://www.arin.net/regrws/core/v1">
                    <type>
                        <description>%s</description>
                        <code>%s</code>
                    </type>
                    <number>%s</number>
                    <extensions>%s</extension>
                </phone>""" % (self.description, self.code, self.number, self.extension)


class CustomerPayload:
    """Customer Payload"""
    def __init__(self, customerName, iso3166_1name, iso3166_1code2, iso3166_1code3, iso3166_1e164, streetAddress, city, iso3166_2, postalCode, comment, parentOrgHandle=None, privateCustomer=True):
        self.customerName = customerName
        self.iso3166_1name = iso3166_1name
        self.iso3166_1code2 = iso3166_1code2
        self.iso3166_1code3 = iso3166_1code3
        self.iso3166_1e164 = iso3166_1e164
        self.streetAddress = streetAddress
        self.city = city
        self.iso3166_2 = iso3166_2
        self.postalCode = postalCode
        self.comment = comment
        self.parentOrgHandle = parentOrgHandle
        self.privateCustomer = privateCustomer

    def __str__(self):
        return """<customer xmlns="http://www.arin.net/regrws/core/v1" >
                    <customerName>%s</customerName>
                    <iso3166-1>
                        <name>UNITED STATES</name>
                        <code2>US</code2>
                        <code3>USA</code3>
                        <e164>1</e164>
                    </iso3166-1>
                    <handle></handle>
                    <streetAddress>
                        <line number = "1">%s</line>
                    </streetAddress>
                    <city>%s</city>
                    <iso3166-2>%s</iso3166-2>
                    <postalCode>%s</postalCode>
                    <comment>
                        <line number = "1">%s</line>
                    </comment>
                    <parentOrgHandle>%s</parentOrgHandle>
                    <registrationDate></registrationDate>
                    <privateCustomer>%s</privateCustomer>
                </customer>""" % (self.customerName, self.streetAddress, self.city, self.iso3166_2, self.postalCode, self.comment, self.parentOrgHandle, self.privateCustomer)



class OrganizationPayload:
    """Organization Payload"""
    def __init__(self, iso3166_1name, iso3166_1code2, iso3166_1code3, iso3166_1e164, streetAddress, city, iso3166_2, postalCode, comment, orgName, dbaName, taxId, orgUrl):
        self.iso3166_1name = iso3166_1name
        self.iso3166_1code2 = iso3166_1code2
        self.iso3166_1code3 = iso3166_1code3
        self.iso3166_1e164 = iso3166_1e164
        self.streetAddress = streetAddress
        self.city = city
        self.iso3166_2 = iso3166_2
        self.postCode = postalCode
        self.comment = comment
        self.orgName = orgName
        self.dbaName = dbaName
        self.taxId = taxId
        self.orgUrl = orgUrl

    def __str__(self):
        return """<org xmlns="http://www.arin.net/regrws/core/v1">
                    <handle></handle>
                    <registrationDate></registrationDate>
                    <iso3166-1>
                        <name>UNITED STATES</name>
                        <code2>US</code2>
                        <code3>USA</code3>
                        <e164>1</e164>
                    </iso3166-1>
                    <streetAddress>
                        <line number = "1">%s</line>
                    </streetAddress>
                    <city>%s</city>
                    <iso3166-2>%s</iso3166-2>
                    <postalCode>%s</postalCode>
                    <comment>
                        <line number = "1">%s</line>
                    </comment>
                    <orgName>%s</orgName>
                    <dbaName>%s</dbaName>
                    <taxId>%s</taxId>
                    <orgUrl>%s</orgUrl>
                </org>""" % (self.streetAddress, self.city, self.iso3166_2, self.postalCode, self.comment, self.orgName, self.dbaName, self.orgUrl)


class RoaPayload:
    """Route Origin Authorization Payload"""
    def __init__(self, signature, roaData):
        self.signiture = signature
        self.roaData = roaData

    def __str__(self):
        return """<roa xmlns="http://www.arin.net/regrws/rpki/v1">
                    <signature>%s</signature>
                    <roaData>%s</roaData>
                </roa>""" % (self.signature, self.roaData)


class NetBlockPayload:
    """Net Block Payload"""
    def __init__(self, net_type, description, startAddress, endAddress, cidrLength):
        valid_types = ['A', 'AF', 'AP', 'AR', 'AV', 'DA', 'DS', 'FX', 'IR', 'IU', 'LN', 'LX', 'PV', 'PX', 'RD', 'RN', 'RV', 'RX', 'S']
        if net_type not in valid_types:
            raise Exception("Invalid net_type")

        self.net_type = net_type
        self.description = description
        self.startAddress = startAddress
        self.endAddress = endAddress
        self.cidrLength = cidrLength

    def __str__(self):
        return """<netBlock>
                <type>%s</type>
                <description>%s</description>
                <startAddress>%s</startAddress>
                <endAddress>%s</endAddress>
                <cidrLength>%s</cidrLength>
            </netBlock>""" % (self.net_type, self.description, self.startAddress, self.endAddress, self.cidrLength)


class NetPayload:
    """Net Payload"""
    def __init__(self, comment, orgHandle, customerHandle, parentNetHandle, netName, originAS, netBlocks):
        self.comment = comment
        self.orgHandle = orgHandle
        self.customerHandle = customerHandle
        self.parentNetHandle = parentNetHandle
        self.netName = netName
        self.netBlocks = netBlocks
        self.originAS = originAS

    def __str__(self):
        return """<net xmlns="http://www.arin.net/regrws/core/v1">
                    <version>4</version>
                    <registrationDate></registrationDate>
                    <comment>
                        <line number="1">%s</line>
                    </comment>
                    <orgHandle>%s</orgHandle>
                    <handle></handle>
                    <customerHandle>%s</customerHandle>
                    <parentNetHandle>%s</parentNetHandle>
                    <netName>%s</netName>
                    <originASes>
                        <originAS>%s</originAS>
                    </originASes>
                    <netBlocks>%s   </netBlocks>
                </net>""" % (self.comment, self.orgHandle, self.customerHandle, self.parentNetHandle, self.netName, self.originAS, self.netBlocks)


class PocLinkPayload:
    """Poc Link Payload"""
    def __init__(self, poc_handle, link_type):
        valid_types = ['AD', 'AB', 'N', 'T']
        if link_type not in valid_types:
            raise Exception("Invalid link_type")

        self.poc_handle = poc_handle
        self.link_type = link_type

    def __str__(self):
        return """<pocLinkRef xmlns="http://www.arin.net/regrws/core/v1" description="" handle="%s" function="%s"></pocLinkRef>""" % (self.poc_handle, self.link_type)


class MessagePayload:
    """Message Payload"""
    def __init__(self, subject, text, category="NONE", attachment=None):
        valid_categories = ["NONE", "JUSTIFICATION"]
        if category not in valid_categories:
            raise Exception("Invalid category")

        self.subject = subject
        self.text = text
        self.category = category
        self.attachment = attachment

    def __str__(self):
        return """<message xmlns="http://www.arin.net/regrws/core/v1">
                    <subject>%s</subject>
                    <text>
                        <line number="1">%s</line>
                    </text>
                    <category>%s</category>
                    <attachments>%s</attachments>
                </message""" % (self.subject, self.text, self.category, self.attachment)

class Arin:
    def __init__(self, apikey):
        """Constructor

        Parameters
            apikey: str arin apikey
        Returns
            None
        """
        self.apikey = apikey

    def _api_query(self, resource, payload=None, method="GET", return_type="xml"):
        """Query ARIN API

            Queries ARIN WOHIS/RWS REST API with specified resource.

        Parameters
            resource: str uri
            *payload: str xml-formatted payload
            *method: str http method type
            *return_Type: str response formatting
        Returns
            response: api response
        """
        try:
            if method not in ["GET", "POST", "DELETE", "PUT"]:
                raise Exception("Invalid method specified")

            if return_type not in ["json", "html", "plain", "xml"]:
                raise Exception("Invalid return type specified")

            headers = {'Content-Type': 'application/xml'}

            if return_type is "json":
                headers.update({'Accept:': 'application/json'})
            elif return_type is "html":
                headers.update({'Accept:': 'text/html'})
            elif return_type is "plain":
                headers.update({'Accept:': 'text/plain'})
            elif return_type is "xml":
                headers.update({'Accept:': 'application/xml'})

            if method is "GET":
                request = requests.get("https://www.arin.net/rest%s?apikey=%s" % (resource, self.apikey), headers=headers)
            elif method is "POST":
                request = requests.post("https://www.arin.net/rest%s?apikey=%s" % (resource, self.apikey), data=payload, headers=headers)
            elif method is "PUT":
                request = requests.put("https://www.arin.net/rest%s?apikey=%s" % (resource, self.apikey), data=payload, headers=headers)
            elif method is "DELETE":
                request = requests.delete("https://www.arin.net/rest%s?apikey=%s" % (resource, self.apikey), headers=headers)

            if request.status_code is not 200:
                raise Exception("Server returned error code %s: %s" % (request.status_code, request.text))

            if return_type is "json":
                return request.json().replace('\\"', "\"")
            else:
                return request.text
        except Exception as ex:
            print "_api_query(%s) exception: %s" % (resource, ex)
            return False

    def request_whowas_asn_report(self, asnumber):
        """Request WhoWas ASN Report

            https://www.arin.net/resources/restfulmethods.html#reports

            Note: requires special access, see https://www.arin.net/resources/whowas/index.html.

        Parameters
            asnumber: str as number
        Returns
            TicketedRequestPayload - https://www.arin.net/resources/restfulpayloads.html#ticketedrequest
        """
        return self._api_query("/report/whoWas/asn/%s" % asnumber)

    def request_whowas_net_report(self, ip_address):
        """Request WhoWas Net Report

            https://www.arin.net/resources/restfulmethods.html#reports

            Note: requires special access, see https://www.arin.net/resources/whowas/index.html.

        Parameters
            ip_address: str ipv4 address
        Returns
        """
        return self._api_query("/report/whoWas/net/%s" % ip_address)

    def request_associations_report(self):
        """Request Associations Report

            https://www.arin.net/resources/restfulmethods.html#reports

        Parameters
            None
        Returns
            TicketedRequestPayload - https://www.arin.net/resources/restfulpayloads.html#ticketedrequest
        """
        return self._api_query("/report/associations")

    def request_reassignment_report(self, net_handle):
        """Request Associations Report

            https://www.arin.net/resources/restfulmethods.html#reports

        Parameters
            net_handle: str net handle
        Returns
            TicketedRequestPayload - https://www.arin.net/resources/restfulpayloads.html#ticketedrequest
        """
        return self._api_query("/report/reassignment/%s/" % net_handle)

    def get_poc(self, poc_handle):
        """Get Poc Details

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_handle: str poc handle
        Returns
            PocPayload - https://www.arin.net/resources/restfulpayloads.html#poc
        """
        return self._api_query("/poc/%s" % poc_handle)

    def delete_poc(self, poc_handle):
        """Delete Poc

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_handle: str poc handle
        Returns
            PocPayload - https://www.arin.net/resources/restfulpayloads.html#poc
        """
        return self._api_query("/poc/%s" % poc_handle, method="DELETE")

    def create_poc(self, poc_payload, makelink=True):
        """Create Poc

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_payload: str xml poc payload
            makelink = bool link poc to account
        Returns
            PocPayload - https://www.arin.net/resources/restfulpayloads.html#poc
        """
        return self._api_query("/poc;makeLink=%s" % makelink, "%s" % poc_payload)

    def modify_poc(self, poc_handle, poc_payload):
        """Modify Poc

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_handle: str poc handle
            poc_payload: str xml poc payload
        Returns
            PocPayload - https://www.arin.net/resources/restfulpayloads.html#poc
        """
        return self._api_query("/poc/%s" % poc_handle, "%s" % poc_payload, "PUT")

    def modify_poc_add_phone(self, poc_handle, phone_payload):
        """Add Phone to Poc

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_handle: str poc handle
            phone_payload: str xml phone payload
        Returns
            PhonePayload - https://www.arin.net/resources/restfulpayloads.html#phone
        """
        return self._api_query("/poc/%s/phone/" % poc_handle, "%s" % phone_payload, "PUT")

    def modify_poc_delete_phone(self, poc_handle, phone_number=None, phone_type=None):
        """Delete Phone from Poc

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_handle: str poc handle
            *phone_number: str phone number
            *phone_type: str phone type [O,F,M]
        Returns
            PayloadListPayload - https://www.arin.net/resources/restfulpayloads.html#payloadlist
        """
        if not phone_number and not phone_type:
            raise Exception("phone_number or phone_type required")

        valid_types = ["O", "F", "M"]
        if phone_type and not phone_type in valid_types:
            raise Exception("Invalid phone_type")

        return self._api_query("/poc/%s/phone/%s;type=%s" % (poc_handle, phone_number, phone_type), method="DELETE")

    def modify_poc_add_email(self, poc_handle, email_address):
        """Add Email to Poc

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_handle: str poc handle
            email_address: str email address
        Returns
            PocPayload - https://www.arin.net/resources/restfulpayloads.html#poc
        """
        return self._api_query("/poc/%s/email/%s" % (poc_handle, email_address))

    def modify_poc_delete_email(self, poc_handle, email_address):
        """Delete Email from Poc

            https://www.arin.net/resources/restfulmethods.html#pocs

        Parameters
            poc_handle: str poc handle
            email_address: str email address
        Returns
            PocPayload - https://www.arin.net/resources/restfulpayloads.html#poc
        """
        return self._api_query("/poc/%s/email/%s" % (poc_handle, email_address), method="DELETE")

    def get_customer(self, customer_handle):
        """Get Customer

            https://www.arin.net/resources/restfulmethods.html#customers

        Parameters
            customer_handle: str customer handle
        Returns
            CustomerPayload - https://www.arin.net/resources/restfulpayloads.html#customer
        """
        return self._api_query("/customer/%s" % customer_handle)

    def delete_customer(self, customer_handle):
        """Delete Customer

            https://www.arin.net/resources/restfulmethods.html#customers

        Parameters
            customer_handle: str customer handle
        Returns
            CustomerPayload - https://www.arin.net/resources/restfulpayloads.html#customer
        """
        return self._api_query("/customer/%s" % customer_handle, method="DELETE")

    def modify_customer(self, customer_handle, customer_payload):
        """Modify Customer

            https://www.arin.net/resources/restfulmethods.html#customers

        Parameters
            customer_handle: str customer handle
            customer_payload: str xml customer payload
        Returns
            CustomerPayload - https://www.arin.net/resources/restfulpayloads.html#customer
        """
        return self._api_query("/customer/%s" % customer_handle, "%s" % customer_payload, method="PUT")

    def create_roa(self, org_handle, roa_payload, resource_class="AR"):
        """Create Route Origin Authorization (ROA)

            https://www.arin.net/resources/restfulmethods.html#roa

        Parameters
            org_handle: str org handle
            resource_class: str resource class
        Returns
            TicketPayload - https://www.arin.net/resources/restfulpayloads.html#ticket
        """
        valid_types = ["AR", "AP", "RN" "LN", "AF"]
        if resource_class not in valid_types:
            raise Exception("Invalid resource_class")

        return self._api_query("/roa/%s;resourceClass=%s" % (org_handle, resource_class), "%s" % roa_payload)

    def get_org(self, org_handle):
        """Get Org

            https://www.arin.net/resources/restfulmethods.html#orgs

        Parameters
            org_handle: str org handle
        Returns
            OrgPayload - https://www.arin.net/resources/restfulpayloads.html#org
        """
        return self._api_query("/org/%s" % org_handle)

    def delete_org(self, org_handle):
        """Delete Org

            https://www.arin.net/resources/restfulmethods.html#orgs

        Parameters
            org_handle: str org handle
        Returns
            OrgPayload - https://www.arin.net/resources/restfulpayloads.html#org
        """
        return self._api_query("/org/%s" % org_handle, method="DELETE")

    def create_org(self, org_payload):
        """Create Org

            https://www.arin.net/resources/restfulmethods.html#orgs

        Parameters
            org_payload: str xml org payload
        Returns
            TicketPayload - https://www.arin.net/resources/restfulpayloads.html#ticket
        """
        return self._api_query("/org/", "%s" % org_payload)

    def modify_org(self, org_handle, org_payload):
        """Modify Org

            https://www.arin.net/resources/restfulmethods.html#orgs

        Parameters
            org_handle: str org handle
            org_payload: str xml org payload
        Returns
            OrgPayload - https://www.arin.net/resources/restfulpayloads.html#org
        """
        return self._api_query("/org/%s" % org_handle, "%s" % org_payload, "PUT")

    def modify_org_remove_poc(self, org_handle, poc_handle=None, poc_function=None):
        """Remove Poc from Org

            https://www.arin.net/resources/restfulmethods.html#orgs

        Parameters
            org_handle: str org handle
            *poc_handle: str poc handle
            *poc_function: str poc function ["Abuse POC", "Admin POC", "Tech POC", etc...]
        Returns
            OrgPayload - https://www.arin.net/resources/restfulpayloads.html#org
        """
        if not poc_handle and not poc_function:
            raise Exception("At least one of poc_handle,poc_fucntion must be supplied")

        return self._api_query("/org/%s/poc/%s;pocFunction=%s" % (org_handle, poc_handle, poc_function), method="DELETE")

    def modify_org_add_poc(self, org_handle, poc_handle, poc_function):
        """Add Poc to Org

            https://www.arin.net/resources/restfulmethods.html#orgs

        Parameters
            org_handle: str org handle
            poc_handle: str poc handle
            poc_function: str poc function ["Abuse POC", "Admin POC", "Tech POC", etc...]
        Returns
            OrgPayload - https://www.arin.net/resources/restfulpayloads.html#org
        """
        return self._api_query("/org/%s/poc/%s;pocFunction=%s" % (org_handle, poc_handle, poc_function), method="PUT")

    def get_delegation(self, delegation_name):
        """Get Delegation

            https://www.arin.net/resources/restfulmethods.html#delegations

        Parameters
            delegation_name: str delegation name
        Returns
            DelegationPayload - https://www.arin.net/resources/restfulpayloads.html#delegation
        """
        return self._api_query("/delegation/%s" % delegation_name)

    def modify_delegation(self, delegation_name, delegation_payload):
        """Modify Delegation

            https://www.arin.net/resources/restfulmethods.html#delegations

        Parameters
            delegation_name: str delegation name
            delegation_payload: str xml delegation payload
        Returns
            DelegationPayload - https://www.arin.net/resources/restfulpayloads.html#delegation
        """
        return self._api_query("/delegation/%s" % delegation_name, "%s" % delegation_payload, "PUT")

    def modify_delegation_add_nameserver(self, delegation_name, nameserver):
        """Add Nameserver to Delegation

            https://www.arin.net/resources/restfulmethods.html#delegations

        Parameters
            delegation_name: str delegation name
            nameserver: str nameserver address
        Returns
            DelegationPayload - https://www.arin.net/resources/restfulpayloads.html#delegation
        """
        return self._api_query("/delegation/%s/nameserver/%s" % (delegation_name, nameserver))

    def modify_delegation_delete_nameserver(self, delegation_name, nameserver):
        """Delete Nameserver from Delegatoin

        Parameters
            delegation_name: str delegation name
            nameserver: str nameserver address
        Returns
            DelegationPayload - https://www.arin.net/resources/restfulpayloads.html#delegation
        """
        return self._api_query("/delegation/%s/nameserver/%s" % (delegation_name, nameserver), method="DELETE")

    def modify_delegation_delete_all_nameservers(self, delegation_name):
        """Delete all Nameservers from Delegation

            https://www.arin.net/resources/restfulmethods.html#delegations

        Parameters
            delegation_name: str delegation name
        Returns
            DelegationPayload - https://www.arin.net/resources/restfulpayloads.html#delegation
        """
        return self._api_query("/delegation/%s/nameservers" % delegation_name, method="DELETE")

    def get_net(self, net_handle):
        """Get Net

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            net_handle: str nethandle
        Returns
            NetPayload - https://www.arin.net/resources/restfulpayloads.html#net
        """
        return self._api_query("/net/%s/" % net_handle)

    def delete_net(self, net_handle):
        """Delete Net

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            net_handle: str net handle
        Returns
            TicketedRequestPayload - https://www.arin.net/resources/restfulpayloads.html#ticketedrequest
        """
        return self._api_query("/net/%s" % net_handle, method="DELETE")

    def modify_net(self, net_handle, net_payload):
        """Modify Net

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            net_handle: str net handle
            net_payload: str xml netpayload
        Returns
            NetPayload - https://www.arin.net/resources/restfulpayloads.html#net
        """
        return self._api_query("/net/%s" % net_handle, "%s" % net_payload, "PUT")

    def get_delegations(self, net_handle):
        """Get Net's Delegations

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            net_handle: str net handle
        Returns
            PayloadListPayload - https://www.arin.net/resources/restfulpayloads.html#payloadlist
        """
        return self._api_query("/net/%s/delegations" % net_handle)

    def create_recipient_org(self, parent_net_handle, org_paylaod):
        """Create Recipient Org

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            parent_net_handle: str parent net handle
            org_payload: str xml org payload
        Returns
            OrgPayload - https://www.arin.net/resources/restfulpayloads.html#org
        """
        return self._api_query("/net/%s/org" % parent_net_handle, "%s" % org_payload)

    def create_recipient_customer(self, parent_net_handle, customer_payload):
        """Create Recipient Customer

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            parent_net_handle: str parent net handle
            customer_payload: str xml customer payload
        Returns
            CustomerPayload - https://www.arin.net/resources/restfulpayloads.html#customer
        """
        return self._api_query("/net/%s/customer" % parent_net_handle, "%s" % customer_payload)

    def reassign_net(self, parent_net_handle, net_payload):
        """Reassign Net

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            parent_net_handle: str parent net handle
            net_payload: str xml net payload
        Returns
            TicketedRequestPayload - https://www.arin.net/resources/restfulpayloads.html#ticketedrequest
        """
        return self._api_query("/net/%s/reassign" % parent_net_handle, "%s" % net_payload, "PUT")

    def reallocate_net(self, parent_net_handle, net_payload):
        """Reallocate Net

            https://www.arin.net/resources/restfulmethods.html#nets

        Parameters
            parent_net_handle: str parent net handle
            net_payload: str xml net payload
        Returns
            TicketedRequestPayload - https://www.arin.net/resources/restfulpayloads.html#ticketedrequest
        """
        return self._api_query("/net/%s/reallocate" % parent_net_handle, "%s" % net_payload, "PUT")

    def modify_ticket_add_message(self, ticket_number, message_payload):
        """Add Message to Ticket

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            ticket_number: str ticket number
            message_payload: str xml message payload
        Returns
            MessagePayload - https://www.arin.net/resources/restfulpayloads.html#message
        """
        return self._api_query("/ticket/%s/message" % ticket_number, "%s" % message_payload, "PUT")

    def modify_ticket(self, ticket_number, ticket_payload):
        """Modify Ticket

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            ticket_number: str ticket number
            ticket_payload: str xml ticket_payload
        Returns
            TicketPayload - https://www.arin.net/resources/restfulpayloads.html#ticket
        """
        return self._api_query("/ticket/%s" % ticket_number, "%s" % ticket_payload, "PUT")

    def modify_ticket_status(self, ticket_number, ticket_status):
        """Modify Ticket Status

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            ticket_number: str ticket number
            ticket_status: str ticket status
        Returns
            TicketPayload - https://www.arin.net/resources/restfulpayloads.html#ticket
        """
        return self._api_query("/ticket/%s/ticketStatus/%s" % (ticket_number, ticket_status), method="PUT")

    def get_ticket(self, ticket_number):
        """Get Ticket

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            ticket_number: str ticket number
        Returns
            TicketPayload - https://www.arin.net/resources/restfulpayloads.html#ticket
        """
        return self._api_query("/ticket/%s" % ticket_number)

    def get_ticket_summary(self, ticket_number):
        """Get Ticket Summary

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            ticket_number: str ticket number
        Returns
            TicketPayload - https://www.arin.net/resources/restfulpayloads.html#ticket
        """
        return self._api_query("/ticket/%s/summary" % ticket_number)

    def get_tickets(self, ticket_type=None, type_status=None):
        """Get Tickets

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            *ticket_type: str ticket type ["CREATE_ROA", "ASN_REQUEST", etc...]
            *ticket_status: str ticket status ["ACCEPTED", "DENIED", "ABANDONED", etc...]
        Returns
            PayloadListPayload - https://www.arin.net/resources/restfulpayloads.html#payloadlist
        """
        return self._api_query("/ticket;ticketType=%s;ticketStatus=%s" % (ticket_type, ticket_status))

    def get_ticket_summaries(self, ticket_type=None, type_status=None):
        """Get Ticket Summaries

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            *ticket_type: str ticket type ["CREATE_ROA", "ASN_REQUEST", etc...]
            *ticket_status: str ticket status ["ACCEPTED", "DENIED", "ABANDONED", etc...]
        Returns
            PayloadListPayload - https://www.arin.net/resources/restfulpayloads.html#payloadlist
        """
        return self._api_query("/ticket/summary;ticketType=%s;ticketStatus=%s" % (ticket_type, ticket_status))

    def get_ticket_message(self, ticket_number, message_id):
        """Get Ticket Message

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            ticket_number: str ticket number
            message_id: str message id
        Returns
            TicketPayload - https://www.arin.net/resources/restfulpayloads.html#ticket
        """
        return self._api_query("/ticket/%s/message/%s" % (ticket_number, message_id))


    def get_ticket_attachment(self, ticket_number, message_id, attachment_id):
        """Get Ticket Attachment

            https://www.arin.net/resources/restfulmethods.html#tickets

        Parameters
            ticket_number: str ticket number
            message_id: str message id
            attachment_id: str attachment id
        Returns
            application/octet-stream response
        """
        return self._api_query("/ticket/%s/message/%s/attachment/%s" % (ticket_number, message_id, attachment_id))
