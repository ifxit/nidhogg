CHANGELOG
=========

v3.9.0
------

Parameter *share_properties* added to :py:meth:`~.ClusterMode.create_cifs_share` (ClusterMode).
Default is None.


v3.8.0
------

Update requests library.


v3.7.1
------

Parameter *vscan_fileop_profile* added to :py:meth:`~.ClusterMode.create_cifs_share` (ClusterMode).
Default is "standard".


v3.6.2
------

Method :py:meth:`~.ClusterMode.list_snapmirror_destinations` (ClusterMode) added.


v3.6.1
------

Method :py:meth:`~.ClusterMode.get_snapmirror_status` (ClusterMode) added.
Method :py:meth:`~.SevenMode.get_snapmirror_status` (SevenMode) changed.
Returning dict contains now the key *snapmirror_status*. This key returns the current state of the
snapmirror replication process and can be used for both modes.


v3.6.0
------

* Method :py:meth:`~.ClusterMode.update_snapmirror` (ClusterMode) added.
* Method :py:meth:`~.ClusterMode.update_snapmirror_with_snapshot` (ClusterMode) added.
* Method :py:meth:`~.ClusterMode.create_snapshot` (ClusterMode) changed. Optional *label* added.


v3.5.0
------

Parameter *verify* added to :py:func:`nidhogg.get_netapp`.

If true, it checks the certificate of the filer. Default is false.


v3.3
----

New *list_cifs_shares* method.

* See :py:meth:`~.SevenMode.list_cifs_shares` (SevenMode)
* See :py:meth:`~.ClusterMode.list_cifs_shares` (ClusterMode)

PEP8 fixes


v3.2
----

setup.py fixes


v3.1
----

Travis testing

setup.py fixes


v3.00
-----

First public release.


v2.14
-----

Method :py:meth:`~.SevenMode.update_snapmirror` (SevenMode) changed.
Method :py:meth:`~.SevenMode.update_snapmirror_with_snapshot` (SevenMode) changed.
Param *source_filer*, *source_volume* and *source_qtree* introduced.

Update a qtree on a snapmirror destination. Connect to the destination filer,
specify destination volume and qtree, source filer, volume and qtree and invoke command.

.. attention::

    If *source_filer*, *source_volume* and *source_qtree* (source location) are not specified (default),
    then the source in */etc/snapmirror.conf* for the destination path must be present.

Example:

    .. code-block:: python

        import nidhogg
        dst = nidhogg.get_netapp("filer13.example.com", "<username>", "<password>")
        dst.update_snapmirror_with_snapshot(
            name="userdir"
            destination_volume="sm_filer47_nidhoggtest",
            destination_qtree="nidhoggtest",
            source_filer="filer47.example.com",
            source_volume="nidhoggtest",
            source_qtree="nidhoggtest"
        )


Method :py:meth:`~.SevenMode.get_snapmirror_volume_status` (SevenMode) introduced.
Get details about snapmirror status of the specified volume.

Example:

    .. code-block:: python

        import nidhogg
        dst = nidhogg.get_netapp("filer13.example.com", "<username>", "<password>")
        dst.get_snapmirror_volume_status("sm_filer48_userhome_LCP")
        >> {'is_source': False, 'is_destination': True, 'is_transfer_broken': False, 'is_transfer_in_progress': False}


Waiting time for the quota resize operation to finish increased to 2 minutes.

* See :py:meth:`~.SevenMode.set_quota` (SevenMode)
* See :py:meth:`~.ClusterMode.set_quota` (ClusterMode)


v2.13
-----

Method :py:meth:`~.SevenMode.update_snapmirror_with_snapshot` (SevenMode) introduced.
Trigger the snapmirror replication using the named snapshot. Connect to the destination filer,
specify snapshot name and destination volume and invoke command.

Example:

    .. code-block:: python

        import nidhogg
        filer = nidhogg.get_netapp("filer99.example.com", "<username>", "<password>")
        filer.update_snapmirror_with_snapshot("nightly.1", "sq_filer99_test001", "smtest")


v2.12
-----

Method :py:meth:`~.SevenMode.get_snapmirror_status` (SevenMode) introduced.
Check the status of snapmirror relations. Connect to the destination filer,
specify volume of source or destination (optional) and qtree of source or
destination (optional) and invoke command.

Example:

    .. code-block:: python

        import nidhogg
        filer = nidhogg.get_netapp("filer99.example.com", "<username>", "<password>")
        # return status of all snapmirror relations
        status_list = filer.get_snapmirror_status()
        # return status of snapmirror relations of specified volume
        status_list = filer.get_snapmirror_status("sq_filer99_test001")
        # return status of snapmirror relations of specified volume and qtree
        status_list = filer.get_snapmirror_status("sq_filer99_test001", "smtest")


v2.11
-----

Method :py:meth:`~.SevenMode.update_snapmirror` (SevenMode) introduced.
Trigger the snapmirror replication. Connect to the destination filer,
specify destination volume and qtree (optional) and invoke command.

Example:

    .. code-block:: python

        import nidhogg
        filer = nidhogg.get_netapp("filer99.example.com", "<username>", "<password>")
        filer.update_snapmirror("sq_filer99_test001", "smtest")

v2.8
----

Param *local_volumes_only* removed from *list_volumes* (ClusterMode).

This 'feature' removed all volumes where the *owning_vserver != hostname* (hostname is derived
from the connection string). So, if you connected to the filer via DNS alias,
no volumes were found.

Originally it was used to filter volumes when connecting to a filer cluster. Not used in
production mode.

* See :py:meth:`~.ClusterMode.list_volumes` (ClusterMode)


v2.7
----

Method :py:meth:`~.ClusterMode.create_cifs_share` (ClusterMode) now also uses param *group_name*.
Cluster-mode filers with ONTAPI 1.3 supports "force group name".

Method :py:meth:`~.ClusterMode.set_cifs_acl` (ClusterMode) now sets also the correct
*user-group-type* for the specified user or group:

* if param *set_group_rights* is True, *user-group-type* is "unix_group"
* if param *set_group_rights* is False, *user-group-type* is "unix_user"
* if param *set_group_rights* is None, *user-group-type* is "windows"


v2.6
----

Param *user_name* removed from *create_cifs_share*. Had no effect.

* See :py:meth:`~.SevenMode.create_cifs_share` (SevenMode)
* See :py:meth:`~.ClusterMode.create_cifs_share` (ClusterMode)
