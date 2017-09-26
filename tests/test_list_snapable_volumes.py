# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


LIST_VOLS = [{
    'state': u'online',
    'name': u'wtest000',
    'snapable': True
}, {
    'state': u'offline',
    'name': u'test',
    'snapable': True
}, {
    'state': u'online',
    'name': u'wtest000',
    'snapable': False
}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {}),
    (SevenMode, {})
], indirect=True)
def test_list_snapable_volumes(mode):
    mode.list_volumes = lambda: LIST_VOLS
    assert mode.list_snapable_volumes() == [{'state': u'online', 'name': u'wtest000', 'snapable': True}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {}),
    (SevenMode, {})
], indirect=True)
def test_list_snapable_volumes_api(mode):
    mode.list_volumes = lambda: LIST_VOLS
    mode.list_snapable_volumes()
    assert mode.sent == []
