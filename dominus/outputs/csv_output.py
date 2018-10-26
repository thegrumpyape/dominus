import helpers

class CSVOutput():
    def __init__(self, filename, headers):
        if helpers.check_dir(filename):
            if helpers.check_header(filename, headers):
                self.filename = filename
                self.headers = headers

    def store_data(self, data):
        # Add data to csv file
        with open(self.filename, 'a') as f:
            for header in self.headers[:-1]:
                f.write('{},'.format(data[header]))
            f.write('{}\n'.format(data[self.headers[-1]]))
