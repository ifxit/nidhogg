# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def test_vserver(allmodes):
    assert allmodes.vserver == "my"


def test_vserver_fqdn(allmodes):
    assert allmodes.vserver_fqdn == "my.url.to.filer"
