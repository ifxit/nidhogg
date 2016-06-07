# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException


def test_delete_qtree_api(allmodes):
    allmodes.delete_qtree("vol", "haha")
    assert allmodes.sent == [('qtree_delete', {'qtree': '/vol/vol/haha', 'force': "False"})]


def test_delete_qtree(allmodes):
    allmodes.delete_qtree("vol", "haha")


def test_delete_qtree_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.delete_qtree("volume1", "qtree2")
