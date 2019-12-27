import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

async def run(loop):
    nc = NATS()

    await nc.connect("nats://100.116.1.62:4222",loop=loop)
    logging.info("nats connected.")

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        logging.info("'{subject}':{data}".format(subject=subject,data=data))

    await nc.subscribe("1_min_bar", cb=message_handler)

    # await nc.drain()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nats_sub_worker = run(loop)
    asyncio.ensure_future(nats_sub_worker)
    loop.run_forever()
    #loop.run_until_complete(run(loop))
    #loop.close()
