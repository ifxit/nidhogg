# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .sevenmode import SevenMode
from .clustermode import ClusterMode
from .core import NidhoggException


__all__ = ["get_netapp", "get_best_volume_by_size", "get_best_volume_by_quota"]


def get_netapp(url, username, password, verify=False):
    """Return the correct connection object to the filer.

    You do not have to care if the filer is a cluster-mode or a seven-mode filer.

    .. note::

        Provided user must be authorized to use the Netapp API of the filer.

    :param url: hostname of the netapp filer
    :type url: str
    :param username: username to connect to the Netapp API.
    :type username: str
    :param password: password of the provided user
    :type password: str
    :param verify: check SSL certificate
    :type verify: bool
    :return: Nidhogg instance
    :rtype: :class:`~nidhogg.sevenmode.SevenMode` (if the filer is a seven-mode filer)
    :rtype: :class:`~nidhogg.clustermode.ClusterMode` (if the filer is a cluster-mode filer)

    Example:

    .. code-block:: python

        import nidhogg
        filer = nidhogg.get_netapp("filer99.example.com", "<username>", "<password>")
        filer.list_volumes()
    """
    # prepend https if not specified
    if not url.startswith("https://"):
        url = "https://" + url
    nidhogg = SevenMode(url, username, password, 1, 15, verify)
    if nidhogg.clustered:
        return ClusterMode(url, username, password, 1, 21, verify)
    return nidhogg


def get_best_volume_by_size(volumes, filter_func=None, **kwargs):
    """Return the best volume from the list of volumes with the biggest free size.

    Apply filter function before if specified.

    :param volumes: list of volumes
    :type volumes: list of :class:`~nidhogg.compatible.Volume`
    :param filter_func: filter function applied before
    :type filter_func: function
    :return: volume with the biggest free size
    :rtype: :class:`~nidhogg.compatible.Volume`
    """
    if hasattr(filter_func, '__call__'):
        volumes = [v for v in volumes if filter_func(v, **kwargs)]
    if not volumes:
        raise NidhoggException("No volume available.")
    # use max() to get the volume with the biggest free size
    return max(volumes)


def get_best_volume_by_quota(volumes, filter_func=None, **kwargs):
    """Return the best volume from the list of volumes with the smallest quota ration.

    :param volumes: list of volumes
    :type volumes: list of :class:`~nidhogg.compatible.VolumeWithQuotaRatio`
    :param filter_func: filter function applied before
    :type filter_func: function
    :return: volume with the smallest quota ratio (allocated quota size / volume size)
    :rtype: :class:`~nidhogg.compatible.VolumeWithQuotaRatio`
    """
    if hasattr(filter_func, '__call__'):
        volumes = [v for v in volumes if filter_func(v, **kwargs)]
    if not volumes:
        raise NidhoggException("No volume available.")
    # use min() to get the volume with the smallest ratio
    return min(volumes)
