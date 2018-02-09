import os
import tempfile

import mock

from cvec_circus.tests.support import TestCircus, EasyTestSuite
from cvec_circus.stats.streamer import StatsStreamer
from cvec_circus import client


class _StatsStreamer(StatsStreamer):

    msgs = []

    def handle_recv(self, data):
        self.msgs.append(data)


class FakeStreamer(StatsStreamer):
    def __init__(self, *args, **kwargs):
        self._initialize()


class TestStatsStreamer(TestCircus):

    def setUp(self):
        self.old = client.CircusClient.call
        client.CircusClient.call = self._call
        fd, self._unix = tempfile.mkstemp()
        os.close(fd)

    def tearDown(self):
        client.CircusClient.call = self.old
        os.remove(self._unix)

    def _call(self, cmd):
        what = cmd['command']
        if what == 'list':
            name = cmd['properties'].get('name')
            if name is None:
                return {'watchers': ['one', 'two', 'three']}
            return {'pids': [123, 456]}
        elif what == 'dstats':
            return {'info': {'pid': 789}}
        elif what == 'listsockets':
            return {'status': 'ok',
                    'sockets': [{'path': self._unix,
                                 'fd': 5,
                                 'name': 'XXXX',
                                 'backlog': 2048}],
                    'time': 1369647058.967524}

        raise NotImplementedError(cmd)

    def test_get_pids_cvec_circus(self):
        streamer = FakeStreamer()
        streamer.cvec_circus_pids = {1234: 'cvec_circus-top', 1235: 'cvec_circusd'}
        self.assertEqual(streamer.get_pids('cvec_circus'), [1234, 1235])

    def test_get_pids(self):
        streamer = FakeStreamer()
        streamer._pids['foobar'] = [1234, 1235]
        self.assertEqual(streamer.get_pids('foobar'), [1234, 1235])

    def test_get_all_pids(self):
        streamer = FakeStreamer()
        streamer._pids['foobar'] = [1234, 1235]
        streamer._pids['barbaz'] = [1236, 1237]
        self.assertEqual(set(streamer.get_pids()),
                         set([1234, 1235, 1236, 1237]))

    @mock.patch('os.getpid', lambda: 2222)
    def test_get_cvec_circus_pids(self):
        def _send_message(message, name=None):
            if message == 'list':
                if name == 'cvec_circushttpd':
                    return {'pids': [3333]}
                return {'watchers': ['cvec_circushttpd']}

            if message == 'dstats':
                return {'info': {'pid': 1111}}

        streamer = FakeStreamer()
        streamer.client = mock.MagicMock()
        streamer.client.send_message = _send_message

        self.assertEqual(
            streamer.get_cvec_circus_pids(),
            {1111: 'cvec_circusd', 2222: 'cvec_circusd-stats',
             3333: 'cvec_circushttpd'})

    def test_remove_pid(self):
        streamer = FakeStreamer()
        streamer._callbacks['foobar'] = mock.MagicMock()
        streamer._pids = {'foobar': [1234, 1235]}
        streamer.remove_pid('foobar', 1234)
        self.assertFalse(streamer._callbacks['foobar'].stop.called)

        streamer.remove_pid('foobar', 1235)
        self.assertTrue(streamer._callbacks['foobar'].stop.called)

test_suite = EasyTestSuite(__name__)
