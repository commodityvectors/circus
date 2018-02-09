import sys
import os
import tempfile
import six
from copy import copy

from cvec_circus.cvec_circusd import get_maxfd, daemonize, main
from cvec_circus import cvec_circusd
from cvec_circus.arbiter import Arbiter
from cvec_circus.util import REDIRECT_TO
from cvec_circus import util
from cvec_circus.tests.support import (has_gevent, TestCase, skipIf, EasyTestSuite,
                                  IS_WINDOWS)


CIRCUS_INI = os.path.join(os.path.dirname(__file__), 'config', 'cvec_circus.ini')


class TestCircusd(TestCase):

    def setUp(self):
        self.saved = dict(sys.modules)
        self.argv = copy(sys.argv)
        self.starter = Arbiter.start
        Arbiter.start = lambda x: None
        self.exit = sys.exit
        sys.exit = lambda x: None
        self._files = []

        if not IS_WINDOWS:
            self.fork = os.fork
            os.fork = self._forking
            self.setsid = os.setsid
            os.setsid = lambda: None
            self.dup2 = os.dup2
            os.dup2 = lambda x, y: None

        self.forked = 0
        self.closerange = cvec_circusd.closerange
        cvec_circusd.closerange = lambda x, y: None
        self.open = os.open
        os.open = self._open
        self.stop = Arbiter.stop
        Arbiter.stop = lambda x: None
        self.config = util.configure_logger
        cvec_circusd.configure_logger = util.configure_logger = self._logger

    def _logger(self, *args, **kw):
        pass

    def _open(self, path, *args, **kw):
        if path == REDIRECT_TO:
            return
        return self.open(path, *args, **kw)

    def tearDown(self):
        cvec_circusd.configure_logger = util.configure_logger = self.config
        Arbiter.stop = self.stop
        sys.argv = self.argv
        os.open = self.open
        cvec_circusd.closerange = self.closerange
        sys.modules = self.saved
        Arbiter.start = self.starter
        sys.exit = self.exit

        if not IS_WINDOWS:
            os.fork = self.fork
            os.dup2 = self.dup2
            os.setsid = self.setsid

        for file in self._files:
            if os.path.exists(file):
                os.remove(file)
        self.forked = 0

    def _forking(self):
        self.forked += 1
        return 0

    @skipIf('TRAVIS' in os.environ, 'Travis detected')
    @skipIf(not has_gevent(), "Only when Gevent is loaded")
    def test_daemon(self):
        # if gevent is loaded, we want to prevent
        # daemonize() to work
        self.assertRaises(ValueError, daemonize)

        for module in sys.modules.keys():
            if module.startswith('gevent'):
                del sys.modules[module]

        import gevent
        sys.modules['gevent'] = gevent
        self.assertRaises(ValueError, daemonize)

    def test_maxfd(self):
        max = get_maxfd()
        self.assertTrue(isinstance(max, six.integer_types))

    @skipIf(has_gevent(), "Gevent is loaded")
    @skipIf(IS_WINDOWS, "Daemonizing not supported on Windows")
    def test_daemonize(self):
        daemonize()
        self.assertEqual(self.forked, 2)

    def _get_file(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        self._files.append(path)
        return path

    def test_main(self):

        def _check_pid(cls):
            self.assertTrue(os.path.exists(pid_file))

        Arbiter.start = _check_pid
        pid_file = self._get_file()
        sys.argv = ['cvec_circusd', CIRCUS_INI, '--pidfile', pid_file]
        main()
        self.assertFalse(os.path.exists(pid_file))

test_suite = EasyTestSuite(__name__)
