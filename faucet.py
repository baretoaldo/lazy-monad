import sys
import json
import httpx
import random
import string
import asyncio
import time
from config import *
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

# Hardcode API key untuk testing
APIKEY = "CAP-B595A36B146B771CA885034AF7EF3A75"
PROVIDER = "capsolver"

# Tambahkan AUTH_TOKEN di config.py jika ada
try:
    from config import AUTH_TOKEN
except ImportError:
    AUTH_TOKEN = None

def generate_visitor_id():
    return "".join(random.choices(string.digits + string.ascii_lowercase, k=32))

async def test_proxy(proxy):
    try:
        async with httpx.AsyncClient(proxy=proxy, timeout=10) as client:
            response = await client.get("https://api.ipify.org")
            log(f"{white}Proxy test response: {response.status_code}")
            return response.status_code == 200
    except Exception as e:
        log(f"{red}Proxy test failed: {str(e)}")
        return False

async def faucet(address, proxy, max_retries=3):
    url = "https://faucet-claim.monadinfra.com/"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "faucet-claim.monadinfra.com",
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
    
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        headers["X-Request-Verification-Token"] = AUTH_TOKEN

    for attempt in range(max_retries):
        try:
            # Test proxy
            if proxy and not await test_proxy(proxy):
                log(f"{red}Proxy failed: {proxy}")
                return False

            async with httpx.AsyncClient(headers=headers, proxy=proxy, timeout=60) as ses:
                if not APIKEY:
                    log(f"{red}APIKEY is not set")
                    return None

                token = None
                retry_captcha = 0
                while retry_captcha < 3 and token is None:
                    try:
                        log(f"{white}Attempting to get captcha token (try {retry_captcha + 1})")
                        if PROVIDER == "capsolver":
                            _, token = await capsolver(APIKEY)
                            log(f"{white}Capsolver token received: {token[:10]}...")  # Tampilkan sebagian token
                        else:
                            log(f"{red}Unsupported PROVIDER: {PROVIDER}")
                            return None
                    except Exception as e:
                        log(f"{red}Capsolver error: {str(e)}")
                        retry_captcha += 1
                        await asyncio.sleep(2)
                        continue

                if token is None:
                    log(f"{red}Failed to get captcha token after {retry_captcha} attempts")
                    return None

                # Struktur payload sesuai contoh
                data = {
                    "address": address,
                    "visitorId": generate_visitor_id(),
                    "cloudFlareResponseToken": token,
                }

                log(f"{white}Sending request to faucet with data: {json.dumps(data)[:100]}...")
                res = await http(ses=ses, url=url, data=json.dumps(data))
                if res is None:
                    log(f"{yellow}No response received")
                    continue

                log(f"{white}Server Response:")
                log(f"{white}Status Code: {res.status_code}")
                log(f"{white}Headers: {dict(res.headers)}")
                log(f"{white}Body: {res.text}")

                try:
                    message = res.json().get("message", "Unknown response")
                except:
                    message = "Invalid JSON response"

                if "unauthorized" in message.lower():
                    log(f"{red}Authentication failed: {message}")
                    return False
                elif "failed" in message.lower():
                    log(f"{red}{message}")
                    await asyncio.sleep(2)
                    continue
                elif message == "Success":
                    log(f"{green}Successfully claimed faucet!")
                    return True
                elif "already claimed" in message.lower():
                    log(f"{yellow}Address already claimed!")
                    return True
                else:
                    log(f"{yellow}{message}")
                    await asyncio.sleep(2)
                    continue

        except httpx.TimeoutException:
            log(f"{red}Request timeout on attempt {attempt + 1}/{max_retries}")
        except Exception as e:
            log(f"{red}Error on attempt {attempt + 1}: {str(e)}")

        if attempt < max_retries - 1:
            wait_time = 5 * (attempt + 1)
            log(f"{yellow}Retrying in {wait_time} seconds...")
            await asyncio.sleep(wait_time)

    log(f"{red}Failed after {max_retries} attempts")
    return False

def get_proxy(i, proxies):
    if not proxies:
        return None
    return proxies[i % len(proxies)]

async def main():
    print(
        """
>
> AUTO FAUCET MONAD !
>
        """
    )
    
    try:
        proxies = open("proxies.txt", "r").read().splitlines()
        addresses = open("address.txt", "r").read().splitlines()
    except FileNotFoundError as e:
        log(f"{red}Error: {str(e)}. Please ensure proxies.txt and address.txt exist")
        return

    if not addresses:
        log(f"{red}No addresses found in address.txt")
        return

    proxy_index = 0
    for address in addresses:
        log(f"{green}Processing wallet {white}{address}")
        proxy = get_proxy(proxy_index, proxies)
        if proxy:
            log(f"{white}Using proxy: {proxy}")
        result = await faucet(address=address, proxy=proxy)
        if result:
            proxy_index += 1
        await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log(f"{yellow}Script terminated by user")
        sys.exit()
