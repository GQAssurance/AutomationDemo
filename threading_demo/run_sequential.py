from classes_simple import TestLogger, TestRunner, local_log_setup


def sequential_tests():

    local_log_setup()                       # Our logs need to look pretty
    logger = TestLogger()                   # make our shared TestLogger object

    testrun_alpha = TestRunner('Alpha   ')  # Start a new test run
    testrun_alpha.initialize_log(logger)    # connect to logger object
    testrun_alpha.run_tests(2)              # run tests

    testrun_beta = TestRunner('Beta')       # Start a 2nd test run
    testrun_beta.initialize_log(logger)     # connect to same logger object
    testrun_beta.run_tests(2)               # run tests

    logger.report_results()                # how did it end?


if __name__ == '__main__':
    sequential_tests()

