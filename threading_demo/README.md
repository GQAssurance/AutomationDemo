# "Python Threading is Simple" demo

## scripts:

- run_basic: A single test run logging results
- run_squential: 2 test runs happening 1 after the other
- run_parallel: 2 test runs happening in parallel (1st Test ID is lost)
- run_parallel_mutex: 2 test runs happening in parallel (1st Test ID is retained)
- run_parallel_mutex_deadlock: a crashed thread causes deadlock
- run_parallel_mutex_safe: a crashed thread doesn't stop 2nd thread from finishing
- run_parallel_semaphor: test logging resource is limited

## classes:

- classes_simple: the base classes without any thoughts for threading
- classes_mutex: child classes demonstrating mutex locking
- classes_semaphore: child classes demonstrating semaphores

## hints:

Logging includes all of this to help follow along:

- Timestamp
- Thread which created the log
- Objects which created the log
- ... what happened!

Edit the `local_log_setup()` function to adjust if you feel like.
