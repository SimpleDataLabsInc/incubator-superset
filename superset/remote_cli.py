import argparse
import json
import logging
import os
import subprocess
import sys
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPNotFound
)
from pyramid.response import Response
from pyramid.view import view_config, notfound_view_config


class HttpHandler:
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('HttpHandler')
        (self.fac, self.request) = args
        self.kwargs = kwargs

    def execute(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        v = p.communicate()
        return v, p.returncode

    def execute_cmd(self, cmd):
        ((out, err), code) = self.execute(cmd)
        full = {"code": code, "stdout": out.decode("UTF-8"), "stderr": err.decode("UTF-8")}
        return full

    @notfound_view_config(append_slash=HTTPMovedPermanently)
    def aview(self):
        return HTTPNotFound('not found')

    @view_config(route_name="hello", request_method="GET")
    def hello_world(self):
        return Response('Hello World!')

    @view_config(route_name="run_cmd", request_method="POST", renderer='json')
    def run(self):
        cmd = "superset import-datasources -s databases -p %s"
        body = self.request.json
        exec_cmd = cmd % body["file"]
        resp = self.execute_cmd(exec_cmd)
        return resp

    @view_config(route_name="update_metadata", request_method="POST", renderer='json')
    def update(self):
        cmd = "superset update-metadata -c"
        resp = self.execute_cmd(cmd)
        return resp


class PyramidServer:
    def __init__(self):
        self.args = self.parse_args()
        self.host = os.getenv("REMOTE_CLI_HOST_STRING", self.args.bind)
        self.datasource_location = os.getenv("SUPERSET_DATASOURCES_LOC", self.args.location)
        self.port = os.getenv("REMOTE_CLI_PORT_NUMBER") or self.args.port
        if self.port is None:
            sys.exit(-1)
        else:
            self.port = int(self.port)
        self.logger = logging.getLogger('SERVER')
        self.config = Configurator()
        self.endpoints_added = False
        self.app = None
        self.server = None

    def parse_args(self):
        parser = argparse.ArgumentParser("Prophecy Superset Remote Cli")
        parser.add_argument("-b", "--bind", default="0.0.0.0", help="Host Remote Cli Server should bind to")
        parser.add_argument("-p", "--port", help="Port Remote Cli Server should use")
        parser.add_argument("-l", "--location", help="Location to watch for superset datasources")
        return parser.parse_args()

    def configure_endpoints(self):
        self.config.add_route('hello', '/')
        self.config.add_route("run_cmd", "/run")
        self.config.add_route("update_metadata", "/update")
        # self.config.add_view(self.hello_world, route_name='hello')
        # self.config.add_view(self.run, route_name='run_cmd')
        # self.config.add_view(self.update, route_name='update_metadata')
        self.config.scan()

    def create_app(self):
        if not self.endpoints_added:
            self.configure_endpoints()
            self.endpoints_added = True
        self.app = self.config.make_wsgi_app()

    def start_server(self):
        self.server = make_server(self.host, self.port, self.app)
        self.logger.debug("SERVER: %s" % dir(self.server))
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s] %(filename)s:%(lineno)d: %(name)s: %(message)s',
                        )
    server = PyramidServer()
    try:
        logging.debug('Server start')
        logging.debug("SERVER: %s" % dir(server))
        server.create_app()
        logging.debug("APP: %s" % dir(server.app))
        server.start_server()
    except Exception as e:
        logging.exception('Something happened,\n'
                          'if it was not a keyboard break...\n'
                          'check if address taken, '
                          'or another instance is running. Exit')
    finally:
        server.shutdown()
        logging.debug('Goodbye')
