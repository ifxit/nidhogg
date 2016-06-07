# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_list_qtrees_sevenmode_api(sevenmode):
    sevenmode.list_qtrees("asdf")
    assert sevenmode.sent == [('qtree_list', {'volume': 'asdf'})]


def test_list_qtrees_clustermode_api(clustermode):
    clustermode.list_qtrees("asdf")
    assert clustermode.sent == [('qtree_list_iter', {'max_records': 65536, 'query': {'qtree_info': {'volume': "asdf"}}})]


seven_ret_value = {
    "qtrees": {
        "qtree-info": [
            {
                'qtree': "user",
                'status': "normal",
                'security-style': "mixed"
            }, {
                'qtree': "hallo",
                'status': "normal",
                'security-style': "unix"
            }
        ],
    }
}
cluster_ret_value = {
    'attributes-list': {
        'qtree-info': [{
            'qtree': "user",
            'status': "normal",
            'security-style': "mixed"
        }, {
            'qtree': "hallo",
            'status': "normal",
            'security-style': "unix"
        }],
    },
    'num-records': 2,
}


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_list_qtrees(mode):
    assert mode.list_qtrees("asdf") == \
        [{"qtree": "user", "status": "normal", 'security_style': "mixed"},
         {"qtree": "hallo", "status": "normal", 'security_style': "unix"}]


@pytest.mark.parametrize('mode', [
    (ClusterMode, cluster_ret_value),
    (SevenMode, seven_ret_value)
], indirect=True)
def test_exists_qtree(mode):
    assert True is mode.exists_qtree("asdf", "hallo")
    assert False is mode.exists_qtree("asdf", "servus")


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'attributes-list': {
            'qtree-info': {
                'qtree': "user",
                'status': "normal",
                'security-style': "mixed"
            }
        },
        'num-records': 1,
    }),
    (SevenMode, {
        "qtrees": {
            "qtree-info": {
                'qtree': "user",
                'status': "normal",
                'security-style': "mixed"
            }
        }
    })
], indirect=True)
def test_list_qtrees_single_entry(mode):
    assert mode.list_qtrees("asdf") == \
        [{"qtree": "user", "status": "normal", 'security_style': "mixed"}]


def test_list_qtrees_failed(allmodes_failed):
    with pytest.raises(NidhoggException):
        allmodes_failed.list_qtrees("asdf")


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        'status': "passed",
        'num-records': '0'
    }),
    (SevenMode, {})
], indirect=True)
def test_list_qtrees_no_entries(mode):
    assert mode.list_qtrees("asdf") == []
