'''
GNU General Public License v3.0

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

by mopx
'''

import requests
import sys
import re
import os
import getpass
import logging
import os.path

logging.basicConfig(level=logging.DEBUG)

proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

PATH_AWS_CREDENTIALS = os.path.join(os.path.expanduser("~/")[:-1],'.aws\\credentials')

URL = 'https://labs.vocareum.com'
URL_LOGIN = URL+'/util/vcauth.php'
URL_LOGIN_GET = URL+'/home/login.php?code=&e=Please%20enter%20a%20valid%20email%20address'
URL_GET_AWS_ACCESS = URL+'/util/vcput.php?a=getaws&nores=1&stepid=14335&mode=s&type=0&vockey=%s'
URL_HOME_PAGE = URL+'/main/main.php?m=editor&nav=1&asnid=14334&stepid=14335'

wl = ['PHPSESSID', 'logintoken', 'tokenExpire', 'usertoken', 'userid', 'userassignment', 'domain_latestWebProxy']

headers = {
    'Host': 'labs.vocareum.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Origin': URL
}

def try_login(mail, password):
    rq = requests.get(url=URL_LOGIN_GET, headers=headers)
    cookies = rq.headers.get('Set-Cookie')
    cfduid = cookies.split(';')[0].split('=')
    cookie = {cfduid[0]: cfduid[1]}

    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Referer'] = 'https://labs.vocareum.com/home/login.php?code=&e=Please%20enter%20a%20valid%20email%20address'
    headers['DNT'] = '1'

    datapost = 'sender=home&loginid=%s&passwd=%s' % (mail, password)
    datapost = datapost.replace('@', '%40')

    headers['Content-Length'] = str(len(datapost))
    headers['Connection'] = 'Close'
    headers['Cookie'] = '='.join(cfduid)

    rq = requests.post(url=URL_LOGIN, data=datapost, headers=headers, cookies=cookie, allow_redirects=False)
    
    ## print('rq.headers', rq.headers)
    cookies = rq.headers.get('Set-Cookie')
    vockey = re.findall(r'\w{32}', cookies)[0]

    headers.pop('Content-Type')
    headers.pop('Content-Length')
    headers.pop('Cookie')

    ## print(headers)
    ## print('---------------------------------')

    new_cookies = {cfduid[0]: cfduid[1]}
    ## new_cookies['userassignment'] = 14334

    for item in wl:
        for ck in cookies.split(';'):
            if item in ck:
                tmp = ck.replace('Secure, ', '').split('=')
                new_cookies[tmp[0]] = tmp[1]
    
    ## print(new_cookies)

    rq = requests.get(url=URL_HOME_PAGE, headers=headers, cookies=new_cookies)
    ## print('---------------------------------')
    proxy = re.findall(r'https:\/\/proxy.vocareum.com\/hostip\/(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}\/vocproxy\/[\w|.]{10,70}', rq.text)
    proxy = 'https://proxy.vocareum.com/hostip/172.31.18.122:5000/vocproxy/72448074974689574689514335015eee0b738955c4.96014152' if len(proxy) == 0 else proxy[0]
    ## print(proxy)
    new_cookies['domain_latestWebProxy'] = proxy

    headers['Referer'] = 'https://labs.vocareum.com/main/main.php'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    rq = requests.get(url=URL_GET_AWS_ACCESS % vockey, headers=headers, cookies=new_cookies)
    ## print('---------------------------------')
    aws_credentials = rq.text
    ## print(rq.text)
    ## print('---------------------------------')
    aws_access_key_id = re.findall(r'aws_access_key_id=(.*)', aws_credentials)[0]
    aws_secret_access_key = re.findall(r'aws_secret_access_key=(.*)', aws_credentials)[0]
    aws_session_token = re.findall(r'aws_session_token=(.*)', aws_credentials)[0]

    print('aws_access_key_id=%s' % aws_access_key_id)
    print('aws_secret_access_key=%s' % aws_secret_access_key)
    print('aws_session_token=%s' % aws_session_token)

    os.remove(PATH_AWS_CREDENTIALS)

    fp = open(PATH_AWS_CREDENTIALS, 'w+')
    fp.write('[default]\n')
    fp.write('aws_access_key_id=%s\n' % aws_access_key_id)
    fp.write('aws_secret_access_key=%s\n' % aws_secret_access_key)
    fp.write('aws_session_token=%s\n' % aws_session_token)
    fp.close()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        password = getpass.getpass() 
        try_login(sys.argv[1], password)
    else:
        print(' usage: %s e-mail' % sys.argv[0])
