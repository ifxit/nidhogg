# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_start_cifs_acl_sevenmode_api(sevenmode):
    sevenmode._start_cifs_acls("share")
    assert sevenmode.sent == [
        ('cifs_share_acl_list_iter_start', {'share_name': u'share'})
    ]


def test_list_cifs_acl_sevenmode_api(sevenmode, monkeypatch):
    # patching start method to get the tag, used as input param
    def get_tag(*args, **kwargs):
        return dict(
            netapp=dict(
                results=dict(
                    tag="12345"
                )
            )
        )
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._start_cifs_acls", get_tag)
    sevenmode.list_cifs_acls("share")
    assert sevenmode.sent == [
        ('cifs_share_acl_list_iter_next', {'tag': "12345", 'maximum': u'1'}),
        ('cifs_share_acl_list_iter_end', {'tag': "12345"})
    ]


def test_list_cifs_acls_clustermode_api(clustermode):
    clustermode.list_cifs_acls("share")
    assert clustermode.sent == [('cifs_share_access_control_get_iter', {'max_records': 65536, 'query': {'cifs_share_access_control': {'share': u'share'}}})]


seven_ret_value = {
        'cifs-share-acls': {
            'cifs-share-acl-info': {
                'share-name': "share1",
                'user-acl-info': {
                    "access-rights-info": [
                        {
                            'user-name': "user1",
                            'access-rights': "full_control",
                        }, {
                            'unix-group-name': "user2",
                            'access-rights': "r-x",
                        }
                    ],
                }
            }
        }
    }

cluster_ret_value = {
        'num-records': "2",
        'attributes-list': {
            'cifs-share-access-control': [{
                'permission': "full_control",
                'share': "share1",
                'user-or-group': "user1",
                # 'user-group-type': "windows"
            }, {
                'permission': "r-x",
                'share': "share1",
                'user-or-group': "user2",
                # 'user-group-type': "unix_user"
            }]
        }
    }


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_list_cifs_acls(mode, monkeypatch):
    # patching start method to get the tag, used as input param
    def get_tag(*args, **kwargs):
        return dict(
            netapp=dict(
                results=dict(
                    tag="12345"
                )
            )
        )
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._start_cifs_acls", get_tag)
    assert mode.list_cifs_acls("share")[0]['share_name'] == "share1"
    assert mode.list_cifs_acls("share")[0]['permission'] == "full_control"
    assert mode.list_cifs_acls("share")[0]['user_or_group'] == "user1"
    # assert nidhogg.list_cifs_acls("share")[0]['user_group_type'] == "windows"
    assert mode.list_cifs_acls("share")[1]['share_name'] == "share1"
    assert mode.list_cifs_acls("share")[1]['permission'] == "r-x"
    assert mode.list_cifs_acls("share")[1]['user_or_group'] == "user2"
    # assert nidhogg.list_cifs_acls("share")[1]['user_group_type'] == "unix_user"


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_delete_cifs_acls(mode, monkeypatch):
    # patching start method to get the tag, used as input param
    def get_tag(*args, **kwargs):
        return dict(
            netapp=dict(
                results=dict(
                    tag="12345"
                )
            )
        )
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._start_cifs_acls", get_tag)
    mode.delete_cifs_acls("share1")


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'num-records': "1",
        'attributes-list': {
            'cifs-share-access-control': {
                'permission': "full_control",
                'share': "share1",
                'user-or-group': "user1",
                # 'user-group-type': "windows"
            }
        }
    }),
    (SevenMode, {
        'cifs-share-acls': {
            'cifs-share-acl-info': {
                'share-name': "share1",
                'user-acl-info': {
                    "access-rights-info":
                    {
                        'user-name': "user1",
                        'access-rights': "full_control",
                    }
                }
            }
        }
    })
], indirect=True)
def test_list_cifs_acls_single_entry(mode, monkeypatch):
    # patching start method to get the tag, used as input param
    def get_tag(*args, **kwargs):
        return dict(
            netapp=dict(
                results=dict(
                    tag="12345"
                )
            )
        )
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._start_cifs_acls", get_tag)
    assert mode.list_cifs_acls("share")[0]['share_name'] == "share1"
    assert mode.list_cifs_acls("share")[0]['permission'] == "full_control"
    assert mode.list_cifs_acls("share")[0]['user_or_group'] == "user1"
    # assert nidhogg_single_entry.list_cifs_acls("share")[0]['user_group_type'] == "windows"


def test_list_cifs_acls_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.list_cifs_acls("my_share")


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'num-records': "0"}),
    (SevenMode, {})
], indirect=True)
def test_list_cifs_acls_no_entries(mode, monkeypatch):
    # patching start method to get the tag, used as input param
    def get_tag(*args, **kwargs):
        return dict(
            netapp=dict(
                results=dict(
                    tag="12345"
                )
            )
        )
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._start_cifs_acls", get_tag)
    assert [] == mode.list_cifs_acls("share1")
