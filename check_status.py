from io import TextIOWrapper
import json
import asyncio
import os
import unicodedata
from aiohttp import ClientSession
from datetime import datetime
from bs4 import BeautifulSoup
from helpers.telegram import sendDocument, sendMsg
from dotenv import load_dotenv

load_dotenv()

MY_USER_ID = os.getenv('MY_USER_ID')

endpoint = "https://portaltramites.inpi.gob.ar/MarcasConsultas/Resultado"
req_body = json.load(open("marca.json", 'r', encoding='utf-8'))
acta_number = req_body["acta"]


def log(msg: str):
    with open('log', 'w+', encoding='utf-8') as logfile:
        timestamp = datetime.now().isoformat()
        logfile.write(f"{timestamp}: {msg}\n")


def get_last_known_state() -> TextIOWrapper:  # | None
    states = os.listdir("states")
    if len(states) > 0:
        filename = max(states)
        return get_other_state(filename=filename)
    else:
        return None


def get_other_state(filename: str) -> TextIOWrapper:
    filepath = os.path.join("states", filename)
    return open(filepath, 'r', encoding='utf-8')


def save_state(state: str, filename: str = None):
    if filename == None:
        timestamp = datetime.now().isoformat().replace(":", "-")
        filename = timestamp
    with open(os.path.join("states", f"{filename}.html"), 'w', encoding='utf-8') as f:
        f.write(state)


def has_changes(state_from_response: str) -> bool:

    aux_state_name = "0000-00-00T00-00-00.000000_aux_state"
    save_state(state_from_response, aux_state_name)
    current_state = get_other_state(f"{aux_state_name}.html").read()
    current_state = unicodedata.normalize("NFC", current_state)
    os.remove(os.path.join("states", f"{aux_state_name}.html"))

    last_known_state = get_last_known_state()
    last_known_state = "" if last_known_state == None else last_known_state.read()
    last_known_state = unicodedata.normalize("NFC", last_known_state)

    soup_a = BeautifulSoup(current_state, 'html.parser')
    soup_b = BeautifulSoup(last_known_state, 'html.parser')

    body_a = soup_a.find(id='body')
    body_b = soup_b.find(id='body')

    return body_a != body_b


async def main():
    async with ClientSession() as client:
        async with client.post(endpoint, json=req_body) as resp:
            if resp.status == 200:
                resp_text = await resp.text()
                if has_changes(resp_text):
                    save_state(resp_text)
                    log("State has changed!")
                    sendMsg(
                        user_id=MY_USER_ID,
                        text=f"Hay cambios en tu acta n??mero {acta_number}! Mir?? el detalle:",
                        max_retries=3
                    )
                    sendDocument(
                        user_id=MY_USER_ID,
                        file=get_last_known_state(),
                        max_retries=3
                    )
                else:
                    pass
            else:
                log(f"HTTP Request was not successful. Status: {resp.status}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
