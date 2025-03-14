# Program to Help with Monad Testnet

1. Auto Faucet

## How to Use the Auto Faucet

Ensure that Python and Git are installed on your computer/device.

Clone this repository:

```
git clone https://github.com/akasakaid/lazy-monad.git
```

Navigate to the `lazy-monad` folder:

```
cd lazy-monad
```

Install the required libraries:

```
python -m pip install -r requirements.txt
```

Read the explanation below!

You can fill in your wallet address in the `address.txt` file.

You need to configure the `config.py` file, specifically the captcha configuration section, as this is where you will need to use a third-party service to bypass captcha.

This program supports several third-party services, including:

 - [x] [anti-captcha](https://getcaptchasolution.com/iiaiemxamz)
 - [x] [twocaptcha](https://2captcha.com/?from=4688295)
 - [x] [capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=ejmvauaFFnqt)

If you know of a third-party captcha bypass service that is not listed or supported by this program, you can contact me so I can update the program to add support for it.

Regarding proxies, I recommend using rotating residential proxies. You can use the following proxy services:

- [x] [proxy-cheap](https://app.proxy-cheap.com/r/mlShoy)
- [x] [dataimpulse](https://dataimpulse.com/?aff=48082)
- [x] [proxiesfo](https://app.proxies.fo/ref/c02fda06-da42-f640-7ef7-885127487ef0)

You can fill in the `proxies.txt` file with the proxies you have purchased.

The format for filling in the proxies is as follows:

If the proxy requires authentication:

```
protocol://user:password@server:port
```

Example:

```
http://admin:admin@192.168.0.1:8888
```

If the proxy does not require authentication:

```
protocol://server:port
```

Example:

```
http://192.168.0.1:8888
```

# Support

If you find my program useful, you can buy me a coffee through the link below.

[https://sociabuzz.com/fawwazthoerif/tribe](https://sociabuzz.com/fawwazthoerif/tribe)