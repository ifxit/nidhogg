# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch, MagicMock
import pytest

from nidhogg.http import NidhoggHttp, FILER_URL


@pytest.fixture
def http():
    return NidhoggHttp("https://example.com", "user", "password")


def test_invoke_request(http):
    with patch("requests.post") as mock_post:
        mock_post.return_value = MagicMock(text="my return mock")
        rep = http.invoke_request("this object should be posted")
        mock_post.assert_called_with(
            "https://example.com{}".format(FILER_URL),
            auth=("user", "password"),
            data="this object should be posted",
            headers={'Content-Type': 'text/xml; charset="UTF-8"'},
            verify=False
        )
        assert rep == "my return mock"


def test_parse_xml_reply(http):
    xml = "<a>6</a>"
    assert http.parse_xml_reply(xml)['a'] == "6"
