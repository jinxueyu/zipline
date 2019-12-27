#!/bin/python

python read_live_data.py level1ShMktData | python format_sh_tick_to_1min_bar.py sh | python send_to_nats.py
[hadoop@cscs-28-163-1-64 live_data]$ cat send_to_nats.py
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import sys

async def run(loop):
    nc = NATS()

    await nc.connect("nats://100.116.1.62:4222",loop=loop)
    print("nats connected.")

    for data in sys.stdin:
        await nc.publish("1_min_bar",bytes(data,'utf-8'))
        await nc.flush()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nats_sub_worker = run(loop)
    asyncio.ensure_future(nats_sub_worker)
    loop.run_forever()

# pip install asyncio-nats-client

