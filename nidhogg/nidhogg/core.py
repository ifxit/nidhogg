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

from .http import NidhoggHttp
from .compatible import QuotaReport, Quota, QTree, VolumeWithQuotaRatio, Volume
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


class Nidhogg(object):
    """This is the base class for connecting to a NETAPP filer.

    It provides functions that have 7-mode filers and cluster-mode filers in common.

    Subclasses:

    * :class:`~nidhogg.sevenmode.SevenMode`
    * :class:`~nidhogg.clustermode.ClusterMode`
    """

    def __init__(self, url, username, password, major, minor, http=NidhoggHttp):
        """Init conncetion to filer."""
        self.url = url
        self.major = major
        self.minor = minor
        self.http = http(url, username, password)
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
        return self.system_get_version()['netapp']['results']['is-clustered'] == "true"

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

    def create_snapshot(self, volume, name):
        """Create a snapshot.

        :param volume: name of the volume
        :type volume: str
        :param name: name of the snapshot
        :type name: str
        :raises NidhoggException: if an error occurs
        """
        return self.snapshot_create(volume=volume, snapshot=name)

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
    def list_qtrees(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_qtrees` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_qtrees` (ClusterMode)
        """
        pass    # pragma: no cover

    def list_volumes(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_volumes` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_volumes` (ClusterMode)
        """
        pass    # pragma: no cover

    def volume_info(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.volume_info` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.volume_info` (ClusterMode)
        """
        pass    # pragma: no cover

    def list_snapshots(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_snapshots` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_snapshots` (ClusterMode)
        """
        pass    # pragma: no cover

    def get_quota(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.get_quota` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.get_quota` (ClusterMode)
        """
        pass    # pragma: no cover

    def list_quotas(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_quotas` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_quotas` (ClusterMode)
        """
        pass    # pragma: no cover

    def list_cifs_shares(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_cifs_shares` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_cifs_shares` (ClusterMode)
        """
        pass    # pragma: no cover

    def create_cifs_share(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.create_cifs_share` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.create_cifs_share` (ClusterMode)
        """
        pass    # pragma: no cover

    def set_cifs_acl(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.set_cifs_acl` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.set_cifs_acl` (ClusterMode)
        """
        pass    # pragma: no cover

    def list_cifs_acls(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.list_cifs_acls` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.list_cifs_acls` (ClusterMode)
        """
        pass    # pragma: no cover

    def delete_cifs_acl(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.delete_cifs_acl` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.delete_cifs_acl` (ClusterMode)
        """
        pass    # pragma: no cover

    def delete_cifs_acls(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.delete_cifs_acls` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.delete_cifs_acls` (ClusterMode)
        """
        pass    # pragma: no cover

    def set_quota(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.set_quota` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.set_quota` (ClusterMode)
        """
        pass    # pragma: no cover

    def delete_quota(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.delete_quota` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.delete_quota` (ClusterMode)
        """
        pass    # pragma: no cover

    def update_snapmirror(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.update_snapmirror` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.update_snapmirror` (ClusterMode)
        """
        pass    # pragma: no cover

    def update_snapmirror_with_snapshot(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.update_snapmirror_with_snapshot` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.update_snapmirror_with_snapshot` (ClusterMode)
        """
        pass    # pragma: no cover

    def get_snapmirror_status(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.get_snapmirror_status` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.get_snapmirror_status` (ClusterMode)
        """
        pass    # pragma: no cover

    def get_snapmirror_volume_status(self, *args, **kwargs):
        """See sub classes.

        * Go to :py:meth:`~.SevenMode.get_snapmirror_volume_status` (SevenMode)
        * Go to :py:meth:`~.ClusterMode.get_snapmirror_volume_status` (ClusterMode)
        """
        pass    # pragma: no cover
