from collections import namedtuple

proxy = namedtuple("proxy", ["addr", "port"])

class ProxyList:
    def __init__(self, path="proxies.txt", sep="\r\n"):
        with open(path) as fh:
            self.__content = fh.readlines()
        self.__index = 0
        self.__len = len(self.__content)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index < self.__len:
            line = self.__content[self.__index]
            addr, port = line.split(":")
            self.__index += 1
            return proxy(addr, int(port))
        else:
            raise StopIteration
