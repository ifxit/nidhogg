# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.clustermode import ClusterMode


cluster_snapmirror_destination_info = {
    'destination-location': u'filer996sm:t_data01_snapvault',
    'destination-volume': u't_data01_snapvault',
    'destination-vserver': u'filer996sm',
    'is-constituent': u'false',
    'policy-type': u'vault',
    'relationship-group-type': u'none',
    'relationship-id': u'42c9c03f-05b3-11e8-86a3-00a098881a8d',
    'relationship-status': u'idle',
    'relationship-type': u'vault',
    'source-location': u'filer996:t_data01_snapvault',
    'source-volume': u't_data01_snapvault',
    'source-volume-node': u'vihsdnclu98-01',
    'source-vserver': u'filer996',
}


cluster_snapmirror_destination_info_result = {
    'destination_location': u'filer996sm:t_data01_snapvault',
    'destination_volume': u't_data01_snapvault',
    'destination_vserver': u'filer996sm',
    'is_constituent': u'false',
    'policy_type': u'vault',
    'relationship_group_type': u'none',
    'relationship_id': u'42c9c03f-05b3-11e8-86a3-00a098881a8d',
    'relationship_status': u'idle',
    'relationship_type': u'vault',
    'source_location': u'filer996:t_data01_snapvault',
    'source_volume': u't_data01_snapvault',
    'source_volume_node': u'vihsdnclu98-01',
    'source_vserver': u'filer996',
}


def test_list_snapmirror_destinatons_api_1(clustermode):
    clustermode.list_snapmirror_destinations()
    assert clustermode.sent == [(
        'snapmirror_get_destination_iter',
        {}
    )]


def test_list_snapmirror_destinatons_api_2(clustermode):
    clustermode.list_snapmirror_destinations("volume")
    assert clustermode.sent == [(
        'snapmirror_get_destination_iter',
        {
            'query': {
                'snapmirror_destination_info': {
                    'source_location': u'my:volume'
                }
            },
            'max_records': 65536
        }
    )]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "is-clustered": "true",
        'attributes-list': {
            'snapmirror-destination-info': [
                cluster_snapmirror_destination_info,
                cluster_snapmirror_destination_info
            ],
        },
        'num-records': '2'
    })
], indirect=True)
def test_list_snapmirror_destinatons_multiple(mode):
    assert mode.list_snapmirror_destinations() == [
        cluster_snapmirror_destination_info_result,
        cluster_snapmirror_destination_info_result
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "is-clustered": "true",
        'attributes-list': {
            'snapmirror-destination-info': cluster_snapmirror_destination_info
        },
        'num-records': '1'
    })
], indirect=True)
def test_list_snapmirror_destinatons_single_entry(mode):
    assert mode.list_snapmirror_destinations() == [
        cluster_snapmirror_destination_info_result
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'num-records': '0'
    }),
], indirect=True)
def test_list_snapmirror_destinatons_empty_list(mode):
    assert mode.list_snapmirror_destinations() == []
