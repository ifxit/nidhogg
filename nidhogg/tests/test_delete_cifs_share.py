# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException


def test_delete_cifs_share_api(allmodes):
    allmodes.delete_cifs_share("share")
    assert allmodes.sent == [('cifs_share_delete', {'share_name': 'share'})]


def test_delete_cifs_share(allmodes):
    allmodes.delete_cifs_share("share")


def test_delete_cifs_share_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.delete_cifs_share("share")
