# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from nidhogg.compatible import InitDict


class MyTestDict(InitDict):
    """Just a test class."""

    required_arguments = ["fuer", "immer"]


def test_initdict_is_not_initable():
    with pytest.raises(AttributeError):
        InitDict(a=1)


def test_required_arguments_to_few_args():
    with pytest.raises(AttributeError):
        MyTestDict(fuer=1)


def test_required_arguments_to_much_args():
    with pytest.raises(AttributeError):
        MyTestDict(fuer=1, immer=1, fuerimmer=1)


def test_required_arguments_bad_args():
    with pytest.raises(AttributeError):
        MyTestDict(fuerimmer=1, inberlin=1)


def test_required_arguments_ok():
    assert MyTestDict(fuer=1, immer=1) == {"fuer": 1, "immer": 1}


def test_access():
    m = MyTestDict(fuer=1, immer=1)
    m["fuer"] = 2
    m["immer"] = 2
    m["fuerimmer"] = 2
    assert m == {"fuer": 2, "immer": 2, "fuerimmer": 2}


def test_initdict_eq():
    class Band(InitDict):
        required_arguments = ["name", "members_count"]

    bands = [Band(name="fettes brot", members_count=3), Band(name="fanta4", members_count=4)]
    assert "fettes brot" in bands
    assert "fanta4" in bands
    assert "aertze" not in bands
