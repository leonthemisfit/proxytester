#!/usr/bin/python

import socks

class ProxiedIRCSocket:
    def __init__(self, host, port, proto=socks.SOCKS5, enc="utf8", timeout=2):
        self.sock = socks.socksocket()
        self.sock.settimeout(timeout)
        self.sock.set_proxy(proto, host, port)
        self.enc = enc
        self.__buffer = b''

    def connect(self, host="irc.snoonet.org", port=6667):
        try:
            self.sock.connect((host, port))
            self.sock.settimeout(None)
            return True
        except (ConnectionRefusedError,
            socks.ProxyConnectionError,
            ConnectionResetError,
            socks.GeneralProxyError,
            TypeError):
            return False

    def close(self):
        self.sock.close()

    def read_line(self, sep=b'\r\n'):
        try:
            while not sep in self.__buffer:
                old_size = len(self.__buffer)
                self.__buffer += self.sock.recv(1024)
                new_size = len(self.__buffer)
                if old_size == new_size and not sep in self.__buffer:
                    return "ERROR :Invalid Data"
            line, self.__buffer = self.__buffer.split(sep, 1)
            return line.decode(self.enc)
        except (ConnectionResetError):
            return "ERROR :Connection Reset"

    def write_line(self, line):
        self.sock.send((line + "\r\n").encode(self.enc))

    def write_user(self, ident="leonthegrinch", realname="im uppin yr loop"):
        self.write_line("USER " + ident + " NULL NULL :" + realname)

    def write_nick(self, nick="LOLBOT"):
        self.write_line("NICK " + nick)

    def write_pong(self, arg):
        self.write_line("PONG " + arg)

    def write_join(self, chan="#botcentral"):
        self.write_line("JOIN " + chan)

    def write_pmsg(self, msg="OHAI", recp="#botcentral"):
        self.write_line("PRIVMSG " + recp + " :" + msg)

    def write_quit(self, msg="KTHXBAI"):
        self.write_line("QUIT :" + msg)
