# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.compatible import SnapmirrorStatus
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


cluster_snapmirror_status = {
    'break-failed-count': '0',
    'break-successful-count': '0',
    'destination-location': 'vihsdv996sm:t_data01_snapvault',
    'destination-volume': 't_data01_snapvault',
    'destination-volume-node': 'klusdnclu02-01',
    'destination-vserver': 'vihsdv996sm',
    'destination-vserver-uuid': 'e0e4f33d-f9ec-11e7-a832-00a098888ec6',
    'exported-snapshot': 'wohlfaro2',
    'exported-snapshot-timestamp': '1517400867',
    'is-constituent': 'false',
    'is-healthy': 'true',
    'lag-time': '182373',
    'last-transfer-duration': '10',
    'last-transfer-end-timestamp': '1517566113',
    'last-transfer-from': 'vihsdv996:t_data01_snapvault',
    'last-transfer-network-compression-ratio': '1:1',
    'last-transfer-size': '31983664',
    'last-transfer-type': 'update',
    'max-transfer-rate': '50000',
    'mirror-state': 'snapmirrored',
    'newest-snapshot': 'wohlfaro2',
    'newest-snapshot-timestamp': '1517400867',
    'opmask': '18446744073709551615',
    'policy': 'XDP_DBtest',
    'policy-type': 'vault',
    'relationship-control-plane': 'v2',
    'relationship-group-type': 'none',
    'relationship-id': '42c9c03f-05b3-11e8-86a3-00a098881a8d',
    'relationship-status': 'idle',
    'relationship-type': 'vault',
    'resync-failed-count': '0',
    'resync-successful-count': '0',
    'source-location': 'vihsdv996:t_data01_snapvault',
    'source-volume': 't_data01_snapvault',
    'source-vserver': 'vihsdv996',
    'source-vserver-uuid': '77901708-31f1-11e5-aade-00a0988309c0',
    'total-transfer-bytes': '10371917440',
    'total-transfer-time-secs': '566',
    'update-failed-count': '0',
    'update-successful-count': '13',
    'vserver': 'vihsdv996sm',
}

cluster_snapmirror_status_result = {
    'base_snapshot': None,
    'break_failed_count': u'0',
    'break_successful_count': u'0',
    'contents': None,
    'current_transfer_error': None,
    'current_transfer_type': None,
    'destination_location': u'vihsdv996sm:t_data01_snapvault',
    'destination_volume': u't_data01_snapvault',
    'destination_volume_node': u'klusdnclu02-01',
    'destination_vserver': u'vihsdv996sm',
    'destination_vserver_uuid': u'e0e4f33d-f9ec-11e7-a832-00a098888ec6',
    'exported_snapshot': u'wohlfaro2',
    'exported_snapshot_timestamp': u'1517400867',
    'inodes_replicated': None,
    'is_constituent': u'false',
    'is_healthy': u'true',
    'lag_time': u'182373',
    'last_transfer_duration': u'10',
    'last_transfer_end_timestamp': u'1517566113',
    'last_transfer_from': u'vihsdv996:t_data01_snapvault',
    'last_transfer_network_compression_ratio': u'1:1',
    'last_transfer_size': u'31983664',
    'last_transfer_type': u'update',
    'max_transfer_rate': u'50000',
    'mirror_state': u'snapmirrored',
    'mirror_timestamp': None,
    'newest_snapshot': u'wohlfaro2',
    'newest_snapshot_timestamp': u'1517400867',
    'opmask': u'18446744073709551615',
    'policy': u'XDP_DBtest',
    'policy_type': u'vault',
    'relationship_control_plane': u'v2',
    'relationship_group_type': u'none',
    'relationship_id': u'42c9c03f-05b3-11e8-86a3-00a098881a8d',
    'relationship_status': u'idle',
    'relationship_type': u'vault',
    'replication_ops': None,
    'resync_failed_count': u'0',
    'resync_successful_count': u'0',
    'snapmirror_status': u'idle',
    'source_location': u'vihsdv996:t_data01_snapvault',
    'source_volume': u't_data01_snapvault',
    'source_vserver': u'vihsdv996',
    'source_vserver_uuid': u'77901708-31f1-11e5-aade-00a0988309c0',
    'state': None,
    'status': None,
    'total_transfer_bytes': u'10371917440',
    'total_transfer_time_secs': u'566',
    'transfer_progress': None,
    'update_failed_count': u'0',
    'update_successful_count': u'13',
    'vserver': u'vihsdv996sm',
}


