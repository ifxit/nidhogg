# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nidhogg.core import underline_to_dash


def test_underline_to_dash_empty_dict():
    in_dict = {}
    out_dict = {}
    assert underline_to_dash(in_dict) == out_dict


def test_underline_to_dash_flat_dict():
    in_dict = dict(
        na_me="Olga",
        ag_e="old",
        prof_ession="Master of red light district"
    )
    out_dict = {
        'na-me': "Olga",
        'ag-e': "old",
        'prof-ession': "Master of red light district"
    }
    assert underline_to_dash(in_dict) == out_dict


def test_underline_to_dash_deep_dict():
    in_dict = {
        "clustermode": {
            '@status': "passed",
            'attributes_list': {
                'quota_entry': {
                    'disk_limit': "1236",
                    'file_limit': '-',
                },
                'num_records': 1
            }
        }
    }
    out_dict = {
        "clustermode": {
            '@status': "passed",
            'attributes-list': {
                'quota-entry': {
                    'disk-limit': "1236",
                    'file-limit': '-',
                },
                'num-records': 1
            }
        }
    }
    assert underline_to_dash(in_dict) == out_dict


def test_underline_to_dash_deep_dict_with_list():
    in_dict = {
        "clustermode": {
            '@status': "passed",
            'attributes_list': {
                'quota_entry': [{
                    'disk_limit': "1236",
                    'file_limit': '-',
                    'policy': "default",
                    'qtree': "",
                    'quota_target': "/vol/test002/userdir",
                    'quota_type': "tree",
                    'soft_disk_limit': "988",
                    'soft_file_limit': "-",
                    'threshold': "-",
                    'volume': "test002",
                    'vserver': "filer101sm"
                }],
                'num_records': 1
            }
        }
    }
    out_dict = {
        "clustermode": {
            '@status': "passed",
            'attributes-list': {
                'quota-entry': [{
                    'disk-limit': "1236",
                    'file-limit': '-',
                    'policy': "default",
                    'qtree': "",
                    'quota-target': "/vol/test002/userdir",
                    'quota-type': "tree",
                    'soft-disk-limit': "988",
                    'soft-file-limit': "-",
                    'threshold': "-",
                    'volume': "test002",
                    'vserver': "filer101sm"
                }],
                'num-records': 1
            }
        }
    }
    assert underline_to_dash(in_dict) == out_dict
