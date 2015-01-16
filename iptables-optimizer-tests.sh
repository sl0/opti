#!/bin/bash
# Tests for all the shell functions needed by iptables-optimizer
# 2015-01-16
# Johannes Hubertz
#
export TRUE=0
export FALSE=1

# default value for logging
VERBLOG=0

CASUAL=/tmp/opti-tests-iptables-optimizer-tests.tmp-log

IP6=""
[ `basename $0` == "ip6tables-optimizer-tests.sh" ] && IP6="6"

# fake LOG for the tests, do nothing
casual_logger()
{
    cat $* >$CASUAL
}

casual_log_lines()
{
    LINES=$( cat $CASUAL | wc -l )
    echo $LINES
}

LOG=casual_logger

# are we root?
ID=$(id -u)
FAKED=$( printenv | grep -c FAKE )
REAL_ID=$(( $ID | $FAKED ))


# first load the optimizer-functions
. ./iptables-optimizer-functions

test_Needs_to_run_as_root()
{
    ${_ASSERT_EQUALS_} 'expecting-real-root' 0 ${REAL_ID}
}

test_AutoApply_Not_Present()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # first check a non existing file for returning FALSE
    FILE="/tmp/opti-tests-auto-apply-not-present"
    check_auto_apply_ready $FILE
    retval=$?
    ${_ASSERT_EQUALS_} 'auto-apply-found-but-was-not-expeced' ${retval} $FALSE
}

test_AutoApply_Not_Ready()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # create an existing file (0600) for returning FALSE
    FILE="/tmp/opti-tests-auto-apply-not-executable"
    touch ${FILE}
    chmod 600 ${FILE}
    check_auto_apply_ready ${FILE}
    retval=$?
    ${_ASSERT_EQUALS_} 'auto-apply-found-but-not-executable' ${retval} $FALSE
}

test_AutoApply_Ready()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # create an existing file (0700) for returning TRUE
    FILE="/tmp/opti-tests-auto-apply"
    touch ${FILE}
    chmod 700 ${FILE}
    check_auto_apply_ready ${FILE}
    retval=$?
    ${_ASSERT_EQUALS_} 'auto-apply-found-like-expeted' ${retval} $TRUE
}

test_AutoApply_Execute()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    FILE="/tmp/opti-tests-auto-apply"
    touch ${FILE}
    chmod 700 ${FILE}
    auto_apply_execute $FILE
    retval=$?
    ${_ASSERT_EQUALS_} 'auto-apply-execute' $TRUE ${retval}
    PRESENT=$FALSE
    [ -f $FILE ] && PRESENT=$TRUE
    ${_ASSERT_EQUALS_} 'auto-apply-removed' $PRESENT $FALSE
}

test_AutoApply_Execute_fails_due_to_immutable()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    FILE="/tmp/opti-tests-auto-apply"
    touch ${FILE}
    chmod 700 ${FILE}
    # prevent moving after restore by setting immutable-bit
    [ $REAL_ID -eq 0 ] && chattr +i $FILE
    auto_apply_execute $FILE
    retval=$?
    ${_ASSERT_EQUALS_} 'auto-apply-execute' $TRUE ${retval}
    PRESENT=$FALSE
    [ -f $FILE ] && PRESENT=$TRUE
    ${_ASSERT_EQUALS_} 'auto-apply-removed' $PRESENT $TRUE
    # file still present, so reset immutable after test
    [ $REAL_ID -eq 0 ] && chattr -i $FILE
    rm -f $FILE
}

test_Modprobe_NetFilter()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # try to load iptable modules
    /sbin/modprobe iptable_filter
    retval=$?
    ${_ASSERT_EQUALS_} 'modprobe-iptable_filter' $TRUE ${retval}
}

test_Good_iptables_save_without_log()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # try to save iptables from the kernel
    TABLES="/tmp/opti-tests-iptables-save-output"
    ERRORS="/tmp/opti-tests-iptables-save-errors"
    VERBLOG=0
    save_the_tables $TABLES $ERRORS
    retval=$?
    ${_ASSERT_EQUALS_} 'iptables-save' $TRUE ${retval}
}

test_Good_iptables_save_simple_log()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # try to save iptables from the kernel
    TABLES="/tmp/opti-tests-iptables-save-output"
    ERRORS="/tmp/opti-tests-iptables-save-errors"
    VERBLOG=1
    save_the_tables $TABLES $ERRORS
    retval=$?
    ${_ASSERT_EQUALS_} 'iptables-save' $TRUE ${retval}
}

