import yara
import time
import requests
import sys
import datetime
import helpers
import os
from inputs import gists
from outputs import json_output, csv_output

if __name__ == "__main__":
    try:
        print('Starting Dominus v0.1')

        # Load yara rules
        print('Loading yara rules')
        rules = yara.compile('rules/index.yar')

        while True:
            # Load history
            print('Loading history')
            if helpers.check_dir('tmp/history.tmp'):
                if os.path.isfile('tmp/history.tmp'):
                    with open('tmp/history.tmp', 'r') as f:
                        history = f.read().splitlines()
                else:
                    history = []
            else:
                history = []

            # Get gists
            print('Getting gists')
            gists_data = gists.scrape('https://api.github.com/gists')

            print('Comparing to Yara rules')
            for gist in gists_data:
                # If new gist
                if gist['id'] not in history:
                    # Get raw data of gists
                    gist = gists.get_raw_data(gist)

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

                        # Store record of gist in csv
                        csvOutput = csv_output.CSVOutput('logs/csv/gists.csv', ['@timestamp','id','rule','description','url'])
                        csvOutput.store_data(gist)

                        # Store copy of gist
                        jsonOutput = json_output.JSONOutput('logs/json/{}.json'.format(gist['id']))
                        jsonOutput.store_data(gist)

                    # Add gist to history
                    with open('tmp/history.tmp', 'a') as f:
                        f.write('{}\n'.format(gist['id']))

            print('Sleeping for 5 minutes')
            time.sleep(300)
    except KeyboardInterrupt:
        sys.exit(1)
