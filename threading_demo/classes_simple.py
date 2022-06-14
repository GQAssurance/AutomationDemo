import random
import time
import logging


class TestLogger:
    """ This is the equivalent of our TestRail API interface class """

    d = {'src': 'Logger'.ljust(14)}     # used for local logging
    testrun_id = None                   # A new TestLogger doesn't have any run ID
    testrun_initialize_time = 4         # How long does it take to get a testrun ID?
    results_transmit_time = 1           # How long does it take to transmit a test result?
    results = []                        # All the test results we've logged

    def get_testrun(self, testrunner: str):
        """ Obtain a new Testrun ID from our imaginary Testrail server """

        logging.info(f"Getting a new TestRun ID for '{testrunner}'", extra=self.d)

        # We don't need to create more than 1 test run ID
        if self.testrun_id:
            logging.info(f"Exsqueeze me {testrunner}, but test run '{self.testrun_id}' "
                         f"was already created; i'm not making another!", extra=self.d)
        else:
            logging.info(f"Making a new run will take some time, "
                         f"give me a {self.testrun_initialize_time} seconds...", extra=self.d)
            progress = f"Run initialization for '{testrunner}'"

            # Getting a Testrun ID from our imaginary Testrail server takes time
            for _ in range(self.testrun_initialize_time):
                progress += " initializing..."
                logging.info(f"{progress}", extra=self.d)
                time.sleep(1)

            new_id = str(int(random.random() * 1000))
            self.testrun_id = testrunner + "_" + new_id  # Let's remember which runner's request actually make this ID
            logging.info(f"Test run '{self.testrun_id}' has been created.", extra=self.d)

    def log_results(self, testrunner: str, test_id: int, result: str):
        """ Transmit test results to our imaginary Testrail server """

        logging.info(f"Transmitting test results, "
                     f"this  will take {self.results_transmit_time} second(s).", extra=self.d)
        time.sleep(self.results_transmit_time)
        self.results.append(f"{testrunner.rjust(7)} {test_id}: {result}")
        logging.info(f"Test result '{result}' for test id {test_id} has been logged.", extra=self.d)

    def report_results(self):
        """ Display a list of all the test results """

        logging.info(f"Showing Test results for run {self.testrun_id}:", extra=self.d)
        for result in self.results:
            logging.info(f"{result}", extra=self.d)


class TestRunner:
    """ This is the equivalent of a PyTest instance """

    results_logger = None
    test_time = 3

    def __init__(self, name: str):
        self.d = {'src': name.rjust(14)}     # used for local logging
        self.name = name.strip()             # remember who I am!

        logging.info(f"I exist!  My tests will take {self.test_time} seconds to run", extra=self.d)

    def initialize_log(self, logger: TestLogger):
        """ Connect to the TestLogger object, and tell it to provide a Testrun ID """

        self.results_logger = logger
        logging.info(f"I am asking for a new Testrun ID", extra=self.d)
        self.results_logger.get_testrun(testrunner=self.name)

    def run_tests(self, number_of_tests: int):
        """ Run imaginary tests, and log the results to our TestLogger """

        logging.info(f"Starting to run {number_of_tests} tests", extra=self.d)

        for test_num in range(1, number_of_tests+1):
            logging.info(f"Starting test number {test_num}, this will take "
                         f"{self.test_time} seconds.", extra=self.d)
            progress = f"Test {test_num}"

            # Running the test takes time
            for _ in range(self.test_time):
                progress += " testing..."
                logging.info(f"{progress}", extra=self.d)
                time.sleep(1)

            # There's a lot of different possible results!
            result = random.choice(["pass", "fail", "skip", "xfail", "timeout"])
            logging.info(f"I have a test result of {result}", extra=self.d)
            self.send_results_to_logger(self.name, test_num, result)

    def send_results_to_logger(self, name: str, test_num: int, result: str):
        """ Sends test results to our imaginary Testrail server.  This is separate because it could take some time. """

        self.results_logger.log_results(name, test_num, result)


def local_log_setup():
    logging.basicConfig(format='%(asctime)s (%(threadName)-10s) [object: %(src)14s] %(message)s', level=logging.INFO, datefmt='%I:%M:%S')
