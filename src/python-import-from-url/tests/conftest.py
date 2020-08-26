import os
import sys
import pytest
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pyimporter import enable_url_import, disable_url_import

class LiveServer:
    _stop = False
    thread = None
    value = 0
    httpd = None

    def __init__(self, path=None, address='127.0.0.1', port=8000):
        self.path = path
        self.address = address
        self.port = port
        self.ready = False

    def _start_server(self):
        address = (self.address, self.port)
        handler_class = SimpleHTTPRequestHandler
        if self.path is not None:
            os.chdir(self.path)
        with HTTPServer(address, handler_class) as httpd:
            self.httpd = httpd
            self.ready = True
            httpd.serve_forever()


    def start(self):
        if self.thread:
            raise Exception('Already running')
        self._stop = False
        self.thread = threading.Thread(name='live server',
                             target = self._start_server,
                             args = ())
        self.thread.setDaemon(True)
        self.thread.start()
        give_up_at_time = time.time() + 10
        while not self.ready:
            time.sleep(0.1)
            if time.time() > give_up_at_time:
                raise Exception("Live server didn't start on time. Giving up.")

    def stop(self):
        if self.thread:
            # self.thread._stop()
            self.httpd.shutdown()
            self.thread.join()
            self.thread = None
        pass

def pytest_addoption(parser):
    parser.addoption('--functional', action='store_true', dest="functional",
                 default=False, help="enable functional tests")

def pytest_configure(config):
    if not config.option.functional:
        setattr(config.option, 'markexpr', 'not functional')


@pytest.fixture(scope='session')
def fix_dir():
    dir = os.path.abspath(os.path.dirname(__file__)) + '/fixture'
    return dir

@pytest.fixture(scope='session')
def live_server(fix_dir):
    server = LiveServer(path=fix_dir)
    server.start()
    yield server
    server.stop()

@pytest.fixture
def urlimport(live_server):
    enable_url_import()
    sys.path.append('http://127.0.0.1:8000/')
    yield None
    sys.path.remove('http://127.0.0.1:8000/')
    disable_url_import()
    sys.path_importer_cache.clear()

