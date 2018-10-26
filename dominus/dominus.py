import yara
import time
import requests
import sys
import datetime
import helpers
import os
import inputs
import scanner
import outputs

if __name__ == "__main__":
    try:
        print('Starting Dominus v0.1')

        print('Initializing inputs')
        gistInput = inputs.Gist('https://api.github.com/gists')

        print('Initializing scanner')
        scanner = scanner.Scanner('tmp/history.tmp','rules/index.yar')

        print('Initializing outputs')
        csvOutput = outputs.CSV('logs/csv/')
        jsonOutput = outputs.JSON('logs/json/')

        while True:
            # Get gists
            print('Getting gists')
            gists = gistInput.scrape()

            print('Comparing to Yara rules')
            for gist in gists:
                    results = scanner.scan(gist)

                    #Outputs results if a match occurred
                    if len(results) > 0:
                        print('Found match in gist {}'.format(gist['id']))
                        gist['rule'] = results

                        # Store record of gist in csv
                        csvOutput.store_data(gist, 'gists.csv', ['@timestamp','id','rule','description','url'])
                        # Store copy of gist
                        jsonOutput.store_data(gist, '{}.json'.format(gist['id']))

            print('Sleeping for 5 minutes')
            time.sleep(300)
    except KeyboardInterrupt:
        sys.exit(1)
