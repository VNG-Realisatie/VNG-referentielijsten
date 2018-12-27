Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess vrl-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/vrl/log/apache2/error.log"
        CustomLog "/srv/sites/vrl/log/apache2/access.log" common

        WSGIProcessGroup vrl-<target>

        Alias /media "/srv/sites/vrl/media/"
        Alias /static "/srv/sites/vrl/static/"

        WSGIScriptAlias / "/srv/sites/vrl/src/vrl/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-vrl-<target>]
    user = <user>
    command = /srv/sites/vrl/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/vrl/src/vrl/wsgi/wsgi_<target>.py
    home = /srv/sites/vrl/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/vrl/log/uwsgi_err.log
    stdout_logfile = /srv/sites/vrl/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_vrl_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/vrl/log/nginx-access.log;
      error_log /srv/sites/vrl/log/nginx-error.log;

      location /500.html {
        root /srv/sites/vrl/src/vrl/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/vrl/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/vrl/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_vrl_<target>;
      }
    }
