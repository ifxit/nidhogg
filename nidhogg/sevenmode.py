# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    # py2
    from backports.functools_lru_cache import lru_cache
except ImportError:     # pragma: no cover
    # py3
    from functools import lru_cache

from time import sleep
from .core import Nidhogg, NidhoggException
import nidhogg.core     # this style needed for patching
from .compatible import Volume, Snapshot, ACE, SnapmirrorVolumeStatus, CifsShare
from .utils import safe_get

import logging
logger = logging.getLogger(__name__)


class SevenMode(Nidhogg):
    """This class implements seven-mode filer specific API calls."""

    #: ACL permission constant for full control
    ACL_FULL_CONTROL = "Full Control"
    #: ACL permission constant for read access
    ACL_READ = "Read"
    #: ACL permission constant for write access
    ACL_CHANGE = "Change"
    #: ACL permission constant for denying access
    ACL_NO_ACCESS = "No Access"
    #: list of all permission constants
    ACL_PERMISSIONS = [
        ACL_FULL_CONTROL,
        ACL_READ,
        ACL_CHANGE,
        ACL_NO_ACCESS
    ]

    def _item_to_volume(self, item):
        return Volume(
            name=item['name'],
            state=item['state'],
            snapable=True if "raid-status" in item and "snapmirror" not in item['raid-status'] else False,
            size_total=float(item['size-total']) if "size-total" in item else None,
            size_used=float(item['size-used']) if "size-used" in item else None,
            size_available=float(item['size-available']) if "size-available" in item else None,
            files_used=float(item['files-used']) if "files-used" in item else None,
            files_total=float(item['files-total']) if "files-total" in item else None,
            filer=self.vserver_fqdn,
        )

    def _item_to_ace(self, share_name, item):
        return ACE(
            share_name=share_name,
            user_or_group=item['user-name'] if 'user-name' in item else item['unix-group-name'],
            permission=item['access-rights'],
            is_group=False if 'user-name' in item else True,
            user_group_type=None       # not used
        )

    def _item_to_snapmirrorvolumestatus(self, item):
        return SnapmirrorVolumeStatus(
            is_source=item["is-source"] == "true",
            is_destination=item["is-destination"] == "true",
            is_transfer_in_progress=item["is-transfer-in-progress"] == "true",
            is_transfer_broken=item["is-transfer-broken"] == "true"
        )

    #
    # API FUNCTIONS
    #
    def list_qtrees(self, volume):
        """Return a list of qtrees of type :class:`~nidhogg.compatible.QTree`.

        :param volume: name of the volume
        :type volume: str
        :return: list of qtrees
        :rtype: list of :class:`~nidhogg.compatible.QTree` or empty list
        :raises NidhoggException: if an error occurs
        """
        results = self.qtree_list(volume=volume)["netapp"]["results"]
        if results.get("qtrees", {}).get("qtree-info", False):
            if isinstance(results["qtrees"]["qtree-info"], list):
                return [
                    self._item_to_qtree(item)
                    for item in results["qtrees"]["qtree-info"]
                ]
            elif isinstance(results["qtrees"]["qtree-info"], dict):
                return [
                    self._item_to_qtree(results["qtrees"]["qtree-info"])
                ]
        logger.warn("list_qtrees: no entries found")
        return []

    @lru_cache(maxsize=100)
    def list_volumes(self):
        """Return a list of volumes of type :class:`~nidhogg.compatible.Volume`.

        :return: list of volumes
        :rtype: list of :class:`~nidhogg.compatible.Volume` or empty list
        :raises NidhoggException: if an error occurs
        """
        results = self.volume_list_info()["netapp"]["results"]
        if results.get("volumes", {}).get("volume-info", False):
            if isinstance(results['volumes']['volume-info'], list):
                return [
                    self._item_to_volume(item)
                    for item in results['volumes']['volume-info']
                ]
            elif isinstance(results['volumes']['volume-info'], dict):
                return [
                    self._item_to_volume(results['volumes']['volume-info'])
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
        return self._item_to_volume(self.volume_list_info(volume=volume)["netapp"]["results"]['volumes']['volume-info'])

    def list_snapshots(self, target_name, target_type="volume"):
        """Return list of snapshots for given volume.

        :param target_name: name of the volume
        :type target_name: str
        :param target_type: type of the volume
        :type target_type: str
        :return: list of snapshots
        :rtype: list of :class:`~nidhogg.compatible.Snapshot` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            target_name=target_name,
            target_type=target_type,
        )
        results = self.snapshot_list_info(**opts)["netapp"]["results"]
        if results.get("snapshots", {}).get("snapshot-info", False):
            if isinstance(results['snapshots']['snapshot-info'], list):
                return [
                    Snapshot(name=item['name'])
                    for item in results['snapshots']['snapshot-info']
                ]
            elif isinstance(results['snapshots']['snapshot-info'], dict):
                return [
                    Snapshot(name=results['snapshots']['snapshot-info']['name'])
                ]
        logger.warn("list_snapshots: no entries found")
        return []

    def get_quota(self, volume, qtree):
        """Return the quota of the specified qtree on the given volume.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree
        :type qtree: str
        :return: quota
        :rtype: :class:`~nidhogg.compatible.Quota`
        :raises NidhoggException: if an error occurs
        """
        return self._item_to_quota(
            self.quota_get_entry(**{
                'qtree': "",
                'quota-target': "/vol/{0}/{1}".format(volume, qtree),
                'quota-type': "tree",
                'volume': volume})["netapp"]["results"]
        )

    def list_quotas(self, volume):
        """Return a list of quota reports of the specified volume.

        :param volume: name of the volume
        :type volume: str
        :return: list of quota reports
        :rtype: :class:`~nidhogg.compatible.QuotaReport` or empty list
        :raises NidhoggException: if an error occurs
        """
        results = self.quota_report(volume=volume)["netapp"]["results"]
        if "error" in results:
            logger.warn(results["error"]["reason"])
            # TODO: sometimes volume not found, although it exists
            raise NidhoggException(results["error"]["reason"])

        if safe_get(safe_get(results, "quotas"), "quota"):
            if isinstance(results["quotas"]["quota"], list):
                return [
                    self._item_to_quota_report(item)
                    for item in results["quotas"]["quota"]
                ]
            elif isinstance(results["quotas"]["quota"], dict):
                return [
                    self._item_to_quota_report(results["quotas"]["quota"])
                ]
        logger.warn("list_quotas: no entries found")
        return []

    def _start_cifs_shares(self):
        return self.cifs_share_list_iter_start()

    def _get_cifs_shares(self, tag):
        return self.cifs_share_list_iter_next(tag=tag, maximum=1000000)

    def _end_cifs_shares(self, tag):
        return self.cifs_share_list_iter_end(tag=tag)

    def list_cifs_shares(self):
        """List all cifs shares.

        :return: list of cifs shares
        :rtype: list of :class:`~nidhogg.compatible.CifsShare` or empty list
        :raises NidhoggException: if an error occurs
        """
        tag = self._start_cifs_shares()["netapp"]["results"]["tag"]
        results = self._get_cifs_shares(tag=tag)["netapp"]["results"]
        self._end_cifs_shares(tag)
        if int(results['records']) > 1:
            return [
                CifsShare(path=item['mount-point'], share_name=item['share-name'])
                for item in results['cifs-shares']['cifs-share-info']
            ]
        elif int(results['records']) == 1:
            return [
                CifsShare(path=results['cifs-shares']['cifs-share-info']['mount-point'], share_name=results['cifs-shares']['cifs-share-info']['share-name'])
            ]
        logger.warning("list_cifs_shares: cifs shares found")
        return []

    def create_cifs_share(self, volume, qtree, share_name, group_name=None, comment=None, umask="007"):
        """Create a cifs share.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree
        :type qtree: str
        :param share_name: name of the share
        :type share_name: str
        :param group_name: force group if specified
        :type group_name: str
        :param comment: description of the share
        :type comment: str
        :param umask: file permission umask
        :type umask: str
        :raises NidhoggException: if an error occurs
        """
        opts = dict(
            path="/vol/{0}/{1}".format(volume, qtree),
            share_name=share_name,
            umask=umask
        )
        if group_name:
            opts['forcegroup'] = group_name
        if comment:
            opts['comment'] = comment
        self.cifs_share_add(**opts)

    def set_cifs_acl(self, share_name, user="everyone", right=ACL_READ, set_group_rights=False):
        """Set a single ACL for the specifed share.

        :param share_name: name of the share
        :type share_name: str
        :param user: name of a user or unix group (if set_group_rights = True)
        :type user: str
        :param right: right to be set, value must be one of :py:const:`~ACL_PERMISSIONS`
        :type right: str
        :param set_group_rights: if true, *user* param specifies a unix group name
        :type set_group_rights: bool
        :raises NidhoggException: if an error occurs
        :raises NidhoggException: if wrong right was set
        """
        # check permissions
        if right not in self.ACL_PERMISSIONS:
            raise NidhoggException("Permission {0} not in {1}.".format(right, self.ACL_PERMISSIONS))

        if set_group_rights:
            opts = dict(
                access_rights=right,
                share_name=share_name,
                unix_group_name=user,
                is_unixgroup="true"
            )
        else:
            opts = dict(
                access_rights=right,
                share_name=share_name,
                user_name=user
            )
        self.cifs_share_ace_set(**opts)

    def _start_cifs_acls(self, share_name):
        return self.cifs_share_acl_list_iter_start(share_name=share_name)

    def _get_cifs_acls(self, tag):
        return self.cifs_share_acl_list_iter_next(tag=tag, maximum="1")

    def _end_cifs_acls(self, tag):
        return self.cifs_share_acl_list_iter_end(tag=tag)

    def list_cifs_acls(self, share_name):
        """Return ACL of the specified share.

        :param share_name: name of the share
        :type share_name: str
        :return: list of ACEs (access control entries)
        :rtype: :class:`~nidhogg.compatible.ACE` or empty list
        :raises NidhoggException: if an error occurs
        """
        tag = self._start_cifs_acls(share_name=share_name)["netapp"]["results"]["tag"]
        results = self._get_cifs_acls(tag=tag)["netapp"]["results"]
        if safe_get(safe_get(safe_get(safe_get(results, "cifs-share-acls"), "cifs-share-acl-info"), "user-acl-info"), "access-rights-info"):
            name = results["cifs-share-acls"]["cifs-share-acl-info"]["share-name"]
            acls = results["cifs-share-acls"]["cifs-share-acl-info"]["user-acl-info"]["access-rights-info"]
            if isinstance(acls, list):
                self._end_cifs_acls(tag=tag)
                return [
                    self._item_to_ace(name, item)
                    for item in acls
                ]
            elif isinstance(acls, dict):
                self._end_cifs_acls(tag=tag)
                return [
                    self._item_to_ace(name, acls)
                ]
        self._end_cifs_acls(tag=tag)
        logger.warn("list_cifs_acls: no entries found")
        return []

    def delete_cifs_acl(self, share_name, user_or_group, is_group=False):
        """Delete cifs ACL of the specified user or group.

        :param share_name: name of the share
        :type share_name: str
        :param user_or_group: name of a user or group
        :type user_or_group: str
        :param is_group: if true, param *user_or_group* specifies a unix group name
        :type is_group: bool
        :raises NidhoggException: if an error occurs
        """
        if is_group:
            opts = dict(
                share_name=share_name,
                unix_group_name=user_or_group,
                is_unixgroup="true"
            )
        else:
            opts = dict(
                share_name=share_name,
                user_name=user_or_group,
                is_unixgroup="false"
            )
        self.cifs_share_ace_delete(**opts)

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
                user_or_group=ace["user_or_group"],
                is_group=ace["is_group"]
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
        self.quota_set_entry(
            volume=volume,
            qtree="",
            disk_limit=quota_in_kb,
            soft_disk_limit=int(round(quota_in_kb * 0.8)),  # use 80% of the given quota as warn-limit
            quota_target=quota_target,
            quota_type=quota_type
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
        self.quota_delete_entry(
            volume=volume,
            qtree="",
            quota_target=quota_target,
            quota_type=quota_type
        )

    def update_snapmirror(self, destination_volume, destination_qtree=None, source_filer=None, source_volume=None, source_qtree=None):
        """Trigger the snapmirror replication.

        If source_filer, source_volume and source_qtree (source location) are not specified (default),
        then the source in */etc/snapmirror.conf* for the destination path must be present.

        :param destination_volume: name of snapmirror destination volume
        :type destination_volume: str
        :param destination_qtree: name of snapmirror destination qtree
        :type destination_qtree: str
        :param source_filer: hostname of source filer
        :type source_filer: str
        :param source_volume: name of snapmirror source volume
        :type source_volume: str
        :param source_qtree: name of snapmirror source qtree
        :type source_qtree: str
        :raises NidhoggException: if an error occurs
        :raises NidhoggException: if source params are incomplete
        :raises NidhoggException: if qtree params are used, but incomplete
        """
        if bool(source_filer) ^ bool(source_volume):
            raise NidhoggException("Incomplete source params.")
        if source_qtree and not source_volume:
            raise NidhoggException("Param source_volume missing.")
        if destination_qtree and source_filer and not source_qtree:
            raise NidhoggException("Param source_qtree missing.")
        if source_qtree and not destination_qtree:
            raise NidhoggException("Param destination_qtree missing.")
        opts = dict()
        if destination_qtree:
            opts['destination_location'] = "/vol/{0}/{1}".format(destination_volume, destination_qtree)
        else:
            opts['destination_location'] = destination_volume
        if source_filer:
            if source_qtree:
                opts['source_location'] = "{0}:/vol/{1}/{2}".format(source_filer, source_volume, source_qtree)
            else:
                opts['source_location'] = "{0}:{1}".format(source_filer, source_volume)
        self.snapmirror_update(**opts)

    def update_snapmirror_with_snapshot(self, name, destination_volume, destination_qtree=None, source_filer=None, source_volume=None, source_qtree=None):
        """Update the named snapshot to the snapmirror destination.

        Use the specified snapshot name also for the snapshot to be created on the destination server if possible.

        If source_filer, source_volume and source_qtree (source location) are not specified (default),
        then the source in */etc/snapmirror.conf* for the destination path must be present.

        :param name: name of the snapshot
        :type name: str
        :param destination_volume: name of snapmirror destination volume
        :type destination_volume: str
        :param destination_qtree: name of snapmirror destination qtree
        :type destination_qtree: str
        :param source_filer: hostname of source filer
        :type source_filer: str
        :param source_volume: name of snapmirror source volume
        :type source_volume: str
        :param source_qtree: name of snapmirror source qtree
        :type source_qtree: str
        :raises NidhoggException: if an error occurs
        :raises NidhoggException: if source params are incomplete
        :raises NidhoggException: if qtree params are used, but incomplete
        :raises NidhoggException: if source contains no new data
        :raises NidhoggException: if destination is busy
        """
        if bool(source_filer) ^ bool(source_volume):
            raise NidhoggException("Incomplete source params.")
        if source_qtree and not source_volume:
            raise NidhoggException("Param source_volume missing.")
        if destination_qtree and source_filer and not source_qtree:
            raise NidhoggException("Param source_qtree missing.")
        if source_qtree and not destination_qtree:
            raise NidhoggException("Param destination_qtree missing.")
        opts = dict(
            source_snapshot=name,
            destination_snapshot=name,
        )
        if destination_qtree:
            opts['destination_location'] = "/vol/{0}/{1}".format(destination_volume, destination_qtree)
        else:
            opts['destination_location'] = destination_volume
        if source_filer:
            if source_qtree:
                opts['source_location'] = "{0}:/vol/{1}/{2}".format(source_filer, source_volume, source_qtree)
            else:
                opts['source_location'] = "{0}:{1}".format(source_filer, source_volume)
        self.snapmirror_update(**opts)

    def get_snapmirror_status(self, volume=None, qtree=None):
        """Get status of snapmirror replication pairs. If no params are provided, return all snapmirror status pairs.

        :param volume: name of source or destination volume
        :type volume: str
        :param qtree: name of source or destination qtree
        :type qtree: str
        :return: list of all snapmirror pair status
        :rtype: list of :class:`~nidhogg.compatible.SnapmirrorStatus` or empty list
        :raises NidhoggException: if an error occurs
        """
        opts = dict()
        if volume and qtree:
            opts['location'] = "/vol/{0}/{1}".format(volume, qtree)
        elif volume:
            opts['location'] = "{0}".format(volume)
        results = self.snapmirror_get_status(**opts)["netapp"]["results"]
        if results["is-available"] == "true":
            if results.get("snapmirror-status", {}).get("snapmirror-status-info", False):
                if isinstance(results["snapmirror-status"]["snapmirror-status-info"], list):
                    return [
                        self._item_to_snapmirrorstatus(item)
                        for item in results["snapmirror-status"]["snapmirror-status-info"]
                    ]
                elif isinstance(results["snapmirror-status"]["snapmirror-status-info"], dict):
                    return [
                        self._item_to_snapmirrorstatus(results["snapmirror-status"]["snapmirror-status-info"])
                    ]
        logger.warn("get_snapmirror_status: no entries found")
        return []

    def get_snapmirror_volume_status(self, volume):
        """Get status of a snapmirror volume.

        :param volume: name of volume
        :type volume: str
        :rtype: :class:`~nidhogg.compatible.SnapmirrorVolumeStatus`
        :raises NidhoggException: if an error occurs
        """
        return self._item_to_snapmirrorvolumestatus(self.snapmirror_get_volume_status(
            volume=volume
        )["netapp"]["results"])

    def create_snapshot(self, volume, name):
        """Create a snapshot.

        :param volume: name of the volume
        :type volume: str
        :param name: name of the snapshot
        :type name: str
        :raises NidhoggException: if an error occurs
        """
        self.snapshot_create(volume=volume, snapshot=name)

    def list_snapmirror_destinations(self, volume=None, qtree=None):
        """Not implemented yet for seven mode."""
        raise NotImplementedError()     # pragma: no cover
