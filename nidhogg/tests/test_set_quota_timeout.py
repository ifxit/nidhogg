# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.core import NidhoggException
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


pytestmark = pytest.mark.usefixtures(
    "patch_timeout",
)


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "resizing"}),
    (SevenMode, {'@status': "passed", 'status': "resizing"})
], indirect=True)
def test_set_quota_time_out(mode):
    with pytest.raises(NidhoggException):
        mode.set_quota("volume", "qtree", 1000, True)


@pytest.mark.parametrize('mode', [
    (ClusterMode, {'@status': "passed", 'status': "resizing"}),
    (SevenMode, {'@status': "passed", 'status': "resizing"})
], indirect=True)
def test_set_quota_time_out_ignored(mode):
    mode.set_quota("volume", "qtree", 1000, False)
