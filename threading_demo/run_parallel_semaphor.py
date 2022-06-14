from classes_simple import local_log_setup
from classes_semaphore import SemaphoreRunner, SemaphoreLogger
import time
import threading


def threaded_tests(name: str, logger: SemaphoreLogger):
    """ Every Test Runner gets it own thread to initialize & run tests """

    testrun = SemaphoreRunner(name)  # Start a new test run
    testrun.initialize_log(logger)   # connect to logger object
    testrun.run_tests(5)             # run tests


def safe_parallel_tests():
    """ Use threads for our test runners to both run at the same time, with a threadsafe logger """

    local_log_setup()                       # Our logs need to look pretty
    logger = SemaphoreLogger()              # make our semaphore logger object

    thread_alpha = threading.Thread(target=threaded_tests, name="Thread-A", args=("Alpha   ", logger))   # Make new thread objects
    thread_beta  = threading.Thread(target=threaded_tests, name="Thread-B", args=("Beta",     logger))
    thread_delta = threading.Thread(target=threaded_tests, name="Thread-D", args=("Delta",    logger))
    thread_gamma = threading.Thread(target=threaded_tests, name="Thread-G", args=("Gamma",    logger))

    thread_alpha.start()                    # Start the Alpha thread right away
    time.sleep(2)                           # ... start the rest of the runs slowly ...
    thread_beta.start()
    time.sleep(2)
    thread_delta.start()
    time.sleep(2)
    thread_gamma.start()

    thread_alpha.join()                     # Wait until all our tests finish running.
    thread_beta.join()
    thread_delta.join()
    thread_gamma.join()

    logger.report_results()                 # how did it end?


if __name__ == '__main__':
    safe_parallel_tests()

