import yara
import os
import datetime
import helpers
import requests

class Scanner():
    def __init__(self, rules):
        self.rules = yara.compile(rules)

    def scan(self, data):
        results = []
        matches = self.rules.match(data=data['raw_paste'])
        for match in matches:
            results.append(match.rule)
        return results
