# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_list_quotas_sevenmode_api(sevenmode):
    sevenmode.list_quotas("asdf")
    assert sevenmode.sent == [('quota_report', {'volume': 'asdf'})]


def test_list_quotas_clustermode_api(clustermode):
    clustermode.list_quotas("asdf")
    assert clustermode.sent == [('quota_report_iter', {'max_records': 65536, 'query': {'quota': {'volume': "asdf"}}})]


seven_ret_value = {
    "quotas": {
        "quota": [{
            'disk-limit': "1236",
            'file-limit': "-",
            'threshold': "-",
            'soft-disk-limit': "988",
            'soft-file-limit': "-",
            'quota-target': "/vol/volume/qtree1",
            'files-used': "123",
            'disk-used': "500",
            'tree': "qtree1",
        }, {
            'disk-limit': "1000",
            'file-limit': "1000",
            'threshold': "1000",
            'soft-disk-limit': "1000",
            'soft-file-limit': "1000",
            'quota-target': "/vol/volume/qtree2",
            'files-used': "1000",
            'disk-used': "1000",
            'tree': "qtree2",
        }],
    }
}
cluster_ret_value = {
    'attributes-list': {
        'quota': [{
            'disk-limit': "1236",
            'file-limit': "-",
            'threshold': "-",
            'soft-disk-limit': "988",
            'soft-file-limit': "-",
            'quota-target': "/vol/volume/qtree1",
            'files-used': "123",
            'disk-used': "500",
            'tree': "qtree1",
        }, {
            'disk-limit': "1000",
            'file-limit': "1000",
            'threshold': "1000",
            'soft-disk-limit': "1000",
            'soft-file-limit': "1000",
            'quota-target': "/vol/volume/qtree2",
            'files-used': "1000",
            'disk-used': "1000",
            'tree': "qtree2",
        }],
    },
    'num-records': 2,
}


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_list_quotas(mode):
    assert mode.list_quotas("asdf") == \
        [{'quota_target': u'/vol/volume/qtree1', 'file_limit': -1, 'tree': u'qtree1', 'disk_limit': 1265664.0, 'soft_file_limit': -1, 'threshold': -1, 'disk_used': 512000.0, 'files_used': 123.0, 'soft_disk_limit': 1011712.0},
         {'quota_target': u'/vol/volume/qtree2', 'file_limit': 1000.0, 'tree': u'qtree2', 'disk_limit': 1024000.0, 'soft_file_limit': 1000.0, 'threshold': 1024000.0, 'disk_used': 1024000.0, 'files_used': 1000.0, 'soft_disk_limit': 1024000.0}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_allocated_quota_size(mode):
    assert mode.get_allocated_quota_size("vol") == 2289664.0


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'quota': {
                'disk-limit': "1236",
                'file-limit': "-",
                'threshold': "-",
                'soft-disk-limit': "988",
                'soft-file-limit': "-",
                'quota-target': "/vol/volume/qtree",
                'files-used': "123",
                'disk-used': "500",
                'tree': "qtree",
            }
        },
        'num-records': 1,
    }),
    (SevenMode, {
        "quotas": {
            "quota": {
                'disk-limit': "1236",
                'file-limit': "-",
                'threshold': "-",
                'soft-disk-limit': "988",
                'soft-file-limit': "-",
                'quota-target': "/vol/volume/qtree",
                'files-used': "123",
                'disk-used': "500",
                'tree': "qtree",
            }
        }
    })
], indirect=True)
def test_list_quotas_single_entry(mode):
    assert mode.list_quotas("asdf") == \
        [{'quota_target': u'/vol/volume/qtree', 'file_limit': -1, 'tree': u'qtree', 'disk_limit': 1265664.0, 'soft_file_limit': -1, 'threshold': -1, 'disk_used': 512000.0, 'files_used': 123.0, 'soft_disk_limit': 1011712.0}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "failed"}),
    (SevenMode, {'@status': "failed"}),
    (SevenMode, {
        'error': {
            'reason': "something went wrong",
        }
    }),
], indirect=True)
def test_list_quotas_failed(mode):
    with pytest.raises(NidhoggException):
        mode.list_quotas("asdf") == []


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'status': "passed",
        'num-records': '0'
    }),
    (SevenMode, {})
], indirect=True)
def test_list_qtrees_no_entries(mode):
    assert mode.list_quotas("asdf") == []
