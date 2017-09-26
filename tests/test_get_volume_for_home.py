# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


cluster_ret_value = {
    'attributes-list': {
        'volume-attributes': [{
            'volume-id-attributes': {
                'name': "name11",
                'type': "dp",
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
        }, {
            'volume-id-attributes': {
                'name': "name12",
                'type': "rw",
            },
            'volume-state-attributes': {'state': "online"},
            'volume-space-attributes': {
                "size-total": "1202590842",
                "size-used": "95758254",
                "size-available": "1106832588",
            },
            'volume-inode-attributes': {
                "files-total": "4358138",
                "files-used": "14024",
            }
        }, {
            'volume-id-attributes': {
                'name': "name13",
                'type': "rw",
            },
            'volume-state-attributes': {'state': "online"},
            'volume-space-attributes': {
                "size-total": "1202590842",
                "size-used": "95758334",
                "size-available": "1106832508",
            },
            'volume-inode-attributes': {
                "files-total": "4358138",
                "files-used": "14024",
            }
        }]
    },
    'num-records': '3'
}

seven_ret_value = {
    'volumes': {
        'volume-info': [{
            'name': "name11",
            'state': "online",
            "size-total": "120259084288",
            "size-used": "9575825408",
            "size-available": "110683258880",
            "files-total": "4358138",
            "files-used": "14024",
            "raid-status": "snapmirror",
        }, {
            'name': "name12",
            'state': "online",
            "size-total": "1202590842",
            "size-used": "95758254",
            "size-available": "1106832588",
            "files-total": "4358138",
            "files-used": "14024",
            "raid-status": "ok",
        }, {
            'name': "name13",
            'state': "online",
            "size-total": "1202590842",
            "size-used": "95758334",
            "size-available": "1106832508",
            "files-total": "4358138",
            "files-used": "14024",
            "raid-status": "ok",
        }]
    }
}


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_get_volume_for_project(mode, monkeypatch):

    def get_quota_size(*args, **kwargs):
        return 12345.0
    monkeypatch.setattr("nidhogg.core.Nidhogg.get_allocated_quota_size", get_quota_size)

    def get_quota_ratio(*args, **kwargs):
        return 0.1
    monkeypatch.setattr("nidhogg.core.Nidhogg.get_allocated_quota_ratio", get_quota_ratio)

    project_volumes = mode.get_volumes_with_quota_info(filter_volume_names=[])

    assert project_volumes == [
        # only online volumes with state = rw are returned
        # {
        #     'filer': u'my.url.to.filer',
        #     'files_total': 4358138.0,
        #     'files_used': 14024.0,
        #     'name': 'name11',
        #     'size_available': 110683258880.0,
        #     'size_total': 120259084288.0,
        #     'size_used': 9575825408.0,
        #     'state': 'offline',
        #     'snapable': False,
        #     'quota_ratio': 0.1,
        #     'quota_size': 12345.0,
        # },
        {
            'filer': u'my.url.to.filer',
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name12',
            'size_available': 1106832588.0,
            'size_total': 1202590842.0,
            'size_used': 95758254.0,
            'state': 'online',
            'snapable': True,
            'quota_ratio': 0.1,
            'quota_size': 12345.0,
        },
        {
            'filer': u'my.url.to.filer',
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name13',
            'size_available': 1106832508.0,
            'size_total': 1202590842.0,
            'size_used': 95758334.0,
            'state': 'online',
            'snapable': True,
            'quota_ratio': 0.1,
            'quota_size': 12345.0,
        }]


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_get_volume_for_project_with_filter(mode, monkeypatch):

    def get_quota_size(*args, **kwargs):
        return 12345.0
    monkeypatch.setattr("nidhogg.core.Nidhogg.get_allocated_quota_size", get_quota_size)

    def get_quota_ratio(*args, **kwargs):
        return 0.1
    monkeypatch.setattr("nidhogg.core.Nidhogg.get_allocated_quota_ratio", get_quota_ratio)

    project_volumes = mode.get_volumes_with_quota_info(filter_volume_names=["name12"])
    assert project_volumes == \
        [{
            'filer': u'my.url.to.filer',
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name12',
            'size_available': 1106832588.0,
            'size_total': 1202590842.0,
            'size_used': 95758254.0,
            'state': 'online',
            'snapable': True,
            'quota_ratio': 0.1,
            'quota_size': 12345.0,
        }]


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_get_volume_for_user(mode):
    home_volumes = mode.get_volumes(filter_volume_names=[])
    assert home_volumes == [
        # only online volumes with state = rw are returned
        # {
        #     'filer': u'my.url.to.filer',
        #     'files_total': 4358138.0,
        #     'files_used': 14024.0,
        #     'name': 'name11',
        #     'size_available': 110683258880.0,
        #     'size_total': 120259084288.0,
        #     'size_used': 9575825408.0,
        #     'state': 'offline',
        #     'snapable': False,
        # },
        {
            'filer': u'my.url.to.filer',
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name12',
            'size_available': 1106832588.0,
            'size_total': 1202590842.0,
            'size_used': 95758254.0,
            'state': 'online',
            'snapable': True,
        },
        {
            'filer': u'my.url.to.filer',
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name13',
            'size_available': 1106832508.0,
            'size_total': 1202590842.0,
            'size_used': 95758334.0,
            'state': 'online',
            'snapable': True,
        }]


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_get_volume_for_user_with_filter(mode):
    home_volumes = mode.get_volumes(filter_volume_names=['name12'])
    assert home_volumes == \
        [{
            'filer': u'my.url.to.filer',
            'files_total': 4358138.0,
            'files_used': 14024.0,
            'name': 'name12',
            'size_available': 1106832588.0,
            'size_total': 1202590842.0,
            'size_used': 95758254.0,
            'state': 'online',
            'snapable': True,
        }]
