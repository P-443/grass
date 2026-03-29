import asyncio
import random
import ssl
import json
import time
import uuid
import os
from loguru import logger
from websockets_proxy import proxy_connect

async def connect_to_wss(user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, "RAILWAY_SERVER_IP"))
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
            
            # الإصلاح هنا: إرسال الـ proxy كـ None صراحةً لتجنب خطأ الـ __init__
            async with proxy_connect(uri, 
                                     proxy=None, 
                                     proxy_url=None, 
                                     ssl=ssl_context, 
                                     server_hostname=server_hostname,
                                     extra_headers=custom_headers) as websocket:
                
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        await websocket.send(send_message)
                        await asyncio.sleep(20)

                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(f"Message received: {message.get('action')}")
                    
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
                        await websocket.send(json.dumps(auth_response))
                        logger.success("Auth sent successfully!")

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(f"Connection Error: {e}")
            await asyncio.sleep(5)

async def main():
    _user_id = os.getenv("USER_ID")
    if not _user_id:
        logger.error("USER_ID variable is missing in Railway!")
        return
    await connect_to_wss(_user_id)

if __name__ == '__main__':
    asyncio.run(main())
