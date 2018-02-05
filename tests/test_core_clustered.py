# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


@pytest.mark.parametrize('mode', [
    (ClusterMode, {"is-clustered": "true"}),
], indirect=True)
def test_clustered(mode):
    assert mode.clustered is True


@pytest.mark.parametrize('mode', [
    (ClusterMode, {"is-clustered": "false"}),
], indirect=True)
def test_clustered_false(mode):
    assert mode.clustered is False


@pytest.mark.parametrize('mode', [
    (ClusterMode, {"is-clustered": "true"}),
    (SevenMode, {"is-clustered": "false"})
], indirect=True)
def test_clustered_api(mode):
    # provoke API call
    mode.clustered
    assert mode.sent == [('system_get_version', {})]
