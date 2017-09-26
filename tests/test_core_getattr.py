# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


@pytest.mark.parametrize('mode', [
    (ClusterMode, {"@status": "passed"}),
    (SevenMode, {"@status": "passed"})
], indirect=True)
def test_getattr_without_kwargs(mode, std_netapp_reply):
    assert mode.system_get_version() == std_netapp_reply
    assert mode.sent == [('system_get_version', {})]


@pytest.mark.parametrize('mode', [
    (ClusterMode, {"@status": "passed"}),
    (SevenMode, {"@status": "passed"})
], indirect=True)
def test_getattr_with_kwargs(mode, std_netapp_reply):
    assert mode.create_foo(foo="bar") == std_netapp_reply
