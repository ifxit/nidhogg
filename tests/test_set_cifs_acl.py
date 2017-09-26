# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_set_cifs_acl_sevenmode_api(sevenmode):
    sevenmode.set_cifs_acl("hallo", "user", "Full Control")
    assert sevenmode.sent == [('cifs_share_ace_set', {'user_name': u'user', 'access_rights': u'Full Control', 'share_name': u'hallo'})]


def test_set_cifs_acl_clustermode_api_windows(clustermode):
    clustermode.set_cifs_acl("hallo", "Everyone", "read")
    assert clustermode.sent == [('cifs_share_access_control_create', {'user_or_group': u'Everyone', 'share': u'hallo', 'permission': u'read', 'user_group_type': u'windows'})]


def test_set_cifs_acl_clustermode_api_unix_user(clustermode):
    clustermode.set_cifs_acl("hallo", "ccplat", "read", False)
    assert clustermode.sent == [('cifs_share_access_control_create', {'user_or_group': u'ccplat', 'share': u'hallo', 'permission': u'read', 'user_group_type': u'unix_user'})]


def test_set_cifs_acl_clustermode_api_unix_group(clustermode):
    clustermode.set_cifs_acl("hallo", "ccplatg", "read", True)
    assert clustermode.sent == [('cifs_share_access_control_create', {'user_or_group': u'ccplatg', 'share': u'hallo', 'permission': u'read', 'user_group_type': u'unix_group'})]


def test_set_cifs_acl_sevenmode(sevenmode):
    sevenmode.set_cifs_acl("hallo", "group", "Full Control", True)
    sevenmode.set_cifs_acl("hallo", "user", "Full Control")


def test_set_cifs_acl_sevenmode_wrong_permission(sevenmode):
    with pytest.raises(NidhoggException):
        sevenmode.set_cifs_acl("hallo", "group", "wrong perm", True)


def test_set_cifs_acl_clustermode(clustermode):
    clustermode.set_cifs_acl("hallo", "user_or_group", "full_control")


def test_set_cifs_acl_clustermode_wrong_permission(clustermode):
    with pytest.raises(NidhoggException):
        clustermode.set_cifs_acl("hallo", "user_or_group", "asdf")


def test_set_cifs_acl_failed(allmodes_failed):
    # check needed because wrong permission is catched before
    if isinstance(allmodes_failed, ClusterMode):
        with pytest.raises(NidhoggException):
            allmodes_failed.set_cifs_acl("hallo", "user", "full_control")

    if isinstance(allmodes_failed, SevenMode):
        with pytest.raises(NidhoggException):
            allmodes_failed.set_cifs_acl("hallo", "user", "Full Control")
