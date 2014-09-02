=========================================
iptables-optimizer-tests.sh - shell tests
=========================================

shunit2
-------

Thanks to Kate Ward, who has build the shunit2, which is available in the debian universe.
A reference file for input into iptables-optimizer is present as it is needed to run the tests.

All the functions of the shell wrapper are sourced from an external file, so
they may be tested independantly from the wrapper itself. Unfortunateley
only root is allowed to run the iptables-optimier as it modifies the rules 
within the kernel. So the effctive uid is checked in the first test and all others are skipped
if it is not zero.

Excuting the tests is done like this as root user (uid=0)::

   .../opti# bash iptables-optimizer-tests.sh 
   test_Needs_to_run_as_root
   test_AutoApply_Not_Present
   test_AutoApply_Not_Ready
   test_AutoApply_Ready
   test_AutoApply_Execute
   test_Modprobe_NetFilter
   test_Good_iptables_save_without_log
   test_Good_iptables_save_simple_log
   test_Run_python_part_without_log
   test_Run_python_part_simple_log
   test_Run_python_part_verb_log_all_chains
   test_Run_python_part_verb_log_in_out_chains
   test_Bad_iptables_save
   test_Correct_iptables_restore
   test_Faulty_iptables_restore
   
   Ran 15 tests.
   
   OK
   .../opti#


If the executing user is not uid=0, the tests fail like this::

   .../devel/opti  master $ bash iptables-optimizer-tests.sh
   test_Needs_to_run_as_root
   ASSERT:[38] expecting-to-run-as-root expected:<0> but was:<1000>
   test_AutoApply_Not_Present
   test_AutoApply_Not_Ready
   test_AutoApply_Ready
   test_AutoApply_Execute
   test_Modprobe_NetFilter
   test_Good_iptables_save_without_log
   test_Good_iptables_save_simple_log
   test_Run_python_part_without_log
   test_Run_python_part_simple_log
   test_Run_python_part_verb_log_all_chains
   test_Run_python_part_verb_log_in_out_chains
   test_Bad_iptables_save
   test_Correct_iptables_restore
   test_Faulty_iptables_restore
   
   Ran 15 tests.
   
   FAILED (failures=1,skipped=18)
   .../devel/opti  master $

As a consequence, the makefile will stop and no packages are build. So be sure to be root.

Testing is great fun.
