# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import xmltodict

FILER_URL = "/servlets/netapp.servlets.admin.XMLrequest_filer"


class NidhoggHttp(object):
    """Requests the Netapp API und converts the response into a dictionary."""

    def __init__(self, url, username, password, verify=False):
        """Init object."""
        self.url = url + FILER_URL
        self.username = username
        self.password = password
        self.verify = verify

    def parse_xml_reply(self, xmlresponse):
        """Convert XML reply into a dictionary.

        :param xmlresponse: Response from Netapp API.
        :type xmlresponse: str
        :return: response
        :rtype: dict
        """
        return xmltodict.parse(xmlresponse)

    def invoke_request(self, req):
        """Request the Netapp API.

        :param req: dictionary of request params
        :type req: dict
        :return: Netapp API response
        :rtype: str
        """
        r = requests.post(
            self.url, auth=(self.username, self.password),
            data=req,
            headers={'Content-Type': 'text/xml; charset="UTF-8"'},
            verify=self.verify
        )
        return r.text
