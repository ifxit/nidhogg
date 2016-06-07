# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_list_volumes_sevenmode_api(sevenmode):
    sevenmode.list_volumes()
    assert sevenmode.sent == [('volume_list_info', {})]


def test_list_volumes_clustermode_api(clustermode):
    clustermode.list_volumes()
    assert clustermode.sent == [('volume_get_iter', {'max_records': 65536})]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'volume-attributes': [{
                'volume-id-attributes': {
                    'name': "name1",
                    'type': "dp",
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
            }, {
                'volume-id-attributes': {
                    'name': "name2",
                    'type': "rw",
                },
                'volume-state-attributes': {'state': "online"},
                'volume-space-attributes': {
                    "size-total": "120259084288",
                    "size-used": "9575825408",
                    "size-available": "110683258880",
                },
                'volume-inode-attributes': {
                    "files-total": "4358138",
                    "files-used": "14024",
                }
            }]
        },
        'num-records': '2'
    }),
    (SevenMode, {
        'volumes': {
            'volume-info': [{
                'name': "name1",
                'state': "offline",
                "size-total": "120259084288",
                "size-used": "9575825408",
                "size-available": "110683258880",
                "files-total": "4358138",
                "files-used": "14024",
                "raid-status": "snapmirror",
            }, {
                'name': "name2",
                'state': "online",
                "size-total": "120259084288",
                "size-used": "9575825408",
                "size-available": "110683258880",
                "files-total": "4358138",
                "files-used": "14024",
                "raid-status": "foobar",
            }]
        }
    })
], indirect=True)
def test_list_volumes(mode):
    assert mode.list_volumes() == \
        [{
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name1',
            'size_available': 110683258880.0,
            'size_total': 120259084288.0,
            'size_used': 9575825408.0,
            'state': 'offline',
            'snapable': False,
            'filer': u'my.url.to.filer',
        }, {
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name2',
            'size_available': 110683258880.0,
            'size_total': 120259084288.0,
            'size_used': 9575825408.0,
            'state': 'online',
            'snapable': True,
            'filer': u'my.url.to.filer',
        }]


seven_ret_value = {
    'volumes': {
        'volume-info': {
            'name': "name1",
            'state': "offline",
            "size-total": "120259084288",
            "size-used": "9575825408",
            "size-available": "110683258880",
            "files-total": "4358138",
            "files-used": "14024",
            "raid-status": "snapmirror",
        }
    }
}
cluster_ret_value = {
    'attributes-list': {
        'volume-attributes': {
            'volume-id-attributes': {
                'name': "name1",
                'type': "dp",
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
    },
    'num-records': '1'
}


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_list_volumes_single_entry(mode):
    assert mode.list_volumes() == \
        [{
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name1',
            'size_available': 110683258880.0,
            'size_total': 120259084288.0,
            'size_used': 9575825408.0,
            'state': 'offline',
            'snapable': False,
            'filer': u'my.url.to.filer',
        }]


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_allocated_quota_ratio(mode, monkeypatch):
    def get_allocated_quota_size(*args, **kwargs):
        return 123567890
    monkeypatch.setattr("nidhogg.core.Nidhogg.get_allocated_quota_size", get_allocated_quota_size)
    assert mode.get_allocated_quota_ratio("vol") == 0.0010275139772732342
    assert mode.get_allocated_quota_ratio("vol", 120259084288.0) == 0.0010275139772732342


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'status': "passed",
        'num-records': '0'
    }),
    (SevenMode, {})
], indirect=True)
def test_list_volumes_no_entries(mode):
    assert [] == mode.list_volumes()
