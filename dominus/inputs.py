import requests
import json
import datetime

class Gist():
    def __init__(self, url):
        self.url = url

    def scrape(self):
        return requests.get(self.url).json()
