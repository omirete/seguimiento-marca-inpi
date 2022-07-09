import json
import asyncio
import os
from aiohttp import ClientSession
from datetime import datetime

endpoint = "https://portaltramites.inpi.gob.ar/MarcasConsultas/Resultado"
req_body = json.load(open("marca.json", 'r', encoding='utf-8'))


def log(msg: str):
    with open('log', 'w+', encoding='utf-8') as logfile:
        timestamp = datetime.now().isoformat()
        logfile.write(f"{timestamp}: {msg}\n")


def get_current_state():
    states = os.listdir("states")
    if len(states) > 0:
        return max(states)
    else:
        return ""


def save_new_state(state: str):
    timestamp = datetime.now().isoformat().replace(":", "-")
    with open(os.path.join("states", f"{timestamp}.html"), 'w', encoding='utf-8') as f:
        f.write(state)


async def main():
    async with ClientSession() as client:
        async with client.post(endpoint, json=req_body) as resp:
            if resp.status == 200:
                resp_text = await resp.text()
                if get_current_state() != resp_text:
                    save_new_state(resp_text)
                    log(f"State has changed!")
                else:
                    pass
            else:
                log(f"HTTP Request was not successful. Status: {resp.status}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
