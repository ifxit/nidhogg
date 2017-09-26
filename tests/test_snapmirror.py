# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def test_update_snapmirror(sevenmode):
    sevenmode.update_snapmirror("vol")
    sevenmode.update_snapmirror("vol", "qtree")
    sevenmode.update_snapmirror("vol", source_filer="host", source_volume="vol")
    sevenmode.update_snapmirror("vol", "qtree", source_filer="host", source_volume="vol", source_qtree="qtree")


def test_update_snapmirror_with_snapshot(sevenmode):
    sevenmode.update_snapmirror_with_snapshot("name", "vol")
    sevenmode.update_snapmirror_with_snapshot("name", "vol", "qtree")
    sevenmode.update_snapmirror_with_snapshot("name", "vol", source_filer="host", source_volume="vol")
    sevenmode.update_snapmirror_with_snapshot("name", "vol", "qtree", source_filer="host", source_volume="vol", source_qtree="qtree")


def test_update_snapmirror_sevenmode_api_1(sevenmode):
    sevenmode.update_snapmirror("volume", "qtree")
    assert sevenmode.sent == [('snapmirror_update', {'destination_location': '/vol/volume/qtree'})]


def test_update_snapmirror_sevenmode_api_2(sevenmode):
    sevenmode.update_snapmirror("volume")
    assert sevenmode.sent == [('snapmirror_update', {'destination_location': 'volume'})]


def test_update_snapmirror_sevenmode_api_3(sevenmode):
    sevenmode.update_snapmirror("volume", source_filer="host", source_volume="src_vol")
    assert sevenmode.sent == [('snapmirror_update', {'destination_location': 'volume', 'source_location': 'host:src_vol'})]


def test_update_snapmirror_sevenmode_api_4(sevenmode):
    sevenmode.update_snapmirror("volume", "qtree", source_filer="host", source_volume="src_vol", source_qtree="src_qtree")
    assert sevenmode.sent == [('snapmirror_update', {
        'destination_location': '/vol/volume/qtree',
        'source_location': 'host:/vol/src_vol/src_qtree'
    })]


def test_update_snapmirror_with_snapshot_sevenmode_api_1(sevenmode):
    sevenmode.update_snapmirror_with_snapshot("name", "volume", "qtree")
    assert sevenmode.sent == [('snapmirror_update', {
        'destination_location': '/vol/volume/qtree',
        'source_snapshot': "name",
        'destination_snapshot': "name"
    })]


def test_update_snapmirror_with_snapshot_sevenmode_api_2(sevenmode):
    sevenmode.update_snapmirror_with_snapshot("name", "volume")
    assert sevenmode.sent == [('snapmirror_update', {
        'destination_location': 'volume',
        'source_snapshot': "name",
        'destination_snapshot': "name"
    })]


def test_update_snapmirror_with_snapshot_sevenmode_api_3(sevenmode):
    sevenmode.update_snapmirror_with_snapshot("name", "volume", source_filer="host", source_volume="src_vol")
    assert sevenmode.sent == [('snapmirror_update', {
        'destination_location': 'volume',
        'source_location': 'host:src_vol',
        'source_snapshot': "name",
        'destination_snapshot': "name"
    })]


def test_update_snapmirror_with_snapshot_sevenmode_api_4(sevenmode):
    sevenmode.update_snapmirror_with_snapshot("name", "volume", "qtree", source_filer="host", source_volume="src_vol", source_qtree="src_qtree")
    assert sevenmode.sent == [('snapmirror_update', {
        'destination_location': '/vol/volume/qtree',
        'source_location': 'host:/vol/src_vol/src_qtree',
        'source_snapshot': "name",
        'destination_snapshot': "name"
    })]
