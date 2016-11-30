from collections import namedtuple

irc_line = namedtuple("irc_line", ["prefix", "command", "args"])

def parse(msg):
    prefix = ""
    trailing = []

    if not msg:
       return "", "", ""

    if msg[0] == ":":
        prefix, msg = msg[1:].split(" ", 1)

    if msg.find(" :") > -1:
        msg, trailing = msg.split(" :", 1)
        args = msg.split()
        args.append(trailing)
    else:
        args = msg.split()

    cmd = args.pop(0)
    return irc_line(prefix, cmd, args)
