import argparse
import asyncore
import logging
import os
import socket
import subprocess
import sys

# from watchdog.observers import Observer
# from watchdog.events import RegexMatchingEventHandler



def parse_args():
    parser = argparse.ArgumentParser("Prophecy Superset Remote Cli")
    parser.add_argument("-b", "--bind", default="0.0.0.0", help="Host Remote Cli Server should bind to")
    parser.add_argument("-p", "--port", help="Port Remote Cli Server should use")
    parser.add_argument("-l", "--location", help = "Location to watch for superset datasources")
    return parser.parse_args()


class Server(asyncore.dispatcher):

    def __init__(self, queue_size):
        args = parse_args()
        HOST = os.getenv("REMOTE_CLI_HOST_STRING", args.bind)
        LOCATION = os.getenv("SUPERSET_DATASOURCES_LOC", args.location)
        PORT = os.getenv("REMOTE_CLI_PORT_NUMBER") or args.port
        if PORT is None:
            sys.exit(-1)
        else:
            PORT = int(PORT)
        self.logger = logging.getLogger('SERVER')
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((HOST, PORT))
        self.listen(queue_size)
        self.logger.debug('binding to {}'.format(self.socket.getsockname()))

    def handle_accept(self):
        socket, address = self.accept()
        self.logger.debug('new connection accepted')
        SupersetAppenderHandler(100, socket)


class SupersetAppenderHandler(asyncore.dispatcher_with_send):

    def __init__(self, max_message_length, sock = None, map = None):
        super(SupersetAppenderHandler, self).__init__(sock, map)
        self.debug = True
        self.max_length = max_message_length
        self.fmt = "%{}s".format(self.max_length)

    def execute(self, cmd):
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        v = p.communicate()
        return v, p.returncode

    def handle_read(self):
        msg = self.recv(self.max_length)
        print("Received: ", msg)
        msg = msg.strip()#confjson.get('RATE', None))
        cmd = msg.decode("utf8")
        try:
            (out, err) = self.execute(cmd)
        except Exception as e:
            print(e)
        self.out_buffer = (self.fmt % cmd).encode("utf8")#msg.upper().decode("utf8")).encode("utf8")
        # self.out_buffer += ' server recieve: {}'.format(time.time()).encode("utf8")
        print("Sending:  ", self.out_buffer)
        if not self.out_buffer:
            self.close()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] %(filename)s:%(lineno)d: %(name)s: %(message)s',
                        )
    # with open('config.json', 'r') as jfile:
    #     confjson = json.load(jfile)
    try:
        logging.debug('Server start')
        server = Server(100)
        asyncore.loop()
    except Exception as e:
        logging.error('Something happened,\n'
                      'if it was not a keyboard break...\n'
                      'check if address taken, '
                      'or another instance is running. Exit')
    finally:
        logging.debug('Goodbye')


# class ProphecyRemoteCli(socketserver.BaseRequestHandler):
#
#     def handle(self):
#         self.data = self.request.recv(50).strip()
#         print("{} wrote: {}".format(self.client_address[0], self.data))
#         v = "%50s" % self.data.upper()
#         print("Written: ", v)
#         self.request.send(v)
#
#
# if __name__ == "__main__":
#     args = parse_args()
#     HOST = os.getenv("REMOTE_CLI_HOST_STRING", args.bind)
#     PORT = int(os.getenv("REMOTE_CLI_PORT_NUMBER", "%s" % args.port))
#
#     socketserver.ThreadingTCPServer.allow_reuse_address = True
#     server = socketserver.ThreadingTCPServer((HOST, PORT), ProphecyRemoteCli)
#     # Create the server, binding to localhost on port 9999
#     with server:
#         server.serve_forever()
#         # # Activate the server; this will keep running until you
#         # # interrupt the program with Ctrl-C
#         # ip, port = server.server_address
#         # print(ip, port)
#         #
#         # # Start a thread with the server -- that thread will then start one
#         # # more thread for each request
#         # server_thread = threading.Thread(target=server.serve_forever)
#         # # Exit the server thread when the main thread terminates
#         # server_thread.daemon = True
#         # server_thread.start()
#         # print("Server loop running in thread:", server_thread.name)
