# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


@pytest.fixture
def patch_start_cifs_shares(request, monkeypatch):
    # patching start method to get the tag, used as input param
    def get_tag(*args, **kwargs):
        return dict(
            netapp=dict(
                results=dict(
                    tag="12345"
                )
            )
        )
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._start_cifs_shares", get_tag)


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'cifs-share': [{
                'path': "/vol/foobar",
                'share-name': "foobar$"
            }, {
                'path': "/vol/xxx/foobar",
                'share-name': "foobar"
            }],
        },
        'num-records': 2,
    }),
    (SevenMode, {
        "cifs-shares": {
            "cifs-share-info": [
                {
                    'mount-point': "/vol/foobar",
                    'share-name': "foobar$"
                }, {
                    'mount-point': "/vol/xxx/foobar",
                    'share-name': "foobar"
                }
            ],
        },
        'records': 2
    })
], indirect=True)
def test_list_cifs_shares(mode, patch_start_cifs_shares):
    assert mode.list_cifs_shares() == \
        [{"path": "/vol/foobar", "share_name": "foobar$"},
         {"path": "/vol/xxx/foobar", "share_name": "foobar"}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'cifs-share': {
                'path': "/vol/foobar",
                'share-name': "foobar$"
            }
        },
        'num-records': 1,
    }),
    (SevenMode, {
        "cifs-shares": {
            "cifs-share-info": {
                'mount-point': "/vol/foobar",
                'share-name': "foobar$"
            },
        },
        'records': 1
    })
], indirect=True)
def test_list_cifs_shares_single_entry(mode, patch_start_cifs_shares):
    assert mode.list_cifs_shares() == \
        [{"path": "/vol/foobar", "share_name": "foobar$"}]


def test_list_cifs_shares_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.list_cifs_shares()


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'status': "passed",
        'num-records': '0'
    }),
    (SevenMode, {
        'records': 0
    })
], indirect=True)
def test_list_cifs_shares_no_entries(mode, patch_start_cifs_shares):
    assert mode.list_cifs_shares() == []
