# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    # py2
    from backports.functools_lru_cache import lru_cache
except ImportError:     # pragma: no cover
    # py3
    from functools import lru_cache

import nidhogg.core     # this style needed for patching

from .compatible import ACE, CifsShare, SnapmirrorDestinationInfo, Snapshot, Volume
from .core import Nidhogg, NidhoggException
from time import sleep

import logging
logger = logging.getLogger(__name__)


#: maximum records that can be retrieved via NETAPP API
MAX_RECORDS = 2 ** 16


class ClusterMode(Nidhogg):
    """This class implements cluster-mode filer specific API calls."""

    ACL_FULL_CONTROL = "full_control"       #: ACL permission constant for full control
    ACL_READ = "read"                       #: ACL permission constant for read access
    ACL_CHANGE = "change"                   #: ACL permission constant for write access
    ACL_NO_ACCESS = "no_access"             #: ACL permission constant for denying access
    ACL_PERMISSIONS = [
        ACL_FULL_CONTROL,
        ACL_READ,
        ACL_CHANGE,
        ACL_NO_ACCESS
    ]                                       #: list of all permission constants

    def _item_to_volume(self, item):
        return Volume(
            name=item['volume-id-attributes']['name'],
            # RW for read-write, DP for data-protection, DC for data-cache, LS for load-sharing
            snapable=item['volume-id-attributes']['type'] == "rw",
            state=item['volume-state-attributes']['state'] if 'volume-state-attributes' in item and 'state' in item['volume-state-attributes'] else None,
            size_total=float(item['volume-space-attributes']['size-total']) if 'volume-space-attributes' in item and 'size-total' in item['volume-space-attributes'] else None,
            size_used=float(item['volume-space-attributes']['size-used']) if 'volume-space-attributes' in item and 'size-used' in item['volume-space-attributes'] else None,
            size_available=float(item['volume-space-attributes']['size-available']) if 'volume-space-attributes' in item and 'size-available' in item['volume-space-attributes'] else None,
            files_used=float(item['volume-inode-attributes']['files-used']) if 'volume-inode-attributes' in item and 'files-used' in item['volume-inode-attributes'] else None,
            files_total=float(item['volume-inode-attributes']['files-total']) if 'volume-inode-attributes' in item and 'files-total' in item['volume-inode-attributes'] else None,
            filer=self.vserver_fqdn,
        )

    def _item_to_ace(self, item):
        return ACE(
            share_name=item['share'],
            user_or_group=item['user-or-group'],
            permission=item['permission'],
            is_group=None,      # not used
            user_group_type=item['user-group-type'] if "user-group-type" in item else None
        )

    def _item_to_snapmirrordestinationinfo(self, item):
        return SnapmirrorDestinationInfo(
            destination_location=item["destination-location"],
            destination_volume=item['destination-volume'],
            destination_vserver=item['destination-vserver'],
            is_constituent=item['is-constituent'],
            policy_type=item['policy-type'],
            relationship_group_type=item['relationship-group-type'],
            relationship_id=item['relationship-id'],
            relationship_status=item['relationship-status'],
            relationship_type=item['relationship-type'],
            source_location=item["source-location"],
            source_volume=item['source-volume'],
            source_volume_node=item['source-volume-node'],
            source_vserver=item['source-vserver']
        )

    #
    # API FUNCTIONS
    #
    def list_qtrees(self, volume, max_records=MAX_RECORDS):
        """Return a list of qtrees of type :class:`~nidhogg.compatible.QTree`.

        :param volume: name of the volume
        :type volume: str
        :param max_records: limit returned records
        :type max_records: int
        :return: list of qtrees
        :rtype: list of :class:`~nidhogg.compatible.QTree` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            query=dict(
                qtree_info=dict(
                    volume=volume
                )
            ),
            max_records=max_records
        )
        results = self.qtree_list_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) > 1:
            return [
                self._item_to_qtree(item)
                for item in results["attributes-list"]["qtree-info"]
            ]
        elif int(results["num-records"]) == 1:
            return [
                self._item_to_qtree(results["attributes-list"]["qtree-info"])
            ]
        logger.warn("list_qtrees: no entries found")
        return []

    @lru_cache(maxsize=100)
    def list_volumes(self, max_records=MAX_RECORDS):
        """Return a list of volumes of type :class:`~nidhogg.compatible.Volume`.

        :param max_records: limit returned records
        :type max_records: int
        :return: list of volumes
        :rtype: list of :class:`~nidhogg.compatible.Volume` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            max_records=max_records
        )
        results = self.volume_get_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) > 1:
            return [
                self._item_to_volume(item)
                for item in results["attributes-list"]["volume-attributes"]
            ]
        elif int(results["num-records"]) == 1:
            return [
                self._item_to_volume(results["attributes-list"]["volume-attributes"])
            ]
        logger.warn("list_volumes: no entries found")
        return []

    @lru_cache(maxsize=100)
    def volume_info(self, volume):
        """Return basic information about the volume.

        :param volume: name of the volume
        :type volume: str
        :return: volume
        :rtype: :class:`~nidhogg.compatible.Volume`
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            query=dict(
                volume_id_attributes=dict(
                    name=volume
                )
            )
        )
        return self._item_to_volume(
            self.volume_get_iter(**opts)["netapp"]["results"]["attributes-list"]["volume-attributes"])

    def list_snapshots(self, target_name, max_records=MAX_RECORDS):
        """Return list of snapshots for given volume.

        :param target_name: name of the volume
        :type target_name: str
        :param max_records: limit returned records
        :type max_records: int
        :return: list of snapshots
        :rtype: list of :class:`~nidhogg.compatible.Snapshot` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            query=dict(
                snapshot_info=dict(
                    volume=target_name
                )
            ),
            max_records=max_records
        )
        results = self.snapshot_get_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) > 1:
            return [
                Snapshot(name=item['name'])
                for item in results["attributes-list"]["snapshot-info"]
            ]
        elif int(results["num-records"]) == 1:
            return [
                Snapshot(name=results["attributes-list"]["snapshot-info"]['name'])
            ]
        logger.warn("list_snapshots: no entries found")
        return []

    def get_quota(self, volume, qtree, max_records=MAX_RECORDS):
        """Return the quota of the specified qtree on the given volume.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree
        :type qtree: str
        :param max_records: limit returned records
        :type max_records: int
        :return: quota
        :rtype: :class:`~nidhogg.compatible.Quota` or empty dict
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            query=dict(
                quota_entry=dict(
                    quota_target="/vol/{0}/{1}".format(volume, qtree)
                )
            ),
            max_records=max_records
        )
        results = self.quota_list_entries_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) == 1:
            return self._item_to_quota(results['attributes-list']['quota-entry'])
        logger.warn("get_quota: no entries found")
        return {}

    def list_quotas(self, volume, max_records=MAX_RECORDS):
        """Return a list of quota reports of the specified volume.

        :param volume: name of the volume
        :type volume: str
        :param max_records: limit returned records
        :type max_records: int
        :return: list of quota reports
        :rtype: :class:`~nidhogg.compatible.QuotaReport` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            query=dict(
                quota=dict(
                    volume=volume
                )
            ),
            max_records=max_records
        )
        results = self.quota_report_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) > 1:
            return [
                self._item_to_quota_report(item)
                for item in results['attributes-list']['quota']
            ]
        elif int(results["num-records"]) == 1:
            return [
                self._item_to_quota_report(results['attributes-list']['quota'])
            ]
        logger.warn("list_quotas: no entries found")
        return []

    def list_cifs_shares(self):
        """List all cifs shares.

        :return: list of cifs shares
        :rtype: list of :class:`~nidhogg.compatible.CifsShare` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            max_records=2 ** 32 - 1
        )

        results = self.cifs_share_get_iter(**opts)['netapp']['results']

        if int(results['num-records']) > 1:
            return [
                CifsShare(path=item['path'], share_name=item['share-name'])
                for item in results['attributes-list']['cifs-share']
            ]
        elif int(results['num-records']) == 1:
            return [
                CifsShare(path=results['attributes-list']['cifs-share']['path'], share_name=results['attributes-list']['cifs-share']['share-name'])
            ]
        logger.warning("list_cifs_shares: cifs shares found")
        return []

    def create_cifs_share(self, volume, qtree, share_name, group_name=None, comment=None, umask="007", vscan_fileop_profile="standard"):
        """Create a cifs share.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree
        :type qtree: str
        :param share_name: name of the share
        :type share_name: str
        :param group_name: force group name if provided (supported by cluster-mode filers with ontapi >= 1.30)
        :type group_name: str
        :param comment: description of the share
        :type comment: str
        :param umask: file permission umask
        :type umask: str
        :param vscan_fileop_profile: vscan-fileop-profile virus scan option (no_scan, standard, strict, writes_only)
        :type vscan_fileop_profile: str
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            dir_umask=umask,
            file_umask=umask,
            path="/vol/{0}/{1}".format(volume, qtree),
            share_name=share_name,
            vscan_fileop_profile=vscan_fileop_profile
        )
        if group_name and self.has_forcegroup:
            opts['force_group_for_create'] = group_name
        if comment:
            opts['comment'] = comment
        self.cifs_share_create(**opts)

    def set_cifs_acl(self, share_name, user="everyone", right=ACL_READ, set_group_rights=None):
        """Set a single ACL for the specifed share.

        :param share_name: name of the share
        :type share_name: str
        :param user: name of a user or group
        :type user: str
        :param right: right to be set, value must be one of :py:const:`~ACL_PERMISSIONS`
        :type right: str
        :param set_group_rights: if true, *user* param specifies a unix group name; if false, *user*
            param specifies a unix user name; if not defined, *user* param specifies a windows name
        :type set_group_rights: bool
        :raises NidhoggException: if an error occurs
        :raises NidhoggException: if wrong right was set
        """
        # check permissions
        if right not in self.ACL_PERMISSIONS:
            raise NidhoggException("Permission {0} not in {1}.".format(right, self.ACL_PERMISSIONS))

        # set user_group_type
        if set_group_rights is None:
            user_group_type = "windows"
        elif set_group_rights is True:
            user_group_type = "unix_group"
        else:
            user_group_type = "unix_user"
        opts = dict(
            permission=right,
            share=share_name,
            user_or_group=user,
            user_group_type=user_group_type
        )
        self.cifs_share_access_control_create(**opts)

    def list_cifs_acls(self, share_name, max_records=MAX_RECORDS):
        """Return ACL of the specified share.

        :param share_name: name of the share
        :type share_name: str
        :param max_records: limit returned records
        :type max_records: int
        :return: list of ACEs (access control entries)
        :rtype: :class:`~nidhogg.compatible.ACE` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            query=dict(
                cifs_share_access_control=dict(
                    share=share_name
                )
            ),
            max_records=max_records
        )
        results = self.cifs_share_access_control_get_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) > 1:
            return [
                self._item_to_ace(item)
                for item in results['attributes-list']['cifs-share-access-control']
            ]
        elif int(results["num-records"]) == 1:
            return [
                self._item_to_ace(results['attributes-list']['cifs-share-access-control'])
            ]
        logger.warning("get_cifs_acl: no acls found")
        return []

    def delete_cifs_acl(self, share_name, user_or_group, is_group=None):
        """Delete cifs ACL of the specified user or group.

        :param share_name: name of the share
        :type share_name: str
        :param user_or_group: name of a user or group
        :type user_or_group: str
        :param is_group: not used for cluster-mode filers, specified here
            to be compatible with seven-mode method signature
        :type is_group: None
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            share=share_name,
            user_or_group=user_or_group
        )
        self.cifs_share_access_control_delete(**opts)

    def delete_cifs_acls(self, share_name):
        """Remove all cifs permssions.

        :param share_name: name of the share
        :type share_name: str
        :raises NidhoggException: if an error occurs
        """
        acls = self.list_cifs_acls(share_name)
        for ace in acls:
            self.delete_cifs_acl(
                share_name=ace["share_name"],
                user_or_group=ace["user_or_group"]
            )

    def set_quota(self, volume, qtree, quota_in_mb=1024, wait_til_finished=True):
        """Set a quota in MiB (default = 1GiB) for the specified volume and qtree.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree
        :type qtree: str
        :param quota_in_mb: quota in MiB
        :type quota_in_mb: int
        :param wait_til_finished: if false, do not wait for resize operation
        :type wait_til_finished: bool
        :raises NidhoggException: if an error occurs
        :raises NidhoggException: if resize did not finish in time and we were waiting for it
        :raises NidhoggException: if quotas are not enabled
        """
        quota_target = "/vol/{0}/{1}".format(volume, qtree)
        quota_type = "tree"
        quota_in_kb = int(round(quota_in_mb * 1024))
        # policy "default" must be specified for cluster-mode filers
        self.quota_set_entry(
            volume=volume,
            qtree="",
            disk_limit=quota_in_kb,
            soft_disk_limit=int(round(quota_in_kb * 0.8)),  # use 80% of the given quota as warn-limit
            quota_target=quota_target,
            quota_type=quota_type,
            policy="default"
        )
        self.quota_resize(volume=volume)
        if wait_til_finished:
            for i in range(0, nidhogg.core.QUOTA_RESIZE_WAIT_CYCLES):
                sleep(nidhogg.core.QUOTA_RESIZE_WAIT_TIME)
                status = self.quota_status(volume=volume)["netapp"]["results"]["status"]
                if status.lower() == "on":
                    return
                # check if quotas are turned on at all
                if status.lower() == "off":
                    raise NidhoggException("Quotas are not enabled.")
            # waiting for quote resize exceeded
            logger.debug("resize of {0}:/vol/{1} after setting quota for {2} did not finish".format(
                self.vserver_fqdn,
                volume,
                qtree
            ))
            raise NidhoggException("Quota resize did not finish in time.")

    def delete_quota(self, volume, qtree):
        """Delete the quota of the specified volume and qtree.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree
        :type qtree: str
        :raises NidhoggException: if an error occurs
        """
        quota_target = "/vol/{0}/{1}".format(volume, qtree)
        quota_type = "tree"
        # policy "default" must be specified for cluster-mode filers
        self.quota_delete_entry(
            volume=volume,
            qtree="",
            quota_target=quota_target,
            quota_type=quota_type,
            policy="default"
        )

    def update_snapmirror(self, volume):
        """Trigger the snapmirror replication. You have to be connected on the destination server.

        :param volume: name of snapmirror destination volume
        :type volume: str
        :raises NidhoggException: if an error occurs
        """
        self.snapmirror_update(
            destination_location="{}:{}".format(self.vserver, volume)
        )

    def update_snapmirror_with_snapshot(self, name, volume):
        """Trigger the snapmirror replication. You have to be connected on the destination server.

        :param name: name of the source snapshot
        :type name: str
        :param volume: name of snapmirror destination volume
        :type volume: str
        :raises NidhoggException: if an error occurs
        """
        self.snapmirror_update(
            destination_location="{}:{}".format(self.vserver, volume),
            source_snapshot=name
        )

    def get_snapmirror_status(self, volume=None, max_records=MAX_RECORDS):
        """Get status of snapmirror replication pairs. You have to be connected on the destination server.

        If no params are provided, return all snapmirror status pairs.

        :param volume: name of destination volume
        :type volume: str
        :return: list of all snapmirror pair status
        :rtype: list of :class:`~nidhogg.compatible.SnapmirrorStatus` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict()
        if volume:
            opts['query'] = dict(
                snapmirror_info=dict(
                    destination_location="{}:{}".format(self.vserver, volume)
                )
            )
            opts['max_records'] = max_records
        results = self.snapmirror_get_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) > 1:
            return [
                self._item_to_snapmirrorstatus(item)
                for item in results["attributes-list"]["snapmirror-info"]
            ]
        elif int(results["num-records"]) == 1:
            return [
                self._item_to_snapmirrorstatus(results["attributes-list"]["snapmirror-info"])
            ]
        logger.warn("get_snapmirror_status: no entries found")
        return []

    def get_snapmirror_volume_status(self, *args, **kwargs):
        """Not available for cluster mode."""
        raise NotImplementedError()     # pragma: no cover

    def create_snapshot(self, volume, name, label=None):
        """Create a snapshot with an optional label.

        :param volume: name of the volume
        :type volume: str
        :param name: name of the snapshot
        :type name: str
        :param label: add a snapmirror label to snapshot
        :type label: str
        :raises NidhoggException: if an error occurs
        """
        opts = dict()
        if label:
            opts['snapmirror_label'] = label
        opts['volume'] = volume
        opts['snapshot'] = name
        self.snapshot_create(**opts)

    def list_snapmirror_destinations(self, volume=None, max_records=MAX_RECORDS):
        """List all snapmirror destinations. You have to be connected on the source server.

        If no params are provided, return all snapmirror destinations.

        :param volume: name of source volume
        :type volume: str
        :return: list of all snapmirror destinations
        :rtype: list of :class:`~nidhogg.compatible.SnapmirrorDestinationInfo` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict()
        if volume:
            opts['query'] = dict(
                snapmirror_destination_info=dict(
                    source_location="{}:{}".format(self.vserver, volume)
                )
            )
            opts['max_records'] = max_records
        results = self.snapmirror_get_destination_iter(**opts)["netapp"]["results"]
        if int(results["num-records"]) > 1:
            return [
                self._item_to_snapmirrordestinationinfo(item)
                for item in results["attributes-list"]["snapmirror-destination-info"]
            ]
        elif int(results["num-records"]) == 1:
            return [
                self._item_to_snapmirrordestinationinfo(results["attributes-list"]["snapmirror-destination-info"])
            ]
        logger.warn("list_snapmirror_destinations: no entries found")
        return []
