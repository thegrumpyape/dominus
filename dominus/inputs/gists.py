import requests
import json
import datetime

def get_gists(url):
    r = requests.get(url)
    gists = r.json()

    print('Getting data from {} gists'.format(len(gists)))

    gists_data = []
    for gist in gists:
        gist['@timestamp'] = datetime.datetime.now().isoformat()
        #Get raw data of gists
        for filename, values in gist["files"].items():
            r = requests.get(values["raw_url"])
            raw_data = r.text
            gist["files"][filename]["raw_data"] = raw_data
        gists_data.append(gist)

    return gists_data
