import logging
from classes_simple import TestLogger
from threading import Lock


class MutexLogger(TestLogger):
    """ This is the equivalent of our TestRail reporting class, now threadsafe!

        Mutex = "Mutually Exclusive Semaphore"  i.e. only 1 thread can access the
    """

    lock = Lock()

    def get_testrun(self, testrunner: str):
        """ The wrapper will now lock "build my testrun" function so only 1 thread can attempt it at a time. """

        logging.info(f"'{testrunner}' has requested a new test run, but will it get it?", extra=self.d)

        self.lock.acquire()
        logging.info(f"'{testrunner}' Now has a lock on 'get_testrun''", extra=self.d)

        super().get_testrun(testrunner)

        self.lock.release()
        logging.info(f"'{testrunner}' Has released its lock on 'get_testrun''", extra=self.d)


class DeadlockLogger(TestLogger):
    """ This is the equivalent of our TestRail reporting class, now threadsafe!

        This will crash when "Alpha" testrunner created a testrun, causing a deadlock.
    """

    lock = Lock()

    def get_testrun(self, testrunner: str):
        """ The wrapper will now lock "build my testrun" function so only 1 thread can attempt it at a time. """

        logging.info(f"'{testrunner}' has requested a new test run, but will it get it?", extra=self.d)

        self.lock.acquire()
        logging.info(f"'{testrunner}' Now has a lock on 'get_testrun''", extra=self.d)

        if "Alpha" in testrunner:
            logging.info(f"We crashed trying to get a test run for Alpha!", extra=self.d)
            raise Exception("'get_testrun' ran into an error!")

        super().get_testrun(testrunner)

        self.lock.release()
        logging.info(f"'{testrunner}' Has released its lock on 'get_testrun''", extra=self.d)


class CrashingSafeMutexLogger(TestLogger):
    """ This is the equivalent of our TestRail reporting class, now threadsafe!

        Mutex = "Mutually Exclusive Semaphore"  i.e. only 1 thread can access the

        This is a crashing TestLogger which is thread-safe to avoid deadlocks
    """

    lock = Lock()

    def get_testrun(self, testrunner: str):
        """ The wrapper will now lock "build my testrun" function so only 1 thread can attempt it at a time. """

        logging.info(f"'{testrunner}' has requested a new test run, but will it get it?", extra=self.d)

        with self.lock:
            if "Alpha" in testrunner:
                logging.info(f"We crashed trying to get a test run for Alpha!", extra=self.d)
                raise Exception("'get_testrun' ran into an error!")
            super().get_testrun(testrunner)


class SafeMutexLogger(TestLogger):
    """ This is the equivalent of our TestRail reporting class, now threadsafe!

        Mutex = "Mutually Exclusive Semaphore"  i.e. only 1 thread can access the

        This is a safer way to handle locks; so that exceptions do not Deadlock
    """

    lock = Lock()

    def get_testrun(self, testrunner: str):
        """ The wrapper will now lock "build my testrun" function so only 1 thread can attempt it at a time. """

        logging.info(f"'{testrunner}' has requested a new test run, but will it get it?", extra=self.d)

        with self.lock:
            super().get_testrun(testrunner)
