#pylint: disable=broad-except
import json
from ipaddress import ip_network
from os import environ
import asyncio
import itertools

from mcstatus import MinecraftServer

subnets = environ.get('SCAN_SUBNET', '127.0.0.1').split(',')

def status_to_dict(status):
    return {
        'raw': status.raw,
        'players': status.players.online,
        'maximum_players': status.players.max,
        'version': {
            'name': status.version.name,
            'protocol': status.version.protocol,
        },
        'description': status.description,
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

def get_info(address):
    server = MinecraftServer.lookup(address)
    try:
        server.ping()
        out = {}
        try:
            out['query'] = query_to_dict(server.query(tries=1))

        except Exception:
            pass
            #print(e) # TODO logger?
        try:
            out['status'] = status_to_dict(server.status(tries=1))
        except Exception:
            pass
            #print(e) # TODO logger?
        if out != {}:
            out['host'] = {
                'address': address,
            }
            try:
                out['host']['name'], out['host']['alts'], _ = socket.gethostbyaddr(address)
            except Exception:
                pass
            print(json.dumps(out))
            return out
        return None
    except Exception:
        return None

async def main():
    nets = map(ip_network, subnets)

    # get all the ip addresses (using itertools.chain to flatten the ip.hosts() lists)
    hosts = map(str, itertools.chain(*map(lambda ip: ip.hosts(), nets)))

    #create tasks
    tasks = map(asyncio.create_task, map(lambda host: asyncio.to_thread(get_info, host), hosts))

    # and wait for completion
    done, pending = await asyncio.wait(tasks)

asyncio.run(main())
