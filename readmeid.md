# Program untuk membantu mengerjakan testnet monad

1. Auto faucet

## Cara menggunakan auto faucet

Pastikan komputer / perangkat anda sudah terinstall python dan git.

Clone repository ini

```
git clone https://github.com/akasakaid/lazy-monad.git
```

Masuk kefolder lazy-monad

```
cd lazy-monad
```

Install library yang dibutuhkan

```
python -m pip install -r requirements.txt
```

Baca penjelasan dibawah!

Anda bisa mengisi address dari wallet yang anda gunakan di file `address.txt`

Anda perlu mengisi file config.py lebih tepatnya dibagian captcha config karena disini lah Anda harus menggunakan pihak ke-3 untuk melakukan bypass captcha

Program ini mendukung beberapa pihak ke-3, antara lain :

 - [x] [anti-captcha](https://getcaptchasolution.com/iiaiemxamz)
 - [x] [twocaptcha](https://2captcha.com/?from=4688295)
 - [x] [capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=ejmvauaFFnqt)

Jika anda memiliki situs pihak ke-3 untuk melakukan bypass captcha tetapi tidak terdaftar / program ini tidak mendukung situs yang anda ketahui, anda bisa menghubungi saya agar saya bisa melakukan update untuk menambah situs anda.

Tentang proxy saya sarankan menggunakan proxy residensial rotating, anda bisa menggunakan situs proxy dibawah

- [x] [proxy-cheap](https://app.proxy-cheap.com/r/mlShoy)
- [x] [dataimpulse](https://dataimpulse.com/?aff=48082)
- [x] [proxiesfo](https://app.proxies.fo/ref/c02fda06-da42-f640-7ef7-885127487ef0)

Anda bisa mengisi file `proxies.txt` dengan proxy yang sudah anda beli. 

Format pengisian mengikuti format berikut :

Jika proxy memiliki autentikasi 

protocol://user:password@server:port

Contoh :

http://admin:admin@192.168.0.1:8888

Jika proxy tidak memiliki autentikasi : 

protocol://server:port

Contoh : 

http://192.168.0.1:8888


# Support

If you find my program useful, you can buy me a copy through the link below.

[https://sociabuzz.com/fawwazthoerif/tribe](https://sociabuzz.com/fawwazthoerif/tribe)