def test_get_snapmirror_status_sevenmode_api_1(sevenmode):
    sevenmode.get_snapmirror_status("volume")
    assert sevenmode.sent == [(
        'snapmirror_get_status',
        {'location': "volume"}
    )]


def test_get_snapmirror_status_sevenmode_api_2(sevenmode):
    sevenmode.get_snapmirror_status("volume", "qtree")
    assert sevenmode.sent == [(
        'snapmirror_get_status',
        {'location': "/vol/volume/qtree"}
    )]


def test_get_snapmirror_status_sevenmode_api_3(sevenmode):
    sevenmode.get_snapmirror_status()
    assert sevenmode.sent == [(
        'snapmirror_get_status',
        {}
    )]


def test_get_snapmirror_status_cluster_api_1(clustermode):
    clustermode.get_snapmirror_status()
    assert clustermode.sent == [(
        'snapmirror_get_iter',
        {}
    )]


def test_get_snapmirror_status_cluster_api_2(clustermode):
    clustermode.get_snapmirror_status("volume")
    assert clustermode.sent == [(
        'snapmirror_get_iter',
        {
            'query': {
                'snapmirror_info': {
                    'destination_location': u'my:volume'
                }
            },
            'max_records': 65536
        }
    )]


@pytest.mark.parametrize('mode', [
    (SevenMode, {
        'is-available': "true",
        'snapmirror-status': {
            'snapmirror-status-info': {
                'status': u'idle',
                'base-snapshot': u'filer13(0536965720)_sm_filer48_userhome_LCP.1820',
                'source-location': u'filer48:userhome_LCP',
                'mirror-timestamp': u'1459751523',
                'current-transfer-error': None,
                'current-transfer-type': None,
                'replication-ops': None,
                'inodes-replicated': None,
                'transfer-progress': u'0',
                'contents': u'Replica',
                'last-transfer-from': u'filer48:userhome_LCP',
                'last-transfer-duration': u'7',
                'last-transfer-size': u'1044',
                'state': u'snapmirrored',
                'lag-time': u'469',
                'last-transfer-type': u'scheduled',
                'destination-location': u'filer13:sm_filer48_userhome_LCP'
            }
        }
    })
], indirect=True)
def test_get_snapmirror_status_single_entry_sevenmode(mode):
    assert mode.get_snapmirror_status("volume") == [
        {
            'base_snapshot': u'filer13(0536965720)_sm_filer48_userhome_LCP.1820',
            'break_failed_count': None,
            'break_successful_count': None,
            'contents': u'Replica',
            'current_transfer_error': None,
            'current_transfer_type': None,
            'destination_location': u'filer13:sm_filer48_userhome_LCP',
            'destination_volume': None,
            'destination_volume_node': None,
            'destination_vserver': None,
            'destination_vserver_uuid': None,
            'exported_snapshot': None,
            'exported_snapshot_timestamp': None,
            'inodes_replicated': None,
            'is_constituent': None,
            'is_healthy': None,
            'lag_time': u'469',
            'last_transfer_duration': u'7',
            'last_transfer_end_timestamp': None,
            'last_transfer_from': u'filer48:userhome_LCP',
            'last_transfer_network_compression_ratio': None,
            'last_transfer_size': u'1044',
            'last_transfer_type': u'scheduled',
            'max_transfer_rate': None,
            'mirror_state': None,
            'mirror_timestamp': u'1459751523',
            'newest_snapshot': None,
            'newest_snapshot_timestamp': None,
            'opmask': None,
            'policy': None,
            'policy_type': None,
            'relationship_control_plane': None,
            'relationship_group_type': None,
            'relationship_id': None,
            'relationship_status': None,
            'relationship_type': None,
            'replication_ops': None,
            'resync_failed_count': None,
            'resync_successful_count': None,
            'snapmirror_status': u'idle',
            'source_location': u'filer48:userhome_LCP',
            'source_volume': None,
            'source_vserver': None,
            'source_vserver_uuid': None,
            'state': u'snapmirrored',
            'status': u'idle',
            'total_transfer_bytes': None,
            'total_transfer_time_secs': None,
            'transfer_progress': u'0',
            'update_failed_count': None,
            'update_successful_count': None,
            'vserver': None,
        },
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'snapmirror-info': cluster_snapmirror_status
        },
        'num-records': '1'
    })
], indirect=True)
def test_get_snapmirror_status_single_entry_clustermode(mode):
    assert mode.get_snapmirror_status("volume") == [
        cluster_snapmirror_status_result
    ]


