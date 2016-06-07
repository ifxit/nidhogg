# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.compatible import Quota
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_get_quota_sevenmode_api(sevenmode):
    sevenmode.get_quota("volume", "qtree")
    assert sevenmode.sent == [('quota_get_entry', {'qtree': "", 'quota-target': "/vol/volume/qtree", 'quota-type': "tree", 'volume': "volume"})]


def test_get_quota_clustermode_api(clustermode):
    clustermode.get_quota("volume", "qtree")
    assert clustermode.sent == [('quota_list_entries_iter', dict(
        query=dict(
            quota_entry=dict(
                quota_target="/vol/volume/qtree"
            )
        ),
        max_records=65536
    ))]


def test_item_to_quota_no_numbers(allmodes):
    item = {
        'disk-limit': "-",
        'file-limit': "-",
        'threshold': "-",
        'soft-disk-limit': "-",
        'soft-file-limit': "-"
    }
    quota = Quota(
        disk_limit=-1,
        file_limit=-1,
        threshold=-1,
        soft_disk_limit=-1,
        soft_file_limit=-1,
    )
    assert quota == allmodes._item_to_quota(item)


def test_item_to_quota_numbers(allmodes):
    item = {
        'disk-limit': "123",
        'file-limit': "123",
        'threshold': "123",
        'soft-disk-limit': "123",
        'soft-file-limit': "123"
    }
    quota = Quota(
        disk_limit=125952.0,
        file_limit=123.0,
        threshold=125952.0,
        soft_disk_limit=125952.0,
        soft_file_limit=123.0,
    )
    assert quota == allmodes._item_to_quota(item)


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        '@status': "passed",
        'attributes-list': {
            'quota-entry': {
                'disk-limit': "1236",
                'file-limit': '-',
                'policy': "default",
                'qtree': "",
                'quota-target': "/vol/test002/userdir",
                'quota-type': "tree",
                'soft-disk-limit': "988",
                'soft-file-limit': "-",
                'threshold': "-",
                'volume': "test002",
                'vserver': "filer101sm"
            },
        },
        'num-records': 1
    }),
    (SevenMode, {
        '@status': "passed",
        'disk-limit': "1236",
        'file-limit': "-",
        'threshold': "-",
        'soft-disk-limit': "988",
        'soft-file-limit': "-"
    })
], indirect=True)
def test_get_quota(mode):
    assert mode.get_quota("volume", "qtree") == \
        {'threshold': -1, 'file_limit': -1, 'soft_file_limit': -1, 'disk_limit': 1265664.0, 'soft_disk_limit': 1011712.0}


def test_get_quota_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.get_quota("volume1", "qtree2")


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        '@status': "passed",
        'num-records': 0
    }),
], indirect=True)
def test_get_quota_no_entries(mode):
    assert {} == mode.get_quota("volume", "qtree1")
