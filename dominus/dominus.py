import sys
import time
import inputs
import scanner
import outputs
import helpers
import os

if __name__ == "__main__":
    try:
        print('Starting Dominus v0.1')

        print('Loading history')
        if helpers.check_dir('tmp/history.tmp'):
            if os.path.isfile('tmp/history.tmp'):
                with open('tmp/history.tmp', 'r') as f:
                    history = f.read().splitlines()
            else:
                history = []
        else:
            history = []

        print('Initializing inputs')
        gistCollector = inputs.GistCollector('https://api.github.com/gists')

        print('Initializing scanner')
        scanner = scanner.Scanner('rules/index.yar')

        print('Initializing outputs')
        csvOutput = outputs.CSV('logs/csv/')
        jsonOutput = outputs.JSON('logs/json/')

        while True:
            # Get gists
            print('Getting gists')
            gists = gistCollector.scrape(history)

            print('Comparing to Yara rules')
            for gist in gists:
                    results = scanner.scan(gist)

                    #Outputs results if a match occurred
                    if len(results) > 0:
                        print('Found match in gist {}'.format(gist['id']))
                        gist['rule'] = results

                        # Store record of gist in csv
                        csvOutput.store_data(gist, 'gists.csv', ['@timestamp','id','rule','user','raw_url'])
                        # Store copy of gist
                        jsonOutput.store_data(gist, '{}.json'.format(gist['id']))

            print('Sleeping for 5 minutes')
            time.sleep(300)
    except KeyboardInterrupt:
        sys.exit(1)
