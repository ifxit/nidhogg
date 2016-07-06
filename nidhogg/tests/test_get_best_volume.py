# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg import get_best_volume_by_quota, get_best_volume_by_size
from nidhogg.core import NidhoggException
from nidhogg.compatible import Volume, VolumeWithQuotaRatio


def check_volume(volume, size):
    """Helper function that is applied to check if the volume is suitable."""
    size *= 1048576   # convert to byte
    size *= 1.2       # add buffer to the given size
    max_file_count = 32000000
    quota_ratio_threshold = 1.2
    # checks
    check_1 = bool(volume["size_available"] >= size)
    check_2 = bool(volume["files_used"] < max_file_count)
    check_3 = bool(volume["quota_ratio"] < quota_ratio_threshold)
    return check_1 and check_2 and check_3


def test_best_project_home_1():
    volumes = [
        VolumeWithQuotaRatio(**{'size_used': 116086018048.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 193273528320.0, 'size_available': 77187489792.0, 'quota_size': 216895848448.0, 'state': u'online', 'quota_ratio': 1.1222222222222222, 'snapable': True, 'files_used': 1049599.0, 'name': u'proj000'}),
        VolumeWithQuotaRatio(**{'size_used': 768038326272.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 1428076625920.0, 'size_available': 660038287360.0, 'quota_size': 1526860873728.0, 'state': u'online', 'quota_ratio': 1.069172932330827, 'snapable': True, 'files_used': 6377127.0, 'name': u'proj109'}),
        VolumeWithQuotaRatio(**{'size_used': 168616095744.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 483183820800.0, 'size_available': 314567712768.0, 'quota_size': 558345748480.0, 'state': u'online', 'quota_ratio': 1.1555555555555554, 'snapable': True, 'files_used': 882234.0, 'name': u'proj013'}),
        VolumeWithQuotaRatio(**{'size_used': 755761999872.0, 'filer': u'filer07.example.com', 'files_total': 44876648.0, 'size_total': 1122060206080.0, 'size_available': 366298185728.0, 'quota_size': 918049259518.0, 'state': u'online', 'quota_ratio': 0.8181818181800358, 'snapable': True, 'files_used': 35818461.0, 'name': u'proj090'}),
        VolumeWithQuotaRatio(**{'size_used': 1775658102784.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 2415919104000.0, 'size_available': 640259833856.0, 'quota_size': 2655363530744.0, 'state': u'online', 'quota_ratio': 1.0991111111077998, 'snapable': True, 'files_used': 19140696.0, 'name': u'proj320'}),
        VolumeWithQuotaRatio(**{'size_used': 1592106135552.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 2126008811520.0, 'size_available': 533902389248.0, 'quota_size': 2759516487680.0, 'state': u'online', 'quota_ratio': 1.297979797979798, 'snapable': True, 'files_used': 11719412.0, 'name': u'proj108'}),  # quota over 1.2
    ]
    # 50 GB, smallest quota ratio, because proj090 has too much files > 32 mio
    assert 'proj109' == get_best_volume_by_quota(volumes, check_volume, size=50 * 1024)['name']


def test_best_project_home_2():
    volumes = [
        VolumeWithQuotaRatio(**{'size_used': 755761999872.0, 'filer': u'filer07.example.com', 'files_total': 44876648.0, 'size_total': 1122060206080.0, 'size_available': 366298185728.0, 'quota_size': 918049259518.0, 'state': u'online', 'quota_ratio': 0.8181818181800358, 'snapable': True, 'files_used': 31999999.0, 'name': u'proj090'}),
        VolumeWithQuotaRatio(**{'size_used': 1775658102784.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 2415919104000.0, 'size_available': 640259833856.0, 'quota_size': 2655363530744.0, 'state': u'online', 'quota_ratio': 1.0991111111077998, 'snapable': True, 'files_used': 19140696.0, 'name': u'proj320'}),
        VolumeWithQuotaRatio(**{'size_used': 1592106135552.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 2126008811520.0, 'size_available': 533902389248.0, 'quota_size': 2759516487680.0, 'state': u'online', 'quota_ratio': 1.297979797979798, 'snapable': True, 'files_used': 11719412.0, 'name': u'proj108'}),  # quota over 1.2
    ]
    # 100 GB, netapp with sufficient space
    assert 'proj090' == get_best_volume_by_quota(volumes, check_volume, size=100 * 1024)['name']


def test_best_project_home_big():
    volumes = [
        VolumeWithQuotaRatio(**{'size_used': 755761999872.0, 'filer': u'filer07.example.com', 'files_total': 44876648.0, 'size_total': 1122060206080.0, 'size_available': 366298185728.0, 'quota_size': 918049259518.0, 'state': u'online', 'quota_ratio': 0.8181818181800358, 'snapable': True, 'files_used': 31999999.0, 'name': u'proj090'}),
        VolumeWithQuotaRatio(**{'size_used': 1775658102784.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 2415919104000.0, 'size_available': 640259833856.0, 'quota_size': 2655363530744.0, 'state': u'online', 'quota_ratio': 1.0991111111077998, 'snapable': True, 'files_used': 19140696.0, 'name': u'proj320'}),
        VolumeWithQuotaRatio(**{'size_used': 1592106135552.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 2126008811520.0, 'size_available': 533902389248.0, 'quota_size': 2759516487680.0, 'state': u'online', 'quota_ratio': 1.297979797979798, 'snapable': True, 'files_used': 11719412.0, 'name': u'proj108'}),  # quota over 1.2
    ]
    # 350 GB, netapp with sufficient space
    assert 'proj320' == get_best_volume_by_quota(volumes, check_volume, size=350 * 1024)['name']


