#!/bin/sh

export LANG=C

NAME="opti"
DATE=`/bin/date "+%Y%m%d-%H%M%S"`

(
# new ruleset is found by name:
AUTO=/root/auto-apply

# yes, we want logging
LOG="/usr/bin/logger -t $NAME -p user.warn "

# usual suspects: input and output
TMI=/root/reference-input
TMO=/root/reference-output

# unsusual suspects: on error, these are kept
# if present, nothings more done for investigations
TIR=/root/ref-with-error-in
TOR=/root/ref-with-error-out

# stderr shall be written to
STE=/root/iptables-optimizer-partitions
[ $# -eq 0 ] && STE=/dev/null

# any error on last run?
[ -r $TIR ] && exit 0

# look for new ruleset, coming via scp.
[ -r $AUTO -a ! -x $AUTO ] && echo "auto-apply writing in progress" | $LOG
[ -r $AUTO -a ! -x $AUTO ] && echo "auto-apply writing in progress" && exit 0

# look for new ruleset ready, after scp need chmod +x as ready and go indicator
[ -x $AUTO ] && /sbin/iptables-restore $AUTO
[ -x $AUTO ] && /sbin/iptables-save -t filter > /root/rules-saved-filter-only
[ -x $AUTO ] && echo "renaming file to ${AUTO}-${DATE}" | $LOG  && /bin/true
[ -x $AUTO ] && /bin/mv ${AUTO} ${AUTO}-${DATE} && exit 0

# ok, no new ruleset, normal way of doing ...
cd /root

# Step 1: read kernel filter-chains and packet-counters 
/sbin/iptables-save -c -t filter > $TMI
ERR=$?
LINES=`/bin/cat $TMI | /usr/bin/wc -l `
[ $ERR -eq 0 ] && echo "Step 1: $LINES rules, no error" | $LOG 

[ $ERR -gt 0 ] && echo "Step 1: $LINES rules, error: ${ERR}, abort" | $LOG 
[ $ERR -gt 0 ] && exit 1

# Step 2: pythonscript has no foreseen errorvalue for now.
# call in /sbin, stdout: input for restore, stderr: partitions

sbin/iptables_optimizer.py  > $TMO 2>$STE

LINEO=`/bin/cat $TMO | /usr/bin/wc -l `
[ $LINEO -ne $LINES ] && /bin/mv $TMI $TIR
[ $LINEO -ne $LINES ] && /bin/mv $TMO $TOR
[ $LINEO -ne $LINES ] && echo "Step 2: ${LINES} -ne ${LINEO}, abort" | $LOG 
[ $LINEO -ne $LINES ] && exit 1

[ $LINEO -eq $LINES ] && echo "Step 2: ${LINES} rules OK" | $LOG 

[ -f $STE ] && cat $STE | /usr/bin/logger -t $NAME

# for longer lasting debugging sessions perhaps counters should not reset?
#/sbin/iptables-restore  -c < $TMO
# or normal way:
/sbin/iptables-restore     < $TMO
ERR=$?
[ $ERR -eq 0 ] && echo "Step 3: $LINEO rules, no error" | $LOG 
[ $ERR -eq 0 ] && exit 0
# no error in step 3, all done!

# if error, try to repair, show in logging
[ $ERR -gt 0 ] && echo "Step 3: $LINES rules, error: ${ERR}, retry" | $LOG 
[ $ERR -gt 0 ] && /root/bin/flush && /bin/sleep 10 && /sbin/iptables-restore  < $TMO
ERR=$?
[ $ERR -eq 0 ] && echo "Step 4: retry without error" | $LOG 
[ $ERR -eq 0 ] && exit 0

# if still some error, no more try to repair, some other job shall do, and
# prevent from further running.
[ $ERR -gt 0 ] && echo "Step 4: retry with error: ${ERR}, lock and abort" | $LOG 
[ $ERR -gt 0 ] && /bin/mv $TMI $TIR
[ $ERR -gt 0 ] && /bin/mv $TMO $TOR
[ $ERR -gt 0 ] && /bin/mv /tmp/optimizer-last-run /root/ref-last-stdout_stderror
[ $ERR -gt 0 ] && /root/bin/flush
[ $ERR -gt 0 ] && echo "Step5: let filtercheck do the rest" | $LOG 

exit 1
) 2>&1 | /usr/bin/tee /tmp/optimizer-last-run
# EoF
