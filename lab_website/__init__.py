'''Package initialisation for the lab_website project.

Optionally routes Django's MySQL backend through PyMySQL instead of
mysqlclient.  This exists because the conda build of mysqlclient 2.2.7 on the
RHEL server cannot load the mysql_native_password client plugin -- it searches
for `<conda-prefix>/lib/plugin/mysql_native_password.so`, which conda does not
ship, and fails with OperationalError 2059.  That plugin is supposed to be
built into libmysqlclient, so this is a packaging defect, not a server or
credentials problem (see https://github.com/PyMySQL/mysqlclient/issues/761).

PyMySQL is pure Python and performs the authentication handshake itself, so it
sidesteps the missing plugin entirely.  It also reports a mysqlclient-shaped
version_info of its own -- (2, 2, 8, 'final', 1) in PyMySQL 1.2.0 -- which
already satisfies the ">= 2.2.1" check in django.db.backends.mysql.base, so
nothing needs to be spoofed here.

This is opt-in via the USE_PYMYSQL environment variable rather than
unconditional, because this file is tracked in git: hosts with a working
mysqlclient (production, local development) must keep using it, since that is
the driver Django officially supports.  Set USE_PYMYSQL=1 in the environment of
the affected host only -- both in the service definition that runs gunicorn and
in any shell used for manage.py.
'''

import os

if os.environ.get('USE_PYMYSQL'):
    import pymysql

    pymysql.install_as_MySQLdb()
