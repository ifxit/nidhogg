# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import MagicMock
import pytest

import xml
from nidhogg.core import Nidhogg, NidhoggException


@pytest.fixture
def nidhogg(request, monkeypatch, std_netapp_reply):
    def create_request_mock(*args, **kwargs):
        return "req"
    monkeypatch.setattr("nidhogg.core.Nidhogg._create_request", create_request_mock)
    mock_http = MagicMock()
    nidhogg = Nidhogg("url", "user", "password", 1, 1, mock_http)
    nidhogg.http.invoke_request.return_value = "reply"
    nidhogg.http.parse_xml_reply.return_value = std_netapp_reply
    return nidhogg


def test_core_do(nidhogg, std_netapp_reply):
    r = nidhogg._do("foobar_api", a_a=1, b=2)
    assert r == std_netapp_reply
    nidhogg.http.invoke_request.assert_called_with("req")
    nidhogg.http.parse_xml_reply.assert_called_with("reply")


@pytest.fixture
def nidhogg_status_failed(nidhogg):
    nidhogg.http.parse_xml_reply.return_value = {"netapp": {"results": {"@status": "failed", "@reason": "bla blubb error"}}}
    return nidhogg


def test_core_do_failed(nidhogg_status_failed):
    with pytest.raises(NidhoggException):
        nidhogg_status_failed._do("foobar_api", a_a=1, b=2)


@pytest.fixture
def nidhogg_parse_xml_reply_failed(nidhogg):
    nidhogg.http.parse_xml_reply.side_effect = xml.parsers.expat.ExpatError("haha")
    return nidhogg


def test_core_do_parse_xml_reply(nidhogg_parse_xml_reply_failed):
    with pytest.raises(NidhoggException):
        nidhogg_parse_xml_reply_failed._do("foobar_api", a_a=1, b=2)
