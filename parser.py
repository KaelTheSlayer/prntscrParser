import os
import random
import string
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import wget

invalidPhotos = [0, 503]

txtFile = './parsed_urls.txt'
imagesFolder = './images/'

def prntscr_parser():
    while True:
        valid_img = False
        amount = int(''.join(random.choice('5' + '6') for _ in range(1)))
        symbols_count = 3 if amount == 6 else 5
        picture = str(''.join(random.choice(string.ascii_uppercase + string.digits +
                                            string.ascii_lowercase) for _ in range(symbols_count)))
        picture2 = str(''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(symbols_count)))

        pathname = picture2 + picture if amount == 6 else picture2

        name = imagesFolder + pathname
        url_to_parse = "https://prnt.sc/" + "" + str(pathname)

        if not os.path.isfile(txtFile):
            creator = open(txtFile, 'x')
            creator.close()

        with open(txtFile, 'r') as fr:
            if url_to_parse not in fr.read():
                with open(txtFile, 'a') as f:
                    f.write(url_to_parse + '\t')
            else:
                print('[-] Invalid: URL already parsed')
                break

        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        try:
            html = requests.get(url_to_parse, headers=headers).text
            if ("IP address" or "Error 502") in html:
                print("Something went wrong. Retrying...")
                break
            try:
                soup = BeautifulSoup(html, features="html.parser")
                for img_tag in soup.find_all('img'):
                    url = (img_tag['src'])
                    if ("imgur" or "imageshack") in url:
                        valid_img = True
                        try:
                            r = requests.get(url)
                            if r.status_code == 200:
                                wget.download(url, out=str(name) + '.jpg')
                                file = os.path.getsize(str(name) + ".jpg")
                                if file in invalidPhotos:
                                    with open(txtFile, 'a') as f:
                                        f.write('[+] Valid \n')
                                    print("\n[-] Invalid: " + url_to_parse)
                                    os.remove(name + ".jpg")
                                else:
                                    with open(txtFile, 'a') as f:
                                        f.write('[+] Valid \n')
                                    print("\n[+] Valid: " + url_to_parse)
                        except requests.exceptions.HTTPError:
                            with open(txtFile, 'a') as f:
                                f.write('[-] Invalid \n')
                            break
                if not valid_img:
                    with open(txtFile, 'a') as f:
                        f.write('[-] Invalid \n')
                    print("[-] Invalid: " + url_to_parse)
            except ValueError:
                with open(txtFile, 'a') as f:
                    f.write('[-] Invalid \n')
                break
        except requests.exceptions.HTTPError:
            with open(txtFile, 'a') as f:
                f.write('[-] Invalid \n')
            break


directory = os.path.dirname('./images/')
if not os.path.exists(directory):
    os.makedirs(directory)
prntscr_parser()
