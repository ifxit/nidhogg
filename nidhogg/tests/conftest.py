# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import mock

from nidhogg.core import Nidhogg, NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


STD_NETAPP_RESULT_OK = {'netapp': {'results': {"@status": "passed"}}}
STD_NETAPP_RESULT_FAILED = {'netapp': {'results': {"@status": "failed"}}}


def do_mock(self, key, **kwargs):
    self.sent.append((key, kwargs))
    if self.patched_return_value.get("netapp", {}).get("results", {}).get("@status", "passed") == "failed":
        raise NidhoggException("error error error")
    return self.patched_return_value


def get_sevenmode():
    n = SevenMode("https://my.url.to.filer", "user", "password", 1, 1)
    n.sent = []
    return n


@pytest.fixture
def sevenmode(request, monkeypatch):
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._do", do_mock)
    n = get_sevenmode()
    n.patched_return_value = mock.MagicMock()
    return n


@pytest.fixture
def sevenmode_failed(request, monkeypatch):
    monkeypatch.setattr("nidhogg.sevenmode.SevenMode._do", do_mock)
    n = get_sevenmode()
    n.patched_return_value = STD_NETAPP_RESULT_FAILED
    return n


def get_clustermode():
    n = ClusterMode("https://my.url.to.filer", "user", "password", 1, 1)
    n.sent = []
    return n


@pytest.fixture
def clustermode(request, monkeypatch):
    monkeypatch.setattr("nidhogg.clustermode.ClusterMode._do", do_mock)
    n = get_clustermode()
    n.patched_return_value = mock.MagicMock()
    return n


@pytest.fixture
def clustermode_failed(request, monkeypatch):
    monkeypatch.setattr("nidhogg.clustermode.ClusterMode._do", do_mock)
    n = get_clustermode()
    n.patched_return_value = STD_NETAPP_RESULT_FAILED
    return n


@pytest.fixture
def std_netapp_reply():
    return STD_NETAPP_RESULT_OK


@pytest.fixture
def mode(request, monkeypatch):
    # See http://pytest.org/latest/example/parametrize.html#deferring-the-setup-of-parametrized-resources
    klass, results = request.param
    monkeypatch.setattr("{0}.{1}._do".format(klass.__module__, klass.__name__), do_mock)
    n = klass("https://my.url.to.filer", "user", "password", 1, 1)
    n.sent = []
    n.patched_return_value = {'netapp': {'results': results}}
    return n


@pytest.fixture(params=['seven', 'cluster'])
def allmodes(request, sevenmode, clustermode):
    if request.param == "seven":
        return sevenmode
    if request.param == "cluster":
        return clustermode


@pytest.fixture(params=['seven', 'cluster'])
def allmodes_failed(request, sevenmode_failed, clustermode_failed):
    if request.param == "seven":
        return sevenmode_failed
    if request.param == "cluster":
        return clustermode_failed


@pytest.fixture
def patch_timeout(monkeypatch):
    monkeypatch.setattr("nidhogg.core.QUOTA_RESIZE_WAIT_TIME", 1)
    monkeypatch.setattr("nidhogg.core.QUOTA_RESIZE_WAIT_CYCLES", 1)
