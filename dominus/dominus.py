import yara
import time
import requests
import sys
import datetime
from inputs import gists
from outputs import json_output, csv_output

if __name__ == "__main__":
    try:
        print('Starting Dominus v0.1')

        # Load yara rules
        print('Loading yara rules')
        rules = yara.compile('rules/index.yar')

        while True:
            # Get gists
            print('Getting gists')
            gists = gists.get_gists('https://api.github.com/gists')

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

                    # Store record of gist in csv
                    csvOutput = csv_output.CSVOutput('logs/csv/gists.csv', ['@timestamp','id','rule','description','url'])
                    csvOutput.store_data(gist)

                    # Store copy of gist
                    jsonOutput = json_output.JSONOutput('logs/json/{}.json'.format(gist['id']))
                    jsonOutput.store_data(gist)

            print('Sleeping for 5 minutes')
            time.sleep(300)
    except KeyboardInterrupt:
        sys.exit(1)
