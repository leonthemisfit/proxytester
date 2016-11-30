from ircsock import ProxiedIRCSocket
import parser
from time import sleep

def connect(addr, port):
    sock = ProxiedIRCSocket(addr, port)
    out = "PROXY_ERROR"
    if sock.connect():
        out = "IRC_ERROR"
        sock.write_user()
        sock.write_nick()
        while True:
            raw = sock.read_line()
            line = parser.parse(raw)
            if line.command == "ERROR":
                break
            elif line.command == "PING":
                sock.write_pong(line.args[0])
            elif line.command == "004":
                out = "ZLINE"
                sleep(1)
                sock.write_join()
            elif line.command == "JOIN":
                out = "JOINED"
                sock.write_pmsg()
                sock.write_quit()
                break
        sock.close()

        if out == "JOINED":
            with open("joined.txt", "a") as fh:
                fh.write("{}:{}\n".format(addr, port))
    print("{}:{}\t{}".format(addr, port, out))
