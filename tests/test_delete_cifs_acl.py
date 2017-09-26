# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException


def test_delete_cifs_acl_user_sevenmode_api(sevenmode):
    sevenmode.delete_cifs_acl("hallo", "user")
    assert sevenmode.sent == [('cifs_share_ace_delete', {'is_unixgroup': u'false', 'user_name': u'user', 'share_name': u'hallo'})]


def test_delete_cifs_acl_group_sevenmode_api(sevenmode):
    sevenmode.delete_cifs_acl("hallo", "user", True)
    assert sevenmode.sent == [('cifs_share_ace_delete', {'is_unixgroup': u'true', 'unix_group_name': u'user', 'share_name': u'hallo'})]


def test_delete_cifs_acl_clustermode_api(clustermode):
    clustermode.delete_cifs_acl("hallo", "user_or_group")
    assert clustermode.sent == [('cifs_share_access_control_delete', {'user_or_group': u'user_or_group', 'share': u'hallo'})]


def test_delete_cifs_acl(allmodes):
    allmodes.delete_cifs_acl("share", "user_or_group")


def test_delete_cifs_acl_clustermode_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.delete_cifs_acl("share", "user_or_group")
