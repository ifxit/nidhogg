# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def test_create_snapshot_api(allmodes):
    allmodes.create_snapshot("vol", "haha")
    assert allmodes.sent == [('snapshot_create', {'volume': 'vol', 'snapshot': 'haha'})]


def test_create_snapshot_wit_label_api(clustermode):
    clustermode.create_snapshot("volumy", "snappy", "backup")
    assert clustermode.sent == [('snapshot_create', {
        'volume': 'volumy',
        'snapshot': 'snappy',
        'snapmirror_label': "backup",
    })]
