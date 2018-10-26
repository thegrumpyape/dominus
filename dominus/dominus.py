import yara
import time
import requests
import json
import os
import sys

def check_dir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
def save_csv(filename, data):
    check_dir(filename)
    #Create csv header if file does not exist
    if not os.path.isfile(filename):
        try:
            with open(filename, 'a') as f:
                f.write('{0},{1},{2},{3},{4}\n'.format('id','rule','description', 'owner', 'url'))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    # Add data to csv file
    with open(filename, 'a') as f:
        f.write('{0},{1},{2},{3},{4}\n'.format(data['id'],data['rule'],data['description'], data['owner']['login'], data['url']))

def save_json(filename, data):
    check_dir(filename)
    with open(filename, 'a') as f:
        json.dump(data, f)


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

def save_gists(data):
    # Store record of gist in csv
    save_csv('logs/csv/gists.csv', data)
    # Store copy of gist
    save_json('logs/json/{}.json'.format(data['id']), data)

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
                    gist['rule'] = results
                    save_gists(gist)

            print('Sleeping for 5 minutes')
            time.sleep(300)
    except KeyboardInterrupt:
        sys.exit(1)
