#!/bin/sh

#
# IMPORTANT: To use, do the folling:
#
# 1. Change 'NAME' variable to the name of your project. E.g. "bednets_for_nigeria"
# 2. Place this file in the TOP-LEVEL of your project, right where 'manage.py' is
# 3. Link it into /etc/init.d e.g. > ln -s /usr/local/my_project/rapidsms-init.sh /etc/init.d/
# 4. Add it to the runlevels, on Ubuntu/Debian there is a nice tool to do this for you:
#    > sudo update-rc.d rapidsms-init.sh defaults
#
# NOTE: If you want to run multiple instances of RapidSMS, just put this init file in each project dir,
#       set a different NAME for each project, link it into /etc/init.d with _different_ names,
#       and add _each_ script to the runlevels.
#

### BEGIN INIT INFO
# Provides:          amatd daemon instance
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts instances of rapidsms router and web server
# Description:       starts instance of rapidsms router and web server using start-stop-daemon
### END INIT INFO

# set -e

ME=`readlink -f $0`

############### EDIT ME ##################
DJANGO_NAME="fhossapi_server"
DJANGO_PATH="/opt/fhossapi_server"
DJANGO_CMD=$DJANGO_PATH/manage.py
RUN_AS=root
SERVER_IP=0.0.0.0
SERVER_PORT=8081
############### END EDIT ME ##################
test -x $DAEMON_CMD || exit 0

do_start() {
    echo -n "Starting $DJANGO_NAME...  "
    start-stop-daemon -d $DJANGO_PATH -c $RUN_AS --start --background --exec $DJANGO_CMD runserver $SERVER_IP:$SERVER_PORT
    echo "Started"
}

do_stop() {
    echo -n "Stopping $DJANGO_NAME...  "
    for i in `ps aux | grep -i "manage.py runserver" | grep -v grep | awk '{print $2}' ` ; do
        kill -9 $i
    done
    echo "Stopped"
}

do_restart() {
    do_stop
    sleep 2
    do_start
}

case "$1" in
  start)
        do_start
        ;;

  stop)
        do_stop
        ;;

  restart|force-reload)
	do_restart
        ;;

  *)
        echo "Usage: $ME {start|stop|restart|force-reload}" >&2
        exit 1
        ;;
esac

exit 0
