'''
GNU General Public License v3.0

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

by mopx
'''

import requests
import threading
import logging
import sys
import os

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


URL_LOGIN = ''

headers = {'Content-Type': 'application/x-www-form-urlencoded'}

def err(msg): print(' ops... error is %s' % msg); exit(1)

def try_login(payload):
    try:
        datapost = "username=FUZZ&password=password".replace('FUZZ', payload)
        rq = requests.post(url=URL_LOGIN, data=datapost, headers=headers)

        logging.warning(' - requests with payload "%s" and response "%s"' % (datapost, rq.status_code))

        if not 'No account found with that username.' in rq.text:
            print(' * find my frind! \\0.0/\n\tpayload: %s' % (payload))
            os.system('echo "%s" >> ok.txt' % payload)
        return True
    except Exception as e:
        err('- to request > %s' % e)
        return False

def load_wordlist(path):
    fp = open(path, mode='r', errors='ignore')
    lines = fp.readlines()
    fp.close()
    return list(map(lambda x: x.replace('\n', ''), lines))

def main(payloads):
    with ThreadPoolExecutor(max_workers=5) as executor:
        return executor.map(try_login, payloads, timeout=30)


if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s\t %(message)s', filename='fuzz.log', filemode='a+')

    try:
        if len(sys.argv) >= 2:
            print(' hi, friend! fuzz script init :D')

            if not os.path.isfile(sys.argv[1]):
                err('wordlist path not found :(')
            wordlist = load_wordlist(sys.argv[1])

            try:
                for payload in wordlist:
                    resp = try_login(payload)
                    if resp is False:
                        print(' [!] failed to request with payload "%s"' % payload)
                        try_login(payload)
                print(' eh isto, quem achou achou, quem não paciência...')

            except Exception as e:
                err(' - main function > %s ' % e)
        else:
            print(' usage: %s %s' % (sys.argv[0], 'path/to/wordlist'))
    except KeyboardInterrupt:
        sys.stdout.write('\n\r ok ok, vou terminar aqui...')
    except Exception as e:
        err('- grant - %s' % e)