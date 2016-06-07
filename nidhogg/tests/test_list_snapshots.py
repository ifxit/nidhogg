# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_list_snapshots_sevenmode_api(sevenmode):
    sevenmode.list_snapshots("vol")
    assert sevenmode.sent == [('snapshot_list_info', {'target_name': 'vol', 'target_type': 'volume'})]


def test_list_snapshots_clustermode_api(clustermode):
    clustermode.list_snapshots("vol")
    assert clustermode.sent == [('snapshot_get_iter', {'max_records': 65536, 'query': {'snapshot_info': {'volume': 'vol'}}})]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "attributes-list": {
            "snapshot-info": [{
                "access-time": "1407017701",
                "busy": "false",
                "cumulative-percentage-of-total-blocks": "0",
                "cumulative-percentage-of-used-blocks": "86",
                "cumulative-total": "1812",
                "is-7-mode-snapshot": "false",
                "is-constituent-snapshot": "false",
                "name": "name1",
                "percentage-of-total-blocks": "0",
                "percentage-of-used-blocks": "44",
                "snapmirror-label": "weekly",
                "snapshot-instance-uuid": "b1b89b8c-4713-4d7c-a43c-d7364547488f",
                "snapshot-version-uuid": "b1b89b8c-4713-4d7c-a43c-d7364547488f",
                "state": "valid",
                "total": "240",
                "volume": "sdv001_vol0",
                "volume-provenance-uuid": "56d4e5f7-4048-4b38-8a0a-c5f1b3a5b576",
                "vserver": "filername",
            }, {
                "access-time": "1407017701",
                "busy": "false",
                "cumulative-percentage-of-total-blocks": "0",
                "cumulative-percentage-of-used-blocks": "86",
                "cumulative-total": "1812",
                "is-7-mode-snapshot": "false",
                "is-constituent-snapshot": "false",
                "name": "name2",
                "percentage-of-total-blocks": "0",
                "percentage-of-used-blocks": "44",
                "snapmirror-label": "weekly",
                "snapshot-instance-uuid": "b1b89b8c-4713-4d7c-a43c-d7364547488f",
                "snapshot-version-uuid": "b1b89b8c-4713-4d7c-a43c-d7364547488f",
                "state": "valid",
                "total": "240",
                "volume": "sdv001_vol0",
                "volume-provenance-uuid": "56d4e5f7-4048-4b38-8a0a-c5f1b3a5b576",
                "vserver": "filername",
            }]
        },
        'num-records': "2"
    }),
    (SevenMode, {
        'snapshots': {
            'snapshot-info': [{
                'name': "name1",
            }, {
                'name': "name2",
            }]
        }
    })
], indirect=True)
def test_list_snapshots(mode):
    assert mode.list_snapshots("vol") == [{"name": "name1"}, {"name": "name2"}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "attributes-list": {
            "snapshot-info": {
                "access-time": "1407017701",
                "busy": "false",
                "cumulative-percentage-of-total-blocks": "0",
                "cumulative-percentage-of-used-blocks": "86",
                "cumulative-total": "1812",
                "is-7-mode-snapshot": "false",
                "is-constituent-snapshot": "false",
                "name": "name1",
                "percentage-of-total-blocks": "0",
                "percentage-of-used-blocks": "44",
                "snapmirror-label": "weekly",
                "snapshot-instance-uuid": "b1b89b8c-4713-4d7c-a43c-d7364547488f",
                "snapshot-version-uuid": "b1b89b8c-4713-4d7c-a43c-d7364547488f",
                "state": "valid",
                "total": "240",
                "volume": "sdv001_vol0",
                "volume-provenance-uuid": "56d4e5f7-4048-4b38-8a0a-c5f1b3a5b576",
                "vserver": "filername",
            }
        },
        'num-records': "1"
    }),
    (SevenMode, {
        'snapshots': {
            'snapshot-info': {
                'name': "name1",
            }
        }
    })
], indirect=True)
def test_list_snapshots_single_entry(mode):
    assert mode.list_snapshots("vol") == [{"name": "name1"}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'num-records': '0'
    }),
    (SevenMode, {})
], indirect=True)
def test_list_snapshots_no_entries(mode):
    assert mode.list_snapshots("vol") == []
