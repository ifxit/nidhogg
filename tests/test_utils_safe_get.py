# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nidhogg.utils import safe_get


def test_safe_get_no_key():
    assert safe_get({'a': 1}, 'b') == {}


def test_safe_get_is_none():
    assert safe_get({'a': None}, 'a') == {}


def test_safe_get():
    assert safe_get({'a': 1}, 'a') == 1
