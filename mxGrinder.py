# coding=utf-8
import argparse
import requests
import time
from bs4 import BeautifulSoup
import os
# import sys

# Bedøm platform ift. evt. fremtidig konsol clearing
# if sys.platform=='win32':
#     cmd = "cls"
# else:
#     cmd = "clear"

# Definer CLI arguments
parser = argparse.ArgumentParser(description='Stemmer på en bestemt valgmulighed x antal gange i afstemninger på MX.dk')
parser.add_argument('-u', '--url', help='URL til artiklen der indeholder afstemningen.', required=True)
parser.add_argument('-t', '--times', help='Antal stemmer der skal afgives. 0 for uendeligt.', required=True)
parser.add_argument('-c', '--choice', help='Valgmulighed i afstemningen, fra toppen.', required=True)
# parser.add_argument('-w', '--wizard', help='Start interaktiv version.', required=False, action='store_true')
args = parser.parse_args()


# Find afstemningens ID fra artiklens HTML
def getID(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "lxml")

    divs = soup.findAll('div', attrs={'class': 'interactive'})
    pollURL = divs[0].find('a')['href']
    return pollURL.rsplit('/', 1)[-1]


def vote():
    pollID = getID(args.url)
    print "Poll ID: " + str(pollID)

    i = 0

    try:
        while True:

            i += 1

            # Clear konsol
            # print os.system(cmd), chr(13), " ", chr(13),

            if i > int(args.times) and not int(args.times) == 0:
                print 'Stopper.'
                break

            # Send POST request
            r = requests.post('https://interaktiv.mx.dk/toolbox/advancedvotes/vote',
                              data={
                                  'id': pollID,
                                  'vote': int(args.choice) - 1,
                                  'ci_csrf_token': ''})  # Tak til MX for en awesome anti-CSRF implementation.

            # Ved success får vi et 'status: ok' tilbage. Hvis ikke, break.
            if r.text != 'status: ok':
                print 'Uventet svar:', '\"' + r.text + '\"' + '\n', 'Stopper.'
                break

            # Alt gik fint, prinf info.
            else:
                print r.text
                print 'Stemt ' + str(i) + ' gange.'
                time.sleep(1)

    # Stop ved ctrl-C,
    except KeyboardInterrupt:
        print 'Stopper.'


vote()
