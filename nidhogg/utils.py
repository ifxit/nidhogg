# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def underline_to_dash(d):
    """Helper function to replace "_" to "-" in keys of specifed dictionary recursively.

    Netapp API uses "-" in XML parameters.

    :param d: dictionary of dictionaries or lists
    :type d: dict
    :return: new dictionary
    :rtype: dict
    """
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = underline_to_dash(v)
        if isinstance(v, list):
            for i in v:
                v = [underline_to_dash(i)]
        new[k.replace('_', '-')] = v
    return new


def safe_get(d, key):
    """Helper function.

    :param d: dictionary
    :type d: dict
    :param key: key to retrieve from dict
    :type key: str
    :return: value of specified key if not None, otherwise empty dict
    """
    if key in d and d[key] is not None:
        return d[key]
    return {}