@pytest.mark.parametrize('mode', [
    (SevenMode, {
        'is-available': "true",
        'snapmirror-status': {
            'snapmirror-status-info': [{
                'status': u'idle',
                'base-snapshot': u'filer13(0536965720)_sm_filer48_userhome_LCP.1820',
                'source-location': u'filer48:userhome_LCP',
                'mirror-timestamp': u'1459751523',
                'current-transfer-error': None,
                'current-transfer-type': None,
                'replication-ops': None,
                'inodes-replicated': None,
                'transfer-progress': u'0',
                'contents': u'Replica',
                'last-transfer-from': u'filer48:userhome_LCP',
                'last-transfer-duration': u'7',
                'last-transfer-size': u'1044',
                'state': u'snapmirrored',
                'lag-time': u'469',
                'last-transfer-type': u'scheduled',
                'destination-location': u'filer13:sm_filer48_userhome_LCP'
            }, {
                'status': u'idle',
                'base-snapshot': u'filer13(0536965720)_sm_filer48_userhome_LCP.1920',
                'source-location': u'filer47:userhome_LCP',
                'mirror-timestamp': u'1459751523',
                'current-transfer-error': None,
                'current-transfer-type': None,
                'replication-ops': None,
                'inodes-replicated': None,
                'transfer-progress': u'0',
                'contents': u'Replica',
                'last-transfer-from': u'filer47:userhome_LCP',
                'last-transfer-duration': u'7',
                'last-transfer-size': u'1044',
                'state': u'snapmirrored',
                'lag-time': u'469',
                'last-transfer-type': u'scheduled',
                'destination-location': u'filer13:sm_filer48_userhome_LCP'
            }]
        }
    })
], indirect=True)
def test_get_snapmirror_status_sevenmode(mode):
    assert mode.get_snapmirror_status("volume") == [
        {
            'base_snapshot': u'filer13(0536965720)_sm_filer48_userhome_LCP.1820',
            'break_failed_count': None,
            'break_successful_count': None,
            'contents': u'Replica',
            'current_transfer_error': None,
            'current_transfer_type': None,
            'destination_location': u'filer13:sm_filer48_userhome_LCP',
            'destination_volume': None,
            'destination_volume_node': None,
            'destination_vserver': None,
            'destination_vserver_uuid': None,
            'exported_snapshot': None,
            'exported_snapshot_timestamp': None,
            'inodes_replicated': None,
            'is_constituent': None,
            'is_healthy': None,
            'lag_time': u'469',
            'last_transfer_duration': u'7',
            'last_transfer_end_timestamp': None,
            'last_transfer_from': u'filer48:userhome_LCP',
            'last_transfer_network_compression_ratio': None,
            'last_transfer_size': u'1044',
            'last_transfer_type': u'scheduled',
            'max_transfer_rate': None,
            'mirror_state': None,
            'mirror_timestamp': u'1459751523',
            'newest_snapshot': None,
            'newest_snapshot_timestamp': None,
            'opmask': None,
            'policy': None,
            'policy_type': None,
            'relationship_control_plane': None,
            'relationship_group_type': None,
            'relationship_id': None,
            'relationship_status': None,
            'relationship_type': None,
            'replication_ops': None,
            'resync_failed_count': None,
            'resync_successful_count': None,
            'snapmirror_status': u'idle',
            'source_location': u'filer48:userhome_LCP',
            'source_volume': None,
            'source_vserver': None,
            'source_vserver_uuid': None,
            'state': u'snapmirrored',
            'status': u'idle',
            'total_transfer_bytes': None,
            'total_transfer_time_secs': None,
            'transfer_progress': u'0',
            'update_failed_count': None,
            'update_successful_count': None,
            'vserver': None,
        }, {
            'base_snapshot': u'filer13(0536965720)_sm_filer48_userhome_LCP.1920',
            'break_failed_count': None,
            'break_successful_count': None,
            'contents': u'Replica',
            'current_transfer_error': None,
            'current_transfer_type': None,
            'destination_location': u'filer13:sm_filer48_userhome_LCP',
            'destination_volume': None,
            'destination_volume_node': None,
            'destination_vserver': None,
            'destination_vserver_uuid': None,
            'exported_snapshot': None,
            'exported_snapshot_timestamp': None,
            'inodes_replicated': None,
            'is_constituent': None,
            'is_healthy': None,
            'lag_time': u'469',
            'last_transfer_duration': u'7',
            'last_transfer_end_timestamp': None,
            'last_transfer_from': u'filer47:userhome_LCP',
            'last_transfer_network_compression_ratio': None,
            'last_transfer_size': u'1044',
            'last_transfer_type': u'scheduled',
            'max_transfer_rate': None,
            'mirror_state': None,
            'mirror_timestamp': u'1459751523',
            'newest_snapshot': None,
            'newest_snapshot_timestamp': None,
            'opmask': None,
            'policy': None,
            'policy_type': None,
            'relationship_control_plane': None,
            'relationship_group_type': None,
            'relationship_id': None,
            'relationship_status': None,
            'relationship_type': None,
            'replication_ops': None,
            'resync_failed_count': None,
            'resync_successful_count': None,
            'snapmirror_status': u'idle',
            'source_location': u'filer47:userhome_LCP',
            'source_volume': None,
            'source_vserver': None,
            'source_vserver_uuid': None,
            'state': u'snapmirrored',
            'status': u'idle',
            'total_transfer_bytes': None,
            'total_transfer_time_secs': None,
            'transfer_progress': u'0',
            'update_failed_count': None,
            'update_successful_count': None,
            'vserver': None,
        },
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'snapmirror-info': [
                cluster_snapmirror_status,
                cluster_snapmirror_status
            ],
        },
        'num-records': '2'
    })
], indirect=True)
def test_get_snapmirror_status_clustermode(mode):
    assert mode.get_snapmirror_status("volume") == [
        cluster_snapmirror_status_result,
        cluster_snapmirror_status_result
    ]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'num-records': '0'
    }),
    (SevenMode, {
        'is-available': "true"
    }),
], indirect=True)
def test_get_snapmirror_status_empty_list(mode):
    assert mode.get_snapmirror_status() == []


