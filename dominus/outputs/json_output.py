import json
import helpers

class JSONOutput():
    def __init__(self, filename):
        if helpers.check_dir(filename):
            self.filename = filename

    def store_data(self, data):
        with open(self.filename, 'a') as f:
            json.dump(data, f)
