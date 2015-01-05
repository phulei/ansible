#!/bin/bash
# chkconfig: 2345 99 01
# description: Cassandra

. /etc/rc.d/init.d/functions

CASSANDRA_HOME={{ cassandra_base_directory }}/{{ cassandra_directory }}
CASSANDRA_BIN=$CASSANDRA_HOME/bin/cassandra
CASSANDRA_NODETOOL=$CASSANDRA_HOME/bin/nodetool
CASSANDRA_LOG=/var/log/cassandra.log
CASSANDRA_PID=${CASSANDRA_HOME}/cassandra.pid
CASSANDRA_LOCK=/var/lock/subsys/cassandra
PROGRAM="cassandra"
CASSANDRA_USER="cassandra"
CASSANDRA_group="cassandra"

if [ ! -f $CASSANDRA_BIN ]; then
  echo "File not found: $CASSANDRA_BIN"
  exit 1
fi

RETVAL=0

start() {
  if [ -f $CASSANDRA_PID ] && checkpid `cat $CASSANDRA_PID`; then
    echo "Cassandra is already running."
    exit 0
  fi
  echo -n $"Starting $PROGRAM: "
  daemon --user $CASSANDRA_USER $CASSANDRA_BIN -p $CASSANDRA_PID >> $CASSANDRA_LOG 2>&1
  usleep 500000
  RETVAL=$?
  if [ $RETVAL -eq 0 ]; then
    touch $CASSANDRA_LOCK
    echo_success
  else
    echo_failure
  fi
  echo
  return $RETVAL
}

stop() {
  if [ ! -f $CASSANDRA_PID ]; then
    echo "Cassandra is already stopped."
    exit 0
  fi
  echo $" Disabling thrift..."
  $CASSANDRA_NODETOOL -h localhost disablethrift
  if [[ $? -ne 0 ]]; then
    echo -n " Unable to disable thrift."
  fi
  sleep 5

  echo $" Disabling gossip..."
  $CASSANDRA_NODETOOL -h localhost disablegossip
  if [[ $? -ne 0 ]]; then
    echo -n " Unable to disable gossip."
  fi
  sleep 5

  echo $" Draining..."
  $CASSANDRA_NODETOOL -h localhost drain
  if [[ $? -ne 0 ]]; then
    echo -n " Could not drain."
  fi
  sleep 5

  echo -n $"Stopping $PROGRAM: "
  if kill `cat $CASSANDRA_PID`; then
    RETVAL=0
    rm -f $CASSANDRA_LOCK
    echo_success
  else
    RETVAL=1
    echo_failure
  fi
  echo
  [ $RETVAL = 0 ]
}

status_fn() {
  if [ -f $CASSANDRA_PID ] && checkpid `cat $CASSANDRA_PID`; then
    echo "Cassandra is running."
    exit 0
  else
    echo "Cassandra is stopped."
    exit 1
  fi
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  status)
    status_fn
    ;;
  restart)
    stop
    sleep 10
    start
    ;;
  *)
    echo $"Usage: $PROGRAM {start|stop|restart|status}"
    RETVAL=3
esac

exit $RETVAL