def test_item_to_snapmirror_status_all(sevenmode):
    item = {
        'source-location': "-",
        'destination-location': "-",
        'last-transfer-from': "-",
        'last-transfer-size': "-",
        'last-transfer-duration': "-",
        'transfer-progress': "-",
        'lag-time': "-",
        'mirror-timestamp': "-",
        'contents': "-",
        'status': "-",
        'state': "-",
        # optional
        'base-snapshot': "-",
        'current-transfer-error': "-",
        'current-transfer-type': "-",
        'inodes-replicated': "-",
        'last-transfer-type': "-",
        'replication-ops': "-",
    }
    status = SnapmirrorStatus(**{
        'base_snapshot': u'-',
        'break_failed_count': None,
        'break_successful_count': None,
        'contents': u'-',
        'current_transfer_error': u'-',
        'current_transfer_type': u'-',
        'destination_location': u'-',
        'destination_volume': None,
        'destination_volume_node': None,
        'destination_vserver': None,
        'destination_vserver_uuid': None,
        'exported_snapshot': None,
        'exported_snapshot_timestamp': None,
        'inodes_replicated': u'-',
        'is_constituent': None,
        'is_healthy': None,
        'lag_time': u'-',
        'last_transfer_duration': u'-',
        'last_transfer_end_timestamp': None,
        'last_transfer_from': u'-',
        'last_transfer_network_compression_ratio': None,
        'last_transfer_size': u'-',
        'last_transfer_type': u'-',
        'max_transfer_rate': None,
        'mirror_state': None,
        'mirror_timestamp': u'-',
        'newest_snapshot': None,
        'newest_snapshot_timestamp': None,
        'opmask': None,
        'policy': None,
        'policy_type': None,
        'relationship_control_plane': None,
        'relationship_group_type': None,
        'relationship_id': None,
        'relationship_status': None,
        'relationship_type': None,
        'replication_ops': u'-',
        'resync_failed_count': None,
        'resync_successful_count': None,
        'snapmirror_status': u'-',
        'source_location': u'-',
        'source_volume': None,
        'source_vserver': None,
        'source_vserver_uuid': None,
        'state': u'-',
        'status': u'-',
        'total_transfer_bytes': None,
        'total_transfer_time_secs': None,
        'transfer_progress': u'-',
        'update_failed_count': None,
        'update_successful_count': None,
        'vserver': None,
    })
    assert status == sevenmode._item_to_snapmirrorstatus(item)