def test_best_project_home_too_big():
    volumes = [
        VolumeWithQuotaRatio(**{'size_used': 755761999872.0, 'filer': u'filer07.example.com', 'files_total': 44876648.0, 'size_total': 1122060206080.0, 'size_available': 366298185728.0, 'quota_size': 918049259518.0, 'state': u'online', 'quota_ratio': 0.8181818181800358, 'snapable': True, 'files_used': 31999999.0, 'name': u'proj090'}),
    ]
    with pytest.raises(NidhoggException):
        # 350 GB, netapp with sufficient space
        get_best_volume_by_quota(volumes, check_volume, size=350 * 1024)


def test_best_project_home_too_much_files():
    volumes = [
        VolumeWithQuotaRatio(**{'size_used': 755761999872.0, 'filer': u'filer07.example.com', 'files_total': 44876648.0, 'size_total': 1122060206080.0, 'size_available': 366298185728.0, 'quota_size': 918049259518.0, 'state': u'online', 'quota_ratio': 0.8181818181800358, 'snapable': True, 'files_used': 35818461.0, 'name': u'proj090'}),
    ]
    with pytest.raises(NidhoggException):
        get_best_volume_by_quota(volumes, check_volume, size=1234)


def test_best_project_home_too_big_ratio_quota():
    volumes = [
        VolumeWithQuotaRatio(**{'size_used': 1592106135552.0, 'filer': u'filer07.example.com', 'files_total': 31876689.0, 'size_total': 2126008811520.0, 'size_available': 533902389248.0, 'quota_size': 2759516487680.0, 'state': u'online', 'quota_ratio': 1.297979797979798, 'snapable': True, 'files_used': 11719412.0, 'name': u'proj108'}),  # quota over 1.2
    ]
    with pytest.raises(NidhoggException):
        get_best_volume_by_quota(volumes, check_volume, size=1234)


def test_best_user_home_1():
    volumes = [
        Volume(**{'size_used': 432169402368.0, 'filer': u'filer21.example.com', 'files_total': 21790707.0, 'size_total': 676457349120.0, 'size_available': 244287254528.0, 'state': u'online', 'snapable': True, 'files_used': 8648992.0, 'name': u'home000'}),
        Volume(**{'size_used': 81415127040.0, 'filer': u'filer21.example.com', 'files_total': 3112959.0, 'size_total': 96636764160.0, 'size_available': 15221399552.0, 'state': u'online', 'snapable': True, 'files_used': 1413035.0, 'name': u'home002'}),
        Volume(**{'size_used': 349094301696.0, 'filer': u'filer21.example.com', 'files_total': 15564791.0, 'size_total': 429496729600.0, 'size_available': 80396869632.0, 'state': u'online', 'snapable': True, 'files_used': 7136798.0, 'name': u'home050'}),
        Volume(**{'size_used': 133556998144.0, 'filer': u'filer21.example.com', 'files_total': 26460144.0, 'size_total': 429496729600.0, 'size_available': 295939719168.0, 'state': u'online', 'snapable': True, 'files_used': 862642.0, 'name': u'home110'}),
    ]
    assert 'home110' == get_best_volume_by_size(volumes)['name']


def test_best_user_home_2():

    def check(volume):
        if volume['name'] == 'home110':
            return False
        return True

    volumes = [
        Volume(**{'size_used': 432169402368.0, 'filer': u'filer21.example.com', 'files_total': 21790707.0, 'size_total': 676457349120.0, 'size_available': 244287254528.0, 'state': u'online', 'snapable': True, 'files_used': 8648992.0, 'name': u'home000'}),
        Volume(**{'size_used': 81415127040.0, 'filer': u'filer21.example.com', 'files_total': 3112959.0, 'size_total': 96636764160.0, 'size_available': 15221399552.0, 'state': u'online', 'snapable': True, 'files_used': 1413035.0, 'name': u'home002'}),
        Volume(**{'size_used': 349094301696.0, 'filer': u'filer21.example.com', 'files_total': 15564791.0, 'size_total': 429496729600.0, 'size_available': 80396869632.0, 'state': u'online', 'snapable': True, 'files_used': 7136798.0, 'name': u'home050'}),
        Volume(**{'size_used': 133556998144.0, 'filer': u'filer21.example.com', 'files_total': 26460144.0, 'size_total': 429496729600.0, 'size_available': 295939719168.0, 'state': u'online', 'snapable': True, 'files_used': 862642.0, 'name': u'home110'}),
    ]
    assert 'home000' == get_best_volume_by_size(volumes, check)['name']


def test_best_user_home_no_volumes():
    volumes = []
    with pytest.raises(NidhoggException):
        get_best_volume_by_size(volumes)['name']
