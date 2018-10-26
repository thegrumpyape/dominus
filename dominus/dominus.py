import yara
import time
import requests
import json
import os
import sys

def get_gists(url):
    r = requests.get(url)
    gists = r.json()

    print('Getting data from {} gists'.format(len(gists)))

    gists_data = []
    for gist in gists:
        #Get raw data of gists
        for filename, values in gist["files"].items():
            r = requests.get(values["raw_url"])
            raw_data = r.text
            gist["files"][filename]["raw_data"] = raw_data
        gists_data.append(gist)

    return gists_data

def save_gists(data, id):
    filename = 'logs/json/{}.json'.format(id)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(filename, 'a') as f:
        json.dump(data, f)

if __name__ == "__main__":
    try:
        print('Starting Dominus v0.1')

        # Load yara rules
        print('Loading yara rules')
        rules = yara.compile('rules/index.yar')

        while True:
            # Get gists
            print('Getting gists')
            gists = get_gists('https://api.github.com/gists')

            print('Comparing to Yara rules')
            for gist in gists:
                #Compare gists to yara rules
                results = []
                for filename, values in gist['files'].items():
                    matches = rules.match(data=gist['files'][filename]['raw_data'])
                    for match in matches:
                        results.append(match.rule)

                #Outputs results if a match occurred
                if len(results) > 0:
                    print('Found match in gist {}'.format(gist['id']))
                    save_gists(gist, gist['id'])

            print('Sleeping for 5 minutes')
            time.sleep(300)
    except KeyboardInterrupt:
        sys.exit(1)
