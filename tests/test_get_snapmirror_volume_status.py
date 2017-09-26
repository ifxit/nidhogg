# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.compatible import SnapmirrorVolumeStatus
from nidhogg.sevenmode import SevenMode


def test_get_snapmirror_volume_status_sevenmode_api(sevenmode):
    sevenmode.get_snapmirror_volume_status("volume")
    assert sevenmode.sent == [(
        'snapmirror_get_volume_status',
        {'volume': "volume"}
    )]


@pytest.mark.parametrize('mode', [
    (SevenMode, {
        'is-source': "true",
        'is-destination': "false",
        'is-transfer-in-progress': "true",
        'is-transfer-broken': "false",
    })
], indirect=True)
def test_get_snapmirror_volume_status(mode):
    assert mode.get_snapmirror_volume_status("volume") == dict(
        is_source=True,
        is_destination=False,
        is_transfer_in_progress=True,
        is_transfer_broken=False,
    )


def test_item_to_snapmirrorvolumestatus_false(sevenmode):
    item = {
        'is-source': "-",
        'is-destination': "-",
        'is-transfer-in-progress': "-",
        'is-transfer-broken': "-",
    }
    status = SnapmirrorVolumeStatus(
        is_source=False,
        is_destination=False,
        is_transfer_in_progress=False,
        is_transfer_broken=False,
    )
    assert status == sevenmode._item_to_snapmirrorvolumestatus(item)


def test_item_to_snapmirrorvolumestatus_true(sevenmode):
    item = {
        'is-source': "true",
        'is-destination': "true",
        'is-transfer-in-progress': "true",
        'is-transfer-broken': "true",
    }
    status = SnapmirrorVolumeStatus(
        is_source=True,
        is_destination=True,
        is_transfer_in_progress=True,
        is_transfer_broken=True,
    )
    assert status == sevenmode._item_to_snapmirrorvolumestatus(item)
