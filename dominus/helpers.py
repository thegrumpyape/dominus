import os

def check_dir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
            return True
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        return True

def check_header(filename, headers):
    if not os.path.isfile(filename):
        try:
            with open(filename, 'a') as f:
                for header in headers[:-1]:
                    f.write('{},'.format(header))
                f.write('{}\n'.format(headers[-1]))
            return True
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        return True
