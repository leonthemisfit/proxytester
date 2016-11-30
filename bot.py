from proxy import ProxyList
import parser
import connector

proxies = ProxyList()
for proxy in proxies:
    connector.connect(proxy.addr, proxy.port)
