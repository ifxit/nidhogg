# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

# Python 2/3 support
import sys
if sys.version_info[0] >= 3:    # pragma: no cover
    unicode = str

logger = logging.getLogger(__name__)


class InitDict(dict):
    """Base class of the data object classes to enforce required keys in the dict."""

    def __init__(self, **kwargs):
        """Check required keys."""
        if set(self.required_arguments).symmetric_difference(set(kwargs.keys())):
            raise AttributeError("required arguments: {}".format(self.required_arguments))
        super(InitDict, self).__init__(**kwargs)

    def __eq__(self, other):
        """Compare value of first key with specified unicode."""
        if isinstance(other, unicode):
            key_arg = self.required_arguments[0]
            return other == self[key_arg]
        return super(InitDict, self).__eq__(other)


class Volume(InitDict):
    """Data object representing a volume sortable by free size."""

    required_arguments = [
        "name", "state", "size_total", "size_used", "size_available", "files_used", "files_total", "snapable", "filer"
    ]

    def __lt__(self, other):
        """Use max() to get the volume with the biggest free size."""
        return self["size_available"] < other["size_available"]


class VolumeWithQuotaRatio(InitDict):
    """Data object representing a volume sortable by quota ratio."""

    required_arguments = [
        "name", "state", "size_total", "size_used", "size_available", "files_used", "files_total", "snapable",
        "quota_size", "quota_ratio", "filer"
    ]

    def __lt__(self, other):
        """Use min() to get the volume with the smallest ratio."""
        return self["quota_ratio"] < other["quota_ratio"]


class Snapshot(InitDict):
    """Data object representing a snapshot."""

    required_arguments = ["name"]


class QTree(InitDict):
    """Data object representing a qtree."""

    required_arguments = ["qtree", "status", "security_style"]


class Aggregate(InitDict):
    """Data object representing an aggregate."""

    required_arguments = ["id", "volume"]


class Quota(InitDict):
    """Data object representing a quota."""

    required_arguments = ["disk_limit", "file_limit", "threshold", "soft_disk_limit", "soft_file_limit"]


class QuotaReport(InitDict):
    """Data object representing a quota report."""

    required_arguments = [
        "disk_limit", "file_limit", "threshold", "soft_disk_limit", "soft_file_limit", "quota_target", "files_used",
        "disk_used", "tree"
    ]


class ACE(InitDict):
    """Data object representing an *access control entry*."""

    required_arguments = ["share_name", "permission", "user_or_group", "is_group", "user_group_type"]


class SnapmirrorStatus(InitDict):
    """Data object representing a snapmirror status."""

    required_arguments = [
        'source_location', 'destination_location', 'lag_time', 'last_transfer_from',
        'last_transfer_size', 'last_transfer_duration', 'last_transfer_type', 'status', 'transfer_progress',
        'mirror_timestamp', 'contents', 'state', 'base_snapshot', 'current_transfer_error', 'current_transfer_type',
        'inodes_replicated', 'replication_ops', 'break_failed_count', 'break_successful_count',
        'destination_volume', 'destination_volume_node', 'destination_vserver', 'destination_vserver_uuid',
        'exported_snapshot', 'exported_snapshot_timestamp', 'is_constituent', 'is_healthy',
        'last_transfer_end_timestamp', 'last_transfer_network_compression_ratio', 'max_transfer_rate', 'mirror_state',
        'newest_snapshot', 'newest_snapshot_timestamp', 'opmask', 'policy', 'policy_type',
        'relationship_control_plane', 'relationship_group_type', 'relationship_id', 'relationship_status',
        'relationship_type', 'resync_failed_count', 'resync_successful_count', 'source_volume', 'source_vserver',
        'source_vserver_uuid', 'total_transfer_bytes', 'total_transfer_time_secs', 'update_failed_count',
        'update_successful_count', 'vserver', 'snapmirror_status',
    ]


class SnapmirrorVolumeStatus(InitDict):
    """Data object representing a snapmirror volume status."""

    required_arguments = [
        "is_source", "is_destination", "is_transfer_in_progress", "is_transfer_broken"
    ]


class CifsShare(InitDict):
    """Data object representing a cifs share."""

    required_arguments = [
        "path", "share_name"
    ]


class SnapmirrorDestinationInfo(InitDict):
    """Data object representing a snapmirror destination info."""

    required_arguments = [
        "destination_location", "destination_volume", "destination_vserver", "is_constituent", "policy_type",
        "relationship_group_type", "relationship_id", "relationship_status", "relationship_type",
        "source_location", "source_volume", "source_volume_node", "source_vserver"
    ]
