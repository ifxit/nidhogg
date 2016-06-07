# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException


def test_source_volume_missing_1(sevenmode):
    """ Test missing input params. """
    with pytest.raises(NidhoggException):
        """ no source volume """
        sevenmode.update_snapmirror("dst_volume", source_filer="host")

    with pytest.raises(NidhoggException):
        """ no source filer """
        sevenmode.update_snapmirror("dst_volume", source_volume="vol")

    with pytest.raises(NidhoggException):
        """ no source filer """
        sevenmode.update_snapmirror("dst_volume", source_qtree="qtree")

    with pytest.raises(NidhoggException):
        """ no source filer """
        sevenmode.update_snapmirror("dst_volume", source_volume="vol", source_qtree="qtree")

    with pytest.raises(NidhoggException):
        """ no source volume """
        sevenmode.update_snapmirror("dst_volume", source_filer="host", source_qtree="qtree")

    with pytest.raises(NidhoggException):
        """ no src qtree """
        sevenmode.update_snapmirror("dst_volume", "dst_qtree", source_filer="host", source_volume="vol")

    with pytest.raises(NidhoggException):
        """ no dst qtree """
        sevenmode.update_snapmirror("dst_volume", source_filer="host", source_volume="vol", source_qtree="qtree")


def test_source_volume_missing_2(sevenmode):
    """ Test missing input params. """
    with pytest.raises(NidhoggException):
        sevenmode.update_snapmirror_with_snapshot("name", "dst_volume", source_filer="host")

    with pytest.raises(NidhoggException):
        sevenmode.update_snapmirror_with_snapshot("name", "dst_volume", source_volume="vol")

    with pytest.raises(NidhoggException):
        sevenmode.update_snapmirror_with_snapshot("name", "dst_volume", source_qtree="qtree")

    with pytest.raises(NidhoggException):
        sevenmode.update_snapmirror_with_snapshot("name", "dst_volume", source_volume="vol", source_qtree="qtree")

    with pytest.raises(NidhoggException):
        sevenmode.update_snapmirror_with_snapshot("name", "dst_volume", source_filer="host", source_qtree="qtree")

    with pytest.raises(NidhoggException):
        sevenmode.update_snapmirror_with_snapshot("name", "dst_volume", "dst_qtree", source_filer="host", source_volume="vol")

    with pytest.raises(NidhoggException):
        sevenmode.update_snapmirror_with_snapshot("name", "dst_volume", source_filer="host", source_volume="vol", source_qtree="qtree")
