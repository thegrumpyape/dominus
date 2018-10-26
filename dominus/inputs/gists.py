import requests
import json
import datetime

def scrape(url):
    r = requests.get(url)
    return r.json()

def get_raw_data(gist):
    gist['@timestamp'] = datetime.datetime.now().isoformat()
    #Get raw data of gist
    for filename, values in gist["files"].items():
        r = requests.get(values["raw_url"])
        raw_data = r.text
        gist["files"][filename]["raw_data"] = raw_data

    return gist
