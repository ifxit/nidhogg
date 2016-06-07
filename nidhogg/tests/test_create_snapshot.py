# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


@pytest.mark.parametrize('mode', [
    (ClusterMode, {}),
    (SevenMode, {})
], indirect=True)
def test_create_snapshot(mode):
    assert mode.create_snapshot("vol", "haha") == {'netapp': {'results': {}}}


def test_create_snapshot_api(allmodes):
    allmodes.create_snapshot("vol", "haha")
    assert allmodes.sent == [('snapshot_create', {'volume': 'vol', 'snapshot': 'haha'})]
