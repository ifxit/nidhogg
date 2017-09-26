# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException


def test_create_qtree(allmodes):
    allmodes.create_qtree("vol", "haha", "000")
    assert allmodes.sent == [('qtree_create', {'volume': 'vol', 'qtree': 'haha', 'mode': "000"})]


def test_create_qtree_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.create_qtree("volume1", "qtree2")
