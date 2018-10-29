# Dominus
Scrapes pastes from known APIs and compares them to yara rules

## Supported Inputs
Dominus currently supports:
- Pastebin Scraping API
- Github Gist API

## Supported Outputs
Dominus currently supports:
- Dump to JSON file
- Dump to CSV file

## Prerequisites

### Pastebin

You need a Pro account on pastebin that has access to the scraping API.
https://pastebin.com/api_scraping_faq

# Installation
Run in terminal:
~~~
git clone https://github.com/ediblesushi/dominus
cd dominus
pipenv install
~~~

# Run
Run in terminal:
~~~
pipenv run python dominus/dominus.py
~~~
