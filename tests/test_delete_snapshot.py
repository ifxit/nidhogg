# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


@pytest.mark.parametrize('mode', [
    (ClusterMode, {}),
    (SevenMode, {})
], indirect=True)
def test_delete_snapshot(mode):
    assert mode.delete_snapshot("vol", "haha") == {'netapp': {'results': {}}}


def test_delete_snapshot_api(allmodes):
    allmodes.delete_snapshot("vol", "haha")
    assert allmodes.sent == [('snapshot_delete', {'volume': 'vol', 'snapshot': 'haha'})]
