import json
import helpers

class JSON():
    def __init__(self, path):
        if helpers.check_dir(path):
            self.path = path

    def store_data(self, data, filename):
        with open('{0}/{1}'.format(self.path, filename), 'a') as f:
            json.dump(data, f)

class CSV():
    def __init__(self, path):
        if helpers.check_dir(path):
                self.path = path

    def store_data(self, data, filename, headers):
        if helpers.check_header('{0}/{1}'.format(self.path, filename), headers):
            # Add data to csv file
            with open('{0}/{1}'.format(self.path, filename), 'a') as f:
                for header in headers[:-1]:
                    f.write('{},'.format(data[header]))
                f.write('{}\n'.format(data[headers[-1]]))
