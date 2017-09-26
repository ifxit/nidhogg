# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.compatible import SnapmirrorStatus
from nidhogg.sevenmode import SevenMode


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
def test_get_snapmirror_status_single_entry(mode):
    assert mode.get_snapmirror_status("volume") == [
        dict(
            source_location="filer48:userhome_LCP",
            destination_location="filer13:sm_filer48_userhome_LCP",
            last_transfer_from="filer48:userhome_LCP",
            last_transfer_size="1044",
            last_transfer_duration="7",
            transfer_progress="0",
            lag_time="469",
            mirror_timestamp="1459751523",
            contents="Replica",
            status="idle",
            state="snapmirrored",
            base_snapshot="filer13(0536965720)_sm_filer48_userhome_LCP.1820",
            current_transfer_error=None,
            current_transfer_type=None,
            inodes_replicated=None,
            last_transfer_type="scheduled",
            replication_ops=None
        ),
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
def test_get_snapmirror_status(mode):
    assert mode.get_snapmirror_status("volume") == [
        dict(
            source_location="filer48:userhome_LCP",
            destination_location="filer13:sm_filer48_userhome_LCP",
            last_transfer_from="filer48:userhome_LCP",
            last_transfer_size="1044",
            last_transfer_duration="7",
            transfer_progress="0",
            lag_time="469",
            mirror_timestamp="1459751523",
            contents="Replica",
            status="idle",
            state="snapmirrored",
            base_snapshot="filer13(0536965720)_sm_filer48_userhome_LCP.1820",
            current_transfer_error=None,
            current_transfer_type=None,
            inodes_replicated=None,
            last_transfer_type="scheduled",
            replication_ops=None
        ), dict(
            source_location="filer47:userhome_LCP",
            destination_location="filer13:sm_filer48_userhome_LCP",
            last_transfer_from="filer47:userhome_LCP",
            last_transfer_size="1044",
            last_transfer_duration="7",
            transfer_progress="0",
            lag_time="469",
            mirror_timestamp="1459751523",
            contents="Replica",
            status="idle",
            state="snapmirrored",
            base_snapshot="filer13(0536965720)_sm_filer48_userhome_LCP.1920",
            current_transfer_error=None,
            current_transfer_type=None,
            inodes_replicated=None,
            last_transfer_type="scheduled",
            replication_ops=None
        ),
    ]


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
    status = SnapmirrorStatus(
        source_location="-",
        destination_location="-",
        last_transfer_from="-",
        last_transfer_size="-",
        last_transfer_duration="-",
        transfer_progress="-",
        lag_time="-",
        mirror_timestamp="-",
        contents="-",
        status="-",
        state="-",
        base_snapshot="-",
        current_transfer_error="-",
        current_transfer_type="-",
        inodes_replicated="-",
        last_transfer_type="-",
        replication_ops="-"
    )
    assert status == sevenmode._item_to_snapmirrorstatus(item)
