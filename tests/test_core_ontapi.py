# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


@pytest.mark.parametrize('mode', [
    (ClusterMode, {"major-version": 10, "minor-version": 11}),
    (SevenMode, {"major-version": 10, "minor-version": 11})
], indirect=True)
def test_ontapi_version(mode):
    assert mode.ontapi_version == "10.11"
    assert mode.sent == [('system_get_ontapi_version', {})]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "is-clustered": "true",
        "major-version": "1",
        "minor-version": "29",
    })
], indirect=True)
def test_no_force_group(mode):
    assert mode.has_forcegroup is False


@pytest.mark.parametrize('mode', [
    (ClusterMode, {
        "is-clustered": "true",
        "major-version": "1",
        "minor-version": "30",
    }),
    (SevenMode, {
        "is-clustered": "false",
        "major-version": "1",
        "minor-version": "21",
    })
], indirect=True)
def test_has_force_group(mode):
    assert mode.has_forcegroup is True
