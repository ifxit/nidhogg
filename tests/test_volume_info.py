# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_volume_info_sevenmode_api(sevenmode):
    sevenmode.volume_info("name1")
    assert sevenmode.sent == [('volume_list_info', {"volume": "name1"})]


def test_volume_info_clustermode_api(clustermode):
    clustermode.volume_info("name1")
    assert clustermode.sent == [('volume_get_iter', {'query': {'volume_id_attributes': {'name': 'name1'}}})]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'volume-attributes': {
                'volume-id-attributes': {
                    'name': "name1",
                    'type': "rw",
                },
                'volume-state-attributes': {'state': "offline"},
                'volume-space-attributes': {
                    "size-total": "120259084288",
                    "size-used": "9575825408",
                    "size-available": "110683258880",
                },
                'volume-inode-attributes': {
                    "files-total": "4358138",
                    "files-used": "14024",
                }
            }
        }
    }),
    (SevenMode, {
        'volumes': {
            'volume-info': {
                'name': "name1",
                'state': "offline",
                "size-total": "120259084288",
                "size-used": "9575825408",
                "size-available": "110683258880",
                "files-total": "4358138",
                "files-used": "14024",
                "raid-status": "foobar",
            }
        }
    })
], indirect=True)
def test_volume_info(mode):
    assert mode.volume_info("name1") == {
        'filer': u'my.url.to.filer',
        'files_total': 4358138.0,
        'files_used': 14024.0,
        'name': 'name1',
        'size_available': 110683258880.0,
        'size_total': 120259084288.0,
        'size_used': 9575825408.0,
        'state': 'offline',
        'snapable': True
    }
