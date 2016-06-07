# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Python 2/3 support
import sys
if sys.version_info[0] >= 3:    # pragma: no cover
    unicode = str

import logging
logger = logging.getLogger(__name__)


class InitDict(dict):
    """ Base class of the data object classes to enforce required keys in the dict. """

    def __init__(self, **kwargs):
        """ Check required keys. """
        if set(self.required_arguments).symmetric_difference(set(kwargs.keys())):
            raise AttributeError("required arguments: {}".format(self.required_arguments))
        super(InitDict, self).__init__(**kwargs)

    def __eq__(self, other):
        """ Compare value of first key with specified unicode. """
        if isinstance(other, unicode):
            key_arg = self.required_arguments[0]
            return other == self[key_arg]
        return super(InitDict, self).__eq__(other)


class Volume(InitDict):
    """ Data object representing a volume sortable by free size. """
    required_arguments = [
        "name", "state", "size_total", "size_used", "size_available", "files_used", "files_total", "snapable", "filer"
    ]

    def __lt__(self, other):
        """ Use max() to get the volume with the biggest free size. """
        return self["size_available"] < other["size_available"]


class VolumeWithQuotaRatio(InitDict):
    """ Data object representing a volume sortable by quota ratio. """
    required_arguments = [
        "name", "state", "size_total", "size_used", "size_available", "files_used", "files_total", "snapable",
        "quota_size", "quota_ratio", "filer"
    ]

    def __lt__(self, other):
        """ Use min() to get the volume with the smallest ratio. """
        return self["quota_ratio"] < other["quota_ratio"]


class Snapshot(InitDict):
    """ Data object representing a snapshot. """
    required_arguments = ["name"]


class QTree(InitDict):
    """ Data object representing a qtree. """
    required_arguments = ["qtree", "status", "security_style"]


class Aggregate(InitDict):
    """ Data object representing an aggregate. """
    required_arguments = ["id", "volume"]


class Quota(InitDict):
    """ Data object representing a quota. """
    required_arguments = ["disk_limit", "file_limit", "threshold", "soft_disk_limit", "soft_file_limit"]


class QuotaReport(InitDict):
    """ Data object representing a quota report. """
    required_arguments = [
        "disk_limit", "file_limit", "threshold", "soft_disk_limit", "soft_file_limit", "quota_target", "files_used",
        "disk_used", "tree"
    ]


class ACE(InitDict):
    """ Data object representing an *access control entry*. """
    required_arguments = ["share_name", "permission", "user_or_group", "is_group", "user_group_type"]


class SnapmirrorStatus(InitDict):
    """ Data object representing a snapmirror status. """
    required_arguments = [
        "source_location", "destination_location", "last_transfer_from",
        "last_transfer_size", "last_transfer_duration", "transfer_progress", "lag_time",
        "mirror_timestamp", "contents", "status", "state",
        # optional
        "base_snapshot", "current_transfer_error", "current_transfer_type",
        "inodes_replicated", "last_transfer_type", "replication_ops"
    ]


class SnapmirrorVolumeStatus(InitDict):
    """ Data object representing a snapmirror volume status. """
    required_arguments = [
        "is_source", "is_destination", "is_transfer_in_progress", "is_transfer_broken"
    ]
