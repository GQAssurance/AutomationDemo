import logging
from threading import BoundedSemaphore
from classes_mutex import SafeMutexLogger
from classes_simple import TestRunner


class SemaphoreLogger(SafeMutexLogger):
    """ This is the equivalent of our TestRail reporting class, now threadsafe!

        Semaphore: a signalling system to allow access to limited resources
    """

    results_semaphore = BoundedSemaphore(2)  # Only log 2 results at a time

    def __init__(self):
        self.results_transmit_time = 4  # Takes a long time to transmit

    def log_results(self, testrunner: str, test_id: int, result: str):
        """ A wrapper for transmitting test results, so we can add threading code later """
        logging.info(f"runner '{testrunner}' wants to save test results, "
                     f"this  will take {self.results_transmit_time} second(s).", extra=self.d)
        super().log_results(testrunner, test_id, result)
        logging.info(f"Finished saving test results, release the semaphore kracken!", extra=self.d)
        self.results_semaphore.release()


class SemaphoreRunner(TestRunner):
    """ This is the equivalent of a PyTest instance """

    def __init__(self, name: str):
        self.test_time = 1  # We can run tests really fast now
        super().__init__(name)

    def initialize_log(self, logger: SemaphoreLogger):
        super().initialize_log(logger)

    def send_results_to_logger(self, name: str, test_num: int, result: str):
        logging.info(f"I want to log test results, but first I need to acquire a semaphore.", extra=self.d)
        self.results_logger.results_semaphore.acquire()
        logging.info(f"I was given a semaphore, let's log this puppy!", extra=self.d)
        super().send_results_to_logger(name, test_num, result)
