# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def test_create_request(allmodes):
    # tag order differs sometimes
    ver_a = "<foobar><a>1</a><b>2</b></foobar>"
    ver_b = "<foobar><b>2</b><a>1</a></foobar>"

    xml = """<?xml version='1.0' encoding='utf-8'?>
<netapp version='1.1'
        xmlns='http://www.netapp.com/filer/admin'
        nmsdk_version='development'
        nmsdk_language='python'
        nmsdk_app='Nidhogg'>
    {}
</netapp>"""
    try:
        assert allmodes._create_request(foobar={"a": 1, "b": 2}) == xml.format(ver_a)
    except AssertionError:
        # try it with other xml tag order again
        assert allmodes._create_request(foobar={"a": 1, "b": 2}) == xml.format(ver_b)
