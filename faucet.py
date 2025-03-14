import sys
import json
import httpx
import random
import string
import asyncio
from config import *
from config import APIKEY
from config import PROVIDER
from src.service.twocaptcha import twocaptcha
from src.service.anticaptcha import anticaptcha
from src.service.capsolver import capsolver
from src.utils.http import http
from src.utils.log import log
from colorama import Fore, Style

green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
white = Fore.LIGHTWHITE_EX
red = Fore.LIGHTRED_EX


def generate_visitor_id():
    visitor_id = "".join(
        [random.choice(list(string.digits + string.ascii_lowercase)) for _ in range(32)]
    )
    return visitor_id


async def faucet(address, proxy):
    url = "https://testnet.monad.xyz/api/faucet/claim"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "testnet.monad.xyz",
        "Origin": "https://testnet.monad.xyz",
        "Referer": "https://testnet.monad.xyz/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }
    async with httpx.AsyncClient(headers=headers, proxy=proxy) as ses:
        timet = None
        token = None
        while True:
            if len(APIKEY) <= 0:
                log(f"{red}You haven't set the APIKEY & PROVIDER name yet")
                sys.exit()
            if PROVIDER == "twocaptcha":
                timet, token = await twocaptcha(APIKEY)
            elif PROVIDER == "anticaptcha":
                timet, token = await anticaptcha(APIKEY)
            elif PROVIDER == "capsolver":
                tiemt, token = await capsolver(APIKEY)
            if token is None:
                continue
            data = {
                "address": address,
                "visitorId": generate_visitor_id(),
                "cloudFlareResponseToken": token,
            }
            res = await http(ses=ses, url=url, data=json.dumps(data))
            if res is None:
                return None
            if len(res.text) <= 0:
                log(f"{yellow}content result is 0, continue !")
                continue
            try:
                message = res.json().get("message")
            except:
                message = None
            if message == "reCAPTCHA process failed":
                log(f"{red}reCAPTCHA process failed")
                continue
            if message == "reCAPTCHA score too low":
                log(f"{red}reCAPTCHA score too low")
                continue
            if message == "Success":
                log(f"{green}success claim faucet !")
                break
            if message == "Claimed already, Please try again later.":
                log(f"{yellow}already claimed  !")
                break


def get_proxy(i, p):
    if len(p) <= 0:
        return None
    return p[i % len(p)]


async def main():
    print(
        """
>
> AUTO FAUCET MONAD !
>
        """
    )
    proxies = open("proxies.txt", "r").read().splitlines()
    addreses = open("address.txt", "r").read().splitlines()
    p = 0
    for address in addreses:
        log(f"{green}using wallet {white}{address}")
        proxy = get_proxy(p, proxies)
        result = await faucet(address=address, proxy=proxy)
        if result:
            p += 1


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit()
