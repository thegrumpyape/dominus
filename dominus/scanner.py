import yara
import os
import datetime
import helpers
import requests

class Scanner():
    def __init__(self, history, rules):
        self.history = self.get_history(history)
        self.rules = yara.compile(rules)

    def get_history(self, filename):
        if helpers.check_dir(filename):
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    return f.read().splitlines()
            else:
                return []
        else:
            return []

    def scan(self, gist):
        results = []
        if gist['id'] not in self.history:
            print('Scanning gist {}'.format(gist['id']))
            # Get raw data of gists
            gist['@timestamp'] = datetime.datetime.now().isoformat()

            for filename, values in gist["files"].items():
                gist["files"][filename]["raw_data"] = requests.get(values["raw_url"]).text

            for filename, values in gist['files'].items():
                matches = self.rules.match(data=gist['files'][filename]['raw_data'])
                for match in matches:
                    results.append(match.rule)

            # Add gist to history
            with open('tmp/history.tmp', 'a') as f:
                f.write('{}\n'.format(gist['id']))

        return results
