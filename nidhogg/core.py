# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    # py2
    from urlparse import urlparse
    from backports.functools_lru_cache import lru_cache
except ImportError:     # pragma: no cover
    # py3
    from urllib.parse import urlparse
    from functools import lru_cache

from cached_property import cached_property
import xml
import dicttoxml
import collections
import logging
from abc import ABCMeta, abstractmethod
# Python 2 and 3
from six import with_metaclass

from .http import NidhoggHttp
from .compatible import QuotaReport, Quota, QTree, VolumeWithQuotaRatio, Volume, SnapmirrorStatus
from .utils import underline_to_dash

# used the capture urllib3 wannings
logging.captureWarnings(True)
logger = logging.getLogger(__name__)

try:
    import pkg_resources
    version = pkg_resources.get_distribution('nidhogg').version
except:  # pragma: no cover
    version = 'development'


# after a quota resize wait max. 2 min til finished
# max wait time is QUOTA_RESIZE_WAIT_TIME * QUOTA_RESIZE_WAIT_CYCLES
QUOTA_RESIZE_WAIT_TIME = 6
QUOTA_RESIZE_WAIT_CYCLES = 20


class NidhoggException(Exception):
    """Exception wrapper."""

    pass


class Nidhogg(with_metaclass(ABCMeta)):
    """This is the base class for connecting to a NETAPP filer.

    It provides functions that have 7-mode filers and cluster-mode filers in common.

    Subclasses:

    * :class:`~nidhogg.sevenmode.SevenMode`
    * :class:`~nidhogg.clustermode.ClusterMode`
    """

    def __init__(self, url, username, password, major, minor, verify, http=NidhoggHttp):
        """Init conncetion to filer."""
        self.url = url
        self.major = major
        self.minor = minor
        self.http = http(url, username, password, verify)
        self.xmlns = "http://www.netapp.com/filer/admin"
        self.nmsdk_version = version
        self.nmsdk_language = "python"
        self.nmsdk_app = "Nidhogg"

    def __getattr__(self, api):
        """Try to invoke unimplemented API calls directly."""
        def _api_wrapper(**kwargs):
            return self._do(api, **kwargs)
        return _api_wrapper

    def _do(self, api, **kwargs):
        """Invoke wrapper, returns a xmldict."""
        # replace _ -> -
        params = underline_to_dash(kwargs)
        req = self._create_request(**{api.replace("_", "-"): params})
        logger.debug("request: {0}".format(req))
        r = self.http.invoke_request(req)
        logger.debug("response: {0}".format(r))
        try:
            self.xmldict = self.http.parse_xml_reply(r)
        except xml.parsers.expat.ExpatError:
            logger.exception("exception on {}".format(self.vserver))
            raise NidhoggException(r + " (host: {})".format(self.vserver))

        if self.xmldict["netapp"]["results"]['@status'] == "failed":
            logger.error("exception on {}".format(self.vserver))
            logger.error(self.xmldict["netapp"]["results"]['@reason'])
            logger.error("{0} failed with params {1}".format(api, params))
            raise NidhoggException(self.xmldict["netapp"]["results"]['@reason'] + " (host: {})".format(self.vserver))
        return self.xmldict

    def _create_request(self, **kwargs):
        xml_request = dicttoxml.dicttoxml(collections.OrderedDict(**kwargs), root=False, attr_type=False)
        return """
            <?xml version='1.0' encoding='utf-8'?>
            <netapp version='{0.major}.{0.minor}'
                    xmlns='{0.xmlns}'
                    nmsdk_version='{0.nmsdk_version}'
                    nmsdk_language='{0.nmsdk_language}'
                    nmsdk_app='{0.nmsdk_app}'>
                {1}
            </netapp>""".strip().replace("            ", "").format(self, xml_request.decode("utf-8"))

    def _item_to_quota(self, item):
        """Convert to byte (API returns sizes in kbyte) to be consistent with other sizes (i.e. volume info)."""
        return Quota(
            disk_limit=float(item['disk-limit']) * 1024 if item['disk-limit'].isdigit() else -1,
            soft_disk_limit=float(item['soft-disk-limit']) * 1024 if item['soft-disk-limit'].isdigit() else -1,
            threshold=float(item['threshold']) * 1024 if item['threshold'].isdigit() else -1,
            file_limit=float(item['file-limit']) if item['file-limit'].isdigit() else -1,
            soft_file_limit=float(item['soft-file-limit']) if item['soft-file-limit'].isdigit() else -1,
        )

    def _item_to_quota_report(self, item):
        return QuotaReport(
            disk_used=float(item['disk-used']) * 1024 if item['disk-used'].isdigit() else -1,
            disk_limit=float(item['disk-limit']) * 1024 if item['disk-limit'].isdigit() else -1,
            soft_disk_limit=float(item['soft-disk-limit']) * 1024 if item['soft-disk-limit'].isdigit() else -1,
            threshold=float(item['threshold']) * 1024 if item['threshold'].isdigit() else -1,
            files_used=float(item['files-used']) if item['files-used'].isdigit() else -1,
            file_limit=float(item['file-limit']) if item['file-limit'].isdigit() else -1,
            soft_file_limit=float(item['soft-file-limit']) if item['soft-file-limit'].isdigit() else -1,
            quota_target=item['quota-target'],
            tree=item['tree'],
        )

    def _item_to_qtree(self, item):
        return QTree(
            qtree=item['qtree'],
            status=item['status'],
            security_style=item['security-style'],
        )

    def _item_to_snapmirrorstatus(self, item):
        return SnapmirrorStatus(
            # 7mode and cluster mode
            source_location=item["source-location"],
            destination_location=item["destination-location"],
            lag_time=item["lag-time"],
            last_transfer_from=item["last-transfer-from"],
            last_transfer_size=item["last-transfer-size"],
            last_transfer_duration=item["last-transfer-duration"],
            last_transfer_type=item['last-transfer-type'] if 'last-transfer-type' in item else None,
            # sevenmode
            status=item["status"] if 'status' in item else None,
            transfer_progress=item["transfer-progress"] if 'transfer-progress' in item else None,
            mirror_timestamp=item["mirror-timestamp"] if 'mirror-timestamp' in item else None,
            contents=item["contents"] if 'contents' in item else None,
            state=item["state"] if 'state' in item else None,
            # sevenmode optional
            base_snapshot=item['base-snapshot'] if 'base-snapshot' in item else None,
            current_transfer_error=item['current-transfer-error'] if 'current-transfer-error' in item else None,
            current_transfer_type=item['current-transfer-type'] if 'current-transfer-type' in item else None,
            inodes_replicated=item['inodes-replicated'] if 'inodes-replicated' in item else None,
            replication_ops=item['replication-ops'] if 'replication-ops' in item else None,
            # cluster mode
            break_failed_count=item['break-failed-count'] if 'break-failed-count' in item else None,
            break_successful_count=item['break-successful-count'] if 'break-successful-count' in item else None,
            destination_volume=item['destination-volume'] if 'destination-volume' in item else None,
            destination_volume_node=item['destination-volume-node'] if 'destination-volume-node' in item else None,
            destination_vserver=item['destination-vserver'] if 'destination-vserver' in item else None,
            destination_vserver_uuid=item['destination-vserver-uuid'] if 'destination-vserver-uuid' in item else None,
            exported_snapshot=item['exported-snapshot'] if 'exported-snapshot' in item else None,
            exported_snapshot_timestamp=item['exported-snapshot-timestamp'] if 'exported-snapshot-timestamp' in item else None,
            is_constituent=item['is-constituent'] if 'is-constituent' in item else None,
            is_healthy=item['is-healthy'] if 'is-healthy' in item else None,
            last_transfer_end_timestamp=item['last-transfer-end-timestamp'] if 'last-transfer-end-timestamp' in item else None,
            last_transfer_network_compression_ratio=item['last-transfer-network-compression-ratio'] if 'last-transfer-network-compression-ratio' in item else None,
            max_transfer_rate=item['max-transfer-rate'] if 'max-transfer-rate' in item else None,
            mirror_state=item['mirror-state'] if 'mirror-state' in item else None,
            newest_snapshot=item['newest-snapshot'] if 'newest-snapshot' in item else None,
            newest_snapshot_timestamp=item['newest-snapshot-timestamp'] if 'newest-snapshot-timestamp' in item else None,
            opmask=item['opmask'] if 'opmask' in item else None,
            policy=item['policy'] if 'policy' in item else None,
            policy_type=item['policy-type'] if 'policy-type' in item else None,
            relationship_control_plane=item['relationship-control-plane'] if 'relationship-control-plane' in item else None,
            relationship_group_type=item['relationship-group-type'] if 'relationship-group-type' in item else None,
            relationship_id=item['relationship-id'] if 'relationship-id' in item else None,
            relationship_status=item['relationship-status'] if 'relationship-status' in item else None,
            relationship_type=item['relationship-type'] if 'relationship-type' in item else None,
            resync_failed_count=item['resync-failed-count'] if 'resync-failed-count' in item else None,
            resync_successful_count=item['resync-successful-count'] if 'resync-successful-count' in item else None,
            source_volume=item['source-volume'] if 'source-volume' in item else None,
            source_vserver=item['source-vserver'] if 'source-vserver' in item else None,
            source_vserver_uuid=item['source-vserver-uuid'] if 'source-vserver-uuid' in item else None,
            total_transfer_bytes=item['total-transfer-bytes'] if 'total-transfer-bytes' in item else None,
            total_transfer_time_secs=item['total-transfer-time-secs'] if 'total-transfer-time-secs' in item else None,
            update_failed_count=item['update-failed-count'] if 'update-failed-count' in item else None,
            update_successful_count=item['update-successful-count'] if 'update-successful-count' in item else None,
            vserver=item['vserver'] if 'vserver' in item else None,
            # helper state, mapping relationship-status (cluster mode) and status (7mode) to snapmirror-status
            snapmirror_status=item['relationship-status'].lower() if self.clustered else item["status"].lower(),
        )

    #
    # cached PROPERTIES
    #
    @cached_property
    def vserver(self):
        """Hostname of the connected filer.

        :return: hostname
        :rtype: str
        """
        return str(urlparse(self.url).hostname).split(".")[0]

    @cached_property
    def vserver_fqdn(self):
        """FQDN of the connected filer.

        :return: FQDN of the filer
        :rtype: str
        """
        return str(urlparse(self.url).hostname)

    @cached_property
    def clustered(self):
        """True if the filer is a cluster-mode filer, false otherwise.

        :rtype: boolean
        """
        results = self.system_get_version()['netapp']['results']
        return 'is-clustered' in results and results['is-clustered'] == "true"

    @cached_property
    def ontapi_version(self):
        """ONTAPI version of the connected filer.

        :return: ontapi version
        :rtype: str
        """
        # get result
        result = self.system_get_ontapi_version()['netapp']['results']
        # split afterwards, does not work the short way ?:|
        return "{0}.{1}".format(result['major-version'], result['minor-version'])

    @cached_property
    def has_forcegroup(self):
        """Check if this cifs share feature is available.

        :return: true, if feature is available
        :rtype: bool
        """
        # sevenmode supports force group
        if not self.clustered:
            return True
        # clustermode with ontapi 1.30 and onwards
        result = self.system_get_ontapi_version()['netapp']['results']
        return int(result['major-version']) >= 1 and int(result['minor-version']) >= 30

    @cached_property
    def apis(self):
        """List of API commands available with the current credentials.

        :return: list of API commands
        :rtype: list of str or empty list
        """
        try:
            return [
                item["name"]
                for item in self.system_api_list()["netapp"]["results"]["apis"]["system-api-info"]
            ]
        except NidhoggException:
            return []

    #
    # COMMON API FUNCTIONS
    #
    def list_snapable_volumes(self):
        """Return a list of *snapable* volumes.

        That means, ignore volumes that are used as a snapmirror destination.

        :return: list of snapable volumes
        :rtype: list of :class:`~nidhogg.compatible.Volume`
        :raises NidhoggException: if an error occurs
        """
        vols = []
        for vol in self.list_volumes():
            if vol['state'] == 'online' and vol['snapable']:
                vols.append(vol)
        return vols

    def delete_snapshot(self, volume, name):
        """Delete a snapshot.

        :param volume: name of the volume
        :type volume: str
        :param name: name of the snapshot
        :type name: str
        :raises NidhoggException: if an error occurs
        """
        return self.snapshot_delete(volume=volume, snapshot=name)

    def create_qtree(self, volume, qtree, mode="007"):
        """Create a qtree on the specified volume.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree to be created
        :type name: str
        :param mode: initial file system permissions of the qtree
        :type mode: str
        :raises NidhoggException: if an error occurs
        """
        self.qtree_create(volume=volume, qtree=qtree, mode=mode)

    def delete_qtree(self, volume, qtree, force=False):
        """Delete a qtree on the specified volume.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree to be deleted
        :type qtree: str
        :param force: force deletion if true
        :type force: bool
        :raises NidhoggException: if an error occurs
        """
        self.qtree_delete(force=str(bool(force)), qtree="/vol/{0}/{1}".format(volume, qtree))

    def delete_cifs_share(self, share_name):
        """Delete the share with the given name.

        :param share_name: name of the share
        :type share_name: str
        :raises NidhoggException: if an error occurs
        """
        self.cifs_share_delete(share_name=share_name)

    def exists_qtree(self, volume, qtree):
        """Check if a qtree exits.

        :param volume: name of the volume
        :type volume: str
        :param qtree: name of the qtree
        :type qtree: str
        :return: true, if the qtree exists
        :rtype: bool
        :raises NidhoggException: if an error occurs
        """
        return len([qt for qt in self.list_qtrees(volume) if qt['qtree'] == qtree]) > 0

    #
    # cached API functions
    #
    @lru_cache(maxsize=100)
    def get_allocated_quota_size(self, volume):
        """Return the sum of all quotas of the specified volume.

        :param volume: name of the volume
        :type volume: str
        :return: sum of all qtree quotas on this volume in byte
        :rtype: int
        :raises NidhoggException: if an error occurs
        """
        # only use those where a tree is specified
        return sum(quota['disk_limit'] for quota in self.list_quotas(volume) if quota['tree'])

    @lru_cache(maxsize=100)
    def get_allocated_quota_ratio(self, volume, volume_size_total=None):
        """Return the ratio *allocated quota size / volume size*.

        :param volume: name of the volume
        :type volume: str
        :param volume_size_total: if specified we have the total size already from a previous API call
        :type volume_size_total: int
        :return: ratio *allocated quota size / volume size*
        :rtype: int
        :raises NidhoggException: if an error occurs
        """
        # shortcut: if specified we have the size already from a previous api call
        if volume_size_total:
            return self.get_allocated_quota_size(volume) / volume_size_total
        return self.get_allocated_quota_size(volume) / self.volume_info(volume)["size_total"]

    def get_volumes_with_quota_info(self, filter_volume_names=[]):
        """Return a list of snapable volumes of type :class:`~nidhogg.compatible.VolumeWithQuotaRatio`.

        :param filter_volume_names: consider only volumes that are in this list
        :type filter_volume_names: list of str
        :return: list of project home volumes
        :rtype: list of :class:`~nidhogg.compatible.VolumeWithQuotaRatio`
        :raises NidhoggException: if an error occurs
        """
        volumes = []
        # get all volumes with type "rw"
        for v in self.list_snapable_volumes():
            # return only volumes with matching volume names if specified
            if filter_volume_names:
                if v["name"] not in filter_volume_names:
                    logger.debug("filer: {0}, skipped volume '{1}' because not in filter".format(
                        self.vserver_fqdn,
                        v["name"])
                    )
                    continue
            project_volume = VolumeWithQuotaRatio(
                quota_size=self.get_allocated_quota_size(volume=v["name"]),
                quota_ratio=self.get_allocated_quota_ratio(
                    volume=v["name"],
                    volume_size_total=v["size_total"]),
                **v
            )
            volumes.append(project_volume)
        return volumes

    def get_volumes(self, filter_volume_names=[]):
        """Return a list of snapable volumes of type :class:`~nidhogg.compatible.Volume`.

        :param filter_volume_names: consider only volumes that are in this list
        :type filter_volume_names: list of str
        :return: list of user home volumes
        :rtype: list of :class:`~nidhogg.compatible.Volume`
        :raises NidhoggException: if an error occurs
        """
        volumes = []
        # get all volumes with type "rw"
        for v in self.list_snapable_volumes():
            # return only volumes with matching volume names
            if filter_volume_names:
                if v["name"] not in filter_volume_names:
                    logger.debug("filer: {0}, skipped volume '{1}' because not in filter".format(
                        self.vserver_fqdn,
                        v["name"])
                    )
                    continue
            volumes.append(Volume(**v))
        return volumes

    #
    # API FUNCTIONS implemented in subclasses
    #
    @abstractmethod
    def list_qtrees(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_qtrees` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_qtrees` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def list_volumes(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_volumes` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_volumes` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def volume_info(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.volume_info` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.volume_info` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def list_snapshots(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_snapshots` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_snapshots` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def get_quota(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.get_quota` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.get_quota` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def list_quotas(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_quotas` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_quotas` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def list_cifs_shares(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_cifs_shares` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_cifs_shares` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def create_cifs_share(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.create_cifs_share` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.create_cifs_share` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def set_cifs_acl(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.set_cifs_acl` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.set_cifs_acl` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def list_cifs_acls(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_cifs_acls` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_cifs_acls` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def delete_cifs_acl(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.delete_cifs_acl` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.delete_cifs_acl` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def delete_cifs_acls(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.delete_cifs_acls` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.delete_cifs_acls` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def set_quota(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.set_quota` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.set_quota` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def delete_quota(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.delete_quota` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.delete_quota` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def update_snapmirror(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.update_snapmirror` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.update_snapmirror` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def update_snapmirror_with_snapshot(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.update_snapmirror_with_snapshot` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.update_snapmirror_with_snapshot` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def get_snapmirror_status(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.get_snapmirror_status` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.get_snapmirror_status` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def get_snapmirror_volume_status(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.get_snapmirror_volume_status` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.get_snapmirror_volume_status` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def create_snapshot(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.create_snapshot` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.create_snapshot` (ClusterMode)
        """
        pass    # pragma: no cover

    @abstractmethod
    def list_snapmirror_destinations(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_snapmirror_destinations` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_snapmirror_destinations` (ClusterMode)
        """
        pass    # pragma: no cover
