import asyncio
import random
import ssl
import json
import time
import uuid
import os
from loguru import logger
from websockets_proxy import proxy_connect

async def connect_to_wss(user_id, proxy_url=None):
    # إصلاح الخطأ: إذا لم يوجد بروكسي نستخدم اسم ثابت لتوليد الـ ID
    name_for_uuid = proxy_url if proxy_url else "RAILWAY_SERVER_IP"
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, name_for_uuid))
    
    logger.info(f"Starting connection for device: {device_id}")
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            uri = "wss://proxy.wynd.network:4650/"
            server_hostname = "proxy.wynd.network"
            
            async with proxy_connect(uri, proxy_url=proxy_url, ssl=ssl_context, server_hostname=server_hostname,
                                     extra_headers=custom_headers) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(f"Sending PING: {send_message}")
                        await websocket.send(send_message)
                        await asyncio.sleep(20)

                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(f"Received message: {message}")
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "2.5.0"
                            }
                        }
                        logger.debug(f"Sending AUTH: {auth_response}")
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(f"Sending PONG: {pong_response}")
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(f"Error: {e} on connection")
            await asyncio.sleep(5)

async def main():
    _user_id = os.getenv("USER_ID")
    
    if not _user_id:
        logger.error("USER_ID variable is missing in Railway Variables!")
        return

    await connect_to_wss(_user_id)

if __name__ == '__main__':
    asyncio.run(main())
