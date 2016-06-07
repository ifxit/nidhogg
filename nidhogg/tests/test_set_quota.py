# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


pytestmark = pytest.mark.usefixtures(
    "patch_timeout",
)


@pytest.mark.parametrize('mode', [
    (SevenMode, {'@status': "passed", 'status': "on"}),
], indirect=True)
def test_set_quota_sevenmode_api(mode):
    mode.set_quota("volume", "qtree", 1000)
    assert mode.sent == [
        ('quota_set_entry', {'disk_limit': 1024000, 'qtree': '', 'quota_target': '/vol/volume/qtree', 'quota_type': 'tree', 'soft_disk_limit': 819200, 'volume': 'volume'}),
        ('quota_resize', {'volume': 'volume'}),
        ('quota_status', {'volume': "volume"})
    ]


@pytest.mark.parametrize('mode', [
    (SevenMode, {'@status': "passed", 'status': "on"}),
], indirect=True)
def test_set_quota_sevenmode_api_without_wait(mode):
    mode.set_quota("volume", "qtree", 1000, False)
    assert mode.sent == [
        ('quota_set_entry', {'disk_limit': 1024000, 'qtree': '', 'quota_target': '/vol/volume/qtree', 'quota_type': 'tree', 'soft_disk_limit': 819200, 'volume': 'volume'}),
        ('quota_resize', {'volume': 'volume'})
    ]


@pytest.mark.parametrize('mode', [
    (SevenMode, {'@status': "passed", 'status': "on"}),
], indirect=True)
def test_delete_quota_sevenmode_api(mode):
    mode.delete_quota("volume", "qtree")
    assert mode.sent == [
        ('quota_delete_entry', {'qtree': '', 'quota_target': '/vol/volume/qtree', 'quota_type': 'tree', 'volume': 'volume'}),
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "on"}),
], indirect=True)
def test_set_quota_clustermode_api(mode):
    mode.set_quota("volume", "qtree", 1000)
    assert mode.sent == [
        ('quota_set_entry', {'disk_limit': 1024000, 'qtree': '', 'quota_target': '/vol/volume/qtree', 'quota_type': 'tree', 'soft_disk_limit': 819200, 'volume': 'volume', 'policy': 'default'}),
        ('quota_resize', {'volume': 'volume'}),
        ('quota_status', {'volume': "volume"})
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "on"}),
], indirect=True)
def test_set_quota_clustermode_api_without_wait(mode):
    mode.set_quota("volume", "qtree", 1000, False)
    assert mode.sent == [
        ('quota_set_entry', {'disk_limit': 1024000, 'qtree': '', 'quota_target': '/vol/volume/qtree', 'quota_type': 'tree', 'soft_disk_limit': 819200, 'volume': 'volume', 'policy': 'default'}),
        ('quota_resize', {'volume': 'volume'})
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "on"}),
], indirect=True)
def test_delete_quota_clustermode_api(mode):
    mode.delete_quota("volume", "qtree")
    assert mode.sent == [
        ('quota_delete_entry', {'qtree': '', 'quota_target': '/vol/volume/qtree', 'quota_type': 'tree', 'volume': 'volume', 'policy': 'default'}),
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "on"}),
    (SevenMode, {'@status': "passed", 'status': "on"})
], indirect=True)
def test_set_quota(mode):
    mode.set_quota("volume", "qtree", 1000, False)
    mode.set_quota("volume", "qtree", 1000, True)


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "on"}),
    (SevenMode, {'@status': "passed", 'status': "on"})
], indirect=True)
def test_delete_quota(mode):
    mode.delete_quota("volume", "qtree")


def test_set_quota_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.set_quota("volume", "qtree", 1000)


def test_delete_quota_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.delete_quota("volume", "qtree")


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "off"}),
    (SevenMode, {'@status': "passed", 'status': "off"})
], indirect=True)
def test_quotas_off(mode):
    with pytest.raises(NidhoggException):
        mode.set_quota("volume", "qtree", 1000)