test_Run_python_part_without_log()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    TABLES="/tmp/opti-tests-iptables-save-output"
    OPTOUT="/tmp/opti-tests-iptables-optimizer-output"
    STATIS="/tmp/opti-tests-iptables-optimizer-partitions"
    VERBLOG=0
    run_python_part $TABLES $OPTOUT $STATIS
    retval=$?
    ${_ASSERT_EQUALS_} 'run-python-part' $TRUE ${retval}
}

test_Run_python_part_simple_log()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    TABLES="/tmp/opti-tests-iptables-save-output"
    OPTOUT="/tmp/opti-tests-iptables-optimizer-output"
    STATIS="/tmp/opti-tests-iptables-optimizer-partitions"
    VERBLOG=1
    run_python_part $TABLES $OPTOUT $STATIS
    retval=$?
    ${_ASSERT_EQUALS_} 'run-python-part' $TRUE ${retval}
}

test_Run_python_part_verb_log_all_chains()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    TABLES="/tmp/opti-tests-iptables-save-output"
    OPTOUT="/tmp/opti-tests-iptables-optimizer-output"
    STATIS="/tmp/opti-tests-iptables-optimizer-partitions"
    VERBLOG=2
    run_python_part $TABLES $OPTOUT $STATIS $FALSE
    retval=$?
    ${_ASSERT_EQUALS_} 'run-python-part' $TRUE ${retval}
    COUNT=$( casual_log_lines )
    ${_ASSERT_EQUALS_} 'verbose:5-lines-expected ' 5 $COUNT
}

test_Run_python_part_verb_log_in_out_chains()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    TABLES="/tmp/opti-tests-iptables-save-output"
    OPTOUT="/tmp/opti-tests-iptables-optimizer-output"
    STATIS="/tmp/opti-tests-iptables-optimizer-partitions"
    VERBLOG=2
    run_python_part $TABLES $OPTOUT $STATIS $TRUE
    retval=$?
    ${_ASSERT_EQUALS_} 'run-python-part' $TRUE ${retval}
    COUNT=$( casual_log_lines )
    ${_ASSERT_EQUALS_} 'verbose:5-lines-expected ' 2 $COUNT
}


test_Bad_iptables_save()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # try to save iptables from the kernel
    TABLES="/tmp/opti-tests-iptables-save-output"
    touch $TABLES
    chattr +i $TABLES >/dev/null 2>/dev/null
    retval=$?
    ${_ASSERT_EQUALS_} 'chattr-returned' $TRUE ${retval}
    FAULTS="/tmp/opti-tests-iptables-save-faults"
    VERBLOG=2
    save_the_tables $TABLES $FAULTS  2>/dev/null
    retval=$?
    chattr -i $TABLES
    ${_ASSERT_EQUALS_} 'iptables-save' $FALSE ${retval}
}

test_Correct_iptables_restore()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # try to restore iptables file into the kernel
    TABLES="/tmp/opti-tests-iptables-save-output"
    NORMAL="/tmp/opti-tests-iptables-restore-output"
    FAULTS="/tmp/opti-tests-iptables-restore-faults"
    COUNTS=1
    load_the_tables $TABLES $NORMAL $FAULTS $COUNTS
    retval=$?
    ${_ASSERT_EQUALS_} 'iptables-restore' $TRUE ${retval}
}

test_Faulty_iptables_restore()
{
    [ $REAL_ID -ne 0 ] && startSkipping
    # try to restore faulty iptables file into the kernel
    # create a faulty iptables statement and append
    TABLES="/tmp/opti-tests-iptables-save-output"
    NORMAL="/tmp/opti-tests-iptables-restore-output"
    FAULTS="/tmp/opti-tests-iptables-restore-faults"
    COUNTS=1
    echo "/sbin/iptables -A OUTPUT -p udp --port 53 -j ACCEPT" >> $TABLES
    load_the_tables $TABLES $NORMAL $FAULTS $COUNTS
    retval=$?
    ${_ASSERT_EQUALS_} 'iptables-restore' $FALSE ${retval}
}

# some things before starting all these tests

oneTimeSetUp()
{
    [ $REAL_ID -eq 0 ] && ip${IP6}tables-save -c > /tmp/opti-tests-tables-before-status
    [ $REAL_ID -eq 0 ] && ip${IP6}tables -F
    [ $REAL_ID -eq 0 ] && ip${IP6}tables-restore -c reference-input${IP6}
}

# finalize some things after running all these tests

oneTimeTearDown()
{
    [ $REAL_ID -eq 0 ] && ip${IP6}tables -F
    [ $REAL_ID -eq 0 ] && ip${IP6}tables -X IPSEC
    [ $REAL_ID -eq 0 ] && ip${IP6}tables-restore -c /tmp/opti-tests-tables-before-status
    rm -f /tmp/opti*
}

# load shunit2 and execute the tests

. shunit2

exit 0
