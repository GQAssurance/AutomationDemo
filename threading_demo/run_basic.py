from classes_simple import TestLogger, TestRunner, local_log_setup


def basic_tests():

    local_log_setup()                 # Our logs need to look pretty
    logger = TestLogger()             # Make our TestLogger object

    testrun = TestRunner('Alpha   ')  # Start a new test run
    testrun.initialize_log(logger)    # Connect test run to our logger object
    testrun.run_tests(3)              # Run tests

    logger.report_results()           # how did it end?


if __name__ == '__main__':
    basic_tests()

