import requests
import json
import datetime

class GistCollector():
    def __init__(self, url):
        self.url = url

    def scrape(self, history):
        gists = []

        for gist_meta in requests.get(self.url).json():
            if gist_meta['id'] in history:
                continue

            print('Grabbing data from {}'.format(gist_meta['id']))

            for file_name, file_meta in gist_meta["files"].items():
                gist_data = file_meta
                gist_data['@timestamp'] = gist_meta['created_at']
                gist_data['id'] = gist_meta['id']
                gist_data['user'] = gist_meta['user']
                gist_data['raw_paste'] = requests.get(file_meta['raw_url']).text
                gists.append(gist_data)

            with open('tmp/history.tmp', 'a') as f:
                f.write('{}\n'.format(gist_meta['id']))

        return gists
