import time
import threading
from classes_simple import TestLogger, TestRunner, local_log_setup


def threaded_tests(name: str, logger: TestLogger):
    """ Every Test Runner gets it own thread to initialize & run tests """

    testrun = TestRunner(name)      # Start a new test run
    testrun.initialize_log(logger)  # connect to logger object
    testrun.run_tests(2)            # run tests


def parallel_tests():
    """ Use threads for our test runners to both run at the same time """

    local_log_setup()                       # Our logs need to look pretty
    logger = TestLogger()                   # make our logger object

    thread_alpha = threading.Thread(target=threaded_tests, name="Thread-A", args=("Alpha   ", logger))   # Make new thread objects
    thread_beta  = threading.Thread(target=threaded_tests, name="Thread-B", args=("Beta",     logger))

    thread_alpha.start()                    # Start the Alpha thread right away
    time.sleep(2)                           # ... wait until alpha's 1/2 initialized ...
    thread_beta.start()                     # Beta tests start a bit later

    thread_alpha.join()                     # Wait until all our tests finish running.
    thread_beta.join()

    logger.report_results()                 # how did it end?


if __name__ == '__main__':
    parallel_tests()
