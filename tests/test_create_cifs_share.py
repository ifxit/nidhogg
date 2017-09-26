# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.clustermode import ClusterMode


def test_create_cifs_share_sevenmode_api(sevenmode):
    sevenmode.create_cifs_share(volume="vol1", qtree="asdf", share_name="asdf", group_name="group", comment="comment")
    assert sevenmode.sent == [('cifs_share_add', {'path': u'/vol/vol1/asdf', 'umask': u'007', 'share_name': u'asdf', 'forcegroup': "group", 'comment': "comment"})]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "is-clustered": "true",
        "major-version": 1,
        "minor-version": 30,
    })
], indirect=True)
def test_create_cifs_share_clustermode_api(mode):
    mode.create_cifs_share(volume="vol1", qtree="asdf", share_name="asdf", group_name="ccplatg", comment="comment")
    assert mode.sent == [
        ('system_get_version', {}),
        ('system_get_ontapi_version', {}),
        ('cifs_share_create', {'dir_umask': u'007', 'path': u'/vol/vol1/asdf', 'file_umask': u'007', 'share_name': u'asdf', 'comment': "comment", 'force_group_for_create': "ccplatg"}),
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "is-clustered": "true",
        "major-version": 1,
        "minor-version": 29,
    })
], indirect=True)
def test_create_cifs_share_clustermode_no_force_group_api(mode):
    mode.create_cifs_share(volume="vol1", qtree="asdf", share_name="asdf", group_name="ccplatg", comment="comment")
    assert mode.sent == [
        ('system_get_version', {}),
        ('system_get_ontapi_version', {}),
        ('cifs_share_create', {'dir_umask': u'007', 'path': u'/vol/vol1/asdf', 'file_umask': u'007', 'share_name': u'asdf', 'comment': "comment"}),
    ]


def test_create_cifs_share(allmodes):
    allmodes.create_cifs_share(volume="vol1", qtree="asdf", share_name="asdf")


def test_create_cifs_share_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.create_cifs_share(volume="vol1", qtree="asdf", share_name="asdf")
