# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


ret_value = {
    '@status': "passed",
    'apis': {
        'system-api-info': [
            {'name': "api1"},
            {'name': "api2"}
        ]
    }
}


@pytest.mark.parametrize('mode', [
    (ClusterMode, ret_value),
    (SevenMode, ret_value)
], indirect=True)
def test_list_api(mode):
    assert mode.apis == ['api1', 'api2']


def test_list_api_failed(allmodes_failed):
    assert allmodes_failed.apis == []


@pytest.mark.parametrize('mode', [
    (ClusterMode, ret_value),
    (SevenMode, ret_value)
], indirect=True)
def test_list_api_sent(mode):
    mode.apis
    assert mode.sent == [
        ('system_api_list', {})
    ]
