#pylint: disable=broad-except
from ipaddress import ip_network
from os import environ

from mcstatus import MinecraftServer

subnet = environ.get('SCAN_SUBNET', '127.0.0.1')

def status_to_dict(status):
    return {
        'players': status.online,
        'maximum_players': status.max,
        'sample (whatever that is)': status.sample,
        'latency': status.latency,
    }

def query_to_dict(query):
    return {
        'raw': query.raw,
        'motd': query.motd,
        'map': query.map,
        'players': {
            'num': query.players.online,
            'maximum': query.players.max,
            'names': query.players.names,
            },
        'software': {
            'version': query.software.version,
            'brand': query.software.brand,
            'plugins': query.software.plugins,
            },
    }


scan_hosts = ip_network(subnet).hosts()

servers = {}
for address in map(str, scan_hosts):
    server = MinecraftServer.lookup(address)
    try:
        server.ping()
        servers[address] = {}
        try:
            servers[address]['status'] = status_to_dict(server.status())
        except Exception:
            pass
        try:
            servers[address]['query'] = query_to_dict(server.query())
        except Exception:
            pass
        if servers[address] == {}:
            del servers[address]
    except Exception:
        continue

print(servers)
