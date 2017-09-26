# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch, PropertyMock

from nidhogg import get_netapp
from nidhogg.sevenmode import SevenMode
from nidhogg.clustermode import ClusterMode


def test_7mode():
    with patch("nidhogg.SevenMode.clustered", new_callable=PropertyMock) as mock_clustered:
        mock_clustered.return_value = False
        nidhogg = get_netapp(url="mynetapp.example.com", username="admin", password="secret")
    assert isinstance(nidhogg, SevenMode)


def test_clustermode():
    with patch("nidhogg.SevenMode.clustered", new_callable=PropertyMock) as mock_clustered:
        mock_clustered.return_value = True
        nidhogg = get_netapp(url="mynetapp.example.com", username="admin", password="secret")
    assert isinstance(nidhogg, ClusterMode)
