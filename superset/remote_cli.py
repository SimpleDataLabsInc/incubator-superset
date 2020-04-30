import argparse
import socketserver
import threading
import os, sys


class ProphecyRemoteCli(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        print("{} wrote: {}".format(self.client_address[0], self.data))
        self.wfile.write(self.data.upper())


def parse_args():
    parser = argparse.ArgumentParser("Prophecy Superset Remote Cli")
    parser.add_argument("-b", "--bind", default="0.0.0.0", help = "Host Remote Cli Server should bind to")
    parser.add_argument("-p", "--port", help = "Port Remote Cli Server should use")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    HOST = os.getenv("REMOTE_CLI_HOST_STRING", args.bind)
    PORT = int(os.getenv("REMOTE_CLI_PORT_NUMBER", "%s" % args.port))

    server = socketserver.ThreadingTCPServer((HOST, PORT), ProphecyRemoteCli)
    # Create the server, binding to localhost on port 9999
    with server:
        server.serve_forever()
        # # Activate the server; this will keep running until you
        # # interrupt the program with Ctrl-C
        # ip, port = server.server_address
        # print(ip, port)
        #
        # # Start a thread with the server -- that thread will then start one
        # # more thread for each request
        # server_thread = threading.Thread(target=server.serve_forever)
        # # Exit the server thread when the main thread terminates
        # server_thread.daemon = True
        # server_thread.start()
        # print("Server loop running in thread:", server_thread.name)
